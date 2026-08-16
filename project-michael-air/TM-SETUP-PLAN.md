# Time Machine Setup Plan: michael-air

**Decision date:** 2026-08-16  
**Status:** Planning phase (awaiting NAS configuration)

---

## Strategy Reference

**Source:** 1Password item "Identity Strategy - NAS + MB - Human+Service Accounts"  
**1Password UUID:** `z264ew5xvmndlg5aliwmgl3cam`  
**Vault:** Shared-Wolf Den  
**Private link:** https://start.1password.com/open/i?a=3ZA4DCBZFRF2VKJQ2ORZMVLZAA&v=t736oydhzbj3cfci6w54zi5aju&i=z264ew5xvmndlg5aliwmgl3cam&h=my.1password.com

**Retrieve from CLI:**
```bash
op item get z264ew5xvmndlg5aliwmgl3cam --format json | pbcopy
# Or read directly:
op item get z264ew5xvmndlg5aliwmgl3cam
```

**Key principles from Identity Strategy:**
- Human accounts (`michael`, `wendy`) are consistent across all Macs + NAS (interactive + storage)
- Service accounts (`tm-<hostname>`) are machine-scoped, automated roles only
- Long-term ideal: `michael` everywhere, `tm-*` for backups only

---

## Naming Decisions

| Component | Value | Rationale |
|-----------|-------|-----------|
| **Machine hostname** | `michael-air` | Matches hardware; enables SSI-like behavior across fleet |
| **Human account** | `michael` | Already consistent across michael-pro, wolf-air, NAS |
| **TM service account** | `tm-michael-air` | Machine-scoped per Identity Strategy; distinct from human account |
| **NAS share (new)** | `Backups-TM-Michael-Air` | Clear semantic name; machine-specific; separate from legacy backup |
| **NAS share (legacy)** | `Backups-TM-Michael` | PRESERVED (do not delete); contains michael-pro backup (436GB, 25 snapshots, Intel) |
| **TM credential** | `smb://tm-michael-air@wolfden_NAS._smb._tcp.local./Backups-TM-Michael-Air` | Service account over Bonjour mDNS |

---

## Audit Findings

**Previous backup (michael-pro):**
- Location: `Backups-TM-Michael` on NAS
- Credential: `tm-michael-pro`
- Size: 436 GB
- Snapshots: 25 (April 2025 – Aug 13 2026)
- Hardware UUID: `3D9DF3C9-1B29-5FAA-A9E9-859D7316915A`
- Issues:
  - Full-system backup via `IncludeByPath` forcing `/System`, `/usr`, `/bin`, `/sbin` into backups (unnecessary)
  - Intel-only binaries (x86_64 Homebrew, compiled tools)
  - 5-year history from older MacBook (possibly bootstrapped)

**New backup (michael-air):**
- Location: `Backups-TM-Michael-Air` (to be created)
- Credential: `tm-michael-air` (to be created)
- Hardware UUID: `58ED3E12-7C1A-5473-BD8A-89246A584DCC`
- Scope: User-focused (home directory + preferences + keychains), no system files
- Expected size: ~50-60 GB (first backup)
- Expected duration: 6-12 hours (network TM over Bonjour)

---

## Setup Checklist

### Phase 1: NAS Configuration

**Prerequisites:**
- [ ] SSH access to Synology NAS (`wolfden-nas`)
- [ ] Admin credentials (or delegated share creation)

**Tasks:**
- [ ] Create NAS share: `Backups-TM-Michael-Air`
  - Permissions: Read/Write for `tm-michael-air` service account
  - Quota: At least 100 GB (for initial baseline + snapshots)
  
- [ ] Create NAS service account: `tm-michael-air`
  - Type: Service account (no interactive login)
  - Password: Store in 1Password under appropriate vault
  - Permissions: Full access to `Backups-TM-Michael-Air` only (principle of least privilege)

- [ ] Verify connectivity:
  ```bash
  # From michael-air:
  open smb://tm-michael-air@wolfden_NAS._smb._tcp.local./Backups-TM-Michael-Air
  # Should prompt for password; verify share is accessible
  ```

### Phase 2: Machine Preparation

**Prerequisites:**
- [ ] Ethernet connectivity to NAS (USB-C dongle + Gigabit recommended for first backup speed)

**Tasks:**
- [ ] Change machine hostname from `michael-pro` to `michael-air`
  - System Settings → General → About → Edit
  - Restart required

- [ ] Verify Time Machine is not currently running:
  ```bash
  tmutil status
  # Should show: Running = 0
  ```

### Phase 3: Time Machine Configuration

**Tasks:**
- [ ] Open System Settings → General → Time Machine

- [ ] Remove old backup destination:
  - Click the ⚙️ menu → "Change Backup Disk"
  - Deselect `Backups-TM-Michael`
  - Optional: Remove from list (but keep NAS share itself as archive)

- [ ] Add new backup destination:
  - Click "Add or Change Backup Disk"
  - Select "Other Network Disks..."
  - Enter: `smb://tm-michael-air@wolfden_NAS._smb._tcp.local./Backups-TM-Michael-Air`
  - Authenticate with `tm-michael-air` password

- [ ] Verify current exclusions:
  ```bash
  defaults read /Library/Preferences/com.apple.TimeMachine SkipPaths
  ```
  - Should NOT include: `/System`, `/usr`, `/bin`, `/sbin` (remove if present)
  - Should include: `/Applications`, `~/Library/Caches`, `~/Library/Developer`, `~/Library/Containers`, etc.

- [ ] Apply clean exclusion policy (if needed):
  ```bash
  # Remove problematic system-level inclusions
  sudo defaults delete /Library/Preferences/com.apple.TimeMachine IncludeByPath
  # This removes the override that forced /System, /usr, etc. to be backed up
  ```

### Phase 4: Initial Backup

**Prerequisites:**
- [ ] At least 2 hours of power + network connectivity
- [ ] No intensive disk activity (fresh machine, so this should be fine)

**Tasks:**
- [ ] Manually trigger initial backup:
  ```bash
  tmutil startbackup
  ```

- [ ] Monitor progress:
  ```bash
  tmutil status
  # Or: System Settings → General → Time Machine → "Back Up Now"
  ```

- [ ] After completion, verify first snapshot was created:
  ```bash
  tmutil latestbackup
  # Should show path like: /Volumes/Backups-TM-Michael-Air/Backups.backupdb/michael-air/2026-08-16-HHMMSS
  ```

---

## Post-Setup

- [ ] Schedule automatic backups (System Settings → Time Machine → Automatic backup ON)
- [ ] Configure backup interval (default: hourly; adjust if needed)
- [ ] Add exclusions as needed post-setup (e.g., large project directories, development caches)
- [ ] Monitor first week of backups for any issues
- [ ] Update [tm-strategy.md](tm-strategy.md) with measured data once initial backups complete

---

## Risk Mitigation

**Preserve legacy backup:** The `Backups-TM-Michael` share remains on NAS untouched. If fresh michael-air backup has issues, the old backup serves as fallback. Do not delete without explicit decision after confirming michael-air backups are stable (~2-4 weeks).

**Exclusion testing:** After configuring exclusions, run `prove TimeMachine/verify-tm-isexcluded` to validate that TM policy matches expectations.

---

## Related Documentation

- [tm-strategy.md](tm-strategy.md) — Time Machine efficiency audit framework and measurement data
- [equipment_computing.md](../wolf-soho/equipment_computing.md) — Machine specifications, UUIDs, serial numbers
- [michael-pro_water-damage.md](../wolf-soho/2026-06-18_michael-pro_water-damage.md) — Incident context
- [GitHub issue #8](https://github.com/MichaelRWolf/wolf-soho/issues/8) — Intel x86_64 binary audit (related, stays open)
