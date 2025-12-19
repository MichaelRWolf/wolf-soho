#!/usr/bin/env python3
"""
Diagnostic script to understand the image structure and adjust extraction parameters.
"""

import cv2
import numpy as np
from PIL import Image
import os

def diagnose_image(image_path):
    """Analyze the image to understand its structure."""
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    
    print(f"Image shape: {img.shape}")
    print(f"Image dtype: {img.dtype}")
    print(f"Min/Max values: {img.min()}/{img.max()}")
    
    # Check alpha channel
    if img.shape[2] == 4:
        alpha = img[:, :, 3]
        print(f"Alpha channel - Min: {alpha.min()}, Max: {alpha.max()}, Mean: {alpha.mean()}")
        print(f"Transparent pixels: {(alpha < 255).sum()}")
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
    print(f"\nGrayscale - Min: {gray.min()}, Max: {gray.max()}, Mean: {gray.mean()}")
    
    # Try different thresholds
    print("\nTrying different threshold values:")
    for thresh_val in [50, 100, 127, 150, 200]:
        _, thresh = cv2.threshold(gray, thresh_val, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        areas = [cv2.contourArea(c) for c in contours]
        if areas:
            print(f"  Threshold {thresh_val}: {len(contours)} contours, areas: min={min(areas):.0f}, max={max(areas):.0f}, mean={np.mean(areas):.0f}")
        else:
            print(f"  Threshold {thresh_val}: {len(contours)} contours")
    
    # Try adaptive threshold
    print("\nTrying adaptive threshold:")
    adaptive = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    contours, _ = cv2.findContours(adaptive, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    areas = [cv2.contourArea(c) for c in contours]
    if areas:
        print(f"  Adaptive: {len(contours)} contours, areas: min={min(areas):.0f}, max={max(areas):.0f}, mean={np.mean(areas):.0f}")
    
    # Try Canny edge detection
    print("\nTrying Canny edge detection:")
    edges = cv2.Canny(gray, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    areas = [cv2.contourArea(c) for c in contours]
    if areas:
        print(f"  Canny: {len(contours)} contours, areas: min={min(areas):.0f}, max={max(areas):.0f}, mean={np.mean(areas):.0f}")

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, '..', 'Kinesis Thumb Keys.png')
    diagnose_image(image_path)
