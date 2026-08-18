# Time Machine: Configuration & Reference

**Purpose:** Quick reference for Time Machine setup, exclusions, and troubleshooting.

**Status:** Decisions finalized (2026-08-17); implementation ongoing.

**Related:** [tm-strategy.md](tm-strategy.md) (decision framework), [PLAN-names-networks-backups.md](PLAN-names-networks-backups.md) (full setup), [TEMPLATE-macbook-air-setup.md](TEMPLATE-macbook-air-setup.md) (generic setup flow).

---

## Quick Setup Checklist

```bash
# 1. Configure destination (NAS share)
tmutil setdestination smb://tm-<hostname>@192.168.8.129/Backups-TM-<Hostname>

# 2. Set exclusions via System Settings GUI
#    → General → Time Machine → Options
#    Add: ~/Downloads, ~/Pictures, ~/repos, ~/.cache

# 3. Set system path exclusions via CLI (optional but recommended)
tmutil addexclusion -p /opt/homebrew        # Persistent

# 4. Verify no IncludeByPath (legacy contamination risk)
defaults read /Library/Preferences/com.apple.TimeMachine | grep IncludeByPath
# If found: sudo defaults delete ... IncludeByPath

# 5. Start backup
tmutil startbackup

# 6. Monitor
tmutil status
```

---

## Final Exclusion Decisions (michael-air, 2026-08-17)

### User Directories (Excluded via GUI)

| Path          | Size      | Rationale                                                       |
|---------------|-----------|-----------------------------------------------------------------|
| `~/Downloads` | Ephemeral | Cleared regularly; no data loss risk                            |
| `~/Pictures`  | ~15-20 GB | Stored on NAS separately; redundant backup                      |
| `~/repos`     | ~30-50 GB | GitHub-based; can be re-cloned (high file count = slow restore) |
| `~/.cache`    | ~5-10 GB  | Application caches; rebuilt on first launch                     |

### System Paths (Excluded via CLI)

| Path            | Rationale                                        |
|-----------------|--------------------------------------------------|
| `/opt/homebrew` | Package manager binaries; regenerable            |
| `/private`      | System logs, temps; ephemeral                    |
| `/System`       | System files; already mostly excluded by default |

### Paths to KEEP (in Backup)

| Path                       | Rationale                                                  |
|----------------------------|------------------------------------------------------------|
| `~/Library`                | Contains preferences, app data, credentials; irreplaceable |
| `~/Documents`, `~/Desktop` | Important user data                                        |

---

## Time Machine Commands Reference

### Status & Monitoring

```bash
# Current status
tmutil status

# List all backups
tmutil listbackups

# Get latest backup path
tmutil latestbackup

# Check if specific path is excluded
tmutil isexcluded ~/Downloads

# Show destination info
tmutil destinationinfo
```

### Configuration

```bash
# Set backup destination
tmutil setdestination smb://user@host/share

# Add exclusion (temporary, resets if TM reconfigured)
tmutil addexclusion /path

# Add persistent exclusion (survives TM reconfiguration)
tmutil addexclusion -p /path

# Remove exclusion
tmutil removeexclusion /path

# View plist configuration
defaults read /Library/Preferences/com.apple.TimeMachine
```

### Control

```bash
# Start backup
tmutil startbackup

# Stop backup
tmutil stopbackup

# Disable Time Machine entirely
sudo tmutil disable

# Enable Time Machine
sudo tmutil enable

# Delete specific backup (if supported by macOS version)
tmutil delete <backup-path>
```

### Audit via xattr (Apple's Native Markers)

```bash
# Mark path as excluded (via xattr)
xattr -w com.apple.metadata:com_apple_backup_excludeItem "bplist00_com.apple.backupd" <path>

# Remove exclusion via xattr
xattr -d com.apple.metadata:com_apple_backup_excludeItem <path>

# Check if path has exclusion attribute
xattr -p com.apple.metadata:com_apple_backup_excludeItem <path>
```

---

## Troubleshooting

### TM Backup Includes System Files (100+ GB)

**Symptom:** First backup is 150+ GB instead of expected 50-100 GB.

**Cause:** `IncludeByPath` is active (legacy setting from previous machine).

**Fix:**

```bash
# 1. Stop backup
tmutil stopbackup

# 2. Remove problematic setting
sudo defaults delete /Library/Preferences/com.apple.TimeMachine IncludeByPath

# 3. Add explicit system path exclusions
sudo tmutil addexclusion /Library /System /bin /sbin /usr /private /Developer /Applications

# 4. Verify all paths now show [Excluded]
for path in /Library /System /bin /sbin /usr /private /Developer /Applications; do
  tmutil isexcluded "$path"
done

# 5. Delete contaminated snapshot(s) and restart
rm -rf /Volumes/com.apple.TimeMachine.localsnapshots/Backups.backupdb/<hostname>/*
tmutil startbackup
```

### "Authentication failed" during backup

**Cause:** Keychain entry missing or credentials incorrect.

**Fix:**

```bash
# Check Keychain entry
security find-internet-password -s "wolfden_NAS._smb._tcp.local." /Library/Keychains/System.keychain

# Re-add if missing
security add-internet-password \
  -a "tm-<hostname>" \
  -s "wolfden_NAS._smb._tcp.local." \
  -p "PASSWORD_FROM_1P" \
  -l "WolfDen NAS - Time Machine (<hostname>)" \
  -t smb \
  -w \
  /Library/Keychains/System.keychain
```

### Backup Never Completes

**Cause:** Large initial backup hitting network timeouts (WiFi latency).

**Fix:**

```bash
# Interrupt and retry iteratively
tmutil stopbackup
sleep 10
tmutil startbackup

# Or: use wired Ethernet for first backup
# USB-C Ethernet dongle recommended; see troubleshooting in PLAN
```

### "No route to host" when connecting to NAS

**Cause:** Network unreachable or NAS down.

**Fix:**

```bash
# Verify network connectivity
ping 192.168.8.129
ping wolfden-nas.local

# Check NAS is up
tmutil destinationinfo  # Should show NAS share info

# If none work: check WiFi connection, NAS status, network routing
```

---

## Key Insights (Lessons from michael-air)

1. **IncludeByPath is dangerous** -- It forces system files to be backed up. Always check for and delete it on fresh restore.

2. **File count matters as much as GB** -- A 2 GB cache with 250K files takes longer to restore than a 50 GB archive with 100 files.

3. **System paths must be excluded explicitly** -- GUI exclusions don't cover `/System`, `/usr`, `/Library`, etc. Use CLI `tmutil addexclusion` for system paths.

4. **Backup destination naming** -- Use semantic names that include hostname (e.g., `Backups-TM-Michael-Air`). Makes future audits easier.

5. **Validate after first backup** -- Always inspect snapshot contents to confirm system files are excluded.

6. **WiFi is slow for large initial backups** -- Consider wired Ethernet for first backup of 50+ GB.

---

## NAS Service Account Setup (Reference)

For new machine backups, create corresponding NAS account and share:

```bash
# 1. SSH to NAS
ssh admin@192.168.8.129

# 2. Create service account
sudo synouser --add tm-<hostname> PASSWORD "TM Backup <hostname>" 0

# 3. Create share directory
sudo mkdir -p /volume1/Backups-TM-<Hostname>
sudo chown tm-<hostname>:tm-<hostname> /volume1/Backups-TM-<Hostname>
sudo chmod 750 /volume1/Backups-TM-<Hostname>

# 4. Store credentials in 1Password
# Entry: "NAS - TM - tm-<hostname>"
# Fields: username, password, website (https://192.168.8.129:5001), tags (NAS, wolfden, backup)

# 5. Add to macOS Keychain (see PLAN-names-networks-backups.md Phase 3)
```

---

## Monitoring Script

Use included `tmutil_analysis` script to check:

- Backup status (running, idle, error)
- Destination info (name, URL, ID)
- Configured exclusions (via SkipPaths + tmutil)
- Apple auto-exclusions (via xattr markers)
- Recent backup attempts (with RESULT codes)

```bash
./tmutil_analysis
```

---

## Post-Implementation Tasks

- [ ] Monitor hourly backups run automatically (1-2 weeks)
- [ ] Verify first snapshot contains only user data (no system files)
- [ ] Check TM logs for errors: `log stream --predicate 'process == "backupd"'`
- [ ] After 2-4 weeks of stable backups: decide on legacy backup share (delete or archive)
- [ ] Update this document with any new issues discovered

---

## Related Documentation

- [PLAN-names-networks-backups.md](PLAN-names-networks-backups.md) -- Full setup including NAS account creation
- [tm-strategy.md](tm-strategy.md) -- Decision framework for what to backup
- [setup.md](setup.md) -- Migration issues and TM-related findings
- [x86_64-remediation.md](x86_64-remediation.md) -- Excluding old Intel artifacts
