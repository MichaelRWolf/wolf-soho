#!/usr/bin/env python3
"""
Extract keys using manually specified coordinates.
Edit the KEY_COORDINATES list below with the bounding boxes for each key.
Format: (x, y, width, height)
"""

import cv2
import numpy as np
from PIL import Image
import os

# MANUAL KEY COORDINATES - Edit these based on image inspection
# Format: list of tuples, each tuple is (x, y, width, height, label)
# Labels will be used for filenames (sanitized)
KEY_COORDINATES = [
    # Example format - these need to be filled in by inspecting the image
    # (x, y, w, h, 'label'),
    # You can use an image viewer to get pixel coordinates
]

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
    
    # Make bright pixels transparent (threshold can be adjusted)
    alpha[gray > 240] = 0
    
    if img_array.shape[2] == 4:
        img_array[:, :, 3] = alpha
    else:
        img_array = np.dstack([img_array, alpha])
    
    return Image.fromarray(img_array, 'RGBA')

def sanitize_filename(name):
    """Convert label to safe filename."""
    import re
    name = re.sub(r'[^a-zA-Z0-9_\-]', '_', name.lower())
    name = re.sub(r'_+', '_', name)
    return name.strip('_')

def main():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, '..', 'Kinesis Thumb Keys.png')
    output_dir = os.path.join(script_dir, '..', 'extracted_keys')
    
    # Load image
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        raise ValueError(f"Could not load image: {image_path}")
    
    print(f"Image dimensions: {img.shape[1]}x{img.shape[0]}")
    
    if not KEY_COORDINATES:
        print("\nERROR: No key coordinates specified!")
        print("\nPlease edit this script and add key coordinates to KEY_COORDINATES list.")
        print("Format: (x, y, width, height, 'label')")
        print("\nTo find coordinates:")
        print("1. Open the image in an image viewer")
        print("2. Note the (x, y) position of top-left corner of each key")
        print("3. Note the width and height of each key")
        print("4. Add entries like: (x, y, w, h, 'left_cmd'), ...")
        return
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Clear existing files
    for f in os.listdir(output_dir):
        if f.endswith('.png'):
            os.remove(os.path.join(output_dir, f))
    
    print(f"\nExtracting {len(KEY_COORDINATES)} keys...")
    
    for idx, coord in enumerate(KEY_COORDINATES):
        if len(coord) == 5:
            x, y, w, h, label = coord
            filename = f"{sanitize_filename(label)}.png"
        else:
            x, y, w, h = coord[:4]
            filename = f"key_{idx+1:02d}.png"
        
        key_img = extract_key(img, (x, y, w, h))
        filepath = os.path.join(output_dir, filename)
        key_img.save(filepath, 'PNG')
        print(f"  {filename}: bbox=({x}, {y}, {w}, {h})")
    
    print(f"\nExtraction complete! {len(KEY_COORDINATES)} keys saved to {output_dir}/")

if __name__ == '__main__':
    main()
