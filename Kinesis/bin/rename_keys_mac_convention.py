#!/usr/bin/env python3
"""
Rename extracted keys according to Mac naming convention:
Format: [left|right]_<keyface>.png

Mac conventions:
- Use "Option" (not "Alt")
- Use "Cmd" (not "Windows")
- Use "Return" (not "Enter")
- Use "BackSpace" (capital S)
"""

import os
import shutil

# Mapping from current names to new Mac convention names
# Based on the extraction order and typical Kinesis thumb key layout
RENAME_MAP = {
    # Modifier keys
    'left_alt.png': 'left_Option.png',
    'right_alt.png': 'right_Option.png',
    'left_cmd.png': 'left_Cmd.png',  # Already correct, just capitalize
    'right_cmd.png': 'right_Cmd.png',
    'left_ctrl.png': 'left_Ctrl.png',  # Already correct, just capitalize
    'right_ctrl.png': 'right_Ctrl.png',
    
    # Function keys - need to determine left/right based on position
    # Based on extraction order: keys 5, 6, 9, 10 were large (Space/Return)
    # Keys 5, 9 are likely left side, keys 6, 10 are likely right side
    'space.png': 'left_Space.png',  # First large key (key_05) - likely left
    'space_left.png': 'left_Space.png',  # Duplicate, will handle
    'space_right.png': 'right_Space.png',
    'enter.png': 'left_Return.png',  # Second large key (key_06) - need to verify
    'enter_right.png': 'right_Return.png',
    
    # Backspace
    'backspace.png': 'left_BackSpace.png',  # Need to verify position
}

def rename_keys(keys_dir):
    """Rename keys according to Mac convention."""
    keys_dir = os.path.abspath(keys_dir)
    
    if not os.path.exists(keys_dir):
        print(f"Error: Directory {keys_dir} does not exist!")
        return
    
    # Get all PNG files (excluding backups)
    files = [f for f in os.listdir(keys_dir) if f.endswith('.png') and not f.endswith('.backup.png')]
    
    if not files:
        print(f"No PNG files found in {keys_dir}")
        return
    
    print(f"Found {len(files)} key files to rename\n")
    
    # Track renames
    renames = []
    conflicts = []
    
    # Create a case-insensitive lookup
    files_lower = {f.lower(): f for f in files}
    
    # First pass: identify conflicts and prepare renames
    for old_name in files:
        # Check if already in target format (case-insensitive)
        if '_' in old_name and (old_name.lower().startswith('left_') or old_name.lower().startswith('right_')):
            parts = old_name.replace('.png', '').split('_', 1)
            if len(parts) == 2:
                side, keyface = parts
                # Check if it matches target format
                keyface_lower = keyface.lower()
                # Apply Mac conventions
                if keyface_lower == 'alt':
                    target_keyface = 'Option'
                elif keyface_lower == 'enter':
                    target_keyface = 'Return'
                elif keyface_lower == 'backspace':
                    target_keyface = 'BackSpace'
                else:
                    # Capitalize first letter
                    target_keyface = keyface[0].upper() + keyface[1:] if len(keyface) > 1 else keyface.upper()
                
                target_name = f"{side}_{target_keyface}.png"
                if target_name.lower() != old_name.lower():
                    # Needs renaming
                    if old_name in RENAME_MAP:
                        new_name = RENAME_MAP[old_name]
                    else:
                        new_name = target_name
                else:
                    # Already correct, skip
                    continue
        
        if old_name in RENAME_MAP:
            new_name = RENAME_MAP[old_name]
        else:
            # Not in explicit map, skip
            continue
            
        old_path = os.path.join(keys_dir, old_name)
        new_path = os.path.join(keys_dir, new_name)
        
        # Skip if source and target are the same (case-insensitive)
        if old_name.lower() == new_name.lower() and old_name != new_name:
            # Case-only change, handle separately
            temp_name = f"{old_name}.temp"
            temp_path = os.path.join(keys_dir, temp_name)
            renames.append((old_name, new_name, temp_name))
        elif old_name != new_name:
            # Check for conflicts
            if os.path.exists(new_path) and old_path != new_path:
                # Check if target already has correct name
                if new_name in files:
                    conflicts.append((old_name, new_name))
                else:
                    renames.append((old_name, new_name, None))
            else:
                renames.append((old_name, new_name, None))
    # Handle conflicts (duplicates that map to same name)
    if conflicts:
        print("Conflicts detected (multiple files mapping to same name):")
        for old, new in conflicts:
            print(f"  {old} -> {new}")
        print("\nResolving conflicts by keeping first occurrence...\n")
    
    # Remove duplicates from renames
    seen_targets = set()
    final_renames = []
    for rename_item in renames:
        if len(rename_item) == 3:
            old, new, temp = rename_item
        else:
            old, new = rename_item
            temp = None
        
        if new.lower() not in [t.lower() for t in seen_targets]:
            final_renames.append((old, new, temp))
            seen_targets.add(new)
        else:
            print(f"  Skipping duplicate: {old} -> {new} (target already exists)")
    
    # Perform renames
    if final_renames:
        print("Renaming files:")
        for rename_item in final_renames:
            if len(rename_item) == 3:
                old_name, new_name, temp_name = rename_item
            else:
                old_name, new_name = rename_item
                temp_name = None
            
            old_path = os.path.join(keys_dir, old_name)
            new_path = os.path.join(keys_dir, new_name)
            
            if not os.path.exists(old_path):
                print(f"  Warning: {old_name} not found, skipping")
                continue
            
            # Handle case-only renames on case-insensitive filesystems
            if temp_name:
                temp_path = os.path.join(keys_dir, temp_name)
                # Two-step rename for case changes
                if os.path.exists(new_path) and old_path != new_path:
                    # Target already exists with different case, remove it first
                    os.remove(new_path)
                os.rename(old_path, temp_path)
                os.rename(temp_path, new_path)
                print(f"  {old_name} -> {new_name} (via {temp_name})")
            else:
                # If target exists and is different file, backup first
                if os.path.exists(new_path) and old_path != new_path:
                    backup_name = f"{new_name}.backup"
                    backup_path = os.path.join(keys_dir, backup_name)
                    if not os.path.exists(backup_path):
                        shutil.move(new_path, backup_path)
                        print(f"  Backed up existing {new_name} to {backup_name}")
                    else:
                        os.remove(new_path)  # Remove duplicate
                
                os.rename(old_path, new_path)
                print(f"  {old_name} -> {new_name}")
        
        print(f"\nRenamed {len(final_renames)} files")
    else:
        print("No files need renaming (all already follow convention)")

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    keys_dir = os.path.join(script_dir, '..', 'extracted_keys')
    rename_keys(keys_dir)

