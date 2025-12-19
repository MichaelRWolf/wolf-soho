# Key Remapping Plan

## Task Summary

Extract each individual keycap from the keyboard diagram (`Kinesis Thumb Keys.png`) into **separate PNG files**, each named according to its position and label. Later, recombine the remapped keys into a new layout.

**Important:** The Kinesis keyboard keys are arranged diagonally, not in a standard horizontal/vertical grid. This affects the extraction approach - coordinate-based grid slicing will not work; individual key detection and edge detection will be necessary.

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

6. **Cropping precision:** Keys are arranged diagonally (not horizontal/vertical grid), so edge detection will be required rather than coordinate-based slicing

---

## Current State

**Analysis Complete:**

* Image dimensions: 362x164 pixels
* Image mode: RGBA (supports transparency)
* Key layout: Diagonal arrangement (not standard grid)
* Challenge: White background makes automatic key detection difficult

**Scripts Created:**

* `bin/extract_keys_interactive.py` - Interactive tool for manual selection
* `bin/extract_with_coords.py` - Coordinate-based extraction
* `bin/visualize_keys.py` - Creates annotated image with coordinate grid
* `bin/extract_keys_improved.py` - Multi-strategy automated detection (SUCCESSFUL)
* `bin/diagnose_image.py` - Image analysis tool

See `EXTRACTION_STATUS.md` for detailed status of previous attempts.

**Status:** Keys successfully extracted using watershed segmentation method.

* **Keys extracted:** 12 keys
* **Output location:** `extracted_keys/` directory
* **File naming:** `key_01.png` through `key_12.png` (temporary names)
* **Image properties:** RGBA mode with transparent backgrounds (white pixels >240 threshold)
* **Detection method:** Watershed segmentation successfully identified all keys
* **Visualization:** `detection_visualization.png` shows bounding boxes for all detected keys

## Implementation Plan

1. **Implement improved automated detection:**
   * Create `bin/extract_keys_improved.py` with multiple detection strategies:
     * Watershed segmentation
     * Color-based segmentation
     * Hough line detection for key boundaries
     * Template matching (if applicable)
   * Try each strategy and combine results
   * Visualize detections for debugging

2. **Extract keys with transparent backgrounds:**
   * Use best detection results or combination of strategies
   * Extract each key region with padding
   * Make white/light backgrounds transparent (threshold ~240)
   * Save to `extracted_keys/` with temporary names (`key_01.png`, etc.)

3. **Review and refine:**
   * Visual inspection of extracted keys
   * Refine parameters or try hybrid approach if needed
   * Document which strategy worked best

4. **Determine naming convention:**
   * Analyze extracted keys visually
   * Identify key labels (Cmd, Ctrl, Alt, Enter, Backspace, Space, etc.)
   * Create naming scheme based on key labels or positions
   * Rename extracted files accordingly

5. **Update documentation:**
   * Update `EXTRACTION_STATUS.md` with results
   * Document successful detection method

6. **Phase 2 (Future):**
   * Create recombination script for remapped layout
