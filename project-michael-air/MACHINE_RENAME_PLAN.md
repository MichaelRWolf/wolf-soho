# Machine Rename Plan: michael-pro → michael-air

**Status:** NAS-dependent action (TM backup must remain accessible)  
**Date:** 2026-08-16  
**Scope:** ADD michael-air entries; PRESERVE michael-pro historical records (no updates)  
**Rationale:** Machine rename required before Time Machine backup adoption continues; preserve audit trail of original intel machine.

---

## Naming Convention (Canonical References)

**Source of truth:** `CONTEXT.md` and `equipment_computing.md` in wolf-soho

**Current pattern (Brewfile, line 75):**
```ruby
when "michael-pro", "wendy-pro", "michael-air"
  # Full Homebrew installation (formulae + casks)
```

**Principle:** ADD `"michael-air"` alongside existing machine names; DO NOT remove `"michael-pro"`.

---

## Phase 1: Machine Rename + TM Adoption (NAS Access Required)

**Prerequisite:** NAS backup must be accessible and mounted.

### Step 1: Rename Machine
```bash
scutil --set ComputerName michael-air
scutil --set HostName michael-air
scutil --set LocalHostName michael-air
# Also: System Settings → General → About → Computer Name
```

### Step 2: Time Machine Adoption
- Time Machine will detect name change and prompt: "This backup was created for a different computer (michael-pro)"
- **Choose: "Keep Using This Backup"** (NOT "Start New Backup")
- This appends future snapshots to existing timeline, preserving history

### Step 3: Verify Continuity
```bash
tmutil destinationinfo  # Should show michael-air with pre-rename history
```

---

## Phase 2: Registry & Configuration Updates (Add Only)

**Golden rule:** If an entry mentions `michael-pro`, do not edit it. Add a NEW entry for `michael-air` instead.

### 🔴 MUST UPDATE: Machine-Specific Configuration

These files directly reference machine hostnames and WILL NOT WORK until updated:

#### 1. `wolf-soho/CONTEXT.md` — Device Registry (Line 55-64)

**Current:**
```markdown
| Name             | Device                          |
|------------------|---------------------------------|
| `michael-pro`    | MacBook Pro (Michael's primary) |
| `wendy-pro`      | MacBook Pro (Wendy's)           |
| `wolf-air`       | MacBook Air                     |
```

**Action:** ADD row for michael-air:
```markdown
| Name             | Device                          |
|------------------|---------------------------------|
| `michael-pro`    | MacBook Pro (Michael's primary, water damaged 2026-06-18; retired) |
| `michael-air`    | MacBook Air (M3, 2024; michael-pro replacement, active) |
| `wendy-pro`      | MacBook Pro (Wendy's)           |
| `wolf-air`       | MacBook Air                     |
```

**Rationale:** Registry must reflect current active machine. michael-pro entry kept for audit trail.

---

#### 2. `wolf-soho/equipment_computing.md` — Device Specs

**Current sections:**
- `michael-pro` -- MacBook Pro (Michael's primary)
- `wendy-pro` -- MacBook Pro (Wendy's) -- ABANDONED
- `wolf-air` -- MacBook Air

**Action:** ADD new section `## \`michael-air\` -- MacBook Air (M3, 2024)` with:
```markdown
## `michael-air` -- MacBook Air (M3, 2024)

- Model: MacBook Air (13-inch, M3, 2024)
- MPN: A3113
- Processor: Apple M3 (8-Core GPU)
- RAM: 16 GB
- Storage: 256 GB SSD
- Display: 13", 2560×1664, Liquid Retina
- Color: Space Gray
- OS: macOS 15.7 Sequoia
- Status: **ACTIVE** (replacement for michael-pro; Time Machine backup adopted 2026-08-16)
- mDNS name: michael-air.local
- Connectivity: USB-C (Thunderbolt 4), HDMI, DisplayPort, Wi-Fi 6E, Bluetooth
- Serial: [from About → Serial Number]
- Notes: Migration from michael-pro via Time Machine (2026-08-13/14). See [project-michael-air/](project-michael-air/) for setup details.
```

**Rationale:** Full specs required for inventory. Keep michael-pro entry unchanged (historical record of water damage incident).

---

#### 3. `portable-profile/homebrew/Brewfile` — Machine Conditional (Line 75)

**Current:**
```ruby
when "michael-pro", "wendy-pro", "michael-air"
  # Full Homebrew installation (formulae + casks)
```

**Status:** ✓ ALREADY CORRECT (michael-air already included!)

**Verification:** Confirm line 75 has all three machine names:
```bash
grep -n 'when "michael-pro"' /path/to/Brewfile
```

If missing, add:
```ruby
when "michael-pro", "wendy-pro", "michael-air"
```

---

#### 4. `portable-profile/Makefile` — Machine Conditional Targets

**Action:** Verify machine conditionals in Makefile include michael-air. Common patterns:

```makefile
ifeq ($(HOSTNAME), michael-pro)
  # michael-pro specific config
else ifeq ($(HOSTNAME), michael-air)
  # michael-air specific config (copy michael-pro block if identical)
else ifeq ($(HOSTNAME), wendy-pro)
  # wendy-pro specific config
endif
```

**Search & verify:**
```bash
grep -n "michael-pro\|michael-air\|wendy-pro" /path/to/Makefile | head -20
```

If michael-air is missing, add it alongside michael-pro entries.

---

### 🟡 SHOULD UPDATE: Cross-References & Documentation

These files reference machines as examples; should be updated for completeness, but not blocking:

#### 5. `portable-profile/README.md` — General References

**Action:** Search for mentions of "michael-pro" in setup instructions. If examples list:
```
Installation tested on: michael-pro, wendy-pro, wolf-air
```

**Update to:**
```
Installation tested on: michael-air, michael-pro (historical), wendy-pro, wolf-air
```

---

#### 6. `portable-profile/Makefile` — Comments & Target Help

**Action:** Review comments in Makefile that mention machine names. If found, add michael-air as example:

Before:
```bash
# Example: make install_npm_globals HOSTNAME=michael-pro
```

After:
```bash
# Example: make install_npm_globals HOSTNAME=michael-air  # or michael-pro (historical)
```

---

#### 7. `portable-profile/docs/` — Documentation Files

**Files to review:**
- `docs/CLEANUP_INTEL_HOMEBREW.md` — May reference michael-pro; add michael-air as variant
- Other docs that use michael-pro as setup example

**Action:** Add michael-air alongside michael-pro in examples (keep michael-pro for historical context).

---

### ✓ NO ACTION NEEDED: Historical Records

**DO NOT TOUCH THESE** — They are audit trails:

- `wolf-soho/2026-06-18_michael-pro_water-damage.md` — Incident log (keep as-is)
- `wolf-soho/2026-07-summer_trails_end.md` — Historical log mentioning michael-pro
- `wolf-soho/michael-pro_battery.md` — Maintenance record (keep as-is)
- `wolf-soho/project_compare_network_responsiveness_(wolf-air_v_michael-pro).md` — Historical experiment (keep as-is)
- `portable-profile/PLAN_claude_tools.md` — Past planning notes (keep as-is)
- All incident/project logs with michael-pro in title or content (keep as-is)
- All water-damage/failure logs (keep as-is)

**Rationale:** These are historical artifacts. Leaving them unchanged preserves audit trail of what machine did what, when it failed, why it was replaced.

---

## Checklist: Before Machine Rename

- [ ] **NAS backup is mounted and accessible** (required for TM adoption)
- [ ] **All documentation updates staged** (CONTEXT.md, equipment_computing.md reviewed)
- [ ] **Brewfile verified** (michael-air already in conditional, line 75)
- [ ] **Makefile machine conditionals verified** (michael-air added if missing)
- [ ] **GitHub issues #9 & #10 updated** (machine rename & TM stabilization tracking)

---

## Checklist: After Machine Rename

- [ ] **Machine renamed** (scutil commands + System Preferences)
- [ ] **TM backup adoption confirmed** (choose "Keep Using This Backup")
- [ ] **TM continuity verified** (`tmutil destinationinfo` shows michael-air with pre-rename history)
- [ ] **CONTEXT.md & equipment_computing.md committed** (michael-air entry added)
- [ ] **All documentation updates committed** (no uncommitted changes left)
- [ ] **GitHub issues #9 & #10 marked done** (issues closed/resolved)

---

## Files Already Updated (No Action Needed)

- ✓ `portable-profile/homebrew/Brewfile` (michael-air already in line 75)
- ✓ `wolf-soho/project-michael-air/` (entire directory is for michael-air setup)

---

## References

- **GitHub Issue #9:** Machine rename (michael-pro → michael-air)
- **GitHub Issue #10:** Stabilize Time Machine backups (michael-pro → michael-air)
- **Related:** [setup.md](setup.md) — Migration process & decisions
- **Related:** [tm-strategy.md](tm-strategy.md) — Time Machine efficiency audit

---

## Notes

**Why "ADD, don't replace":**
- michael-pro entries are historical records of an incident (water damage 2026-06-18)
- Removing them obscures what machine did what and why it was replaced
- Future forensics/audits need the full timeline
- Naming convention supports both machines (old and new) in conditionals (Brewfile line 75)

**Why TM adoption matters:**
- Adopted backup preserves all michael-pro snapshots (recovery possible)
- Machine rename mid-stream creates one continuous timeline
- Alternative (new backup) would fork history into two separate, unsearchable backups

**Why NAS access is required:**
- Time Machine adoption decision happens when TM detects the name change
- NAS must be mounted to present the choice
- Without NAS access, cannot proceed to step 2; can do steps 1 & 3 later
