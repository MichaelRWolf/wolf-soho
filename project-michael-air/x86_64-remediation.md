# x86_64 Binary Remediation Plan for michael-air

**Audit Date:** 2026-08-15  
**Log:** `x86_64-audit.log` (289 KB, comprehensive scan)  
**Status Update:** 2026-08-16 (X11 removed 154 MB; /opt/local held pending Homebrew verification)

---

## Prefix Directories Reference Table

See [detailed prefix map](https://claude.ai/code/artifact/f2e3a0cf-7ed9-495c-8fb0-a2e7fb1dd095) for complete architecture & tool breakdown.

### Quick Summary

| Prefix          | Tool               | Arch      | Status    | Size                |
|-----------------|--------------------|-----------|-----------|---------------------|
| `/opt/homebrew` | Homebrew (primary) | arm64     | ✓ ACTIVE  | —                   |
| `/usr/bin`      | System             | universal | ✓ SAFE    | —                   |
| `~/.cargo`      | Rust env           | N/A       | ✓ MINIMAL | —                   |
| `/opt/local`    | MacPorts           | x86_64    | ⚠️ HELD    | 1.4 GB              |
| `/opt/X11`      | X11                | x86_64    | ✓ REMOVED | 154 MB (2026-08-16) |

---

## Findings Summary

### Category 1: Universal Binaries (Safe — Keep As-Is)

**Status:** ✓ OK to keep; ARM64 version will be invoked automatically

**Details:**
- `/usr/bin/ruby` (Mach-O universal: x86_64 + arm64e)
- `/usr/bin/perl` (Mach-O universal: x86_64 + arm64e)
- Python extensions (`charset_normalizer`, `lxml`, `CoreBluetooth`, `dispatch`, `Foundation`)
  - All are universal binaries with both x86_64 + arm64 versions
  - Reinstalled fresh with ARM Homebrew; x86_64 component ignored automatically

**Action:** Do nothing; macOS automatically selects arm64 when available.

---

### Category 2: Rust Toolchain (x86_64-only — Priority High)

**Location:** `~/.cargo/bin/`

**Affected binaries:**
- Core: `rustup`, `rustc`, `rustdoc`, `cargo`
- Tools: `cargo-clippy`, `cargo-fmt`, `cargo-miri`, `clippy-driver`, `rls`, `rust-analyzer`
- Debugging: `rust-gdb`, `rust-gdbgui`, `rust-lldb`

**Current status:** Non-functional on ARM

**Remediation:**

```bash
# Step 1: Remove old x86_64 installation
rm -rf ~/.cargo ~/.rustup

# Step 2: Reinstall Rust via rustup (will auto-detect ARM64)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Step 3: Verify ARM64 install
rustc --version
file $(which rustc)  # Should show: Mach-O 64-bit executable arm64

# Step 4: Reinstall components
rustup component add rustfmt clippy
rustup component add rust-analyzer  # or via Homebrew: brew install rust-analyzer
```

**Timeline:** Do immediately (Rust likely broken on ARM now)

---

### Category 3: MacPorts Tree (x86_64-only — Priority: Hold Pending Verification)

**Location:** `/opt/local/` (entire tree)

**Scale:** 497 binaries in `/opt/local/bin/` alone; ~1.4 GB total  
Examples: dbus, graphviz, dia, fonts, perl@5.8, perl@5.12, db46, graph tools, etc.

**Status (2026-08-16 audit):**
- All confirmed x86_64 architecture (broken on ARM)
- Homebrew equivalents verified installed for major tools:
  - ✓ autoconf, automake, libtool (build tools)
  - ✓ dbus (message bus)
  - ✓ graphviz (graph layout)
  - ✓ python3 (Homebrew; replaces python2.6/2.7)
  - ✓ perl (system 5.34; replaces perl5.8/5.12)
  - ✓ ruby (system; universal binary)
  - ✓ git (Homebrew)
  - ⚠️ dia (diagram editor) — NOT in standard Homebrew (check if needed)
  - ⚠️ postgresql — available in Homebrew but NOT currently installed
  - ⚠️ subversion — available in Homebrew but NOT currently installed

**Inventory Notes:**
- 497 binaries = many are symlinks and variants (perl 5.8/5.12, python 2.6/2.7, autoconf-1.11/1.13, etc.)
- Core tools (dbus, graphviz, autotools) have working ARM64 Homebrew equivalents
- Legacy tools (perl 5.8, python 2.6) superseded by system/Homebrew versions

**Assessment:**
- Original MacPorts installation (from intel machine migration)
- Most tools available in Homebrew with ARM64 support
- **Decision pending:** Verify if dia, postgresql, subversion actually needed before removal
- **Recommendation:** Hold removal; create inventory of any actual dependencies before deleting

**Remediation:**

```bash
# Step 1: Identify what's actually needed from MacPorts
# Common tools in Homebrew instead:
# - graphviz → brew install graphviz
# - dbus → brew install dbus (if needed)
# - postgresql → brew install postgresql
# - perl variants → brew install perl (if needed)

# Step 2: Inventory for any custom tools
ls /opt/local/bin | head -20
# If nothing essential, proceed to removal

# Step 3: Remove MacPorts tree
sudo rm -rf /opt/local

# Step 4: Clean up any MacPorts references in PATH/dotfiles
grep -r "opt/local" ~/.bashrc ~/.zshrc ~/.profile 2>/dev/null
# Remove any lines that reference /opt/local

# Step 5: Optional MacPorts cleanup (if installed as package)
# sudo port selfupdate && sudo port uninstall --follow-dependencies all
```

**Decision point:** Do you use any MacPorts tools regularly?
- If **NO**: Proceed with removal (free up space, clean up)
- If **YES**: Identify specific tools; install ARM-compatible versions via Homebrew

---

### Category 4: X11 (x86_64-only — Priority: Low)

**Location:** `/opt/X11/`  
**Binaries:** xdotool, xdpyinfo, xset, xwininfo, xwud, etc.

**Assessment:**
- X11 on macOS is deprecated and rarely needed
- Most macOS applications use native frameworks, not X11
- Usually installed as legacy dependency

**Remediation:**

```bash
# Step 1: Check if anything actually uses X11
lsof | grep -i X11 || echo "X11 not in use"

# Step 2: If not used, remove
sudo rm -rf /opt/X11

# Step 3: If needed: install XQuartz (ARM-native version)
# Download from: https://www.xquartz.org/
```

**Decision point:** Do you need X11?
- If **NO**: Remove `/opt/X11` (free up space)
- If **YES**: Install XQuartz (native ARM version) instead

---

### Category 5: UV Python Package Manager (x86_64-only — Priority: Medium)

**Location:** `~/.local/bin/uv`, `~/.local/bin/uvx`

**Current status:** Non-functional on ARM

**Remediation:**

```bash
# Step 1: Remove old x86_64 installation
rm -f ~/.local/bin/uv ~/.local/bin/uvx
rm -rf ~/.cache/uv

# Step 2: Install ARM-native version via Homebrew
brew install uv

# Step 3: Verify
which uv  # Should show /opt/homebrew/bin/uv
file $(which uv)  # Should show arm64
```

**Timeline:** Do immediately (uv is useful for Python workflows)

---

## PATH & Dotfiles Update Strategy

### Current PATH (likely)

```bash
echo $PATH
# Example: ~/.cargo/bin:/opt/local/bin:/opt/local/sbin:/opt/X11/bin:...
```

### Action: Update ~/.zshrc, ~/.bashrc, ~/.profile

**Search for and remove references to:**
- `~/.cargo/bin` (will reinstall, add back automatically)
- `/opt/local/bin` and `/opt/local/sbin`
- `/opt/X11/bin`

**Commands:**

```bash
# Backup first
cp ~/.zshrc ~/.zshrc.backup-2026-08-15

# Remove x86_64 paths
grep -v "/opt/local\|/opt/X11\|~/.cargo" ~/.zshrc > ~/.zshrc.tmp && mv ~/.zshrc.tmp ~/.zshrc

# Verify (check for any remaining x86_64-only paths)
grep "opt/local\|opt/X11\|\.cargo" ~/.zshrc && echo "WARNING: Found remaining x86_64 paths"

# Source and test
source ~/.zshrc
echo $PATH  # Should not contain /opt/local, /opt/X11
```

### Homebrew PATH (already correct)

Homebrew installations via `brew install` are already under `/opt/homebrew/bin` (ARM-native). No changes needed.

---

## File Removal Checklist

**Remove completely:**

```bash
# Rust (will reinstall fresh)
[ ] ~/.cargo/         (~500 MB typical)
[ ] ~/.rustup/        (~300 MB typical)

# MacPorts (decision: yes/no)
[ ] /opt/local/       (varies; typically 1-3 GB)

# X11 (decision: yes/no)
[ ] /opt/X11/         (varies; typically 100-500 MB)

# UV old installation (small)
[ ] ~/.local/bin/uv   (1-2 MB)
[ ] ~/.local/bin/uvx  (1-2 MB)
[ ] ~/.cache/uv       (varies)
```

**Safe to leave (universal binaries):**
- `/usr/bin/ruby`
- `/usr/bin/perl`
- Python site-packages (universal binaries)

**Total reclaimed:** 2-5 GB depending on what's removed

---

## Update Strategy: Integration into portable-profile

### Option A: Standalone Script (Current)

Create `x86_64-remediation.sh` in `bin/` or `portable-profile/scripts/`:

```bash
#!/usr/bin/env bash
# Remediate x86_64 binaries after intel→arm migration

set -e  # Exit on error

echo "=== x86_64 Remediation for ARM MacBook ==="

# Rust
echo "Rebuilding Rust toolchain..."
rm -rf ~/.cargo ~/.rustup
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
source ~/.cargo/env

# UV
echo "Removing old UV, installing via Homebrew..."
rm -f ~/.local/bin/uv ~/.local/bin/uvx
brew install uv

# MacPorts (optional)
read -p "Remove MacPorts? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
  sudo rm -rf /opt/local
fi

# X11 (optional)
read -p "Remove X11? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
  sudo rm -rf /opt/X11
fi

# Clean PATH
echo "Cleaning PATH references..."
for shell_rc in ~/.zshrc ~/.bashrc ~/.profile; do
  if [ -f "$shell_rc" ]; then
    grep -v "/opt/local\|/opt/X11" "$shell_rc" > "$shell_rc.tmp" && mv "$shell_rc.tmp" "$shell_rc"
  fi
done

echo "=== Remediation complete ==="
```

### Option B: Integrate into portable-profile Brewfile

**Status:** ✓ DONE (2026-08-15)

**Changes made:**
- Added `brew "rust"` to Brewfile (precompiled stable, not nightly/rustup)
- Added `"michael-air"` to when clause: `when "michael-pro", "wendy-pro", "michael-air"`
- `brew "uv"` already present in Brewfile for michael-pro/wendy-pro (now includes michael-air)
- Wolf-air continues to use Makefile `install_rust` and `install_uv` (MacPorts workflow)

**Implication for future michael-air setups:**
- When running `make install_brew_thingies`, both `rust` and `uv` install automatically
- Precompiled ARM64 bottles, no compilation, no nightly complexity
- Post-install script not needed (unlike rustup approach)

---

## Time Machine: Exclusion & Ignore Strategy

### What NOT to Back Up (x86_64-related)

**Add to Time Machine exclusions:**

```
~/.cargo/                    (Rust build cache, easily regenerated)
~/.rustup/                   (Rust toolchain, reinstalled via rustup)
~/.cache/uv/                 (uv package cache, regenerated on use)
/opt/local/                  (After removal; MacPorts)
/opt/X11/                    (After removal; X11)
```

### Implementation

```bash
# Via Terminal/System Preferences:
System Settings → General → Time Machine → Options
→ Add: ~/.cargo, ~/.rustup, ~/.cache/uv

# Or via command line (Sonoma+):
tmutil excludeItem ~/.cargo
tmutil excludeItem ~/.rustup
tmutil excludeItem ~/.cache/uv
```

### portable-profile Integration

**Proposed addition to portable-profile setup:**

```bash
# In setup/time-machine-exclusions.sh or Makefile target:

# Exclude architecture-specific caches
tmutil excludeItem ~/.cargo
tmutil excludeItem ~/.rustup
tmutil excludeItem ~/.cache/uv
tmutil excludeItem ~/.cache/pip
tmutil excludeItem ~/.cache/npm
tmutil excludeItem ~/.cache/go

echo "Time Machine exclusions configured"
```

---

## Execution Order & Timeline

### Immediate (Today)

**Option A (Current, before portable-profile updated):**
1. [ ] Rebuild Rust: `rm -rf ~/.cargo ~/.rustup && curl https://sh.rustup.rs | sh`
2. [ ] Rebuild UV: `rm -f ~/.local/bin/uv && brew install uv`
3. [ ] Verify: `rustc --version && uv --version`

**Option B (Future, using updated portable-profile):**
1. [ ] Run: `make install_brew_thingies` (installs rust + uv automatically)
2. [ ] Verify: `rustc --version && uv --version`

**Recommended:** Option B (cleaner, automatic via Homebrew)

### Short-term (This week)

4. [ ] Decide on MacPorts: remove or keep?
5. [ ] Decide on X11: remove or keep?
6. [ ] Clean PATH dotfiles: `grep -v "/opt/local\|/opt/X11" ~/.zshrc > ~/.zshrc.tmp`
7. [ ] Configure Time Machine exclusions

### Integration (Parallel)

8. [ ] Add Rust/UV to portable-profile Brewfile
9. [ ] Create x86_64-remediation.sh script in bin/
10. [ ] Document in portable-profile README

---

## Verification Checklist

After remediation:

```bash
# No x86_64 binaries in PATH
echo $PATH | tr ':' '\n' | while read d; do file "$d"/* 2>/dev/null | grep x86_64 && echo "FOUND: $d"; done

# Rust works
rustc --version
rustc --print sysroot  # Should show .rustup/toolchains/stable-aarch64-apple-darwin

# UV works
uv --version

# No broken symlinks
find ~ -type l ! -exec test -e {} \; -print 2>/dev/null | grep -E "cargo|uv|local|X11" | head -20

# Time Machine knows to skip
tmutil destinationinfo
# (should show excluded items)
```

---

## Risk Mitigation

**Backup before removing:**

```bash
# Backup ~/.cargo in case custom configs
tar czf ~/Desktop/cargo-backup-2026-08-15.tar.gz ~/.cargo ~/.rustup

# Backup ~/.local/bin
tar czf ~/Desktop/local-bin-backup-2026-08-15.tar.gz ~/.local/bin
```

**If something breaks:**

1. Restore from backup: `tar xzf ~/Desktop/cargo-backup-*.tar.gz`
2. Reinstall via Homebrew: `brew install rust-analyzer uv`
3. Check git history: portable-profile setup for canonical setup

---

## Progress Log (2026-08-16 Sunday)

### X11 Cleanup (✓ COMPLETED)

**Action:** User manually removed `/opt/X11` (X11 x86_64 binaries)

```
Space reclaimed: 154 MB
Arch confirmed: All x86_64 (broken on ARM)
Decision: Not needed; native macOS frameworks preferred
Status: ✓ REMOVED
```

### MacPorts Verification (⏳ IN PROGRESS)

**Finding:** `/opt/local` is 1.4 GB (not 3-4 GB estimate)

**Inventory:** 497 binaries verified as x86_64

**Homebrew Equivalents Verified:**
- ✓ autoconf, automake, libtool (build tools installed)
- ✓ dbus (message bus installed)
- ✓ graphviz (graph layout installed)
- ✓ python3 (Homebrew 3.14.7 installed; replaces python 2.6/2.7)
- ✓ perl (system 5.34 installed; replaces perl 5.8/5.12)
- ✓ ruby (system universal; replaces MacPorts ruby)
- ✓ git (Homebrew installed)

**Pending Verification:**
- ⚠️ dia (diagram editor) — check if actually used
- ⚠️ postgresql — available but not currently installed
- ⚠️ subversion — available but not currently installed

**Decision:** HOLD removal of `/opt/local` until confirmed that dia/postgresql/subversion are not needed or user explicitly approves.

### Cache Cleanup (✓ COMPLETED)

**Removed 2026-08-16:**
- `~/.local/share/uv/python/cpython-3.10-*-x86_64-none`
- `~/.local/share/uv/python/cpython-3.11-*-x86_64-none`
- `~/.local/share/uv/python/cpython-3.12-*-x86_64-none`
- `~/.cache/uv` (old x86_64 cache)
- `~/.local/share/claude/versions/2.1.118` (x86_64 binary)
- `~/.local/share/claude/versions/2.1.119` (x86_64 binary)
- `~/.local/share/cursor-agent/versions/2026.02.13-41ac335` (x86_64 binaries)

**Result:**
- `make install-dependencies` now works (uv auto-downloads ARM64 Python)
- Claude Code & Cursor auto-redownload ARM64 versions on next launch
- Fresh uv cache created (62 MB ARM64)

### Space Accounting

| Directory | Size | Arch | Status |
|-----------|------|------|--------|
| `/opt/X11` | 154 MB | x86_64 | ✓ REMOVED (2026-08-16) |
| `/opt/local` | 1.4 GB | x86_64 | ⏳ HELD (pending dia/postgresql/subversion check) |
| `~/.cache/uv` | 62 MB | arm64 | ✓ FRESH (regenerated) |
| **Total x86_64 still present:** | **1.4 GB** | | |
| **Total x86_64 removed:** | **154 MB** | | |

**Note:** Original estimate of 3.1-4.5 GB was conservative; actual /opt/local is 1.4 GB.

