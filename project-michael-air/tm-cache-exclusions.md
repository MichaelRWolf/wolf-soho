# Time Machine: Comprehensive Cache & Churn Exclusions

**Purpose:** Prevent high-churn ephemeral files from being preserved forever in snapshots.

**Problem:** A single cache directory that stays ~5 GB will accumulate across 52 annual snapshots = 260 GB of useless data. Exclude before first snapshot to prevent forever-bloat.

**Status:** Proposed; to be applied before re-running backup if snapshot is found to contain cache churn.

---

## High-Churn Categories to Exclude

### Package Manager Caches (Regenerable on Install)

| Path                      | Size       | Churn      | Rationale                                    |
|---------------------------|------------|------------|----------------------------------------------|
| `/opt/homebrew`           | 5-15 GB    | High       | Downloads, build artifacts, version caches   |
| `~/.cache/pip`            | 0.5-2 GB   | Medium     | Python package downloads (auto-redownloaded) |
| `~/.cache/npm`            | 0.5-2 GB   | Medium     | Node package downloads (auto-redownloaded)   |
| `~/.cache/uv`             | 0.5-1 GB   | Medium     | UV package cache (auto-regenerated)          |
| `~/.cargo/registry/cache` | 1-5 GB     | Medium     | Rust crate downloads (auto-redownloaded)     |
| `~/.gem/cache`            | 0.1-0.5 GB | Low-Medium | Ruby gem downloads (auto-redownloaded)       |
| `~/go/pkg/mod/cache`      | 0.5-2 GB   | Medium     | Go module cache (auto-regenerated)           |

### IDE & Build Tool Caches

| Path                                    | Size     | Churn         | Rationale                                  |
|-----------------------------------------|----------|---------------|--------------------------------------------|
| `~/Library/Developer/Xcode/DerivedData` | 10-50 GB | **Very High** | Build artifacts, indexes (100K+ files)     |
| `~/Library/Developer/Xcode/Archives`    | 5-20 GB  | High          | Old app archives (keep manually if needed) |
| `~/Library/Caches/Xcode`                | 1-5 GB   | High          | Build cache, indexes                       |
| `~/.vscode/extensions`                  | 2-10 GB  | Medium        | Extensions auto-redownload on launch       |
| `~/.vscode-insiders/extensions`         | 2-10 GB  | Medium        | Insiders extensions                        |
| `~/.cache/JetBrains`                    | 1-5 GB   | High          | IntelliJ/CLion caches, indexes             |
| `~/.cache/gradle`                       | 1-5 GB   | Medium        | Gradle build cache                         |
| `~/.cache/maven`                        | 0.5-2 GB | Medium        | Maven dependency cache                     |

### System & App Caches

| Path                        | Size       | Churn         | Rationale                                     |
|-----------------------------|------------|---------------|-----------------------------------------------|
| `~/Library/Caches`          | 5-20 GB    | **Very High** | System-level app caches (100K+ files)         |
| `~/Library/Caches/CloudKit` | 1-5 GB     | High          | iCloud sync artifacts (auto-rebuilt)          |
| `~/Library/Caches/pip`      | 0.1-0.5 GB | Low           | System pip cache                              |
| `~/.cache`                  | 2-10 GB    | High          | User-level cache (various apps)               |
| `~/.cache/chromium`         | 1-5 GB     | Medium        | Chromium browser cache (if using Arc, Chrome) |
| `~/.cache/fontconfig`       | 0.1-1 GB   | Low           | Font cache (auto-rebuilt)                     |

### Language-Specific Version Managers

| Path                       | Size    | Churn  | Rationale                                       |
|----------------------------|---------|--------|-------------------------------------------------|
| `~/.local/share/uv/python` | 2-5 GB  | High   | UV-installed Python versions (auto-regenerated) |
| `~/.pyenv/versions`        | 5-20 GB | Medium | pyenv Python versions (auto-redownloaded)       |
| `~/.nvm`                   | 2-10 GB | Medium | Node version manager (auto-redownloaded)        |
| `~/.rbenv/versions`        | 2-10 GB | Medium | Ruby version manager (auto-redownloaded)        |

### Browser Caches

| Path                                                        | Size     | Churn  | Rationale                           |
|-------------------------------------------------------------|----------|--------|-------------------------------------|
| `~/Library/Safari/History.db`                               | Variable | Medium | History database changes constantly |
| `~/Library/Application Support/Google/Chrome/Default/Cache` | 1-5 GB   | High   | Chrome cache (auto-rebuilt)         |
| `~/Library/Application Support/Firefox/Profiles/*/cache2`   | 1-5 GB   | High   | Firefox cache (auto-rebuilt)        |
| `~/Library/Application Support/Arc/User Data/Default/Cache` | 1-5 GB   | High   | Arc cache (auto-rebuilt)            |

### Development Tool Artifacts

| Path                                  | Size     | Churn      | Rationale                                      |
|---------------------------------------|----------|------------|------------------------------------------------|
| `~/.cache/pre-commit`                 | 0.1-1 GB | Low-Medium | pre-commit hook downloads (auto-redownloaded)  |
| `~/.cache/huggingface`                | 5-50 GB  | Medium     | Hugging Face model cache (user-managed)        |
| `~/.cache/torch`                      | 5-50 GB  | Medium     | PyTorch model cache (user-managed)             |
| `~/Library/Application Support/Emacs` | Variable | Low        | Emacs backups, auto-saves (consider excluding) |

---

## Proposed Exclusion Commands

Apply these **before re-running Time Machine** (if cache churn is detected in first backup):

```bash
# Package managers
tmutil addexclusion -p /opt/homebrew
tmutil addexclusion -p ~/.cache/pip
tmutil addexclusion -p ~/.cache/npm
tmutil addexclusion -p ~/.cache/uv
tmutil addexclusion -p ~/.cargo/registry/cache
tmutil addexclusion -p ~/.gem/cache
tmutil addexclusion -p ~/go/pkg/mod/cache

# IDEs & build tools
tmutil addexclusion -p ~/Library/Developer/Xcode/DerivedData
tmutil addexclusion -p ~/Library/Caches/Xcode
tmutil addexclusion -p ~/.vscode/extensions
tmutil addexclusion -p ~/.cache/JetBrains
tmutil addexclusion -p ~/.cache/gradle
tmutil addexclusion -p ~/.cache/maven

# System & app caches
tmutil addexclusion -p ~/Library/Caches
tmutil addexclusion -p ~/.cache

# Language version managers
tmutil addexclusion -p ~/.local/share/uv/python
tmutil addexclusion -p ~/.pyenv/versions
tmutil addexclusion -p ~/.nvm
tmutil addexclusion -p ~/.rbenv/versions

# Browser caches
tmutil addexclusion -p ~/Library/Application\ Support/Google/Chrome/Default/Cache
tmutil addexclusion -p ~/Library/Application\ Support/Firefox/Profiles/*/cache2
tmutil addexclusion -p ~/Library/Application\ Support/Arc/User\ Data/Default/Cache

# Development tools
tmutil addexclusion -p ~/.cache/pre-commit
```

---

## What NOT to Exclude

Keep in backups (valuable or low-churn):

| Path                                | Reason                                                 |
|-------------------------------------|--------------------------------------------------------|
| `~/Library/Preferences`             | User settings (irreplaceable)                          |
| `~/Library/Application Support`     | App data, databases (keep, despite some cache subdirs) |
| `~/Library/Saved Application State` | Window state, undo history (useful)                    |
| `~/Library/Containers`              | Sandboxed app data (keep)                              |
| `~/Documents`, `~/Desktop`          | User files (always keep)                               |
| `~/Library/Mail Downloads`          | Email attachments (keep if important)                  |
| `~/.ssh`, `~/.gnupg`                | Credentials (keep, low churn)                          |

---

## Size Impact (Estimated)

**If cache churn is present in current backup:**

- Current snapshot: 168.54 GB
- Estimated cache/churn: 15-40 GB
- Clean snapshot should be: 130-150 GB

**Annual impact (52 snapshots):**

- Cache bloat per year: 780-2,080 GB (if not excluded)
- Recovered by excluding: Saves ~1.5 TB/year

---

## Implementation Plan

1. **Wait for current backup to complete** (08:57 snapshot)
2. **Inspect snapshot** -- check if high-churn paths are present
3. **If contaminated:**
   - Delete the snapshot: `rm -rf /Volumes/com.apple.TimeMachine.localsnapshots/Backups.backupdb/michael-air/<snapshot-date>`
   - Apply all CLI exclusions from above
   - Restart backup: `tmutil startbackup`
4. **If clean:** -- monitor next few hourly backups for churn; add exclusions proactively

---

## Verification (After Exclusions Applied)

```bash
# Check which paths are excluded
for path in /opt/homebrew ~/.cache ~/Library/Caches ~/Library/Developer/Xcode/DerivedData ~/.vscode/extensions; do
  echo -n "$path: "
  tmutil isexcluded "$path"
done

# Verify next snapshot is smaller & has fewer files
LATEST=$(tmutil latestbackup)
echo "Snapshot size: $(du -sh "$LATEST" | cut -f1)"
echo "File count: $(find "$LATEST" -type f | wc -l)"
```

---

## Notes

- **Persistent exclusions** -- Use `tmutil addexclusion -p` (persistent; survives TM reconfiguration)
- **Test one path** -- If unsure about a path, exclude it and verify in next backup that you don't miss anything
- **User-managed large caches** -- `~/.cache/huggingface`, `~/.cache/torch` (ML models) should be excluded unless you want them backed up
- **Archive important build artifacts** -- If you care about old Xcode builds, manually archive before excluding `DerivedData`
