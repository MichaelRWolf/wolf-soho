# Plan: Names, Networks, Backups (Hostname + NAS + TM Setup)

**Date:** 2026-08-16  
**Status:** Execution phase (Phases 1-4 complete; Phase 5 configured; Phase 6 ready to start)  
**Scope:** Machine naming, NAS service account creation, Time Machine configuration, Keychain/SMB authentication

---

## Execution Status (2026-08-16)

### ✓ COMPLETED

**Phase 1: NAS Configuration**
- ✓ NAS service account created: `tm-michael-air` (password stored in 1Password)
- ✓ NAS share created: `Backups-TM-Michael-Air` (1.98 TB available)
- ✓ SMB credentials tested and mounted successfully
- ✓ Keychain entry added: `wolfden_NAS._smb._tcp.local.` (Account: `tm-michael-air`)

**Phase 2: 1Password Entry**
- ✓ Entry created: "NAS - TM - tm-michael-air" (Shared-Wolf Den vault)
- ✓ Fields: username, password, website, tags (NAS, wolfden, backup)

**Phase 3: Keychain & SMB**
- ✓ System Keychain entry added (auto-populated during SMB mount)
- ✓ Unattended SMB access verified

**Phase 4: Machine Naming**
- ✓ Hostname changed: `michael-pro` → `michael-air`
- ✓ Verified: `scutil --get ComputerName` shows `michael-air`

**Phase 5: Time Machine Configuration**
- ✓ TM destination set: `Backups-TM-Michael-Air – 192.168.8.129`
- ✓ Encryption: Disabled (intentional per security model)
- ✓ Backup frequency: Automatically Every Hour
- ✓ Back up on battery power: OFF (AC power only)
- ✓ Exclusion list verified and cleaned (see below)

### ✓ DECIDED

**Naming & Identity**
- Service account: `tm-michael-air` (per Identity Strategy)
- NAS share: `Backups-TM-Michael-Air` (semantic, machine-specific)
- Legacy backup: `Backups-TM-Michael` PRESERVED (not deleted; fallback for first 2-4 weeks)

**Time Machine Scope**
- User-focused backup (no system files)
- Exclude: /Applications, /Library, /private, /System, /usr, /usr/local, /Developer
- Exclude: ~/repos, ~/Downloads, ~/Pictures, ~/.npm, ~/.gem, ~/.cpan, ~/.cache
- Exclude: ~/Library/Application Support, ~/Library/Containers, ~/Library/Group Containers, ~/Library/CloudStorage
- Exclude: /opt/homebrew/bin, /opt/homebrew/opt, ~/.cargo, ~/go, ~/Library/Developer/Xcode

**Network**
- Use WiFi for now (WiFi → EAP → CG mesh for internet; WiFi → Beryl → NAS for local access)
- Note: USB-C Ethernet dongle not recognized by macOS (will troubleshoot later for large backups)

**Audit Findings**
- x86_64 binaries identified but minimal impact (Python venvs, gcloud SDK, Emacs modules)
- IncludeByPath field exists but appears unused in Sequoia 15.3.1 (legacy)
- /usr/local is empty (old Intel Homebrew already cleaned)

### ⚠️⚠️⚠️ CRITICAL BLOCKER — RESOLVED (2026-08-17)

**IncludeByPath IS ACTIVE — Forces System Files to Backup**

**Findings (2026-08-16 research):**
- IncludeByPath contains: `/Applications`, `/Developer`, `/Library`, `/System`, `/bin`, `/private`, `/sbin`, `/usr`
- Test result: `/Library` shows `[Included]` (confirmed IncludeByPath OVERRIDES natural exclusions)
- Impact: First backup WOULD include 150-200GB+ of system files:
  - `/System`: 675GB (catastrophic)
  - `/Library`: 16GB (system files, not user data)
  - `/private`: 3.8GB (system logs, temps)
  - Plus `/bin`, `/sbin`, `/usr`, `/Developer`, `/Applications`
- Behavior: IncludeByPath takes precedence over defaults; must be DELETED to prevent inclusion

**Fix (Execute before Phase 6):**

```bash
# 1. Delete IncludeByPath entirely
sudo defaults delete /Library/Preferences/com.apple.TimeMachine IncludeByPath

# 2. Add explicit exclusions for all paths that were in IncludeByPath
sudo tmutil addexclusion /Library
sudo tmutil addexclusion /System
sudo tmutil addexclusion /bin
sudo tmutil addexclusion /sbin
sudo tmutil addexclusion /usr
sudo tmutil addexclusion /private
sudo tmutil addexclusion /Developer
sudo tmutil addexclusion /Applications

# 3. Verify ALL paths now show [Excluded]
for path in /Library /System /bin /sbin /usr /private /Developer /Applications; do
  tmutil isexcluded "$path"
done
# Expected: ALL should show [Excluded]
```

**Rationale:** IncludeByPath is a legacy setting from the old michael-pro backup (5-year history). In modern TM, it forces unnecessary system files to be backed up. Deleting it ensures only user data is backed up (estimated 50-60GB, not 150-200GB+).

---

### ⚠️⚠️⚠️ CRITICAL: BACKUPS ARE CONTAMINATED (2026-08-17 AUDIT CONFIRMED)

**STATUS (2026-08-17):** CONTAMINATION CONFIRMED by inspecting snapshot contents.

**Audit Method:** Mounted and inspected actual snapshot contents at `/Volumes/com.apple.TimeMachine.localsnapshots/Backups.backupdb/michael-air/2026-08-16-121217/Macintosh HD - Data/`

**Contamination Evidence (per snapshot):**

| Directory | Size | Should Backup? | Status |
|-----------|------|---|---|
| Users/michael | 85GB | ✓ YES | Good (user data) |
| System | 9.8GB | ✗ NO | **CONTAMINATED** |
| Library | 16GB | PARTIAL | **CONTAMINATED** (system portion) |
| opt | 9.3GB | ✗ NO | **CONTAMINATED** (Homebrew/tools) |
| private | 4.0GB | ✗ NO | **CONTAMINATED** (logs/temps) |
| Applications | 27GB | ✗ NO | **CONTAMINATED** (app binaries) |
| usr | 3.1MB | ✗ NO | Minor |
| **Total per snapshot** | **157GB** | Should be ~85GB | **72GB system cruft** |

**Root Cause:** Backups started BEFORE IncludeByPath was deleted, and BEFORE exclusions were added. Default Apple behavior includes system paths.

**Scale of Problem:**
- 3 snapshots × 157GB = 470GB total
- User data: 255GB (useful)
- System cruft: 216GB (wasted, persists forever)
- **Bloat factor: 72% of each snapshot is system files**

**NAS Status:**
- Transfer in progress (1.8TB accumulated)
- Unknown if all 3 local snapshots transferred yet (need to verify)
- Legacy michael-pro: 436GB (preserved, inaccessible)

**REMEDIATION (Must execute in next session):**

**Phase 1: STOP and DELETE contaminated backups**
```bash
# 1. Stop running backup
tmutil stopbackup

# 2. Delete local snapshots (all 3 are contaminated)
rm -rf /Volumes/com.apple.TimeMachine.localsnapshots/Backups.backupdb/michael-air/*

# 3. Delete NAS backup share (to be recreated clean)
# Option A: Via SSH to NAS
ssh admin@192.168.8.129 "rm -rf /volume1/Backups-TM-Michael-Air"
# Option B: Via Finder/SMB (mount and delete manually)
```

**BEFORE DELETING: Verify NAS Transfer Status**

To check if snapshots have been transferred from Mac to NAS:

```bash
# List dates in local snapshots
ls /Volumes/com.apple.TimeMachine.localsnapshots/Backups.backupdb/michael-air/

# Check NAS for matching snapshot dates
# (Need to mount and inspect NAS Backups.backupdb/michael-air/)
# If NAS has matching dates → snapshots already transferred → safe to delete
# If NAS has NO dates → nothing transferred yet → deleting = losing data
```

**To inspect snapshot contents (read-only, safe):**

```bash
# Browse latest snapshot
SNAP="/Volumes/com.apple.TimeMachine.localsnapshots/Backups.backupdb/michael-air/2026-08-16-132023/Macintosh HD - Data"

# List top-level directories
ls -la "$SNAP"

# Check for system contamination
du -sh "$SNAP"/{System,Library,private,opt,usr,Applications,Users}
```

**Decision Matrix:**

| Scenario | Action | Risk |
|----------|--------|------|
| Snapshots transferred to NAS | Delete local snapshots | None (NAS has backup) |
| Snapshots NOT transferred to NAS | Delete local snapshots | Data loss (72GB system files lost, but that's the point) |
| Keep both local + NAS | None | 72% bloat persists forever in NAS |

**Recommendation:** Verify NAS transfer, then delete local snapshots (even system bloat is better handled by deleting than by keeping permanently).

---

**Phase 2: FIX exclusion configuration**

**THEN FIX IncludeByPath (DO NOT RESUME BACKUP):**
```bash
# 1. Delete IncludeByPath
sudo defaults delete /Library/Preferences/com.apple.TimeMachine IncludeByPath

# 2. Add explicit exclusions
sudo tmutil addexclusion /Library /System /bin /sbin /usr /private /Developer /Applications

# 3. Verify all show [Excluded]
for path in /Library /System /bin /sbin /usr /private /Developer /Applications; do
  tmutil isexcluded "$path"
done
```

---

### ⏳ AUDIT: Inspect What's Already in Backup (Aug 13-17)

**Before resuming backup, inspect what's in the existing snapshot:**

**1. List backup snapshots:**
```bash
tmutil listbackups
# Shows all snapshots. Note the dates.
```

**2. Mount the latest backup snapshot (read-only):**
```bash
# Get path to latest snapshot
LATEST=$(tmutil latestbackup)
echo "Latest backup: $LATEST"

# Browse it (read-only, safe)
ls -la "$LATEST/Volumes/Backups-TM-Michael-Air/Backups.backupdb/michael-air/"
```

**3. Check if contaminated (system files present):**
```bash
LATEST=$(tmutil latestbackup)
echo "=== Checking for contaminated system files in backup ===" && \
du -sh "$LATEST/System" 2>/dev/null && echo "CONTAMINATED: /System found" || echo "OK: /System not in backup" && \
du -sh "$LATEST/Library" 2>/dev/null && echo "CONTAMINATED: /Library found" || echo "OK: /Library not in backup" && \
du -sh "$LATEST/private" 2>/dev/null && echo "CONTAMINATED: /private found" || echo "OK: /private not in backup" && \
du -sh "$LATEST/Applications" 2>/dev/null && echo "CONTAMINATED: /Applications found" || echo "OK: /Applications not in backup"
```

**4. If CONTAMINATED (system files found):**
- Option A: Delete the backup snapshot and start fresh
  ```bash
  # Delete entire first backup
  rm -rf /Volumes/Backups-TM-Michael-Air/Backups.backupdb/michael-air/*
  # OR unmount and delete via macOS UI
  ```
- Option B: Use `tmutil delete` to remove specific snapshot (if available in this macOS version)

**5. If CLEAN (no system files):**
- Resume backup with fixed exclusions: `tmutil startbackup`

---

### ⏳ Phase 6: Initial Backup (REVISED — Fix contamination first)

- [ ] STOP running backup: `tmutil stopbackup`
- [ ] DELETE IncludeByPath: `sudo defaults delete /Library/Preferences/com.apple.TimeMachine IncludeByPath`
- [ ] ADD exclusions: `sudo tmutil addexclusion /Library /System /bin /sbin /usr /private /Developer /Applications`
- [ ] AUDIT existing backup: Check if contaminated (see steps above)
- [ ] If contaminated: DELETE snapshot and start fresh
- [ ] If clean: RESUME backup: `tmutil startbackup`
- [ ] Monitor progress: `tmutil status`

**Post-Backup Monitoring**
- [ ] Verify first snapshot created: `tmutil latestbackup`
- [ ] Monitor TM logs for errors: `log stream --predicate 'process == "backupd"'`
- [ ] Confirm hourly backups run automatically without intervention
- [ ] After 1-2 weeks of stable backups: decide on legacy `Backups-TM-Michael` (keep vs. delete)

### ❓ UNCERTAIN / DEFERRED

**Ethernet Dongle**
- USB-C Ethernet dongle shows power/activity lights but macOS doesn't recognize it
- Impact: Initial backup will use WiFi (slower, ~6-12 hours for 50-60GB)
- Plan: Troubleshoot dongle later (driver, replug, different dongle)
- Recommendation: For future large backups, get working Ethernet for speed

**Old michael-pro Backup**
- Location: `Backups-TM-Michael` on NAS (436GB, 25 snapshots, Intel-based)
- Decision deferred: Keep as archive or delete after michael-air proves stable
- Rationale: Insurance against configuration mistakes; delete after 2-4 weeks of successful michael-air backups

**IncludeByPath Field**
- Status: Exists in plist (legacy from michael-pro setup)
- Behavior: Appears unused in Sequoia 15.3.1 (contradicts tmutil isexcluded)
- Decision: Monitor; delete if it interferes with TM behavior

---

---

## Strategy Reference

**Source:** 1Password "Identity Strategy - NAS + MB - Human+Service Accounts"  
**UUID:** `z264ew5xvmndlg5aliwmgl3cam`  
**Vault:** Shared-Wolf Den  
**Retrieve:** `op item get z264ew5xvmndlg5aliwmgl3cam`

**Key principles:**
- Human accounts (`michael`, `wendy`) consistent across Macs + NAS
- Service accounts (`tm-<hostname>`) machine-scoped, automated only
- Keychain stores network credentials for unattended backups

---

## Naming & Identity Decisions

| Component | Current | Target | Rationale |
|-----------|---------|--------|-----------|
| Machine ComputerName | `michael-pro` | `michael-air` | Matches hardware (M3 2024); SSI consistency |
| Machine LocalHostName | `michael-pro` | `michael-air` | Enables mDNS: `michael-air.local` |
| Human account | `michael` | `michael` | Already consistent (no change needed) |
| NAS TM service account | `tm-michael-pro` | `tm-michael-air` | Service account per Identity Strategy |
| NAS share name | `Backups-TM-Michael` | `Backups-TM-Michael-Air` | Semantic, machine-specific |
| 1Password vault entry | "NAS - TM - tm-michael-pro" | "NAS - TM - tm-michael-air" | Mirrors service account name |
| Keychain entry | `wolfden_NAS._smb._tcp.local.` (tm-michael-pro) | `wolfden_NAS._smb._tcp.local.` (tm-michael-air) | Updated for new credential |

---

## Phase 1: NAS Configuration

### Prerequisites

- SSH access to Synology NAS as admin user
- NAS IP: `192.168.8.129`
- NAS mDNS: `wolfden_NAS._smb._tcp.local.` or `wolfden-nas.local`

### 1.1: Create NAS Service Account (`tm-michael-air`)

**SSH to NAS:**
```bash
ssh admin@192.168.8.129
# Or: ssh admin@wolfden-nas.local
```

**Via Synology DSM web UI (easier):**
1. Open `https://192.168.8.129:5001`
2. Control Panel → User
3. Create → Local User
   - Username: `tm-michael-air`
   - Password: Generate strong password (will store in 1Password)
   - Privilege: Leave unchecked; grant permissions to specific folder only (next step)
   - Confirm create

**OR via CLI (if web UI unavailable):**
```bash
# Create user (replace PASSWORD with actual password)
sudo synouser --add tm-michael-air PASSWORD "TM Backup michael-air" 0

# Verify creation
sudo synouser --list
```

**Verify account was created:**
```bash
# From NAS terminal or via SSH
synouser --list | grep tm-michael-air
```

---

### 1.2: Create NAS Share (`Backups-TM-Michael-Air`)

**Via Synology DSM web UI:**
1. File Station → Home
2. Create → Folder → Name: `Backups-TM-Michael-Air`
3. Right-click → Properties → Permissions
   - Remove: `guest` (if present)
   - Add: `tm-michael-air` with "Read/Write" permission
   - Owner: Set to `tm-michael-air` if possible

**OR via CLI:**
```bash
# SSH to NAS
ssh admin@192.168.8.129

# Create share directory
sudo mkdir -p /volume1/Backups-TM-Michael-Air

# Set permissions (note: exact path/owner syntax varies by DSM version)
sudo chown tm-michael-air:tm-michael-air /volume1/Backups-TM-Michael-Air
sudo chmod 750 /volume1/Backups-TM-Michael-Air

# Verify
ls -ld /volume1/Backups-TM-Michael-Air
```

**Verify share is accessible:**
```bash
# From michael-air:
open smb://tm-michael-air@192.168.8.129/Backups-TM-Michael-Air
# Or: open smb://tm-michael-air@wolfden_NAS._smb._tcp.local./Backups-TM-Michael-Air
# Prompt for password; enter tm-michael-air password
```

---

### 1.3: Test SMB Access from michael-air

```bash
# Test mount (will prompt for password)
mount_smbfs -o nosetuserid //tm-michael-air@192.168.8.129/Backups-TM-Michael-Air /tmp/tm-test

# Check if mounted
mount | grep Backups-TM-Michael-Air

# Verify write access
touch /tmp/tm-test/test-file.txt && rm /tmp/tm-test/test-file.txt

# Unmount
umount /tmp/tm-test
```

---

## Phase 2: 1Password Entry Creation

### 2.1: Create 1P Entry via `op` CLI

**Prerequisites:**
- 1Password CLI signed in: `op signin` (if not already authenticated)
- Vault: "Shared-Wolf Den"

**Create the entry:**
```bash
# Option A: Interactive creation
op item create \
  --category "LOGIN" \
  --title "NAS - TM - tm-michael-air" \
  --vault "Shared-Wolf Den" \
  username="tm-michael-air" \
  password="YOUR_GENERATED_PASSWORD" \
  url="https://192.168.8.129:5001" \
  --tags "NAS,wolfden,backup" \
  'Name *'="tm-michael-air"
```

**Alternative: Copy from existing entry and edit**
```bash
# Get UUID of existing tm-michael-pro entry
op item list --vault "Shared-Wolf Den" --format json | jq '.[] | select(.title | contains("tm-michael-pro")) | .id'

# Copy it (note: `op item duplicate` not available in all versions; use web UI instead)
# Via web: 1Password web → Find "NAS - TM - tm-michael-pro" → ⋯ → Duplicate
# Then edit title/username/passwords in the duplicated entry
```

**Verify entry was created:**
```bash
op item get "NAS - TM - tm-michael-air" --vault "Shared-Wolf Den"
# Should show: username, password, website, tags
```

**Store password locally (macOS) for later reference:**
```bash
# Retrieve password from 1P and copy to clipboard
op item get "NAS - TM - tm-michael-air" --fields username,password --vault "Shared-Wolf Den" | pbcopy
```

---

## Phase 3: Keychain & SMB Authentication

### 3.1: Add Keychain Entry for Unattended Backups

Time Machine needs credentials stored in System Keychain to connect to NAS without user interaction.

**Option A: Manual (via Keychain Access)**
1. Open Keychain Access (Applications → Utilities → Keychain Access)
2. Click "Keychain" → "System Keychain" (left sidebar)
3. File → New Password Item
   - Keychain Item Name: `wolfden_NAS._smb._tcp.local.` (or `wolfden-nas.local`)
   - Account Name: `tm-michael-air`
   - Password: (paste from 1Password)
   - Add to Keychain: Confirm
4. Double-click the entry → "Access Control" tab
   - Allow: `Finder`, `System Events`, `/usr/libexec/authd`
   - Click "Modify…" if needed to add permissions
5. Close and verify entry appears in Keychain list

**Option B: Command-line (faster, scriptable)**
```bash
# Add credential to System keychain
security add-internet-password \
  -a "tm-michael-air" \
  -s "wolfden_NAS._smb._tcp.local." \
  -p "PASSWORD_FROM_1P" \
  -l "WolfDen NAS - Time Machine (michael-air)" \
  -t smb \
  -w \
  /Library/Keychains/System.keychain

# Verify it was added
security find-internet-password -s "wolfden_NAS._smb._tcp.local." -a "tm-michael-air" /Library/Keychains/System.keychain
```

### 3.2: Test Unattended SMB Connection

```bash
# Use the credential from keychain (no interactive prompt)
mount_smbfs -o nosetuserid,noowners //tm-michael-air@wolfden_NAS._smb._tcp.local./Backups-TM-Michael-Air /tmp/tm-test

# Check mount
mount | grep Backups-TM-Michael-Air

# Unmount
umount /tmp/tm-test
```

If this succeeds without prompting for password, the Keychain entry is correctly configured for TM.

---

## Phase 4: Machine Naming (Hostname Change)

### Prerequisites
- Have SSH access ready (if needed for troubleshooting)
- Document current hostname: `michael-pro`
- Target hostname: `michael-air`

### 4.1: Change ComputerName, LocalHostName, and HostName

```bash
# Current state
scutil --get ComputerName
scutil --get LocalHostName
scutil --get HostName

# Change to michael-air (requires sudo)
sudo scutil --set ComputerName "michael-air"
sudo scutil --set LocalHostName "michael-air"
sudo scutil --set HostName "michael-air"

# Verify changes
scutil --get ComputerName
scutil --get LocalHostName
scutil --get HostName

# You may need to restart for full effect, or just restart System Preferences
# Logout/login cycle is sufficient for most services
```

### 4.2: Verify Hostname Change

```bash
# Check Bonjour discovery
hostname
hostname -s
hostname -f

# Verify mDNS (should resolve to michael-air.local)
ping michael-air.local

# Verify SMB Bonjour mDNS name
dns-sd -R "michael-air" _smb._tcp local 445 &
```

### 4.3: Update NAS/Bonjour Records (if applicable)

If the NAS has cached hostname information for this machine, you may want to:
1. Restart NAS: `sudo shutdown -r now` (from NAS SSH)
2. Or manually clear cache on NAS (varies by DSM version)

In practice, Bonjour auto-discovery should pick up the new name within minutes.

---

## Phase 5: Time Machine Configuration

### 5.1: Verify TM is Not Running

```bash
tmutil status
# Should show: Running = 0
```

### 5.2: Remove Old Backup Destination (Optional)

```bash
# Check current destination
tmutil destinationinfo

# Remove old destination if present (do NOT delete NAS share itself)
sudo tmutil removeexclusion /Volumes/Backups-TM-Michael
# OR via System Settings → Time Machine → Remove disk
```

### 5.3: Configure New Destination

**Via System Settings (GUI):**
1. Open System Settings → General → Time Machine
2. Click "Turn Off" if currently on
3. Wait a moment, then click "Turn On"
4. Disk dialog appears; click "Add or Change Backup Disk"
5. Select "Other Network Disks…"
6. Enter: `smb://tm-michael-air@wolfden_NAS._smb._tcp.local./Backups-TM-Michael-Air`
7. Authenticate with `tm-michael-air` password (from 1Password)
8. Confirm selection

**Via Command Line:**
```bash
# Create a bookmark for the destination
tmutil setdestination smb://tm-michael-air@wolfden_NAS._smb._tcp.local./Backups-TM-Michael-Air
```

### 5.4: Verify Exclusions

```bash
# Check what's excluded (should NOT include /System, /usr, /bin, /sbin)
defaults read /Library/Preferences/com.apple.TimeMachine SkipPaths

# If IncludeByPath exists and includes system paths, remove it
sudo defaults delete /Library/Preferences/com.apple.TimeMachine IncludeByPath
```

---

## Phase 6: Initial Backup (Start, Interrupt, Resume)

### 6.1: Start Backup

```bash
# Kick off initial backup
tmutil startbackup

# Monitor progress
tmutil status
# Watch for: Percent increasing, Running = 1
```

### 6.2: Interrupt When Ready (e.g., Low Battery)

```bash
# Stop the backup
tmutil stopbackup

# Verify it stopped
tmutil status
# Should show: Running = 0
```

### 6.3: Resume When Power Stable

```bash
# Resume (does NOT restart from scratch; continues from last checkpoint)
tmutil startbackup
```

### 6.4: Verify First Snapshot Created

```bash
tmutil latestbackup
# Should show path like: /Volumes/Backups-TM-Michael-Air/Backups.backupdb/michael-air/2026-08-16-HHMMSS
```

---

## Execution Checklist

### Pre-Flight

- [ ] Have NAS admin credentials ready
- [ ] Have 1Password vault access (Shared-Wolf Den)
- [ ] Ethernet connection to NAS ready (USB-C dongle recommended)
- [ ] Power adapter connected to michael-air
- [ ] This document reviewed and understood

### NAS Configuration

- [ ] SSH to NAS and verify accessibility
- [ ] Create service account `tm-michael-air` (NAS)
- [ ] Create share `Backups-TM-Michael-Air` (NAS)
- [ ] Set permissions: `tm-michael-air` → full read/write on share
- [ ] Test SMB access from michael-air (manual mount)
- [ ] Password stored securely

### 1Password Entry

- [ ] Create 1P entry "NAS - TM - tm-michael-air" in Shared-Wolf Den
- [ ] Fields: username, password, website (https://192.168.8.129:5001), tags (NAS, wolfden, backup)
- [ ] Entry is accessible via `op item get`

### Keychain Setup

- [ ] Add System Keychain entry for `wolfden_NAS._smb._tcp.local.` / `tm-michael-air`
- [ ] Test unattended SMB mount (should not prompt for password)
- [ ] Verify Keychain entry allows Finder/System Events access

### Machine Configuration

- [ ] Change hostname: `michael-pro` → `michael-air`
- [ ] Verify hostname change with `scutil --get ComputerName`
- [ ] Verify `michael-air.local` is resolvable via ping

### Time Machine Setup

- [ ] Stop current TM if running
- [ ] Remove old destination (optional; preserves NAS share)
- [ ] Add new destination: `smb://tm-michael-air@wolfden_NAS._smb._tcp.local./Backups-TM-Michael-Air`
- [ ] Verify exclusions do NOT include system paths
- [ ] Verify TM is set to automatic backup ON

### Initial Backup

- [ ] Start backup: `tmutil startbackup`
- [ ] Monitor progress: `tmutil status` (watch Percent increase)
- [ ] Interrupt when needed: `tmutil stopbackup`
- [ ] Resume when power stable: `tmutil startbackup`
- [ ] Verify first snapshot created: `tmutil latestbackup`

---

## Post-Execution

- [ ] Monitor TM logs for errors: `log stream --predicate 'process == "backupd"'`
- [ ] Verify automatic hourly backups start without intervention
- [ ] After 1-2 weeks of stable backups, consider deleting legacy `Backups-TM-Michael` share (document decision)
- [ ] Update [tm-strategy.md](tm-strategy.md) with actual measurements

---

## Related Documentation

- [TM-SETUP-PLAN.md](TM-SETUP-PLAN.md) — Original Time Machine plan (superseded by this document)
- [tm-strategy.md](tm-strategy.md) — TM efficiency audit framework and measurements
- [setup.md](setup.md) — Migration process and Intel→ARM issues
- [equipment_computing.md](../wolf-soho/equipment_computing.md) — Machine specs, UUIDs, serials, MAC addresses
- 1Password Identity Strategy: `op://Shared-Wolf Den/z264ew5xvmndlg5aliwmgl3cam/`

---

## Troubleshooting

### "No route to host" when mounting NAS share

**Cause:** NAS not reachable (network disconnected, NAS down, wrong IP/hostname)

**Fix:**
```bash
# Verify network connection
ping 192.168.8.129
ping wolfden_NAS._smb._tcp.local.
# If both fail, check network / NAS status
```

### "Authentication failed" during TM backup

**Cause:** Keychain entry missing or password incorrect

**Fix:**
```bash
# Check Keychain entry exists and is correct
security find-internet-password -s "wolfden_NAS._smb._tcp.local." /Library/Keychains/System.keychain

# Re-add if missing
security add-internet-password -a "tm-michael-air" -s "wolfden_NAS._smb._tcp.local." -p "PASSWORD" /Library/Keychains/System.keychain
```

### TM keeps attempting to backup but never completes

**Cause:** Large initial backup hitting network timeouts; SMB round-trip latency

**Fix:**
```bash
# Interrupt and resume iteratively
tmutil stopbackup
sleep 10
tmutil startbackup

# Or: wired ethernet connection recommended for large initial backup
```

### Machine hostname not updating after `scutil` commands

**Cause:** Caching in System Preferences or Bonjour daemon

**Fix:**
```bash
# Restart mDNS/Bonjour daemon
sudo launchctl stop com.apple.mDNSResponder
sudo launchctl start com.apple.mDNSResponder

# Or full logout/login cycle
```

---

## References

- **Synology DSM CLI Reference:** https://kb.synology.com/en-us/DSM/tutorial/How_to_login_to_DSM_with_root_permission_by_using_SSH_Telnet
- **macOS `scutil` hostname:** `man scutil`
- **Keychain CLI:** `man security add-internet-password`
- **Time Machine CLI:** `man tmutil`
- **SMB/CIFS:** `man mount_smbfs`
