# Key Remapping Plan

## Task Summary

Extract each individual keycap from the keyboard diagram (`Kinesis Thumb Keys.png`) into **separate PNG files**, each named according to its position and label. Later, recombine the remapped keys into a new layout.

Each PNG should have:

* Transparent background
* Cropped tightly around the key
* Same scale and resolution as the source image

---

## Answers to Clarifying Questions

1. **Source image:** `Kinesis Thumb Keys.png` (the referenced file)

2. **Output goal:**
   * **Phase 1:** Extract all individual key images as separate PNG files
   * **Phase 2:** Later, recombine remapped keys into a new layout

3. **Scope:** Extract **all keys** from the source image

4. **Automation:** Generate a script (Python + Pillow or ImageMagick) to automatically crop and name them

5. **Naming convention:** To be determined based on key analysis (literal labels like `left_cmd_key.png` or positional like `L1_alt.png`)

6. **Cropping precision:** To be determined - analyze image to see if keys are evenly spaced (coordinate-based) or need edge detection

---

## Implementation Plan

1. **Analyze source image:**
   * Determine image dimensions and key layout
   * Identify if keys are evenly spaced or irregular
   * Count total number of keys

2. **Determine naming convention:**
   * Analyze key labels and positions
   * Choose appropriate naming scheme

3. **Create extraction script:**
   * Use Python + Pillow for image processing
   * Detect key boundaries (coordinate-based or edge detection)
   * Extract each key with transparent background
   * Save with appropriate names

4. **Test extraction:**
   * Verify all keys are extracted correctly
   * Ensure transparent backgrounds work properly
   * Check naming consistency

5. **Phase 2 (Future):**
   * Create recombination script for remapped layout
