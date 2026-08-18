# Template: MacBook Air Setup (ARM Migration)

**Purpose:** Reusable setup flow for migrating Intel data to new ARM MacBook Air (via Time Machine restore).

**For:** future machines (wendy-air, etc.)  
**Reference:** See `project-michael-air` for completed example and lessons learned.

---

## Quick Overview

1. **Restore** via Time Machine (Migration Assistant)
2. **Identify issues** (Intel binaries, TCC permissions, shell setup)
3. **Rebuild** shell, Homebrew, development environment
4. **Configure** Time Machine with clean exclusions
5. **Validate** that backups contain only intended data

---

## Phase 1: Time Machine Restore

### 1.1: Boot and Launch Migration Assistant

1. Power on new MacBook Air
2. Follow setup to "Transfer information to this Mac"
3. Select "Other Server…" → connect to NAS (`192.168.8.129` or `wolfden-nas.local`)
4. Select Time Machine backup share (e.g., `Backups-TM-Michael` for michael-air backups)
5. Choose accounts/data to restore (typically: main user account + Applications)
6. Let Migration Assistant complete (can take 2-8 hours depending on data size)

**Note:** macOS may warn about backup being from newer OS version. Safe to proceed; defer OS updates until after shell/Homebrew are working.

### 1.2: Account & Data Selection

**Recommended:**

- ✓ Select main user home directory
- ✓ Select Applications (will reinforce)
- ✓ Skip system accounts (like `_guest`, `_unknown`)
- ✓ Investigate unknown accounts; delete if orphaned

**Verify in Setup Checklist (Phase 4) after restore.**

---

## Phase 2: Identify Issues Immediately

### 2.1: Shell Startup Failure

**Symptom:** Terminal.app fails to launch a shell.

**Likely cause:** Login shell is set to Intel binary (e.g., `/usr/local/bin/bash`).

**Quick fix:**

```bash
# Open Terminal if possible; if not, use Recovery Mode
chsh -s /bin/zsh  # System zsh is ARM64 native
```

### 2.2: Homebrew Unusable

**Symptom:** `brew` command fails with `Bad CPU type in executable`.

**Likely cause:** Migrated Homebrew at `/usr/local/Homebrew` is Intel-only.

**Plan:** Do NOT fix in-place. Move to Phase 3.

### 2.3: TCC/Privacy Errors

**Symptom:** `ls` in `~/Downloads` fails with `Operation not permitted`.

**Likely cause:** macOS privacy framework (TCC), not file permissions.

**Plan:** Grant permissions as needed (see Phase 3). Defer proactive grants.

---

## Phase 3: Rebuild Shell & Development Environment

### 3.1: Fix Login Shell

```bash
# 1. Verify Homebrew is installed (already on M-series macs from migration)
which brew

# 2. Install native ARM bash
brew install bash

# 3. Register with system
grep /opt/homebrew/bin/bash /etc/shells || echo /opt/homebrew/bin/bash | sudo tee -a /etc/shells

# 4. Change login shell
chsh -s /opt/homebrew/bin/bash

# 5. Close and reopen Terminal to verify
echo $SHELL  # Should show /opt/homebrew/bin/bash
```

### 3.2: Inventory Intel Artifacts (Non-Destructive)

```bash
# Check for Intel-specific paths
echo "=== Checking for x86_64 artifacts ===" && \
[ -d /opt/local ] && echo "✗ MacPorts tree found (/opt/local)" || echo "✓ No MacPorts" && \
[ -d /opt/X11 ] && echo "✗ X11 legacy found (/opt/X11)" || echo "✓ No X11" && \
[ -f ~/.local/bin/uv ] && file ~/.local/bin/uv || echo "✓ No old uv binary"
```

**Reference:** See `x86_64-remediation.md` in project-michael-air for detailed findings and cleanup steps.

### 3.3: Remove Intel Homebrew & Build ARM Native

```bash
# 1. Remove old Intel tree (safe; ARM Homebrew is independent)
sudo rm -rf /usr/local/Homebrew /usr/local/Cellar /usr/local/Caskroom

# 2. Remove X11 if present
[ -d /opt/X11 ] && sudo rm -rf /opt/X11

# 3. Remove MacPorts if present
[ -d /opt/local ] && sudo rm -rf /opt/local

# 4. Reinstall desired packages via ARM Homebrew
# Use Brewfile or manual installation; see portable-profile for examples
brew install <package-list>
```

### 3.4: Grant TCC Permissions (As Needed)

Permissions fail → fix when you encounter them. Proactive grants are low-ROI.

**Example:**

```bash
# If Terminal fails to access ~/Downloads:
# System Settings → Privacy & Security → Files & Folders
# Enable Terminal for "Downloads"
# Quit and reopen Terminal
```

---

## Phase 4: Setup Checklist

### High Priority (Blocks Development)

- [ ] Shell & Homebrew working (Phase 3.1-3.3)
- [ ] Daylite or other critical apps verified
- [ ] Intel artifacts inventoried and removed
- [ ] PATH cleaned (no stale /usr/local or /opt/local entries)

### Medium Priority (Functionality)

- [ ] TCC permissions granted as needed
- [ ] Unknown accounts investigated (keep or delete)
- [ ] 1Password and other auth tools set up

### Low Priority (Cleanup)

- [ ] Disk space audited (account for 20-50GB unaccounted data)
- [ ] Old caches and logs cleaned
- [ ] Time Machine exclusions finalized (Phase 5)

---

## Phase 5: Time Machine Configuration

### 5.1: Identify Contamination Risk

**Before first backup**, check if previous backup was misconfigured:

```bash
# Check for IncludeByPath (legacy setting that forces system files to backup)
defaults read /Library/Preferences/com.apple.TimeMachine | grep IncludeByPath
# If present: System files may have been backed up unnecessarily
```

If contaminated, proceed to **Phase 5.2**.

### 5.2: Clean Configuration (Before First Backup)

```bash
# 1. Stop any running backup
tmutil stopbackup

# 2. Delete IncludeByPath if present (forces system files to backup)
sudo defaults delete /Library/Preferences/com.apple.TimeMachine IncludeByPath

# 3. Set destination via CLI (or System Settings GUI)
tmutil setdestination smb://tm-<hostname>@192.168.8.129/Backups-TM-<Hostname>

# 4. Add exclusions (GUI or CLI)
# Via GUI: System Settings → General → Time Machine → Options
# Add: ~/Downloads, ~/Pictures, ~/repos, ~/.cache (or customize)

# Via CLI (for system paths):
tmutil addexclusion -p /opt/homebrew  # persistent
```

### 5.3: Validate First Backup

After first backup completes:

```bash
# Get latest snapshot
LATEST=$(tmutil latestbackup)

# Verify size & contents (should be ~50-100 GB user data, NOT system files)
du -sh "$LATEST"

# Check for contamination
du -sh "$LATEST/System" 2>/dev/null && echo "❌ CONTAMINATED" || echo "✓ OK"
du -sh "$LATEST/Applications" 2>/dev/null && echo "❌ CONTAMINATED" || echo "✓ OK"
du -sh "$LATEST/opt" 2>/dev/null && echo "❌ CONTAMINATED" || echo "✓ OK"
```

**If contaminated:** Delete snapshot and redo Phase 5.2.

---

## Phase 6: Finalize & Validate

- [ ] Shell & development environment stable (1-2 weeks)
- [ ] Time Machine hourly backups running automatically
- [ ] First backup validated (user data only)
- [ ] All necessary TCC permissions granted
- [ ] Disk space accounted for (no surprise bloat)

---

## Common Issues & Fixes

### "Bad CPU type in executable" for any command

**Cause:** Command is x86_64 binary.

**Fix:**

1. Identify which path has the binary: `which <command>`
2. Check architecture: `file <path>`
3. If x86_64:
   - If Homebrew tool: `brew reinstall <package>`
   - If custom: locate and remove
4. Verify fix: `which <command>` → should be `/opt/homebrew/bin/` or system path

### Terminal fails to start shell

**Cause:** Login shell is x86_64 binary.

**Fix:**

```bash
chsh -s /bin/zsh  # immediate
chsh -s /opt/homebrew/bin/bash  # permanent (after brew install bash)
```

### Time Machine backup includes system files (100+ GB)

**Cause:** IncludeByPath is active (legacy setting).

**Fix:**

```bash
# Stop backup
tmutil stopbackup

# Delete IncludeByPath
sudo defaults delete /Library/Preferences/com.apple.TimeMachine IncludeByPath

# Add exclusions for system paths
tmutil addexclusion /System /usr /Library /bin /sbin /private /Developer /Applications

# Delete contaminated snapshots (or start fresh)
# Restart backup
tmutil startbackup
```

---

## Reference Documents

For detailed findings and decisions from michael-air setup:

- **[setup.md](setup.md)** -- Migration issues encountered and fixes applied
- **[x86_64-remediation.md](x86_64-remediation.md)** -- Intel binary audit & removal strategy
- **[PLAN-names-networks-backups.md](PLAN-names-networks-backups.md)** -- NAS + Time Machine setup flow
- **[tm-reference.md](tm-reference.md)** -- Time Machine decision rationale and commands

---

## Next Machine (wendy-air, etc.)

When setting up the next machine:

1. Follow this template in order
2. Reference michael-air **[setup.md](setup.md)** for specific issues you encounter
3. Update this template if you discover new issues or better approaches
4. Commit changes back to the repo so future machines benefit
