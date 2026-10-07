# Wendy's MacBook Air Bring-Up Strategy

**Goal:** Restore wendy-pro Time Machine backup to new M3 Air 16GB 512GB, avoiding space crunch and unnecessary bloat.

**Backup source:** `/Volumes/Backups of wendy-pro/2026-06-27-202218.previous/Data/Users/wendy/`

**Date assessed:** 2026-10-07

---

## Backup Contents Audit (Quick Survey)

### What's Actually in the Backup

**Folders identified:**

- **Library/** -- Mail, Preferences, Keychain, app data (critical)
- **Documents/** -- Work files
- **Downloads-precious/** -- Intentionally saved downloads (keep)
- **Desktop/** -- Desktop files
- **Pictures/, fb pics 2010/** -- Photo archives
- **Movies/, Music/** -- Empty or minimal
- **Applications/** -- Skip (reinstall fresh on new machine)
- **bin/, sbin/, Michael/, tmp/** -- Config/system stuff (skip most)

**Estimated sizes (actual content, not metadata):**

- Library: ~10-20GB (Mail, prefs, Keychain)
- Documents: ~5-10GB
- Downloads-precious: ~2-5GB
- Desktop: <1GB
- Pictures/photos: ~10-20GB
- Movies/Music: ~0-2GB
- **Total estimate: 40-60GB**

**Storage budget on new 512GB MBA:**

- macOS Sonoma: ~20GB
- Applications (fresh): ~30GB
- Free space headroom: ~100GB (10GB per major app category)
- **Available for restore: ~360GB** ✅ Comfortable

---

## Selective Restore Strategy

### What to Restore

**MUST RESTORE (Critical to operation):**

1. **Library/** -- All of it
   - Mail.app IMAP config + cache
   - Preferences + settings
   - Keychain (passwords)
   - Safari bookmarks
   - App data (MailChimp client, Photos, Notes, etc.)

2. **Documents/** -- All
   - Work files, projects, writing

3. **Downloads-precious/** -- All
   - Intentionally saved files

4. **Desktop/** -- All
   - Any files saved to Desktop

**SHOULD RESTORE (Helpful but not critical):**

1. **Pictures/, fb pics 2010/** -- Consider restoring
   - Photo archives (Wendy's personal collection)
   - Estimate: ~15-20GB
   - **Decision: Restore if space allows; otherwise skip and rely on iCloud Photos**

**DO NOT RESTORE (Waste of space):**

- **Applications/** -- Reinstall fresh from App Store (cleaner)
- **Movies/, Music/** -- Empty or streaming (don't need local copy)
- **System folders** (bin/, sbin/, tmp/, .Trash/) -- OS provides fresh versions
- **Brewfile, brew-packages, analyze_brew.sh** -- Reference only; skip

---

## Restore Execution Plan

### Step 1: Prepare New Machine (First Boot)

1. Complete macOS setup (Sonoma, Wi-Fi, iCloud login if desired)
2. Create `wendy` user account (or keep default setup)
3. Do NOT use "Migrate from Time Machine" (too heavy; selective approach instead)

### Step 2: Mount Backup (Read-Only)

```bash
# Mount the sparsebundle without modifying it
hdiutil attach -readonly /Volumes/Backups\ of\ wendy-pro/2026-06-27-202218.previous/wendy-pro0.sparsebundle
```

Will show up as `/Volumes/Time Machine Backups/` or similar.

### Step 3: Copy Critical Folders

```bash
# Copy Library (this is the big one; ~15-20GB)
cp -r /Volumes/Time\ Machine\ Backups/Data/Users/wendy/Library ~/Library

# Copy Documents
cp -r /Volumes/Time\ Machine\ Backups/Data/Users/wendy/Documents ~/Documents

# Copy Downloads-precious
cp -r /Volumes/Time\ Machine\ Backups/Data/Users/wendy/Downloads-precious ~/Downloads-precious

# Copy Desktop
cp -r /Volumes/Time\ Machine\ Backups/Data/Users/wendy/Desktop ~/Desktop
```

**Runtime estimate:** 15-30 minutes over LAN/USB (depending on drive speed and network)

### Step 4: Verify & Test

After restore:

- ✅ Mail.app opens and syncs
- ✅ Safari bookmarks appear
- ✅ Keychain accessible (test password entry)
- ✅ iCloud Drive syncs
- ✅ Photos app recognizes library (or import from iCloud)

### Step 5: Photos (Optional)

If restoring Pictures/photo folders:

```bash
cp -r /Volumes/Time\ Machine\ Backups/Data/Users/wendy/Pictures ~/Pictures
cp -r /Volumes/Time\ Machine\ Backups/Data/Users/wendy/fb\ pics\ 2010 ~/fb-pics-archive
```

**If space is tight:** Skip this; Wendy's photos likely live in iCloud Photos or can be imported later.

### Step 6: Eject Backup

```bash
hdiutil eject /Volumes/Time\ Machine\ Backups/
```

---

## Space Accounting

| Component                                  | Size      | Notes                                |
|--------------------------------------------|-----------|--------------------------------------|
| macOS Sonoma (clean install)               | 20GB      | Baseline                             |
| App Store apps (Mail, Safari, Notes, etc.) | 10GB      | Pre-installed; minimal               |
| Restore: Library/                          | 15GB      | Mail, Keychain, prefs                |
| Restore: Documents/                        | 8GB       | Work files                           |
| Restore: Downloads-precious/               | 3GB       | Important files                      |
| Restore: Desktop/                          | 1GB       | Desktop files                        |
| Restore: Pictures/ (optional)              | 15GB      | Photo archives                       |
| **Subtotal (without Pictures)**            | **57GB**  | ✅ Safe                               |
| **With Pictures**                          | **72GB**  | ✅ Still safe                         |
| **Free space after**                       | **440GB** | Headroom for video projects, exports |

---

## Fallback: Space Issues

If copy operations fail or space runs short:

1. **Pause the copy** (Ctrl+C)
2. **Identify the culprit** (check what's consuming space: `du -sh ~/*`)
3. **Defer that folder** (skip Photos or large files; can restore later)
4. **Resume with smaller folders** (Documents, Downloads-precious first)
5. **Later:** Restore large folders to NAS instead of local drive

---

## Post-Restore: NAS Sync Strategy

Once new machine is operational:

1. **Set up NAS Time Machine** (optional; Wendy can rely on iCloud)
2. **Archive old backup to NAS** (keep wendy-pro backup as reference)
3. **Begin daily sync** (if using NAS backup for document history)

---

## Timeline

- **Day 1:** Receive new M3 Air, boot & initial setup (1 hour)
- **Day 1-2:** Selective restore (1-2 hours actual copy time)
- **Day 2:** Verify Mail, Keychain, Safari, Documents work
- **Day 3+:** Restore Photos (if needed) or import from iCloud

---

## Cleanup Checklist

Before declaring success:

- ✅ Mail.app connects to ATT.net IMAP
- ✅ Safari bookmarks present
- ✅ Keychain accessible (test password)
- ✅ iCloud Drive syncing
- ✅ Documents folder populated
- ✅ Photos accessible (cloud or local)
- ✅ Zoom, ChatGPT, MailChimp apps ready
- ✅ Free space >200GB (for video work)

---

## Reference

**Parent plan:** [notes.md](notes.md) -- Overall strategy and timeline

**Shopping status:** [shopping_wendy.md](shopping_wendy.md) -- Hunting for M3 16GB 512GB

**Backup source:** wendy-pro TM backup dated 2026-06-27 on NAS
