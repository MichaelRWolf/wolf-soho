# Time Machine Backup Analysis: `/Library` and `/private`

**Date:** 2026-08-17  
**Status:** Deciding whether to include `/Library` and `/private` in first backup

---

## `/Library` — System-Level Library (15GB+)

### Contents Breakdown

| Directory | Size | Valuable? | Regenerable? |
|-----------|------|-----------|--------------|
| Frameworks | 4.0GB | NO | YES (OS recovery) |
| Application Support | 7.4GB | MIXED | MIXED (third-party app state) |
| Developer | 2.0GB | NO | YES (reinstall Xcode) |
| Fonts | 115MB | **YES** | NO (custom user fonts) |
| Logs | 155MB | NO | YES (regenerated on use) |
| PreferencePanes | 78MB | NO | YES (reinstall extensions) |
| Printers | 278MB | NO | YES (re-add printers) |
| Java | 297MB | NO | YES (reinstall JRE) |
| Keychains | 3.4MB | **YES** | NO (system passwords — takes days to recover) |
| Preferences | 2.5MB | **YES** | MAYBE (system settings worth keeping) |

### PRO: Include `/Library`

- **Keychains (3.4MB)** — System-level passwords, certificates, keys. **CRITICAL** — losing these requires:
  - Re-entering passwords for every system service
  - Re-authenticating network shares, cloud services
  - Potential loss of certificate chains (days of recovery work)
- **Fonts (115MB)** — Custom/user-installed fonts don't reinstall automatically. Nice to have on restore.
- **Preferences (2.5MB)** — System settings like keyboard layouts, accessibility, print settings. Worth keeping.
- **Apple defaults to including it** — suggests it's worth backing up for restore convenience.

### CON: Include `/Library`

- **Frameworks (4.0GB)** — Part of macOS; should be restored via OS recovery, not TM
- **Most of Application Support (7.4GB)** — Contains third-party app state (caches, logs, temp data). Should be rebuilt by apps.
- **Developer (2.0GB)** — Xcode and IDE cache; completely regenerable via `xcode-select --install`
- **Logs, Printers, Java** — All regenerable; no user data value
- **Total cruft: ~14GB of OS/app infrastructure** that shouldn't live in user backup

### Recommendation

**INCLUDE `/Library`** — but only for Keychains, Fonts, Preferences. The 4.0GB Frameworks will be wasted but acceptable cost for preserving critical Keychains.

---

## `/private` — System Temporary & Variable Data (3.5GB)

### Contents Breakdown

| Directory | Size | Valuable? | Regenerable? |
|-----------|------|-----------|--------------|
| /var/log | ~1.5GB | NO | YES (regenerated) |
| /var/tmp | 224MB | NO | YES (temporary files) |
| /var/db | ~1.5GB | MAYBE | MOSTLY (system databases) |
| /etc | 11MB | NO | YES (system config, part of OS) |

### PRO: Include `/private`

- `/var/db` might contain user-specific system state (NFS mounts, DHCP leases, etc.)
- Small size (3.5GB) doesn't significantly bloat backup
- Apple includes it by default (suggests some value)

### CON: Include `/private`

- **Logs (1.5GB)** — Completely regenerable; useless after restore
- **Temporary files (224MB)** — By definition temporary; should not be backed up
- **System config (/etc)** — Part of OS; should come from recovery
- **/var/db databases** — Most are ephemeral (DHCP, DNS cache, etc.); won't work on fresh restore anyway
- **3.5GB is pure cruft** — No user data, all regenerable

### Recommendation

**EXCLUDE `/private`** — Nothing valuable here. All regenerable, all temporary/system-level.

---

## Backup Size Calculation

### Measured Data (Current michael-air)

**Total user-focused backup (home + ~/Library):**
- Home directory (excluding clouds/repos/caches): ~30-40GB
- ~/Library (excluding Containers/Application Support/Caches): ~10-15GB
- **Subtotal: 40-55GB**

**Adding system paths:**
- `/Library`: 15GB
- `/private`: 3.5GB
- **System paths total: 18.5GB**

### Three Scenarios

| Scenario | Size | Notes |
|----------|------|-------|
| **Scenario A: User-only (recommended)** | **50-60GB** | Home + ~/Library (smart exclusions) |
| **Scenario B: + /Library (compromise)** | **65-75GB** | User data + System Keychains/Fonts (acceptable for critical data) |
| **Scenario C: + /Library + /private (wasteful)** | **70-80GB** | User + all system paths (unnecessary cruft) |

### Bloat Analysis

| Path | Size | % of Total (Scenario A) | Worth It? |
|------|------|------------------------|-----------|
| `/Library` alone | 15GB | 25-30% bloat | MAYBE (Keychains are critical) |
| `/private` alone | 3.5GB | 6-7% bloat | NO (all regenerable) |
| Both | 18.5GB | 31-37% bloat | NO (too much cruft for Keychains only) |

**Optimal:** Include `/Library` (for Keychains + Fonts), **EXCLUDE `/private`** → **65-75GB first backup**

---

## Decision Required

**Current State:**
- Both `/Library` and `/private` show `[Included]` (Apple defaults)
- No explicit exclusions have been added yet

**Options:**

1. **Keep both [Included]** (70-80GB) — Simple, matches Apple defaults, but 18.5GB wasted
2. **Include `/Library`, exclude `/private`** (65-75GB) — Balanced: keep critical Keychains, drop temp files
3. **Exclude both** (50-60GB) — Smallest, but lose Keychains (days of recovery work)

**Recommendation:** **Option 2 — Include `/Library`, Exclude `/private`**

```bash
# Execute this:
sudo tmutil addexclusion /private
# DO NOT add /Library to exclusions (keep it [Included])
```

---

## Why This Is Frustrating

The current situation reflects Apple's "safe by default" philosophy:
- Include more than necessary (Keychains are critical, so include all of `/Library`)
- Trust users to exclude cruft manually
- No built-in way to say "backup Keychains + Fonts, skip Frameworks + Logs"

Better approach would be: **Per-directory inclusion levels** in Time Machine settings, but Apple doesn't provide that.

**Result:** Users must cherry-pick (`tmutil addexclusion` each directory separately) to avoid backing up 30-40% bloat.

---

## Next Steps (New Session)

- [ ] Add `/private` to exclusions: `sudo tmutil addexclusion /private`
- [ ] Verify `/private` shows `[Excluded]`, `/Library` shows `[Included]`
- [ ] Start fresh backup: `tmutil startbackup`
- [ ] Monitor first backup size (should be 65-75GB)
- [ ] Measure actual bloat vs estimate
