#!/usr/bin/env python3
"""
Analyze extracted keys and suggest names based on position and typical Kinesis layout.
"""

import cv2
import os
import glob

def analyze_keys(keys_dir):
    """Analyze extracted keys to determine naming."""
    key_files = sorted(glob.glob(os.path.join(keys_dir, 'key_*.png')))
    
    keys_info = []
    for key_file in key_files:
        img = cv2.imread(key_file, cv2.IMREAD_UNCHANGED)
        if img is not None:
            h, w = img.shape[:2]
            filename = os.path.basename(key_file)
            key_num = int(filename.replace('key_', '').replace('.png', ''))
            
            keys_info.append({
                'num': key_num,
                'filename': filename,
                'width': w,
                'height': h,
                'area': w * h,
                'aspect': max(w, h) / min(w, h) if min(w, h) > 0 else 0
            })
    
    # Sort by number
    keys_info.sort(key=lambda k: k['num'])
    
    return keys_info

def suggest_names(keys_info):
    """
    Suggest names based on key characteristics.
    Typical Kinesis thumb keys layout:
    - Smaller keys (Cmd, Ctrl, Alt) are ~38-44px
    - Larger keys (Space, Enter, Backspace) are ~50-60px wide, 70-80px tall
    - Left side typically has left-hand modifiers
    - Right side typically has right-hand modifiers
    - Center has larger keys like Space, Enter
    """
    # Categorize by size
    small_keys = [k for k in keys_info if k['area'] < 2000]
    large_keys = [k for k in keys_info if k['area'] >= 2000]
    
    # Sort small keys by position (assuming left to right, top to bottom extraction)
    small_keys.sort(key=lambda k: (k['num']))
    large_keys.sort(key=lambda k: (k['num']))
    
    # Typical Kinesis thumb cluster has:
    # - 6-8 small modifier keys (Cmd, Ctrl, Alt on left and right)
    # - 2-4 larger keys (Space, Enter, Backspace)
    
    # Suggest names based on typical layout
    # This is a best guess - should be reviewed visually
    suggestions = {}
    
    # Large keys (likely Space, Enter, Backspace)
    if len(large_keys) >= 2:
        # First large key is often Space or Enter
        suggestions[large_keys[0]['num']] = 'space'  # Most common large thumb key
        if len(large_keys) >= 2:
            suggestions[large_keys[1]['num']] = 'enter'
        if len(large_keys) >= 3:
            suggestions[large_keys[2]['num']] = 'backspace'
        if len(large_keys) >= 4:
            suggestions[large_keys[3]['num']] = 'space_right'  # If there's a second space
    
    # Small keys - typically modifiers
    # Left side modifiers (first half)
    left_modifiers = ['left_cmd', 'left_ctrl', 'left_alt']
    right_modifiers = ['right_cmd', 'right_ctrl', 'right_alt']
    
    # Split small keys into left and right groups
    mid_point = len(small_keys) // 2
    left_small = small_keys[:mid_point]
    right_small = small_keys[mid_point:]
    
    for idx, key in enumerate(left_small):
        if idx < len(left_modifiers):
            suggestions[key['num']] = left_modifiers[idx]
        else:
            suggestions[key['num']] = f'left_mod_{idx+1}'
    
    for idx, key in enumerate(right_small):
        if idx < len(right_modifiers):
            suggestions[key['num']] = right_modifiers[idx]
        else:
            suggestions[key['num']] = f'right_mod_{idx+1}'
    
    return suggestions


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    keys_dir = os.path.join(script_dir, '..', 'extracted_keys')
    
    print("Analyzing extracted keys...")
    keys_info = analyze_keys(keys_dir)
    
    print(f"\nFound {len(keys_info)} keys:")
    for key in keys_info:
        print(f"  {key['filename']}: {key['width']}x{key['height']} (area={key['area']})")
    
    print("\nGenerating name suggestions...")
    suggestions = suggest_names(keys_info)
    
    print("\nSuggested names:")
    for num, name in sorted(suggestions.items()):
        key = next(k for k in keys_info if k['num'] == num)
        print(f"  {key['filename']} -> {name}.png")

if __name__ == '__main__':
    main()

