#!/usr/bin/env python3
"""
Interactive script to extract keys by manually specifying coordinates.
Shows the image and allows you to click to define key regions.
"""

import cv2
import numpy as np
from PIL import Image
import os

# Global variables for mouse callback
drawing = False
start_point = None
end_point = None
keys = []

def mouse_callback(event, x, y, flags, param):
    """Handle mouse events for selecting key regions."""
    global drawing, start_point, end_point, keys, img_display
    
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        start_point = (x, y)
        end_point = (x, y)
    
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            end_point = (x, y)
            # Redraw image with current selection
            img_copy = img_display.copy()
            cv2.rectangle(img_copy, start_point, end_point, (0, 255, 0), 2)
            cv2.imshow('Select Keys - Click and drag, press SPACE to save, Q to quit', img_copy)
    
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        end_point = (x, y)
        if start_point and end_point:
            # Calculate bounding box
            x1, y1 = start_point
            x2, y2 = end_point
            x_min = min(x1, x2)
            y_min = min(y1, y2)
            x_max = max(x1, x2)
            y_max = max(y1, y2)
            w = x_max - x_min
            h = y_max - y_min
            
            if w > 10 and h > 10:  # Minimum size
                keys.append({
                    'bbox': (x_min, y_min, w, h),
                    'label': f"key_{len(keys)+1}"
                })
                print(f"Added key {len(keys)}: bbox=({x_min}, {y_min}, {w}, {h})")
                
                # Draw saved rectangle in blue
                cv2.rectangle(img_display, (x_min, y_min), (x_max, y_max), (255, 0, 0), 2)
                cv2.imshow('Select Keys - Click and drag, press SPACE to save, Q to quit', img_display)

def extract_key(img, bbox, padding=2):
    """Extract a key region from the image."""
    x, y, w, h = bbox
    
    x_start = max(0, x - padding)
    y_start = max(0, y - padding)
    x_end = min(img.shape[1], x + w + padding)
    y_end = min(img.shape[0], y + h + padding)
    
    roi = img[y_start:y_end, x_start:x_end].copy()
    pil_img = Image.fromarray(cv2.cvtColor(roi, cv2.COLOR_BGRA2RGBA))
    
    return pil_img

def make_background_transparent(pil_img, threshold=240):
    """Make white/light background transparent."""
    img_array = np.array(pil_img)
    
    if img_array.shape[2] == 4:
        gray = cv2.cvtColor(img_array[:, :, :3], cv2.COLOR_RGBA2RGB)
        gray = cv2.cvtColor(gray, cv2.COLOR_RGB2GRAY)
        alpha = img_array[:, :, 3].copy()
    else:
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        alpha = np.ones((img_array.shape[0], img_array.shape[1]), dtype=np.uint8) * 255
    
    alpha[gray > threshold] = 0
    
    if img_array.shape[2] == 4:
        img_array[:, :, 3] = alpha
    else:
        img_array = np.dstack([img_array, alpha])
    
    return Image.fromarray(img_array, 'RGBA')

def main():
    global img_display
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, '..', 'Kinesis Thumb Keys.png')
    output_dir = os.path.join(script_dir, '..', 'extracted_keys')
    
    # Load image
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        raise ValueError(f"Could not load image: {image_path}")
    
    # Convert to BGR for display (OpenCV uses BGR)
    if img.shape[2] == 4:
        img_display = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    else:
        img_display = img.copy()
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    print("=" * 60)
    print("Interactive Key Extraction")
    print("=" * 60)
    print("\nInstructions:")
    print("1. Click and drag to select a key region (green rectangle)")
    print("2. Release mouse button to save the selection (blue rectangle)")
    print("3. Press SPACE to finish and extract all selected keys")
    print("4. Press Q to quit without extracting")
    print("\nStart selecting keys...")
    
    cv2.namedWindow('Select Keys - Click and drag, press SPACE to save, Q to quit')
    cv2.setMouseCallback('Select Keys - Click and drag, press SPACE to save, Q to quit', mouse_callback)
    
    cv2.imshow('Select Keys - Click and drag, press SPACE to save, Q to quit', img_display)
    
    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            print("\nQuitting without extracting.")
            cv2.destroyAllWindows()
            return
        elif key == ord(' '):
            break
    
    cv2.destroyAllWindows()
    
    if not keys:
        print("\nNo keys selected. Exiting.")
        return
    
    print(f"\nExtracting {len(keys)} keys...")
    
    for idx, key_info in enumerate(keys):
        key_img = extract_key(img, key_info['bbox'])
        key_img = make_background_transparent(key_img)
        
        filename = f"{key_info['label']}.png"
        filepath = os.path.join(output_dir, filename)
        key_img.save(filepath, 'PNG')
        print(f"  Saved: {filename}")
    
    print(f"\nExtraction complete! {len(keys)} keys saved to {output_dir}/")

if __name__ == '__main__':
    main()
