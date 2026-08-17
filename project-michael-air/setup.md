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

- [ ] Update macOS to latest version — **DEFERRED (2026-08-16): Bandwidth constraints + low ROI**
  - Current: 15.7 Sequoia (stable, no blockers)
  - Target: Tahoe (14 GB download, ~30 min at 7 MB/s; prior attempt failed mid-download)
  - Decision: Defer to stable WiFi. No critical bugs in 15.7; upgrade is "nice to have"

- [x] Fix login shell (2026-08-15)
  - [x] Immediate fix: `chsh -s /bin/zsh` (system zsh, working) (2026-08-15)
  - [x] Permanent fix: Switch to Homebrew bash (2026-08-15)
    ```bash
    # 1. Verify Homebrew bash is installed
    brew install bash
    
    # 2. Add to /etc/shells if needed (skip if already present)
    grep /opt/homebrew/bin/bash /etc/shells || echo /opt/homebrew/bin/bash | sudo tee -a /etc/shells
    
    # 3. Change login shell
    chsh -s /opt/homebrew/bin/bash
    
    # 4. Verify (close and reopen Terminal for change to take effect)
    echo $SHELL        # Should show /opt/homebrew/bin/bash
    bash --version     # Should show Homebrew version
    ```

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

- [ ] Fix ~/Downloads TCC/privacy (see Issue 3 above) — **DEFERRED: YAGNI (lazy TCC as needed)**
- [ ] Audit other TCC permissions (Full Disk Access, Spotlight, Calendar, Contacts, etc.) — **DECISION: Grant only on demand, not proactively**

**Rationale:** Terminal mostly works; permissions fail visible → fix when needed. Proactive grant burden > reactive fix burden.

### ⏳ Medium Priority (Account Investigation)

- [x] Investigate mmac-shared account — **SKIP (2026-08-16): ROI not worth audit time**
- [x] Investigate Annie Nomous account — **SKIP (2026-08-16): ROI not worth audit time**
- [x] Decide: keep or delete each (currently 10.4 MB + 20.6 MB) — **DECISION: KEEP both (too small to matter)**

**Rationale:** 31 MB total < 1% of storage; investigation/decision overhead > benefit. Keep as-is.

### ⏳ Low Priority (Data Accounting & Cleanup)

- [ ] Account for 23.42 GB "Other Files & Folders" (see Issue 4)
- [ ] Measure ~/Library by size and file count (see Issue 5)
- [x] Simplify Time Machine exclusions (2026-08-17) — **COMPLETED**
  - Excluded: `~/Downloads` (ephemeral), `~/Pictures` (on NAS), `~/repos` (regenerable)
  - See [tm-strategy.md](tm-strategy.md) → **Final Exclusion Decision** for rationale

---

## Intel x86_64 Binary Audit & Remediation (Issue #8)

Apple silently migrated incompatible x86_64 binaries. Audit completed 2026-08-15; remediation completed 2026-08-16.

**Audit results:** See [x86_64-remediation.md](x86_64-remediation.md) for:
- Complete findings (Universal binaries, Rust toolchain, MacPorts, X11, uv)
- **NEW: Quick Reference table** for future Intel→ARM migrations (what's worth checking, what to skip)
- Replacement strategy (how to install ARM equivalents)
- PATH & dotfiles updates
- File removal checklist (reclaim 2-5 GB)
- Time Machine exclusion strategy

**Remediation completed (2026-08-16):**
1. ✓ Rust rebuilt (ARM64)
2. ✓ UV rebuilt (ARM64)
3. ✓ /opt/local removed (1.4 GB)
4. ✓ /opt/X11 removed (154 MB)
5. ✓ PATH cleaned

**Strategic decision: PATH Verification Strategy (deferred)**
- [PATH-verification-proposal.md](PATH-verification-proposal.md) proposed execution-test approach (prevent broken binaries in PATH)
- **Decision (2026-08-16): DEFER (low ROI post-cleanup)**
- Rationale: Problem is already solved (/opt/local removed); benefits only future migrations. Implement only if pattern recurs or portable-profile requires universal defensiveness.
- Revisit: Only if PATH pollution observed in future machines

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

**Completed (x86_64 cleanup):**
- [x] Removed /opt/local (MacPorts x86_64 tree, 2-3 GB, 2026-08-15)
- [x] Removed /opt/X11 (X11 x86_64 tools, 100-500 MB, 2026-08-15)
- [x] Cleaned PATH: Removed MacPorts entries from portable-profile/.profile (2026-08-15)
- [x] Created X11 migration documentation for future wolf-air retirement (2026-08-15)

**In Progress:**
- [ ] TCC permission audit (proactive, matrix-based approach)

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

---

## Lessons Learned & Troubleshooting

### macOS Installation Attempt (2026-08-14)

**Issue:** Tahoe 26.6.1 upgrade stalled mid-download on saturated conference WiFi (10.88 GB). Reached "Ready to Restart" but rollback to Sequoia 15.3.1 occurred on next boot.

**Root cause:** Network throughput bottleneck; time estimates jumped wildly (3h → 8h → 4h → 5h).

**Lesson:** Do not upgrade OS on shared/saturated networks. Accept technical debt over 6-8 hour install grinds.

**Status:** Tahoe upgrade deferred to post-conference with stable WiFi.

### npm Configuration Pollution (2026-08-15)

**Issue:** After `brew bundle install`, npm was still pointing to MacPorts `/opt/local/bin/npm` (v10.9.8) instead of Homebrew `/opt/homebrew/bin/npm`. `npm install -g` failed with EACCES permission errors.

**Root cause:** Stale `~/.npmrc` with hard-coded `prefix=/usr/local` from previous MacBook setup. npm respects this config regardless of which npm binary is in PATH.

**Fix:** Removed `~/.npmrc`, re-ran `brew bundle install`, verified `npm config get prefix` → `/opt/homebrew`.

**Lesson:** Legacy dotfiles can silently override package manager behavior. Always audit `.npmrc`, `.pythonrc`, `.gemrc` when migrating machines.

### Package Manager Fragmentation (wolf-air)

**Current state:** wolf-air (M1) uses MacPorts; other machines (michael-air, michael-pro, wendy-pro) use Homebrew. This creates PATH conflicts when syncing dotfiles.

**Future decision needed:** Migrate wolf-air from MacPorts → Homebrew (simplifies maintenance, breaks legacy workflows).

---

## Next Session Priorities

1. **TCC permission matrix review** (grant all at once, systematically)
2. **Intel x86_64 audit** (review background output)
3. **Machine rename** (after Homebrew stable; see issue #9)
4. **Time Machine stabilization** (see issue #10)
5. **Time Machine efficiency audit** (ongoing, lower priority)
6. **Xcode Command Line Tools** (run `xcode-select --install`)
