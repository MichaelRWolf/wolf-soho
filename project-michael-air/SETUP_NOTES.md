# michael-air Setup Fuckery & Lessons Learned

## macOS Installation Attempt

**Date:** 2026-08-14

**Issue:** First Tahoe 26.6.1 install stalled mid-download on saturated conference WiFi.

- Estimated 60 min, progressed to 31 min remaining, then held at 31 min for 45 minutes
- Reached "Ready to Restart" screen but install didn't complete
- Machine rolled back to Sequoia 15.3.1 on restart

**Root cause:** Network throughput bottleneck during large file download (10.88 GB). Time estimates jumped wildly (3h → 8h → 4h → 5h remaining).

**Decision:** Cancelled upgrade. Staying on Sequoia 15.3.1 for conference weekend. Tahoe upgrade deferred to stable WiFi (post-conference).

**Lesson:** Don't upgrade OS on saturated shared networks. Better to accept technical debt than spend 6-8 hours grinding on dial-up speeds.

---

## Node.js / npm Installation Issue

**Problem:** After `brew bundle install`, npm was still coming from `/opt/local/bin/npm` (MacPorts v10.9.8), not `/opt/homebrew/bin/npm` (Homebrew).

**Symptoms:**

- `npm install -g @anthropic-ai/claude-code` failed with `EACCES: permission denied mkdir /usr/local/lib`
- `npm config get prefix` returned `/usr/local` (wrong -- should be `/opt/homebrew`)
- `npm config get cache` returned `/Users/michael/.npm` (OK)

**Diagnosis:**

1. Checked no NPM environment variables or system .npmrc files
2. Ran `which node npm` → `/opt/local/bin` (MacPorts, not Homebrew)
3. Checked portable-profile/Makefile: michael-air should use Homebrew Node.js (`brew "node"` in Brewfile)
4. Found `/Users/michael/.npmrc` with hard-coded `prefix=/usr/local`

**Root cause:** Stale `.npmrc` from previous MacBook setup. npm respects this config regardless of which npm binary is running.

**Fix:**

1. Removed `~/.npmrc`
2. Ran `brew bundle install --file=~/repos/portable-profile/homebrew/Brewfile` (installed Homebrew Node.js)
3. Verified `which npm` → `/opt/homebrew/bin/npm`
4. Verified `npm config get prefix` → `/opt/homebrew`
5. Ran `make install_npm_globals` -- succeeded without permission errors

**Outcome:** claude-code and git commands now work on michael-air.

---

## Relevant to wolf-air → Apple Silicon Migration

### Package Manager Fragmentation

**Current state:** wolf-air (M1, macOS 12 Monterey) uses **MacPorts** for CLI tools; other machines use **Homebrew**.

**Issue:** This causes PATH/config conflicts when syncing dotfiles across machines.

- MacPorts npm (10.x) has different defaults than Homebrew npm (18.x+)
- MacPorts installs to `/opt/local/bin`; Homebrew to `/opt/homebrew/bin`
- Old `.npmrc` or shell config can accidentally invoke wrong npm version

**For future Apple Silicon replacement:**

1. **Decision needed:** Migrate wolf-air from MacPorts → Homebrew (breaks old workflows, simplifies maintenance)
2. **If keeping MacPorts:** Update portable-profile to explicitly manage npm version per machine (currently Brewfile comment says "wolf-air: MacPorts nodes22+npm10 via ports.txt")
3. **If switching to Homebrew:** Standardize all machines on Homebrew; retire MacPorts entirely

### portable-profile Brewfile Machine Detection

The Brewfile uses `hostname` variable to detect machine type (wolf-air, michael-pro, wendy-pro). This works but:

- Requires exact hostname match (fragile if machines are renamed)
- No fallback/warning for unknown hostnames (generates cryptic output)
- Possible to accidentally install wrong package set if hostname is wrong

**Recommendation for next major refactor:** Consider environment variable or config file for machine type rather than relying on hostname alone.

### npm Globals Installation

**Current flow (portable-profile/Makefile):**

- `install_npm_globals` runs `npm install -g` for each package in `NPM_GLOBALS` list
- Assumes vanilla npm config (no custom prefix)
- Works if Homebrew/MacPorts npm is correctly in PATH

**Issue:** Stale `.npmrc` files from previous setups silently override npm's built-in behavior.

**Recommendation:** Add pre-flight check to `install_npm_globals`:

```bash
# Warn if npm config prefix is not in expected location
EXPECTED_PREFIX=$(npm config get prefix 2>/dev/null)
if [[ ! "$EXPECTED_PREFIX" =~ (/opt/homebrew|/opt/local) ]]; then
  echo "WARNING: npm prefix is $EXPECTED_PREFIX (expected /opt/homebrew or /opt/local)" >&2
  echo "Check ~/.npmrc for stale config"
fi
```

### Xcode Command Line Tools

**Not yet installed on michael-air.** Needed for development. Command:

```bash
xcode-select --install
```

---

## michael-air Status

✅ Homebrew Node.js installed  
✅ npm globals installed (claude-code, markdownlint-cli)  
✅ Claude Code working  
✅ git working  
⏸️ Xcode Command Line Tools (pending)  
⏸️ macOS Tahoe upgrade (deferred post-conference)  
⏸️ Data migration from michael-pro
