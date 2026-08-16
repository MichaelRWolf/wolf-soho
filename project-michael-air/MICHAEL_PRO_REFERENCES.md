# Complete Audit: 'michael-pro' References in wolf-soho & portable-profile

**Scan Date:** 2026-08-16  
**Status:** Reference audit (no changes made)  
**Purpose:** Understand scope of machine rename impact before NAS-dependent work

---

## Summary Statistics

- **wolf-soho:** 35+ mentions across 23 files
- **portable-profile:** 25+ mentions across 13 files
- **Total files affected:** 36 unique files
- **Pattern:** Mix of historical records, configuration conditionals, and examples

---

## Category 1: Machine Conditionals (Configuration — UPDATE WHEN NAS ACCESSIBLE)

Files that check hostname for machine-specific behavior. **Will not work correctly until michael-air name is active.**

### portable-profile/homebrew/Brewfile (Line 75)
```ruby
when "michael-pro", "wendy-pro", "michael-air"
  # Full Homebrew installation (formulae + casks)
```
**Status:** ✓ Already includes michael-air

### portable-profile/homebrew/README.md (Multiple lines)
```markdown
when "michael-pro", "michael-air", "wendy-pro"
```
**Status:** ✓ Already includes michael-air

### portable-profile/Makefile (Multiple sections)
- Line: `# Package | wolf-air (macOS 12) | michael-pro/wendy-pro/michael-air (macOS 13+)`
- Line: `# michael-pro/wendy-pro/michael-air use Brewfile (brew "rust")`
- Line: `# michael-pro/wendy-pro: Homebrew npm (via brew "node" in Brewfile)`

**Status:** ✓ References are current (michael-air already included)

### portable-profile/REQUIREMENTS_bash_prompt.md
```markdown
- **R12** -- Suppress host part when `hostname` == `michael-pro`
```
**Status:** ⚠️ May need review (check if michael-air should get same treatment)

---

## Category 2: Device Registry (MUST UPDATE)

Files that define canonical machine names. **Core to rename strategy.**

### wolf-soho/CONTEXT.md (Line 59)
```markdown
| `michael-pro`    | MacBook Pro (Michael's primary) |
```
**Status:** 🔴 MUST UPDATE
- Add michael-air entry with "(active)"
- Keep michael-pro with water damage note "(water damaged 2026-06-18; retired)"

### wolf-soho/equipment_computing.md (Line 3+)
```markdown
## `michael-pro` -- MacBook Pro (Michael's primary)
- Model: MacBook Pro 13-inch Late 2020 (A2251)
- Chip: Intel Core i5, Quad-Core, 2 GHz
...
```
**Status:** 🔴 MUST UPDATE
- Keep michael-pro section as-is (historical artifact)
- Add new section: `## \`michael-air\` -- MacBook Air (M3, 2024)`

### portable-profile/macports/README.md
```markdown
| **michael-pro** | Homebrew             | Homebrew         |
```
**Status:** 🟡 SHOULD UPDATE
- Add michael-air row; keep michael-pro as reference

---

## Category 3: Historical Incident Records (DO NOT TOUCH)

Files documenting water damage, recovery, or incidents. **Preserve as audit trail.**

### wolf-soho/2026-06-18_michael-pro_water-damage.md (Full document)
- 500+ lines documenting water damage incident, recovery procedure, teardown
- Multiple references to michael-pro throughout

**Status:** ✓ Keep as-is (historical artifact)

### wolf-soho/2026-08-03_wendy-pro_water-damage.md (Multiple lines)
```markdown
Based on michael-pro recovery (2026-06-18):
...
## Comparison to michael-pro
| Factor            | michael-pro (2026-06-18)       | wendy-pro (2026-08-03)
```
**Status:** ✓ Keep as-is (cross-references michael-pro incident for comparison)

### wolf-soho/michael-pro_battery.md
- Full maintenance record for michael-pro battery replacement project

**Status:** ✓ Keep as-is (historical maintenance record)

---

## Category 4: Project/Experiment Files (DO NOT TOUCH)

Files documenting specific projects, tests, or experiments. **Preserve results as-is.**

### wolf-soho/project_compare_network_responsiveness_(wolf-air_v_michael-pro).md
- Extensive network comparison experiment
- 40+ references to michael-pro throughout
- Data collection from 2025-2026 period

**Status:** ✓ Keep as-is (historical experiment results)

### wolf-soho/experiment_2025-12-27.md (Multiple lines)
```markdown
- michael-pro: pinging `192.168.8.1` and `1.1.1.1` at the same time
- Can ping michael-pro.
```
**Status:** ✓ Keep as-is (experiment log)

### wolf-soho/PROJECT_raccoon_ethernet_2026-05.md (Multiple lines)
```markdown
## CLI Quick Reference -- michael-pro Anker Adapter
michael-pro dongle → white cable → coupler → short black cable → spectrum-router
```
**Status:** ✓ Keep as-is (test procedure documentation)

---

## Category 5: Device Specs & Technical Reference (REVIEW & UPDATE AS NEEDED)

Files with technical details or device specifications. **Update for completeness, not blocking.**

### wolf-soho/equipment_portable.md
```markdown
- Interface: en7 on michael-pro
- Interface: en13 on michael-pro (when connected)
```
**Status:** 🟡 SHOULD UPDATE
- Add michael-air networking interfaces (if applicable)
- Keep michael-pro entries (historical reference)

### wolf-soho/power_consumption.md
```markdown
| michael-pro (charging/Anker) 30% | 70.0  |
- `michael-pro` is always in low-power mode.
```
**Status:** 🟡 SHOULD UPDATE
- Add michael-air power consumption baseline (if measured)
- Keep michael-pro data (historical baseline)

### wolf-soho/network_rv.md
```markdown
To access management UI: connect michael-pro directly to poe-rv LAN port with manual IP
```
**Status:** 🟡 SHOULD UPDATE
- Add michael-air as alternative (or specify michael-pro for historical context)

---

## Category 6: Planning & Documentation (REVIEW & UPDATE IF RELEVANT)

Files with planning notes, examples, or installation instructions.

### portable-profile/README.md (Multiple lines)
```markdown
| michael-pro / wendy-pro | Homebrew (`brew "node"`)
| michael-pro / wendy-pro | 13+         | Homebrew `brew "rust"`
```
**Status:** 🟡 SHOULD UPDATE
- Add michael-air to these tables (likely same as michael-pro)
- Copy michael-pro row and update names

### portable-profile/README_rclone.md
```markdown
Installed via Homebrew on michael-pro / wendy-pro:
```
**Status:** 🟡 SHOULD UPDATE
- Add michael-air to examples

### portable-profile/PLAN_claude_tools.md (Multiple lines)
```markdown
### Tier A -- Install on michael-pro first, then wolf-air
### michael-pro (do first)
- **michael-pro:** OK via Homebrew: `brew install eza`
- [ ] `sudo port install duckdb` -- only if validated useful on michael-pro
```
**Status:** 🟡 SHOULD UPDATE (planning document)
- This is a planning document; update examples to mention michael-air if relevant
- Keep michael-pro for historical context (shows validation path)

### portable-profile/TODO_unified_Python.md
```markdown
- All machines (wolf-air, michael-pro, wendy-pro) use same strategy
```
**Status:** 🟡 SHOULD UPDATE
- Add michael-air: "All machines (wolf-air, michael-pro (retired), michael-air, wendy-pro)"

---

## Category 7: Service Accounts & Backup Identities (REVIEW)

Files documenting user accounts, service principals, or backup identities.

### wolf-soho/Identity Strategy - NAS + MB - Human+Service Accounts.md
```markdown
- `tm-michael-pro`
| tm-michael-pro | Service | NAS (per Mac) | SSH key  | TimeMachine backup
```
**Status:** 🟡 SHOULD UPDATE
- Add `tm-michael-air` service account entry
- Keep `tm-michael-pro` (historical; may still be needed for recovery)

### portable-profile/TODO_Dropbox.md
```markdown
- Machine names in filenames (`michael-pro`, `wendy-pro`) = Mac hostnames at time of backup
| `corrupt_michael-pro.sparsebundle`
| `michael-pro.sparsebundle`
```
**Status:** ✓ Keep as-is (historical backup names; already exist in Dropbox)

---

## Category 8: Reference Documentation (KEEP AS-IS)

Files that mention machines in passing, examples, or footnotes. Not blocking.

### portable-profile/docs/CLEANUP_INTEL_HOMEBREW.md
```markdown
- **Machine:** michael-pro (M3 Mac, migrated from Intel)
```
**Status:** ✓ Keep as-is (historical example from michael-pro cleanup)

### portable-profile/TODO.md
- Generic TODOs; may mention michael-pro in examples

**Status:** ✓ Keep as-is (planning document)

---

## Action Plan Summary

### 🔴 Blocking (Must Update When NAS Accessible)
1. **wolf-soho/CONTEXT.md** — Add michael-air registry entry
2. **wolf-soho/equipment_computing.md** — Add michael-air specs section

### 🟡 Recommended (Update for Completeness)
1. **portable-profile/Makefile comments** — Add michael-air to examples
2. **portable-profile/README.md tables** — Add michael-air rows (copy michael-pro, update names)
3. **wolf-soho/equipment_portable.md** — Add michael-air networking interfaces
4. **wolf-soho/power_consumption.md** — Add michael-air baseline (if measured)
5. **portable-profile/PLAN_claude_tools.md** — Update examples to mention michael-air
6. **portable-profile/TODO_unified_Python.md** — Add michael-air to machine list
7. **wolf-soho/Identity Strategy** — Add tm-michael-air service account

### ✓ Keep As-Is (Historical Records)
- All 2026-06-18 / 2026-08-03 water damage logs
- michael-pro_battery.md
- All experiment and project files
- All Dropbox backup metadata
- All planning documents (mark michael-pro as historical)

---

## Verification Commands

**Count all michael-pro references:**
```bash
cd /Users/michael/repos && grep -r "michael-pro" wolf-soho portable-profile --include="*.md" --include="Makefile" --include="Brewfile" 2>/dev/null | grep -v ".git" | wc -l
```

**Find files NOT yet reviewed:**
```bash
cd /Users/michael/repos && grep -r "michael-pro" wolf-soho portable-profile --include="*.md" --include="Makefile" --include="Brewfile" 2>/dev/null | grep -v ".git" | cut -d: -f1 | sort -u
```

**Quick check: Are all machine conditionals updated?**
```bash
grep -n "michael-pro.*wendy-pro.*michael-air\|michael-air.*michael-pro\|michael-air.*wendy-pro" /path/to/Brewfile
```
(Should appear in one line, indicating all three machines in one conditional)

---

## Notes

- **Why "michael-pro" stays:** It's an audit trail. Water damage 2026-06-18 is not just history; it's context for why michael-air exists.
- **Why add, not replace:** Incident records, experiment results, and backup metadata all reference michael-pro. Removing the name creates orphaned context.
- **Conditionals already updated:** portable-profile/Brewfile line 75 already includes michael-air ✓
- **TM backup identity:** Old backup labeled "michael-pro" on NAS; adoption + rename will label future snapshots "michael-air" while preserving history.
