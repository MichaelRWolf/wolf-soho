# michael-air: Post-Migration Checklist

**Status as of 2026-08-15**

## Completed (2026-08-13 to 2026-08-14)

- [x] Time Machine restore from NAS (2026-08-13/14)
  - Connected to Synology NAS via Setup Assistant
  - Selected 117 GB from backup; transferred ~106 GB
  - All user accounts + system settings migrated
- [x] Account discovery (2026-08-13/14)
  - Reviewed all proposed accounts (MacPorts, Message Bus, mmac-shared, Test User, Annie Nomous, Michael R. Wolf)
  - Retained mmac-shared for later investigation (10.4 MB)
  - Retained Annie Nomous (20.6 MB) 
- [x] Initial error diagnosis (2026-08-13/14)
  - Identified Terminal failure (Intel bash in login shell)
  - Identified Homebrew failure (Intel binary in `/usr/local/Homebrew`)
  - Identified ~/Downloads TCC/privacy issue

## High Priority (Shell & Development Environment)

- [ ] Update macOS to latest version
  - Current: macOS 15.7 Sequoia (from migration)
  - Status: Software Update available; defer Homebrew work until after
  - Do: System Settings → Software Update → reboot after update

- [ ] Fix login shell
  - Current shell: `/usr/local/bin/bash` (Intel, non-functional)
  - Do: `chsh -s /bin/zsh` (immediate, system zsh works)
  - Later: Link to `/opt/homebrew/bin/bash` once ARM Homebrew exists

- [ ] Inventory Intel Homebrew (non-destructive)
  - Do: `find /usr/local/Cellar -maxdepth 1 -mindepth 1 -type d -exec basename {} \; | sort`
  - Do: `ls /usr/local/Caskroom 2>/dev/null`
  - Save output to project for reference before deletion

- [ ] Install native ARM Homebrew
  - Do: `arch -arm64 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
  - Installs under `/opt/homebrew`
  - Verify: `which brew` → should show `/opt/homebrew/bin/brew`

- [ ] Update PATH and shell startup
  - Edit `~/.bashrc`, `~/.zshrc`, or equivalent
  - Ensure `/opt/homebrew/bin` comes before `/usr/local/bin`
  - Test: `brew --version` shows ARM architecture

- [ ] Remove Intel Homebrew (after validation)
  - Only after inventory saved + ARM Homebrew verified working
  - Do: `sudo rm -rf /usr/local/Homebrew /usr/local/Cellar /usr/local/Caskroom`

## Medium Priority (Privacy & Permissions)

- [ ] Fix ~/Downloads TCC/privacy
  - System Settings → Privacy & Security → Files & Folders
  - Verify Terminal has **Downloads** permission
  - Check Full Disk Access if needed
  - Quit and reopen Terminal to apply changes
  - Test: `ls ~/Downloads` should work

- [ ] Inspect remaining TCC permissions
  - Launch System Settings → Privacy & Security
  - Check what Terminal has access to (Full Disk Access, Calendar, Contacts, etc.)
  - Verify Spotlight has proper search paths
  - Note: Migration may have restored stale/overpermissive settings

## Medium Priority (Account Investigation)

- [ ] Investigate mmac-shared account
  - Do: `dscl . -read /Users/mmac-shared`
  - Check: UniqueID, PrimaryGroupID, NFSHomeDirectory, UserShell, real name
  - Inspect: Home directory contents to determine owner/purpose
  - Decision: Keep or delete (currently 10.4 MB)

- [ ] Investigate Annie Nomous account
  - Same as mmac-shared (20.6 MB)
  - Determine if legacy human account or software identity
  - May be safe to delete if no active data

## Low Priority (Data Accounting)

- [ ] Account for "Other Files & Folders" (23.42 GB)
  - Run: `sudo du -xhd 1 / 2>/dev/null | sort -h`
  - Run: `sudo du -xhd 1 /Library /Users/Shared /private 2>/dev/null | sort -h`
  - Run: `du -xhd 1 ~ | sort -h`
  - Identify sources and classify by value

- [ ] Measure ~/Library composition
  - Do: `du -sh ~/Library` (total)
  - Do: `du -sh ~/Library/* | sort -h` (by subdirectory)
  - Expected: Large caches, IDE indexes, app support, browser profiles
  - **Measure file count too:**
    - `find ~/Library/Caches -type f | wc -l` (cache file count)
    - `find ~/Library -type f | wc -l` (total files in Library)

- [ ] Recover launcher configuration
  - Inspect `/Applications` for launcher apps (Quicksilver, Alfred, LaunchBar, Raycast, etc.)
  - Check `~/Library/Preferences` for launcher settings
  - Verify Command-Space keyboard mapping is correct
  - Note: Old machine held procedural memory; don't guess

## Time Machine Audit (See Also: [tm-audit.md](tm-audit.md))

- [ ] Classify ~/Library subdirectories by recovery value and regeneration cost
  - High value / essential: Application data, preferences, keys
  - Medium value: Browser profiles, Mail messages
  - Low value / regenerable: Caches, logs, indexes, build artifacts, IDE state

- [ ] Identify high-file-count, low-value directories
  - Measure both GB and file count (file count is the time killer in restore)
  - Example: 2 GB cache with 250K files costs more than 50 GB with 20 files

- [ ] Decide Time Machine exclusions based on:
  - Recovery value (can you live without it post-restore?)
  - Regeneration cost (how long to rebuild if excluded?)
  - File count impact (how many small files will slow down restore?)

- [ ] Record all exclusion decisions
  - Before deleting or excluding anything, document the decision
  - Include: category, GB, file count, reasoning
  - Purpose: Next replacement machine will need this audit

## Launcher Recovery

- [ ] Verify Command-Space binding
  - Check System Settings → Keyboard → Keyboard Shortcuts → Spotlight
  - May be Spotlight, may be third-party launcher
  - Don't assume Quicksilver; check preferences

## Future TM Efficiency

After completing the above, document:

| Category | GB | File Count | Recovery Value | Regeneration Cost | Proposed Exclusion |
|----------|----|----|---|---|---|
| Personal documents/projects | TBD | TBD | High | High/impossible | Keep |
| ~/Library/Caches | TBD | TBD | Low | Low | Consider exclude |
| Developer caches (pip, npm, etc.) | TBD | TBD | Low | Low | Consider exclude |
| Application Support | TBD | TBD | Mixed | Mixed | Inspect individually |
| /Users/Shared | TBD | TBD | Unknown | Unknown | Inspect |
| /Library migrated leftovers | TBD | TBD | Mixed | Mixed | Inspect |
| Other Files & Folders | 23.42 GB | TBD | Unknown | Unknown | Account for |
| Intel Homebrew tree | TBD | TBD | Low (after inventory) | Reinstall | Remove after rebuild |

---

## Notes

- **Do NOT broadly exclude all of ~/Library.** Goal is granular, measured decisions based on both GB and file count.
- **Record decisions before deleting.** Next machine restoration will need to know what worked.
- **File count matters as much as GB.** 250K small files in a cache is more expensive to restore than 50 GB of large files.
- **Rosetta:** If available post-macOS update, can temporarily run Intel binaries; still plan to remove them after proper ARM migration.
