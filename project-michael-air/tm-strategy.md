# Time Machine Efficiency Strategy: michael-air

**Purpose:** Measure what was restored from Time Machine backup and decide what to exclude from future backups based on recovery value, regeneration cost, and file-count impact.

**Related:** [setup.md](setup.md) (migration process & issues) | [GitHub issue #8](https://github.com/MichaelRWolf/wolf-soho/issues/8) (Intel x86_64 audit)

**Key insight:** Both **GB and file count** matter. A 2 GB cache with 250K files may be far more expensive to restore than a 50 GB archive with 20 large files.

**Status:** Framework ready; measurements in progress (2026-08-15+)

## What Was Restored (2026-08-13/14)

| Category | GB | Source | Notes |
|----------|----|----|-------|
| Applications | 17.6 | Migration Assistant | Standard apps (universal/ARM available for most) |
| Michael R. Wolf (home) | 75.95 | Migration Assistant | Main account; includes ~/Library + everything else |
| Annie Nomous | 20.6 | Migration Assistant | Legacy account; unclear purpose |
| mmac-shared | 10.4 | Migration Assistant | Unknown origin account; retained to investigate |
| Other Files & Folders | 23.42 | Migration Assistant | **Unaccounted; needs audit** |
| System & Network | 1.6 | Migration Assistant | Only settings + network (printers excluded) |
| **Total** | **~149** | — | ~117 GB selected; ~106 GB available after transfer |

### The 23.42 GB "Other Files & Folders" Problem

Possible sources (needs investigation):
- `/Users/Shared` — shared user data
- `/Library` (system library, not ~/Library) — system-level apps, fonts, extensions
- `/private` — temporary directories, system logs
- Package-manager caches (`/opt`, `/usr/local` paths outside Homebrew)
- Old application debris

**Commands to audit:**
```sh
sudo du -xhd 1 / 2>/dev/null | sort -h
sudo du -xhd 1 /Library /Users/Shared /private 2>/dev/null | sort -h
```

## Audit Framework

### Tier 1: High-Recovery-Value (Keep in TM)

**Definition:** Cannot be quickly regenerated; loss would mean data loss or significant work.

**Categories:**
- Personal documents, projects, writing
- Photos, videos, personal media
- Email messages (if IMAP offline storage)
- Application databases (Mail, Calendar, Notes, etc.)
- Preferences for complex applications
- SSH keys, API credentials (if backed up)
- Browser bookmarks, history, saved passwords

**Measurement:**
```sh
du -sh ~/Documents ~/Desktop ~/Pictures ~/Downloads ~/Movies
du -sh ~/Library/Preferences ~/Library/Saved\ Application\ State
find ~ -name "*.gpg" -o -name "*.pem" -o -name ".ssh" 2>/dev/null | xargs du -sh
```

**File count example:**
- Personal documents: Usually 1K–10K files total (manageable)

---

### Tier 2: Medium-Recovery-Value (Measure & Decide Per-Category)

**Definition:** Can be recovered from external source or rebuilt with moderate effort.

**Categories:**
- `~/Library/Preferences` — Mix of valuable settings + regenerable UI state
- `~/Library/Application Support/` — Mix; some apps store cache here
- `~/Library/Application Scripts/` — Workflow/automation state (maybe valuable)
- `~/Library/Cookies` — Typically regenerable (login again)
- `~/Library/HTTPStorages/` — Browser session data
- `~/Library/Safari/` — Bookmarks (valuable), history (regenerable)
- Browser profiles (Chrome/Firefox/Arc) — Mix of valuable + regenerable

**Decision factors:**
- Can you restore bookmarks/settings from sync services? (iCloud, 1Password, LastPass, etc.)
- How long does it take to reconfigure?
- How many files are involved?

**Measurement:**
```sh
du -sh ~/Library/Application\ Support/* | sort -h
du -sh ~/Library/Preferences/* | sort -h
find ~/Library/Application\ Support -type f | wc -l
find ~/Library/Preferences -type f | wc -l
```

---

### Tier 3: Low-Recovery-Value, Regenerable (Exclude from TM)

**Definition:** Can be completely rebuilt with low cost; serves no irreplaceable data.

**Categories:**
- `~/Library/Caches` — Application caches (can be rebuilt)
- `~/Library/Logs` — Old log files (regenerated on use)
- `~/Library/HTTPStorages` — Browser session cache
- `~/Library/WebKit` — Browser webkit cache
- IDE indexes/caches:
  - `~/Library/Developer/Xcode/` — Build cache, derived data, indexes
  - `~/.vscode/extensions` — Downloaded extensions (reinstall)
  - `~/.cache/pip` — Python package download cache
  - `~/.cache/npm` — Node package download cache
  - `~/.cache/uv` — UV package cache
- Language-specific package caches:
  - `~/.gem` — Ruby gems (often downloaded again)
  - `~/.cargo/registry/cache` — Rust crates cache
  - `~/go/pkg/mod/cache` — Go module cache
- Homebrew/MacPorts:
  - `~/Library/Caches/Homebrew` — Downloaded bottles (redownloaded on reinstall)
  - `/Library/Caches/Homebrew` — System cache
  - Old Intel Homebrew tree (`/usr/local/Homebrew`) — **Definitely exclude after migration**

**Measurement (critical: file count):**
```sh
du -sh ~/Library/Caches
find ~/Library/Caches -type f | wc -l

sudo du -sh /Library/Caches
sudo find /Library/Caches -type f | wc -l

du -sh ~/Library/Developer/Xcode/DerivedData
find ~/Library/Developer/Xcode/DerivedData -type f | wc -l

du -sh ~/.cache
find ~/.cache -type f | wc -l

# Developer tool caches
du -sh ~/Library/Developer/Xcode
du -sh ~/.vscode/extensions
du -sh ~/.cache/pip ~/.cache/npm ~/.cache/uv 2>/dev/null
```

---

### Tier 4: Unknown/Uncertain (Inspect Before Excluding)

**Categories that need inspection:**
- `/Library` (system library) — Mix of system essentials, app support, fonts, extensions
- `/Users/Shared` — Shared data directory
- `/private/var/log` — System logs
- Old service accounts (mmac-shared, Annie Nomous) — Unknown purpose

**Measurement:**
```sh
sudo du -sh /Library/* | sort -h
sudo du -sh /Users/Shared
sudo du -sh /private/var/log
dscl . -read /Users/mmac-shared
dscl . -read /Users/Annie\ Nomous
```

---

## Measurement Checklist

Run these commands and capture output (with timestamps) for future reference:

```sh
# Overview
du -sh ~ /Volumes/Macintosh\ HD 2>/dev/null

# Home directory breakdown
du -sh ~/* | sort -h

# Library breakdown (user)
du -sh ~/Library/* | sort -h

# Library subdirectories (user)
du -sh ~/Library/Caches ~/Library/Logs ~/Library/Developer ~/Library/Application\ Support

# Cache file counts
echo "=== Caches (user) ===" 
find ~/Library/Caches -type f | wc -l
echo "=== Caches (system) ==="
sudo find /Library/Caches -type f | wc -l

# Developer tool state
echo "=== Xcode ==="
du -sh ~/Library/Developer/Xcode
find ~/Library/Developer/Xcode/DerivedData -type f | wc -l

echo "=== Other dev tools ==="
du -sh ~/.cache ~/.vscode/extensions 2>/dev/null

# System audit
echo "=== System Library ==="
sudo du -sh /Library/* | sort -h

echo "=== Users/Shared ==="
sudo du -sh /Users/Shared

echo "=== Unknown accounts ==="
dscl . -list /Users | grep -v "^_"
```

---

## Decision Template

For each category, fill in:

| Category | GB | File Count | Recovery Value | Regeneration Cost | Regeneration Time | Proposed Action | Rationale |
|----------|----|----|---|---|---|---|---|
| Example: ~/Library/Caches | 8.5 | 125,000 | Low (ephemeral) | Low (auto-rebuild) | ~5 min | Exclude | File count (125K) makes restore slow; cache rebuilt on app launch |

---

## Final Exclusion Decision (2026-08-17)

**Summary:** Simplified to exclude only 3 high-impact, unambiguous categories.

| Path | Size | File Count | Rationale | Status |
|------|------|-----------|-----------|--------|
| `~/Downloads` | Ephemeral | — | Ephemeral workflow directory; contents cleared regularly. No recovery value. | ✓ Excluded |
| `~/Pictures` | ~15–20 GB | ~50K+ | Stored on NAS; backed up separately. Redundant in Time Machine. | ✓ Excluded |
| `~/repos` | ~30–50 GB | ~250K+ | GitHub-based project repos; no local data loss risk. Can be re-cloned. Huge file count (git metadata) makes restore slow. | ✓ Excluded |

**Reasoning:**

This approach avoids over-engineering the exclusion list by focusing only on paths that are:
1. **Already backed up elsewhere** (`~/Pictures` on NAS)
2. **Regenerable without effort** (`~/repos` via `git clone`)
3. **Genuinely ephemeral** (`~/Downloads`)

Everything else in `~/Library`, `~/Documents`, `~/Desktop`, etc. remains in Time Machine. The cost of restoring these is low (fewer files, higher value), and they contain irreplaceable settings, preferences, and personal data.

**Configuration:**
System Preferences → Time Machine → Options → Add `~/Downloads`, `~/Pictures`, `~/repos`

---

## Managing Time Machine Exclusions via xattr

When Time Machine GUI doesn't support adding certain paths (e.g., dotfiles), use `xattr` to set the backup exclude attribute directly.

### Set Backup Exclude Attribute

```bash
# Mark a directory to be excluded from Time Machine backups
xattr -w com.apple.metadata:com_apple_backup_excludeItem "bplist00_com.apple.backupd" <path>

# Example: exclude ~/.cache
xattr -w com.apple.metadata:com_apple_backup_excludeItem "bplist00_com.apple.backupd" ~/.cache
```

### Remove Backup Exclude Attribute

```bash
# Remove the exclusion attribute (includes in backup)
xattr -d com.apple.metadata:com_apple_backup_excludeItem <path>

# Example: stop excluding ~/.cache
xattr -d com.apple.metadata:com_apple_backup_excludeItem ~/.cache
```

### Verify Attribute Status

```bash
# Check if a path has the attribute
xattr -p com.apple.metadata:com_apple_backup_excludeItem <path>
# Returns: bplist00_com.apple.backupd (if set)
# Returns: error if not set

# List all attributes on a path
xattr -l <path>
```

### Script to Check All Excluded Paths

Use `tmutil_analysis` script in project root to see both:
1. Paths excluded via `tmutil` (CLI or GUI)
2. Paths with `com.apple.metadata:com_apple_backup_excludeItem` attribute (Apple's native marker)

---

## Previous Machine (michael-pro) Strategy

**Goal:** Learn from previous backup decisions to avoid repeating inefficient patterns.

**Questions to answer:**
- Were there exclusions configured on michael-pro? (Check NAS backup metadata)
- Did those exclusions help? (Small restore time, or still slow?)
- What accumulated in Caches/Logs over time? (Measure size + file count)
- Were there any "aha" categories that should have been excluded earlier?

**Lookup if available:**
- `~/Library/Preferences/com.apple.TimeMachine.plist` — May list exclusions
- Time Machine > Options or System Settings → Time Machine > Options — Excluded paths

---

## Post-Audit Deliverables

1. **Measured TM Audit Table** — Fill in all blanks from commands above
2. **Exclusion List** — Specific paths to add to Time Machine exclusions
3. **Rationale Document** — Why each exclusion makes sense for michael-air
4. **Regeneration Playbook** — Steps to rebuild each excluded category if needed
5. **Monitoring** — After first backup, verify that excluded paths do not re-accumulate unexpectedly

