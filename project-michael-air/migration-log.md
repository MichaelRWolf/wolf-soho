# michael-air Migration Log

**Dates:** 2026-08-13 to 2026-08-14  
**Source:** Intel MacBook Pro `michael-pro`, water damaged  
**Destination:** Apple Silicon MacBook Air `michael-air` (M3, 13-inch)  
**Restore source:** Time Machine backup on Synology NAS

This document captures the initial migration/restore phase via Setup Assistant. For setup continuations, see [migration-todos.md](migration-todos.md).

## Quick Summary

Time Machine restore succeeded. Transferred **~106 GB** from NAS to michael-air. Key issues stem from Intel→ARM architecture mismatch (shell, Homebrew, binaries) plus TCC/privacy permissions disturbed by migration.

## Migration Process

### Phase 1: NAS Connection (Setup Assistant)

Setup Assistant → **Transfer information to this Mac** → **Other Server…**

| Issue | Resolution |
|-------|-----------|
| Bare `smb://192.168.8.129` showed no backups | Used NAS share picker; found `Backups-TM-Wolf` |
| macOS text substitution changed `TM` → `™` | Used lowercase `tm` to avoid substitution |

### Phase 2: Backup Warning

Migration Assistant warned that backup was created with macOS 15.7.3; destination was at earlier version. Decision: defer update post-migration to avoid mixing old OS + Intel-to-ARM issues.

### Phase 3: Account Inventory

Migration Assistant discovered these account-like entries:

| Entry                 | Selected | Size     | Notes                                   |
|-----------------------|----------|----------|-----------------------------------------|
| Applications          | Yes      | 17.6 GB  | Standard apps from old Mac              |
| MacPorts              | No       | —        | Legacy package manager                  |
| Message Bus           | No       | —        | System service                          |
| mmac-shared           | Yes      | 10.4 MB  | Unknown origin; retained to investigate |
| Test User             | No       | —        | Legacy test account                     |
| Annie Nomous          | Yes      | 20.6 MB  | Legacy account                          |
| Michael R. Wolf       | Yes      | 75.95 GB | Main user account                       |
| Other Files & Folders | Yes      | 23.42 GB | **Unaccounted; needs audit**            |
| System & Network      | Partial  | 1.6 MB   | Settings + Network only (no Printers)   |

**Total selected:** 117 GB | **Reported available after transfer:** 106.22 GB

### Phase 4: Restore Performance

**Early phase (first 45K files):** 36.6 MB/s  
**Late phase (377K files, many small):** 4.5 MB/s

Bottleneck shift: large-file network throughput → small-file metadata + SMB round trips. Interpretation: Time Machine/SMB handles small-file bulk poorly.

## Intel → ARM Issues Discovered

**Tracking:** See [GitHub issue #8](https://github.com/MichaelRWolf/wolf-soho/issues/8) for full audit of Intel x86_64 binaries migrated to michael-air. That issue stays open for ongoing cleanup.

---

### 1. Terminal Startup Failure

**Symptom:** Terminal.app failed to launch a shell.

**Root cause:** Login shell configured as `/usr/local/bin/bash` (Intel executable from old Homebrew). On ARM Mac without Rosetta, this binary cannot execute.

**Immediate fix:** `chsh -s /bin/zsh` (system zsh works; is ARM-native)

**Permanent fix:** Once native ARM Homebrew is installed, can link `bash` to `/opt/homebrew/bin/bash`.

**Lesson:** Clean shells (`/bin/zsh -f`) proved that shells themselves are fine; problem was in startup/login state.

### 2. Intel Homebrew Failure

**Symptom:** `brew` command failed with `Bad CPU type in executable`

**Details:** Migrated Homebrew lives at `/usr/local/Homebrew` (Intel prefix). Contains Intel-only bundled Ruby.

**Attempted workaround:** `arch -x86_64 /usr/local/bin/brew list` also failed → Rosetta was not yet available.

**Strategy (do not attempt):**
- ~~Try to convert~~ Intel Homebrew in-place to ARM
- ~~Use `brew cleanup`~~ to solve architecture mismatch
- ~~Rosetta emulation as permanent solution~~

**Correct strategy:**
1. Inventory Intel Homebrew without executing it: `find /usr/local/Cellar -maxdepth 1 -mindepth 1 -type d | sort`
2. Install fresh native Homebrew under `/opt/homebrew`
3. Reinstall only desired packages
4. Update PATH and startup files
5. Remove Intel tree only after verification

### 3. ~/Downloads: TCC, Not Unix Permissions

**Symptom:** `ls` in `~/Downloads` failed with `Operation not permitted`  
**But:** `ls -ld .` succeeded

**Diagnosis:** macOS privacy/TCC protection (not ordinary Unix file permissions)

**Fix:**
- System Settings → Privacy & Security → Files & Folders → Terminal → check **Downloads** permission
- Check Full Disk Access if needed
- Quit and reopen Terminal after permission grant

**Lesson:** Do not `chmod` aggressively; this is a privacy/capability issue, not permission damage.

## Unaccounted Capacity

### 23.42 GB "Other Files & Folders"

Unknown contents. Possible sources:
- `/Users/Shared` (shared data directory)
- `/Library` (system library; distinct from ~/Library)
- `/private` (temporary/system internals)
- Package-manager data outside home directory
- Old software support files

### 10.4 MB mmac-shared Account

Unknown origin. Needs investigation before deletion:
```sh
dscl . -read /Users/mmac-shared
# Check: UniqueID, PrimaryGroupID, NFSHomeDirectory, UserShell
# Then inspect the home directory to determine which software owns it
```

### 27.59 GB ~/Library (Main Account)

Migrated as a unit; no itemized breakdown shown in Migration Assistant.

**Valuable contents:**
- Application databases and support
- Preferences
- Browser profiles
- Mail/Messages local databases
- Containers and group containers
- Application state

**Often-regenerable contents:**
- Caches
- Logs
- Indexes
- IDE indexes/build artifacts
- Browser caches
- Downloaded package data

**Goal:** NOT "exclude Library entirely." Goal is to measure and decide exclusions based on recovery value + regeneration cost.

## Next Steps

See [migration-todos.md](migration-todos.md) for the prioritized checklist and Time Machine audit plan.
