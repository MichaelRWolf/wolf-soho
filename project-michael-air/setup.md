# michael-air Setup: Migration & Configuration

**Timeline:** 2026-08-13 (restore) → 2026-08-15 (current)  
**Source:** Intel MacBook Pro (michael-pro), water damaged  
**Method:** Time Machine restore via Setup Assistant from Synology NAS backup

**Issue tracking:** See [GitHub issue #8](https://github.com/MichaelRWolf/wolf-soho/issues/8) for Intel x86_64 binary audit (stays open).

---

## Part 1: Migration Process & Issues Found

### Phase 1: NAS Connection (Setup Assistant)

Setup Assistant → **Transfer information to this Mac** → **Other Server…**

**Result:** Connected to Synology NAS at `192.168.8.129`, found `Backups-TM-Wolf` share.

**Quirks:**
- Bare `smb://192.168.8.129` showed no backups; used NAS share picker instead
- macOS text substitution changed `TM` → `™` while typing username; used lowercase `tm` to avoid

### Phase 2: Backup Version Warning

Migration Assistant warned that backup was created with macOS 15.7.3; destination at earlier version. Decision: defer macOS update post-migration to avoid mixing old OS behavior with Intel→ARM troubleshooting.

### Phase 3: Account & Data Selection

Migration Assistant discovered legacy service/test accounts alongside the main account.

**Selected for transfer (117 GB):**

| Item | Size | Status |
|------|------|--------|
| Applications | 17.6 GB | ✓ Selected |
| Michael R. Wolf (home) | 75.95 GB | ✓ Selected |
| mmac-shared | 10.4 MB | ✓ Selected (unknown origin, investigate later) |
| Annie Nomous | 20.6 MB | ✓ Selected (legacy account, investigate) |
| Other Files & Folders | 23.42 GB | ✓ Selected (**unaccounted, needs audit**) |
| System Settings | 1.6 MB | ✓ Selected |
| Network | 23 KB | ✓ Selected |

**Not selected:**
- MacPorts, Message Bus, Test User, Printers (0 KB each)

**Result:** 106.22 GB available on Mac after transfer.

### Phase 4: Restore Performance

**Early phase:** 36.6 MB/s (45K files)  
**Late phase:** 4.5 MB/s (377K files)

Bottleneck: Large-file network speed → small-file metadata/SMB round trips. Time Machine/SMB handles file-count bulk poorly.

---

## Part 2: Intel → ARM Issues & Fixes

### Issue 1: Terminal Startup Failure

**Symptom:** Terminal.app failed to launch a shell.

**Root cause:** Login shell configured as `/usr/local/bin/bash` (Intel executable from old Homebrew). On ARM Mac, this binary cannot execute.

**Status:** ✓ **FIXED (2026-08-15)**
- Immediate fix: `chsh -s /bin/zsh` (system zsh is ARM-native)
- Permanent fix: Will link to `/opt/homebrew/bin/bash` after native ARM Homebrew installed

### Issue 2: Intel Homebrew Tree Unusable

**Symptom:** `brew` command fails with `Bad CPU type in executable`.

**Root cause:** Migrated Homebrew lives at `/usr/local/Homebrew` (Intel prefix). Contains Intel-only bundled Ruby; entire tree is x86_64.

**Attempted workaround (failed):** `arch -x86_64 /usr/local/bin/brew list` → Rosetta not available during early boot.

**Status:** ⏳ **TODO**
- Do NOT attempt to convert Intel Homebrew in-place
- Do NOT rely on Rosetta as permanent solution

**Correct strategy:**
1. Inventory Intel Homebrew non-destructively: `find /usr/local/Cellar -maxdepth 1 -mindepth 1 -type d -exec basename {} \; | sort`
2. Install fresh native Homebrew under `/opt/homebrew`
3. Reinstall desired packages (one by one, verify functionality)
4. Update PATH and shell startup files
5. Remove Intel tree only after validation

### Issue 3: ~/Downloads TCC Privacy Damage

**Symptom:** `ls` in `~/Downloads` failed with `Operation not permitted`. But `ls -ld .` worked.

**Diagnosis:** macOS privacy/TCC protection (not Unix file permission damage).

**Status:** ⏳ **TODO**

**Fix:**
- System Settings → Privacy & Security → Files & Folders
- Verify Terminal has **Downloads** permission
- Check Full Disk Access if needed
- Quit and reopen Terminal to apply changes

**Lesson:** Do not `chmod` aggressively; this is a capability issue, not permission damage.

### Issue 4: Unaccounted Capacity

**23.42 GB "Other Files & Folders"** — Unknown contents. Possible sources:
- `/Users/Shared` (shared data directory)
- `/Library` (system library; distinct from ~/Library)
- `/private` (temporary directories, system logs)
- Package-manager caches
- Old software debris

**Status:** ⏳ **TODO — Audit needed**

Commands to investigate:
```sh
sudo du -xhd 1 / 2>/dev/null | sort -h
sudo du -xhd 1 /Library /Users/Shared /private 2>/dev/null | sort -h
```

### Issue 5: 27.59 GB ~/Library Mixed Value

Migrated as atomic unit; no itemized breakdown shown. Contains both:

**Valuable:**
- Application databases and support
- Preferences
- Browser profiles
- Mail/Messages local databases
- SSH keys, credentials

**Often regenerable:**
- Caches
- Logs
- Indexes
- IDE build artifacts
- Browser caches
- Package download data

**Status:** ⏳ **TODO — Measure & audit**

See [tm-strategy.md](tm-strategy.md) for detailed framework.

### Issue 6: Legacy Accounts

**mmac-shared (10.4 MB)** and **Annie Nomous (20.6 MB)** — Unknown origin. Retained to investigate.

**Status:** ⏳ **TODO**

```sh
dscl . -read /Users/mmac-shared
# Check: UniqueID, PrimaryGroupID, NFSHomeDirectory, UserShell
# Then inspect home directory to determine owner
```

---

## Part 3: Setup Checklist

### ✓ Completed (2026-08-13 to 2026-08-15)

- [x] Time Machine restore from NAS (2026-08-13/14)
- [x] Account discovery and selection review (2026-08-13/14)
- [x] Terminal failure diagnosis and immediate fix (2026-08-15)
- [x] Launcher recovery verification — Quicksilver (qsapp.com) on Cmd-Space (2026-08-15)

### ⏳ High Priority (Shell & Development Environment)

- [ ] Update macOS to latest version
  - Current: 15.7 Sequoia
  - Do: System Settings → Software Update → reboot

- [ ] Fix login shell (completed immediate fix, needs permanent)
  - Current: `chsh -s /bin/zsh` (system zsh, working)
  - Later: `chsh -s /opt/homebrew/bin/bash` (post-Homebrew rebuild)

- [ ] Inventory Intel Homebrew (non-destructive)
  - `find /usr/local/Cellar -maxdepth 1 -mindepth 1 -type d -exec basename {} \; | sort`
  - `ls /usr/local/Caskroom 2>/dev/null`
  - Save output before deletion

- [ ] Install native ARM Homebrew
  - `arch -arm64 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
  - Installs under `/opt/homebrew`

- [ ] Update PATH and shell startup
  - Edit `~/.bashrc`, `~/.zshrc`, etc.
  - Ensure `/opt/homebrew/bin` comes before `/usr/local/bin`

- [ ] Remove Intel Homebrew (after validation)
  - `sudo rm -rf /usr/local/Homebrew /usr/local/Cellar /usr/local/Caskroom`

### ⏳ Medium Priority (Privacy & Permissions)

- [ ] Fix ~/Downloads TCC/privacy (see Issue 3 above)
- [ ] Audit other TCC permissions (Full Disk Access, Spotlight, Calendar, Contacts, etc.)

### ⏳ Medium Priority (Account Investigation)

- [ ] Investigate mmac-shared account
- [ ] Investigate Annie Nomous account
- [ ] Decide: keep or delete each (currently 10.4 MB + 20.6 MB)

### ⏳ Low Priority (Data Accounting & Cleanup)

- [ ] Account for 23.42 GB "Other Files & Folders" (see Issue 4)
- [ ] Measure ~/Library by size and file count (see Issue 5)
- [ ] Run Time Machine audit (see [tm-strategy.md](tm-strategy.md))

---

## Intel x86_64 Binary Audit & Remediation (Issue #8)

Apple silently migrated incompatible x86_64 binaries. Audit completed 2026-08-15.

**Audit results:** See [x86_64-remediation.md](x86_64-remediation.md) for:
- Complete findings (Universal binaries, Rust toolchain, MacPorts, X11, uv)
- Replacement strategy (how to install ARM equivalents)
- PATH & dotfiles updates
- File removal checklist (reclaim 2-5 GB)
- Time Machine exclusion strategy

**Remediation priorities:**
1. **Immediate:** Rebuild Rust & UV
2. **Short-term:** Remove MacPorts (or keep if needed)
3. **Cleanup:** PATH references, Time Machine exclusions

---

## Progress Log

### Friday, 2026-08-15

**Completed:**
- [x] Skipped macOS update (deferred: time & bandwidth constraints)
- [x] Retained bash shell (chsh REJECTED: too fragile to change underlying shell)
- [x] Homebrew installed and verified working (2026-08-15)
  - `make install_brew_thingies` from portable-profile repo using Brewfile (as altered)
  - All expected packages installed and functional
- [x] Intel x86_64 audit completed (2026-08-15)
  - Comprehensive scan: 289 KB log, 9-part audit
  - Findings: Rust toolchain (x86_64-only), MacPorts tree (300+ binaries), X11, uv
  - Universal binaries (Ruby, Perl, Python extensions) safe to keep
  - See [x86_64-remediation.md](x86_64-remediation.md) for detailed action plan
- [x] Created TCC tools × permissions matrix (below)
- [x] Created GitHub issue #9: Machine rename (michael-pro → michael-air)
- [x] Created GitHub issue #10: Stabilize Time Machine backups (michael-pro → michael-air)
- [x] Rust rebuilt: ARM64 native installed via Homebrew (1.97.1, 2026-08-15)
  - Verified: `rustc`, `cargo` both ARM64 from `/opt/homebrew/bin/`
- [x] UV rebuilt: ARM64 native installed via Homebrew (0.12.5, 2026-08-15)
  - Verified: `uv` ARM64 from `/opt/homebrew/bin/`
- [x] x86_64 binaries inventory & categorization (2026-08-15)
  - /opt/local/bin: 497 binaries (412 have Homebrew equivalents, 85 legacy)
  - /opt/X11/bin: 123 binaries (deprecated; XQuartz alternative available)
  - See [x86_64-binaries-inventory.md](x86_64-binaries-inventory.md)

**In Progress:**
- [ ] TCC permission audit (proactive, matrix-based approach)
- [ ] x86_64 remediation: Rust rebuild, MacPorts/X11 removal, PATH cleanup (see [x86_64-remediation.md](x86_64-remediation.md))

## TCC Permissions Matrix: Tools vs. Required Access

| Tool/App | Full Disk Access | Downloads | Documents | Desktop | Photos | Mail | Calendar | Contacts | Camera | Microphone | Location | Local Network |
|----------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Terminal | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ? | ? | ? | ✓ |
| Xcode | ✓ | ✓ | ✓ | ✓ | ✓ | ? | ? | ? | ? | ? | ? | ✓ |
| VS Code | ✓ | ✓ | ✓ | ✓ | ? | ? | ? | ? | ? | ? | ? | ✓ |
| Emacs | ✓ | ✓ | ✓ | ✓ | ? | ? | ? | ? | ? | ? | ? | ? |
| Python (scripts) | ✓ | ✓ | ✓ | ✓ | ? | ? | ? | ? | ? | ? | ? | ✓ |
| Mail.app | ? | ? | ? | ? | ✓ | ✓ | ✓ | ? | ? | ✓ | ? | ? |
| Spotlight (indexing) | ✓ | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? |
| Backup tools (Time Machine) | ✓ | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? | ? |
| SSH/Git operations | ✓ | ✓ | ✓ | ✓ | ? | ? | ? | ? | ? | ? | ? | ✓ |

**Legend:** ✓ = needed, ? = investigate, blank = not needed

**Status:** Framework ready; to be applied all at once post-decision.

## Next Session Priorities

1. **TCC permission matrix review** (grant all at once, systematically)
2. **Intel x86_64 audit** (review background output)
3. **Machine rename** (after Homebrew stable; see issue #9)
4. **Time Machine stabilization** (see issue #10)
5. **Time Machine efficiency audit** (ongoing, lower priority)
