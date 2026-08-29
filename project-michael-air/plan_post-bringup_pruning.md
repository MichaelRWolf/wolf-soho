# michael-air: Post-Bringup Disk Pruning Plan

**Status:** 2026-08-29 13:52 -- Disk at 89% capacity (181 GB / 228 GB used), 24 GB free. Pruning in progress.  
**Target:** Bring usable headroom to 50+ GB (22% free) for stable operations without thrashing  
**Progress:** 21.3 GB recovered (5.8 + 8 + 2.6 + APFS reclamation lag)

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

### ✅ Homebrew Cache Cleanup -- 2.6 GB (2026-08-29 13:52)

**Method:** Delegated to Homebrew's native tool (not manual filesystem deletion)  
**Command:** `brew cleanup` (removes only old/uninstalled package caches; keeps installed package caches for re-use)  
**Estimate:** 2.7 GB | **Actual:** 2.6 GB freed  
**Cache status:** 4.0 GB retained (was 6.6 GB) -- safe to rebuild with package updates  
**Disk status:** 181 GB used, 24 GB free (89%)

---

## ⏳ Remaining Cache Cleanup (Deferred -- Rebuild on Next Use)

**Decision:** Skip for now. Temporary value (rebuilds within days of normal use). Revisit only if disk pressure returns.

- Browser caches (Chrome/Safari): 2.1 GB -- rebuilds on restart
- System logs/diagnostics: 1.9 GB -- macOS recreates automatically
- Pip/Python cache: 65 MB -- negligible

**Google updater/ML models (4.1 GB):** Will not do. Risky (internal Chrome management). Low ROI (rebuild automatic). Let Chrome manage its own cache.

---

## ⏳ Deferred: Archival Data (Review Before Acting)

These are historical/archival, not active work. Decide: keep locally, move to NAS, or delete.

- **Messages/Attachments:** 30 GB (PRIORITY 1 -- iCloud-backed, safe to clean)
- **Archive:** 3.4 GB (old projects: SEA Greenways, GEM Training, bankruptcy records, etc.)
- **Scrum_Alliance:** 1.2 GB (2012-2016 CSM training/certification docs)
- **Downloads:** ~1 GB (old installers; review for stale entries)
- **iTunes Library:** 14 GB (old media from michael-pro; review if actively used)

**Low ROI, Skip for Now:**

- VSCode/Cursor config (2.5 GB) -- rebuilds on launch if deleted
- Claude/Codex cache (669 MB) -- negligible for current disk pressure

---

## System Data Analysis (2026-08-29 14:00)

**Question:** Does 96 GB System Data seem normal?

**Investigation:**

- `/System/Library`: 16 GB (frameworks, fonts, language packs)
- `/Library`: 9.6 GB (support, Java, Perl, printers, Developer)
- Caches, logs, hibernation, APFS metadata
- Xcode Command Line Tools installed (in-use)

**Verdict:** Normal. Post-upgrade M3 Mac with CLT typically 80--100 GB. Not bloated. No actionable reclamation without removing CLT or language packs (not recommended).

---

## Status Tracking

- [x] System junk cleanup (/Users/Shared) -- 5.8 GB freed (2026-08-29)
- [x] Activated_LLC archive removal -- 8 GB freed (2026-08-29)
- [x] Homebrew cache cleanup -- 2.6 GB freed (2026-08-29)
- [x] System Data analysis -- confirmed normal, not bloated (2026-08-29)
- [ ] **NEXT: Messages/Attachments cleanup -- 30 GB (deferred, HIGH PRIORITY)**
- [ ] **NEXT: Archive review -- 3.4 GB (decide: keep/move/delete)**
- [ ] Scrum_Alliance review -- 1.2 GB (decide: keep/move/delete)
- [ ] Downloads cleanup -- ~1 GB (easy, low priority)

**Current state:** 182 GB used, 23 GB free (89%). Suboptimal but functional. Messages/Attachments is the main lever for significant improvement (target: 60 GB free / 26% if cleaned).

---

## Next Steps (Pick Up After Campground)

1. **Messages/Attachments** -- 30 GB awaits cleanup (safe to delete, backed by iCloud)
2. **iTunes Library** -- 14 GB (CONFIRMED ORPHANED 2026-08-29: Music.app opened, library empty; safe to delete ~/Music/iTunes)
3. **Archive** -- 3.4 GB, decide if archival or active
4. **Scrum_Alliance** -- 1.2 GB, archival review
5. Downloads cleanup -- minor but easy
