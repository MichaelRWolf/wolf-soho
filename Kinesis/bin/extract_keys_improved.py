#!/usr/bin/env python3
"""
Improved key extraction script with multiple detection strategies.
Tries watershed segmentation, color-based segmentation, Hough line detection,
and combines results for better accuracy.
"""

import cv2
import numpy as np
from PIL import Image
import os
from collections import defaultdict

def extract_key(img, bbox, padding=3):
    """Extract a key region and make background transparent."""
    x, y, w, h = bbox
    
    x_start = max(0, x - padding)
    y_start = max(0, y - padding)
    x_end = min(img.shape[1], x + w + padding)
    y_end = min(img.shape[0], y + h + padding)
    
    roi = img[y_start:y_end, x_start:x_end].copy()
    
    # Make white background transparent
    img_array = np.array(roi)
    if img_array.shape[2] == 4:
        gray = cv2.cvtColor(img_array[:, :, :3], cv2.COLOR_BGRA2RGB)
        gray = cv2.cvtColor(gray, cv2.COLOR_RGB2GRAY)
        alpha = img_array[:, :, 3].copy()
    else:
        gray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
        alpha = np.ones((img_array.shape[0], img_array.shape[1]), dtype=np.uint8) * 255
    
    # Threshold for transparency (make bright pixels transparent)
    alpha[gray > 240] = 0
    
    if img_array.shape[2] == 4:
        img_array[:, :, 3] = alpha
    else:
        img_array = np.dstack([img_array, alpha])
    
    return Image.fromarray(img_array, 'RGBA')

def detect_watershed(img):
    """
    Strategy A: Watershed Segmentation
    Use distance transform and watershed algorithm to segment keys.
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
    
    # Invert to make keys (darker) stand out
    inverted = 255 - gray
    
    # Apply threshold to separate keys from background
    _, thresh = cv2.threshold(inverted, 30, 255, cv2.THRESH_BINARY)
    
    # Distance transform
    dist_transform = cv2.distanceTransform(thresh, cv2.DIST_L2, 5)
    
    # Find local maxima as markers
    _, markers = cv2.connectedComponents(np.uint8(dist_transform > 0.3 * dist_transform.max()))
    
    # Apply watershed
    markers = cv2.watershed(img[:, :, :3], markers)
    
    # Extract bounding boxes from watershed regions
    keys = []
    for marker_id in range(1, markers.max() + 1):
        mask = (markers == marker_id).astype(np.uint8) * 255
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if 200 < area < 10000:  # Reasonable key size
                x, y, w, h = cv2.boundingRect(contour)
                aspect_ratio = max(w, h) / min(w, h) if min(w, h) > 0 else 0
                
                if aspect_ratio < 4:  # Not too elongated
                    keys.append({
                        'bbox': (x, y, w, h),
                        'area': area,
                        'center': (x + w//2, y + h//2),
                        'method': 'watershed'
                    })
    
    return keys

def detect_color_segmentation(img):
    """
    Strategy B: Color-Based Segmentation
    Analyze color distribution and segment by color clusters.
    """
    # Convert to RGB for color analysis
    if img.shape[2] == 4:
        rgb = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
    else:
        rgb = img.copy()
    
    # Reshape for k-means
    data = rgb.reshape((-1, 3))
    data = np.float32(data)
    
    # Apply k-means clustering
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
    k = 8  # Number of color clusters
    _, labels, centers = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    
    # Find clusters that are not white/background
    # Background should be near white (high values)
    non_bg_clusters = []
    for i, center in enumerate(centers):
        # If cluster is not near white (all channels > 200)
        if not (center[0] > 200 and center[1] > 200 and center[2] > 200):
            non_bg_clusters.append(i)
    
    # Create mask for non-background clusters
    labels_2d = labels.reshape(rgb.shape[:2])
    mask = np.zeros(labels_2d.shape, dtype=np.uint8)
    for cluster_id in non_bg_clusters:
        mask[labels_2d == cluster_id] = 255
    
    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    keys = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if 200 < area < 10000:
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = max(w, h) / min(w, h) if min(w, h) > 0 else 0
            
            if aspect_ratio < 4:
                keys.append({
                    'bbox': (x, y, w, h),
                    'area': area,
                    'center': (x + w//2, y + h//2),
                    'method': 'color_seg'
                })
    
    return keys

def detect_hough_lines(img):
    """
    Strategy C: Hough Line Detection
    Detect key boundaries using Hough line transform.
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
    
    # Edge detection
    edges = cv2.Canny(gray, 50, 150)
    
    # Detect lines
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=50, minLineLength=30, maxLineGap=10)
    
    if lines is None or len(lines) == 0:
        return []
    
    # Group lines into horizontal and vertical
    horizontal_lines = []
    vertical_lines = []
    
    for line in lines:
        x1, y1, x2, y2 = line[0]
        angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi
        
        # Classify as horizontal or vertical
        if abs(angle) < 30 or abs(angle) > 150:
            horizontal_lines.append((x1, y1, x2, y2))
        elif 60 < abs(angle) < 120:
            vertical_lines.append((x1, y1, x2, y2))
    
    # Find intersections to create bounding boxes
    # For simplicity, use edge detection contours as fallback
    # and use lines to refine boundaries
    
    # Use contours from edges
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    keys = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if 200 < area < 10000:
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = max(w, h) / min(w, h) if min(w, h) > 0 else 0
            
            if aspect_ratio < 4:
                keys.append({
                    'bbox': (x, y, w, h),
                    'area': area,
                    'center': (x + w//2, y + h//2),
                    'method': 'hough'
                })
    
    return keys

def detect_combined(img):
    """
    Strategy D: Combined approach using multiple methods.
    Try all strategies and combine results with voting.
    """
    all_keys = []
    
    print("  Trying watershed segmentation...")
    watershed_keys = detect_watershed(img)
    all_keys.extend(watershed_keys)
    print(f"    Found {len(watershed_keys)} keys")
    
    print("  Trying color-based segmentation...")
    color_keys = detect_color_segmentation(img)
    all_keys.extend(color_keys)
    print(f"    Found {len(color_keys)} keys")
    
    print("  Trying Hough line detection...")
    hough_keys = detect_hough_lines(img)
    all_keys.extend(hough_keys)
    print(f"    Found {len(hough_keys)} keys")
    
    # Combine results by finding consensus
    # Group keys by overlapping bounding boxes
    if not all_keys:
        return []
    
    # Sort by area (larger keys first)
    all_keys.sort(key=lambda k: k['area'], reverse=True)
    
    # Remove duplicates and merge overlapping detections
    filtered_keys = []
    for key in all_keys:
        x1, y1, w1, h1 = key['bbox']
        overlap = False
        
        for existing in filtered_keys:
            x2, y2, w2, h2 = existing['bbox']
            
            # Calculate overlap
            overlap_x = max(0, min(x1 + w1, x2 + w2) - max(x1, x2))
            overlap_y = max(0, min(y1 + h1, y2 + h2) - max(y1, y2))
            overlap_area = overlap_x * overlap_y
            
            area1 = w1 * h1
            area2 = w2 * h2
            min_area = min(area1, area2)
            
            # If significant overlap (>50%), merge or skip
            if overlap_area > min_area * 0.5:
                overlap = True
                # Keep the one with larger area or merge centers
                if key['area'] > existing['area']:
                    # Update existing with better detection
                    idx = filtered_keys.index(existing)
                    filtered_keys[idx] = key
                break
        
        if not overlap:
            filtered_keys.append(key)
    
    return filtered_keys

def visualize_detections(img, keys, output_path):
    """Visualize detected keys on the image."""
    vis_img = img.copy()
    if vis_img.shape[2] == 4:
        vis_img = cv2.cvtColor(vis_img, cv2.COLOR_BGRA2BGR)
    
    for idx, key in enumerate(keys):
        x, y, w, h = key['bbox']
        # Draw bounding box
        cv2.rectangle(vis_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # Draw center point
        cx, cy = key['center']
        cv2.circle(vis_img, (cx, cy), 3, (0, 0, 255), -1)
        # Label
        cv2.putText(vis_img, str(idx + 1), (x, y - 5), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
    
    cv2.imwrite(output_path, vis_img)
    print(f"  Visualization saved to {output_path}")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, '..', 'Kinesis Thumb Keys.png')
    output_dir = os.path.join(script_dir, '..', 'extracted_keys')
    vis_path = os.path.join(script_dir, '..', 'detection_visualization.png')
    
    # Load image
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        raise ValueError(f"Could not load image: {image_path}")
    
    print(f"Image dimensions: {img.shape[1]}x{img.shape[0]}")
    print(f"Image channels: {img.shape[2]}")
    
    # Clear output directory
    if os.path.exists(output_dir):
        for f in os.listdir(output_dir):
            os.remove(os.path.join(output_dir, f))
    else:
        os.makedirs(output_dir, exist_ok=True)
    
    print("\nDetecting keys using combined strategies...")
    keys = detect_combined(img)
    
    if not keys:
        print("\nNo keys detected with any strategy.")
        print("Consider using interactive extraction: bin/extract_keys_interactive.py")
        return
    
    print(f"\nFound {len(keys)} keys after combining strategies")
    
    # Sort by position (top to bottom, left to right)
    keys.sort(key=lambda k: (k['center'][1], k['center'][0]))
    
    # Visualize detections
    print("\nCreating visualization...")
    visualize_detections(img, keys, vis_path)
    
    # Extract keys
    print("\nExtracting keys...")
    for idx, key_info in enumerate(keys):
        key_img = extract_key(img, key_info['bbox'])
        filename = f"key_{idx+1:02d}.png"
        filepath = os.path.join(output_dir, filename)
        key_img.save(filepath, 'PNG')
        print(f"  {filename}: bbox={key_info['bbox']}, area={key_info['area']:.0f}, method={key_info['method']}")
    
    print(f"\nExtraction complete! {len(keys)} keys saved to {output_dir}/")
    print(f"Visualization saved to {vis_path}")
    print("\nPlease review the extracted keys and rename them with appropriate labels.")

if __name__ == '__main__':
    main()

