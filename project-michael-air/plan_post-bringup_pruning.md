# michael-air: Post-Bringup Disk Pruning Plan

**Status:** 2026-08-29 13:38 -- Disk at 90% capacity (182 GB / 228 GB used), 22 GB free. Pruning in progress.  
**Target:** Bring usable headroom to 50+ GB (22% free) for stable operations without thrashing  
**Progress:** 15.8 GB recovered so far (5.8 + 8 + APFS reclamation)

---

## Overview: Migration Bloat Sources

michael-air was restored from michael-pro (water damaged, macOS 15.x) and upgraded to macOS 26. This created three categories of junk:

1. **Migrated historical data** (iTunes library, old archives) -- relocate to NAS/external
2. **Upgrade/first-boot caches** (Homebrew, browser caches, system temp) -- safe to nuke
3. **Application cruft** (Chrome optimization models, Google Updater cache) -- rebuild automatically

---

## ✅ COMPLETED (2026-08-29)

### ✅ System Junk from /Users/Shared -- 5.8 GB

**Deleted:** Previously Relocated Items (Malwarebytes quarantine), old Address Book 2012, Daylite backups  
**Result:** 5.8 GB freed

### ✅ Activated_LLC Archive -- 7.8 GB

**Deleted:** Old job files (2018 employment/termination docs)  
**Result:** 8 GB freed (with APFS reclamation)  
**Disk status:** 182 GB used, 22 GB free (90%)

---

## Remaining Actions (No Risk -- Caches Only)

### ✅ 1. Homebrew Cache -- 6.6 GB (SAFE)

**What:** Package download cache, automatically rebuilds.

```bash
rm -rf ~/Library/Caches/Homebrew
```

**Recovers:** 6.6 GB  
**Rebuild:** Automatic on next `brew install`

### ✅ 2. Browser Caches -- 2.1 GB (SAFE)

**What:** Chrome/Safari cached pages, ads, images.

```bash
rm -rf ~/Library/Caches/Google/Chrome
# Safari rebuilds automatically
```

**Recovers:** 2.1 GB  
**Rebuild:** Automatic on browser restart

### ✅ 3. Google Updater & Optimization Models -- 4.1 GB (SAFE)

**What:** Google Chrome updater cache + on-device ML models for Chrome suggestions.

```bash
rm -rf ~/Library/Application\ Support/Google/GoogleUpdater
rm -rf ~/Library/Application\ Support/Google/Chrome/OptGuideOnDeviceModel
rm -rf ~/Library/Application\ Support/Google/Chrome/component_crx_cache
rm -rf ~/Library/Application\ Support/Google/Chrome/extensions_crx_cache
rm -rf ~/Library/Application\ Support/Google/Chrome/GraphiteDawnCache
```

**Recovers:** 4.1 GB  
**Rebuild:** Automatic on Chrome restart

### ✅ 4. Empty Trash -- 2.9 GB (MANUAL)

```bash
rm -rf ~/.Trash/*
```

**Recovers:** 2.9 GB  
**Status:** Already removed old Messages attachments; verify trash is empty

### ✅ 5. System Logs & Diagnostics -- 2.0 GB (MOSTLY SAFE)

**What:** Application and system crash logs from first-boot chaos.

```bash
rm -rf ~/Library/Logs/*
mkdir -p ~/Library/Logs  # Rebuild directory
```

**Recovers:** 1.9 GB  
**Note:** Safe -- macOS recreates as needed. Keep if you're debugging a specific issue.

### ✅ 6. Pip/Python Cache -- 65 MB (SAFE)

```bash
rm -rf ~/Library/Caches/pip
```

**Recovers:** 65 MB

---

## Second Pass (Strategic Moves -- Relocate to NAS/External)

### ⏳ 7. iTunes Library -- 14 GB (MEDIUM RISK)

**Location:** `~/Music/iTunes`  
**What:** Old iTunes media library from michael-pro.
**Decision:**

- [ ] Keep locally: Do you actively use iTunes/Music.app?
- [ ] Move to NAS: `rsync -av ~/Music/iTunes /mnt/nas/Archive/`
- [ ] Delete: If not needed

**To move safely:**

```bash
# After confirming you have NAS backup:
mv ~/Music/iTunes /Volumes/YOUR_NAS/Archive/iTunes-michael-pro-backup
ln -s /Volumes/YOUR_NAS/Archive/iTunes-michael-pro-backup ~/Music/iTunes  # Symlink
```

**Recovers:** 14 GB (if deleted)

### ⏳ 8. Archive Directory -- 3.4 GB (LOW PRIORITY)

**Location:** `~/Archive`  
**What:** Old project files from michael-pro (SEA Greenways, GEM Training, bankruptcy records, etc.).
**Status:** Likely migrated from michael-pro; need it?
**Decision:**

- [ ] Keep locally: Often-accessed projects?
- [ ] Move to NAS: `rsync -av ~/Archive /mnt/nas/`
- [ ] Delete: If archived elsewhere

**Recovers:** 3.4 GB

### ⏳ 9. Downloads Folder -- 1.6 GB (LOW EFFORT)

**Location:** `~/Downloads`  
**What:** Old installer downloads (1Password 83 MB, iCloud Photos tools, etc.).
**Decision:**

- [ ] Review & delete old installers
- [ ] Keep only active/recent downloads

**To safely review:**

```bash
ls -lhtr ~/Downloads | tail -20  # Newest first
find ~/Downloads -type f -mtime +30 -exec ls -lh {} \;  # Older than 30 days
```

**Recovers:** ~500 MB - 1 GB

---

## Third Pass (Application Cruft -- Medium Risk)

### ⏳ 10. VSCode/Cursor Extensions & Config -- 2.5 GB (SAFE IF UNUSED)

**Locations:**

- `~/.vscode` (1.5 GB)
- `~/.cursor` (1.4 GB)

**What:** Extension cache + project metadata.
**Decision:**

- [ ] Keep: If you use VSCode/Cursor daily
- [ ] Clean extensions: `code --list-extensions` → remove unused
- [ ] Delete config: Rebuilds on first launch

```bash
# Option 1: Delete entire config (rebuild on launch)
rm -rf ~/.vscode ~/.cursor

# Option 2: Keep, but purge extensions
# Open VSCode/Cursor, Extensions panel → Remove unused ones
```

**Recovers:** 2.5 GB (if deleted entirely)

### ⏳ 11. Chrome Profile Cruft -- 624 MB (SAFE)

**Location:** `~/Library/Application Support/Google/Chrome/Default`  
**What:** Browser history, cookies, site data.
**Note:** Safe to nuke if you're OK losing saved passwords/history.

```bash
rm -rf ~/Library/Application\ Support/Google/Chrome/Default/Cache
rm -rf ~/Library/Application\ Support/Google/Chrome/Default/Code\ Cache
```

**Recovers:** ~200-300 MB

### ⏳ 12. Claude/Codex Application Support -- 669 MB (SAFE TO CLEAN)

**Locations:**

- `~/Library/Application Support/Claude` (416 MB) -- cache/models
- `~/Library/Application Support/Codex` (253 MB) -- unused?

**Decision:**

- [ ] Claude: Keep (you're using it now), but can nuke cache
- [ ] Codex: Delete if unused (OpenAI competitor)

```bash
# Clean Claude cache (keep app, nuke cache)
rm -rf ~/Library/Application\ Support/Claude/Cache
rm -rf ~/Library/Application\ Support/Claude/*.log

# Delete Codex if not using
rm -rf ~/Library/Application\ Support/Codex
```

**Recovers:** 300-500 MB

---

## Not-Yet-Examined Possibilities

### System Data (110.73 GB Total) -- Deep Dive Needed

**Known safe zones:**

```bash
# Xcode derived data (if you have Xcode installed)
du -xhd 0 ~/Library/Developer/Xcode/DerivedData

# Old Time Machine metadata
du -xhd 0 ~/Library/Metadata

# Spotlight index (safe to disable/rebuild)
du -xhd 0 ~/.Spotlight-V100
```

### Language/Locale Duplicates

**Symptom:** Large `/System` footprint after OS upgrade.
**Check:**

```bash
ls -la /System/Library/fonts  # Might have duplicate language packs
du -xhd 1 /System/Library 2>/dev/null | sort -rh | head -5
```

**Note:** Don't delete system fonts/locales unless absolutely certain.

### iCloud Drive Folder -- 904 MB (Archive?)

**Location:** `~/iCloud Drive (Archive) - 1`  
**What:** Old iCloud Drive backup created during migration setup?
**Decision:**

- [ ] Review contents
- [ ] Delete if redundant

```bash
du -xhd 1 ~/iCloud\ Drive\ \(Archive\)\ -\ 1 2>/dev/null
ls -la ~/iCloud\ Drive\ \(Archive\)\ -\ 1
```

---

## Execution Plan

### Phase 1: Quick Wins (30 min, recovers ~17 GB)

1. Empty Trash (2.9 GB)
2. Remove Homebrew cache (6.6 GB)
3. Remove Chrome caches (2.1 GB)
4. Remove Google Updater (4.1 GB)
5. Remove system logs (1.9 GB)

**Expected free space after:** ~45 GB (18% available)

### Phase 2: Strategic Moves (60 min, recovers ~20+ GB)

1. Review & move iTunes to NAS (14 GB)
2. Review & move Archive to NAS (3.4 GB)
3. Clean Downloads (500 MB - 1 GB)

**Expected free space after:** ~65+ GB (27% available)

### Phase 3: Optional Deep Clean (30 min, recovers 2-3 GB)

1. Delete VSCode/Cursor if unused
2. Clean Chrome profile
3. Remove Codex if unused

**Expected free space after:** ~70+ GB (28% available)

---

## Verification Commands

**Before each phase:**

```bash
df -h / | awk 'NR==2 {printf "Free: %.1f GB / %.1f GB total\n", $4/1024/1024, $2/1024/1024}'
du -xhd 1 ~ 2>/dev/null | sort -rh | head -15
```

**After deletion:**

```bash
df -h /
```

---

## Gotchas & Warnings

1. **Don't delete ~/Library/Preferences** -- contains system settings
2. **Don't delete ~/Library/Application Support/*** unless sure the app isn't installed
3. **iCloud Drive symlink:** If you moved Documents to iCloud and deleted, re-enable carefully to avoid dupes
4. **Rebuild time:** After nuking caches, first app launch can be slow (rebuilding caches)
5. **iTunes symlink:** If you symlink iTunes to NAS, ensure NAS is always available (else Music.app hangs)

---

## Status Tracking

- [x] System junk cleanup (/Users/Shared) -- 5.8 GB freed (2026-08-29)
- [x] Activated_LLC archive removal -- 8 GB freed (2026-08-29)
- [ ] Phase 1 caches (Homebrew, Chrome, logs) -- ~17.6 GB available
- [ ] Scrum_Alliance review -- move or delete? (1.2 GB)
- [ ] Archive review -- move or delete? (3.4 GB)
- [ ] Downloads cleanup -- delete old installers (1 GB)
- [ ] Free space verified (current: 22 GB / 10%; target: 50+ GB / 22%)
- [ ] Normal operations verified (no disk thrashing at 90%+)

---

## Next Steps

1. Run Phase 1 immediately (safe, high ROI)
2. Verify free space reaches 45 GB
3. Resume Photos.app sync test
4. Plan Phase 2 after confirming iTunes/Archive needs
