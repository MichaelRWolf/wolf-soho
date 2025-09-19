# Plan to Recover Org Files

## Overview

Files were created with emacs org-mode, then used in Logseq.app (macOS local), then eventually on Logseq iOS ap.

To get the mobile app to work required making the files cloud visible.

I did lots of symlink fuckery to make this happen.

Then I got annoyed with emacs-org mode.  It just fickin stopped working.  Rolled over.  Took it up the back side when SQL stopped playing with dependencies among emacs packages.  I was left disconnected.  Frustrated, I (probably, purportedly) deleted (or disconnected) Logseq apps.  This seems to have cut the cord for cloud files.  I though I had the files local on my macbook, and mirrored via some kind of symlink magic to iCloud.

The files used to be in `~/org*`, then refined as the nepatistic interfuckery increased to `~/org-roam-logseq`.  It was like fucking a beachball while riding a river rapids.  Tough to stay on.  Or get traction.  And not very satisfying in the end.  But it worked.  For a while.  The house of cards stood.  Until org-mode stopped being able to use SQL.  Then, because it all depends on SQL, it all crashed.  I was disconnected from my files.

## Step - Analyze macOS directories

Analyze ~~/org-*` directories and symlinks.

## Step - Analyze iCloud archives

Analyze `~/iPhone/iCloud Archive*`
See where `*.org` files exist.  Specifically, find `*quotes.org`.
When were they last modified?
See if there are ones from 1-3 months ago.  Maybe in TimeMachine.  Mayb in some fucker-based archive.

## Analysis Results - Directories and Symlinks

| Location                               | Type      | Status | Contents                                       | Last Modified | Notes                    |
|----------------------------------------|-----------|--------|------------------------------------------------|---------------|--------------------------|
| `~/org-roam-logseq`                    | Symlink   | Active | Points to `org-roam-logseq-nodes-MichaelRWolf` | Jul 25 2023   | Working symlink          |
| `~/org-roam-logseq-nodes-MichaelRWolf` | Symlink   | Broken | Points to iCloud logseq directory              | Mar 20 2023   | Target not accessible    |
|----------------------------------------|-----------|--------|------------------------------------------------|---------------|--------------------------|
| `~/org-files-without-org-mode`         | Directory | Active | 2 org files: `far_from_a_road.org` + backup    | Apr 17 2025   | Contains recovered files |
| `~/repos/org-roam-logseq`              | Directory | Active | Git repo with migration tools                  | Jul 9 2025    | Migration documentation  |
| `~/.cache/org-persist`                 | Directory | Active | Emacs org-mode cache                           | -             | System cache             |

### Key Findings

- **Broken Symlink Chain**: `~/org-roam-logseq` → `~/org-roam-logseq-nodes-MichaelRWolf` → iCloud (inaccessible)
- **Recovered Files**: Found 2 org files in `~/org-files-without-org-mode/`
- **Migration Tools**: Active git repo with migration documentation and scripts
- **iCloud Access Lost**: Original iCloud logseq directory is no longer accessible

## iCloud Archive Analysis Results

| Archive Location                       | Org Files Found | Key Files          | Last Modified | Notes                       |
|----------------------------------------|-----------------|--------------------|---------------|-----------------------------|
| `~/iCloud Drive (Archive) - 1`         | **1,431 files** | `quotes.org` found | Sep 18, 2024  | **MAJOR DISCOVERY**         |
| `~/Library/CloudStorage/iCloudDrive-*` | 0 files         | None               | -             | Current iCloud drives empty |

### Archive Findings:

**quotes.org Located**: `/Users/michael/iCloud Drive (Archive) - 1/Logseq/org-roam-logseq/pages/20230711112147-quotes.org`
- **File Size**: 198,174 bytes (substantial content)
- **Last Modified**: September 18, 2024 (recent!)
- **167 files** modified between June-September 2024 (1-3 month range)
- **Complete Logseq Structure**: journals/, pages/, assets/, templates/ directories preserved
- **Backup Files**: Multiple timestamped backups in logseq/bak/ directories

## Archive Directory Comparison Results

### Data Duration Analysis

**File Modification Dates (Last Edit Time)**:
- **Earliest**: March 7, 2023 (Tue Mar 7 20:30:27 EST 2023)
- **Latest**: October 24, 2024 (Thu Oct 24 14:08:30 EDT 2024)
- **Duration**: ~19 months, 3 weeks
- **Purpose**: When files were last edited/updated

**Filename-Encoded Dates (File Creation Time + UID)**:
- **Earliest Page**: 20230413 (April 13, 2023) - `20230413-*`
- **Latest Page**: 20241024 (October 24, 2024) - `20241024121632-*`
- **Duration**: ~18 months, 1 week
- **Purpose**: File creation timestamp, used as unique identifier in org-roam

**Journal File Dates**:
- **Earliest Journal**: 2023_03_20.org (March 20, 2023)
- **Latest Journal**: 2023-07-05.org (July 5, 2023)
- **Journal Duration**: ~3.5 months (35 journal files)

**Data Volume**:
- **Total org files**: 1,431
- **Date-encoded pages**: 1,060 files
- **Journal files**: 35 files
- **Other files**: ~336 files

### Date Analysis Summary
- **Two distinct timestamps**: Creation time (filename) vs. last edit time (modification date)
- **Journal activity stopped** after July 2023 (only 3.5 months of journals)
- **Page creation continued** until October 2024 (18+ months of sustained activity)
- **Active editing continued** until October 2024 (19+ months of usage)
- **Actual content span**: ~18-19 months of meaningful data creation and editing
- **Both timestamps are valid** - filename shows creation, modification shows last edit

| Archive Directory                      | Org Files Total | quotes.org Found | org-roam-logseq/pages/ Files | Directory Contents          | Completeness      |
|----------------------------------------|-----------------|------------------|------------------------------|-----------------------------|-------------------|
| `~/iCloud Drive (Archive) - 1`         | **1,431**       | ✅ **YES**       | **1,100**                    | Full Logseq structure       | **MOST COMPLETE** |
| `~/iCloud Drive (Archive)`             | 0               | ❌ No            | 0                            | Basic iCloud files only     | Empty             |
| `~/iCloud Drive (Archive) - 2`         | 0               | ❌ No            | 0                            | Desktop, Documents, Numbers | Empty             |
| `~/Library/CloudStorage/iCloudDrive-*` | 0               | ❌ No            | 0                            | Restricted/empty            | Inaccessible      |

### Archive Analysis Summary:

- **Only Archive - 1 contains org files**: 1,431 total org files
- **quotes.org only found in Archive - 1**: `/Logseq/org-roam-logseq/pages/20230711112147-quotes.org`
- **Archive - 1 has 1,100 files in pages/ directory**: Most complete org-roam-logseq structure
- **Other archives are empty or contain only basic iCloud files**
- **Recommendation**: Focus recovery efforts on `~/iCloud Drive (Archive) - 1` exclusively

## Research and Analysis Results

### Mobile App Integration Issues
**Root Cause**: Logseq mobile app required iCloud sync, which necessitated complex symlink chains to make files cloud-visible.

**Symlink Structure Discovered**:
```
~/org-roam-logseq → org-roam-logseq-nodes-MichaelRWolf → /Users/michael/Library/Mobile Documents/iCloud~com~logseq~logseq/Documents/org-roam-logseq
```

**Why It Failed**: When Logseq apps were deleted, the symlink chain broke, cutting off access to the original iCloud directory.

### SQL Dependency Issues (org-mode Failure)
**Problem**: org-roam depends heavily on SQL for database operations and linking.

**Evidence from Migration Docs**:
- "org-roam is being abandoned due to reliability issues"
- "org-roam reliability: Abandoning org-roam due to persistent issues"
- Migration plan explicitly states: "This plan focuses solely on the org-roam-logseq project and does not consider any other independent projects or submodules"

**Root Cause**: SQL dependency conflicts between emacs packages caused org-mode to "roll over" and stop working.

## Comprehensive Recovery Strategy

### Phase 1: Immediate Recovery (Recommended)
**Source**: `~/iCloud Drive (Archive) - 1` (1,431 org files, including quotes.org)

**Steps**:
1. **Copy archive to local directory** (preserving metadata):
   ```bash
   rsync -av "/Users/michael/iCloud Drive (Archive) - 1/Logseq/org-roam-logseq/" ~/recovered-org-files/
   ```

2. **Verify quotes.org recovery**:
   ```bash
   ls -la ~/recovered-org-files/pages/20230711112147-quotes.org
   # Expected: 198,174 bytes, last modified Sep 18, 2024
   ```

3. **Set up new local workflow** (no iCloud dependencies):
   ```bash
   mkdir ~/org-workspace
   rsync -av ~/recovered-org-files/ ~/org-workspace/
   ```

### Phase 2: Alternative Approaches
**Option A - Direct Archive Usage**: Use archive directory directly (risky if iCloud sync issues)
**Option B - Selective Recovery**: Copy only essential files (quotes.org + recent journals)
**Option C - Hybrid Approach**: Recover to local + manual backup strategy

### Phase 3: Prevention Strategy
**Avoid**: Complex symlink chains, org-roam dependencies, iCloud sync complications
**Implement**: Local git repository, simple backup scripts, direct file management

### Recommendations Summary
1. **Focus on Archive - 1**: Only viable source with complete data
2. **Abandon org-roam**: Use plain org-mode or Logseq without org-roam
3. **Local-first approach**: Avoid iCloud dependencies for core workflow
4. **Simple backup strategy**: Regular git commits + external backup
5. **Mobile access**: Use Logseq app with local directory (no cloud sync required)

## Step - TimeMachine Analysis (Probably Futile)

**Original Hypothesis**: More recent org files may exist in TimeMachine backups, as org-mode was used more recently than October 2024 but stopped due to emacs auto-update package incompatibility.

**Architecture Reality Check**:
- **Original Intent**: Local files (MacBook) as source of truth, iCloud as convenience mirror
- **What Actually Happened**: Some obstinate tool (Logseq mobile) required cloud-native data
- **Architecture Flipped**: iCloud became source of truth, local files became ghost/JIT-mirrored symlinks
- **TimeMachine Exclusion**: Likely excluded `~/Library/Mobile Documents/` (iCloud directories)
- **Result**: TimeMachine never backed up the actual data (only symlinks)

**Why TimeMachine Won't Help**:
- **TimeMachine probably excluded** iCloud directories (assuming cloud was "secure")
- **Local files were just symlinks** - no actual content to backup
- **Real data was in iCloud** - which TimeMachine doesn't backup
- **Archive - 1 is likely the only source** of actual content

**Surgeon General Warning**: TimeMachine is the fuckery wrapped in buggery surrounded by an enigma. The orange asshole may have given up on health and truth and fired the surgeon general, but we can still issue our own warning: **TimeMachine exploration is probably futile**.

**Alternative Recovery Approach**: Since the data in `~/iCloud Drive (Archive) - 1` IS backed up by TimeMachine, you could use a simple `mv` instead of `rsync`:

```bash
# Simple move instead of copy (since it's already backed up)
mv "/Users/michael/iCloud Drive (Archive) - 1/Logseq/org-roam-logseq" ~/recovered-org-files/
```

**TimeMachine Behavior with Renames**: TimeMachine should notice the rename operation and handle it efficiently:
- **First backup after rename**: TimeMachine will detect the move/rename and update its index
- **Subsequent backups**: Should not need to copy the 1,431 files again (they're already in the backup)
- **Space efficiency**: Rename operations are much more efficient than copy operations in TimeMachine
- **Caveat**: This assumes TimeMachine is still actively backing up the archive directory

**Recommendation**: Use `mv` instead of `rsync` for faster recovery, since the data is already safely backed up in TimeMachine.

**Conclusion**: Archive - 1 (`~/iCloud Drive (Archive) - 1`) is almost certainly the complete and only source of your org files. TimeMachine analysis is not recommended unless you're feeling particularly masochistic.

## Step - Research mobile app fuckery and collusion with cloud files
