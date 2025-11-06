#!/usr/bin/env python3
"""
Helper script to visualize extracted keys in a grid for identification.
"""

import cv2
import numpy as np
from PIL import Image
import os
import glob

def create_key_grid(keys_dir, output_path=None, cols=4):
    """Create a grid visualization of all extracted keys."""
    if output_path is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(script_dir, '..', 'keys_grid.png')
    key_files = sorted(glob.glob(os.path.join(keys_dir, 'key_*.png')))
    
    if not key_files:
        print("No key files found!")
        return
    
    # Load all keys
    keys = []
    for key_file in key_files:
        img = cv2.imread(key_file, cv2.IMREAD_UNCHANGED)
        if img is not None:
            keys.append((img, os.path.basename(key_file)))
    
    if not keys:
        print("No valid key images found!")
        return
    
    # Calculate grid dimensions
    rows = (len(keys) + cols - 1) // cols
    
    # Find max dimensions
    max_h = max(img.shape[0] for img, _ in keys)
    max_w = max(img.shape[1] for img, _ in keys)
    
    # Add padding
    padding = 10
    cell_h = max_h + padding * 2 + 30  # Extra space for label
    cell_w = max_w + padding * 2
    
    # Create grid
    grid_h = rows * cell_h
    grid_w = cols * cell_w
    grid = np.ones((grid_h, grid_w, 4), dtype=np.uint8) * 255
    
    # Place keys in grid
    for idx, (key_img, filename) in enumerate(keys):
        row = idx // cols
        col = idx % cols
        
        y_start = row * cell_h + padding
        x_start = col * cell_w + padding
        
        # Center the key in its cell
        key_h, key_w = key_img.shape[:2]
        y_offset = (max_h - key_h) // 2
        x_offset = (max_w - key_w) // 2
        
        y_pos = y_start + y_offset
        x_pos = x_start + x_offset
        
        # Place key image
        if key_img.shape[2] == 4:
            # Handle RGBA
            alpha = key_img[:, :, 3:4] / 255.0
            rgb = key_img[:, :, :3]
            grid[y_pos:y_pos+key_h, x_pos:x_pos+key_w, :3] = (
                grid[y_pos:y_pos+key_h, x_pos:x_pos+key_w, :3] * (1 - alpha) + 
                rgb * alpha
            ).astype(np.uint8)
        else:
            grid[y_pos:y_pos+key_h, x_pos:x_pos+key_w, :3] = key_img
        
        # Add label
        label_y = y_start + max_h + 5
        label_x = x_start + max_w // 2
        cv2.putText(grid, filename.replace('.png', ''), 
                   (label_x - 40, label_y), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)
    
    # Save grid
    cv2.imwrite(output_path, grid)
    print(f"Key grid saved to {output_path}")
    print(f"Total keys: {len(keys)}")
    print("\nReview the grid to identify key labels, then update the naming.")

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    keys_dir = os.path.join(script_dir, '..', 'extracted_keys')
    create_key_grid(keys_dir)

