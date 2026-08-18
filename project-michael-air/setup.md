# michael-air Setup: Migration Issues & Resolutions

**Timeline:** 2026-08-13 (restore) → 2026-08-16 (remediation complete)  
**Source:** Intel MacBook Pro (michael-pro), water damaged  
**Method:** Time Machine restore via Setup Assistant from NAS backup

**For future machines:** See [TEMPLATE-macbook-air-setup.md](TEMPLATE-macbook-air-setup.md) and [x86_64-remediation.md](x86_64-remediation.md).

---

## Migration Issues & Fixes

### Issue 1: Terminal Shell Failure ✓ FIXED (2026-08-15)

**Symptom:** Terminal.app failed to launch.

**Root cause:** Login shell configured as `/usr/local/bin/bash` (Intel executable).

**Resolution:**

```bash
# Immediate fix
chsh -s /bin/zsh  # system zsh is ARM64

# Permanent fix (after Homebrew installed)
brew install bash
chsh -s /opt/homebrew/bin/bash
```

### Issue 2: Intel Homebrew Unusable ✓ FIXED (2026-08-16)

**Symptom:** `brew` command fails with `Bad CPU type in executable`.

**Root cause:** Migrated Homebrew at `/usr/local/Homebrew` is x86_64-only.

**Resolution:** Removed entire Intel tree; installed fresh ARM64 Homebrew.

**Details:** See [x86_64-remediation.md](x86_64-remediation.md) (1.6 GB reclaimed via /opt/local + /opt/X11 removal).

### Issue 3: ~/Downloads TCC Privacy ⏳ DEFERRED

**Symptom:** `ls` in ~/Downloads failed with `Operation not permitted`.

**Status:** Lazy resolution -- grant permissions as needed. No proactive grants required.

### Issue 4: Unaccounted 23 GB "Other Files & Folders" ⏳ DEFERRED

**Impact:** Low (1% of storage).

**Investigation commands available in [tm-strategy.md](tm-strategy.md).**

### Issue 5: Legacy Accounts (mmac-shared, Annie Nomous) ✓ SKIP (2026-08-16)

**Size:** 31 MB combined.

**Decision:** Keep as-is (too small to matter; investigation overhead > benefit).

---

## Completed Tasks Summary

### High Priority (Blocking Development)

- ✓ Shell & Homebrew working (2026-08-15/16)
- ✓ Intel artifacts removed (/opt/local, /opt/X11, ~/.local/share/uv) (2026-08-16)
- ✓ Rust & UV rebuilt (ARM64 native) (2026-08-15/16)
- ✓ PATH cleaned (no stale /usr/local or /opt/local entries) (2026-08-16)
- ✓ Xcode Command Line Tools verified (worked after restore)

### Medium Priority (Functionality)

- ✓ TCC permission matrix created (reference available)
- ✓ Homebrew packages verified via Brewfile
- ✓ Daylite operational (2026-08-15; login/sync complete 2026-08-18)
- ✓ Launcher recovery (Quicksilver on Cmd-Space) (2026-08-18)
- ✓ SSH Beryl passwordless access (2026-08-18; working)
- ✓ Device naming & identity strategy (2026-08-18)
  - SSH key comments: michael@michael-air
  - CONTEXT.md: device registry updated (michael-air primary; michael-pro/wendy-pro/wolf-air preserved)
  - Identity Strategy: merged GitHub + 1P, sync script added
  - portable-profile: Ethernet adapter interfaces updated
- ✓ Mail.app setup (ATT email: working; Safari/Chrome deferred) (2026-08-18)
- ⏳ SSH NAS (Synology kex_exchange error; deferred)

### Low Priority (Optimization)

- ✓ macOS update deferred (15.7 Sequoia stable; Tahoe upgrade deferred to stable WiFi)
- ✓ x86_64 audit completed (2026-08-15) -- findings documented
- ✓ Time Machine exclusions finalized (2026-08-17)

---

## Validation & Monitoring (Ongoing)

---

## Ongoing Monitoring & Validation

### Time Machine Backups

- Monitor hourly backups for errors: `log stream --predicate 'process == "backupd"'`
- Verify snapshots contain only user data (no system files)
- Decision on legacy `Backups-TM-Michael` share (keep or archive) -- deferred to 2-4 weeks of stable backups
- ✓ Backup completed at 13:11 (2026-08-18)

**Related:** [tm-reference.md](tm-reference.md) (commands and troubleshooting)

### Shell & Development Environment

- Verify all dev tools working (Python, Node, Ruby, Rust, etc.)
- Monitor for x86_64 binaries appearing in PATH
- Update portable-profile as needed

### Disk Space Accounting

- Monitor for unexpected bloat in ~/Library, ~/.cache, or other categories
- Annual cleanup of old caches, logs, downloads

---

## Lessons Learned

### 1. IncludeByPath is a Contamination Risk

Legacy plist setting forces system files to be backed up. Always delete it before first backup.

### 2. File Count Matters as Much as GB

A 2 GB cache with 250K files is slower to restore than a 50 GB archive with 100 files. Use `tmutil addexclusion` for high-file-count paths.

### 3. System Paths Aren't Visible in TM GUI

User paths (~/Downloads, ~/Pictures, ~/repos) are GUI-selectable. System paths (/System, /usr, /Library, /opt/homebrew) require CLI `tmutil addexclusion`.

### 4. WiFi is Slow for Large Initial Backups

For backups >50 GB, use wired Ethernet. USB-C Ethernet dongle recommended (though may require troubleshooting on new Macs).

### 5. Legacy Dotfiles Can Override Package Managers

Stale `~/.npmrc`, `~/.pythonrc`, etc. can silently configure the wrong tool prefix. Audit these on migration.

### 6. Lazy TCC Permission Grants are Lower Overhead

Granting permissions proactively (all at once) is administratively simpler than letting errors bubble up. But errors do bubble up visibly, so lazy approach is viable if you monitor Terminal output.

---

## Reference

For setup and troubleshooting details, see:

- [TEMPLATE-macbook-air-setup.md](TEMPLATE-macbook-air-setup.md) -- Reusable setup flow
- [x86_64-remediation.md](x86_64-remediation.md) -- Intel binary audit and removal
- [tm-reference.md](tm-reference.md) -- Time Machine commands and troubleshooting
- [PLAN-names-networks-backups.md](PLAN-names-networks-backups.md) -- Full NAS + TM setup
