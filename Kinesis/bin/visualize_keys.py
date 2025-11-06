#!/usr/bin/env python3
"""
Visualization helper to identify key positions.
Creates an annotated image showing coordinates and grid lines.
"""

import cv2
import numpy as np

def create_annotated_image(image_path, output_path):
    """Create an annotated version of the image with coordinate grid."""
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    
    # Convert to BGR for annotation
    if img.shape[2] == 4:
        annotated = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    else:
        annotated = img.copy()
    
    h, w = annotated.shape[:2]
    
    # Draw grid lines every 20 pixels
    for x in range(0, w, 20):
        cv2.line(annotated, (x, 0), (x, h), (200, 200, 200), 1)
        if x % 100 == 0:
            cv2.putText(annotated, str(x), (x+2, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (100, 100, 255), 1)
    
    for y in range(0, h, 20):
        cv2.line(annotated, (0, y), (w, y), (200, 200, 200), 1)
        if y % 100 == 0 and y > 0:
            cv2.putText(annotated, str(y), (2, y+12), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (100, 100, 255), 1)
    
    # Add corner coordinates
    cv2.putText(annotated, "(0,0)", (5, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)
    cv2.putText(annotated, f"({w},{h})", (w-60, h-5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)
    
    # Add instructions
    cv2.putText(annotated, "Use this image to identify key bounding boxes", 
                (10, h-30), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 0), 1)
    cv2.putText(annotated, "Format: (x, y, width, height)", 
                (10, h-15), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 0), 1)
    
    cv2.imwrite(output_path, annotated)
    print(f"Annotated image saved to: {output_path}")
    print(f"Image dimensions: {w}x{h}")
    print("\nUse an image viewer to identify key positions.")
    print("For each key, note:")
    print("  - x: left edge position")
    print("  - y: top edge position") 
    print("  - width: key width")
    print("  - height: key height")

if __name__ == '__main__':
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, '..', 'Kinesis Thumb Keys.png')
    output_path = os.path.join(script_dir, '..', 'Kinesis Thumb Keys_annotated.png')
    create_annotated_image(image_path, output_path)
