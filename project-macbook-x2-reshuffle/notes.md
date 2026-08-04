# MacBook Reshuffle Project 2026-08

**Goal:** Recover Wendy and Michael to working machines following water damage incidents (wendy-pro 2026-08-03, michael-pro 2026-06-18).

**Scope:** Both users need functional machines by EOY 2026. Constraint: Price-sensitive. Preference: Used/refurbished M-series over expensive repairs.

---

## Requirements

### Wendy's Needs

**Workload:** Cloud-first SaaS user. Minimal local storage requirements.

| Category            | Requirement                                                           | Notes                                                |
|---------------------|-----------------------------------------------------------------------|------------------------------------------------------|
| **Primary limiter** | Safari tab management (10-50+ tabs open simultaneously)               | Need 16GB+ RAM; CPU matters less                     |
| **Communication**   | Zoom video calls                                                      | 1080p sufficient; no advanced features               |
| **Web services**    | ChatGPT, MailChimp, Facebook, GoDaddy website builder, webmail        | All SaaS; no native apps required                    |
| **Cloud storage**   | iCloud, Google Sheets/Docs, GitHub (git operations only)              | Light git use; no local development                  |
| **Apple ecosystem** | Mail.app (ATT.net IMAP), Notes.app, macOS apps                        | Native apps for convenience; not critical            |
| **Streaming**       | Amazon Prime Video                                                    | 1080p+ video codec support                           |
| **Optional**        | Native ChatGPT or Claude apps (nice-to-have)                          | Web versions work fine                               |
| **Backup**          | NAS Time Machine (current as of 3 weeks ago; sufficient)              | SaaS data in cloud; not concerned about recent files |
| **OS constraint**   | Must support current macOS (Monterey minimum; Tahoe/Sonoma preferred) | Monterey EOL is imminent; prefer Tahoe+              |

**CPU/RAM profile:** CPU is NOT the bottleneck. RAM is. Wendy needs **16GB minimum** to handle Safari tab addictions. M3 Air/Pro (16GB) is sufficient; M4/M5 overkill for her workload.

---

### Michael's Needs

**Workload:** Light development + Claude Code sessions. Limping along acceptable until cash flow improves.

| Category            | Requirement                                                       | Notes                                                                |
|---------------------|-------------------------------------------------------------------|----------------------------------------------------------------------|
| **Primary use**     | Claude Code (running locally on machine)                          | Currently using wolf-air (2015 Intel); works but nags about Homebrew |
| **Development**     | Git operations (clone, push, pull, commit)                        | Very light; no complex CI/CD or builds                               |
| **Secondary**       | Bash scripting, shell operations                                  | Writing shell scripts for project automation                         |
| **No requirement**  | Native development IDEs, compilers, heavy frameworks              | Not doing active coding; just repo management                        |
| **Backup**          | NAS Time Machine (current)                                        | Low data loss risk; SaaS + git repos                                 |
| **OS constraint**   | Must support current macOS (Tahoe preferred; Monterey acceptable) | Intel cutoff is a factor; M-series preferred                         |
| **Brew limitation** | Current wolf-air (Intel) nags about unsupported packages          | Not a blocker, just annoying                                         |

**CPU/RAM profile:** M3 MacBook Air (8GB RAM, base M3) is sufficient. Michael doesn't need M4/M5 performance. Can use refurbished/used 2023+ M-series without issue.

---

## Strategy

### Option A: Wendy Adopts wolf-air + Michael Gets Used M4/M3

**Rationale:**

- wolf-air is functional hardware (just old OS); moving Wendy to it frees up budget for Michael's better machine
- Wendy's SaaS-first workflow is compatible with Monterey (all major cloud apps support it through 2026)
- Michael gets a modern M-series to escape Intel warnings + longer OS support
- Timing: Fast (NAS restore is quick); no repair delays

**Wendy's Machine (wolf-air):**

- **Hardware:** MacBook Air (MacBookAir7,2), 2015 model, Intel Core i5 1.8 GHz, 8GB RAM
- **Current OS:** Monterey 12.7.6 (capped; cannot upgrade to Tahoe)
- **Limitations:**
  - No new macOS versions; security patches via Monterey only
  - Intel; Homebrew/brew formula support declining
  - 8GB RAM for 50+ Safari tabs will be tight (but not impossible; manageable with some tab discipline)
- **Migration:** Restore from wendy-pro's 3-week-old NAS Time Machine backup
  - All Wendy's apps, settings, user data restored
  - Backup is sufficient (no SSD recovery needed)
- **Timeline:** 1-2 days (mostly Time Machine restore)
- **Success probability:** ~95% (standard Time Machine to different hardware)

**Michael's Machine (Used M4 or M3):**

- **Options:**
  - Used 2024 M4 MacBook Air (~$700-$900)
  - Used 2023 M3 MacBook Air (~$500-$700)
  - Used 2022 M2 MacBook Air (~$400-$600, if avoiding shitty 2022 Pro models)
- **Specs needed:**
  - 16GB RAM (breathing room for Claude Code + git)
  - 256GB+ SSD
- **Migration:** Restore from michael-pro's NAS Time Machine backup
  - Michael's dotfiles, SSH keys, git config, shell scripts all restored
- **Timeline:** 1-2 days (Time Machine restore)
- **Success probability:** ~95%

**Total cost estimate:**

- Wendy machine: $0 (repurpose wolf-air)
- Michael machine: $500-$900 (used M3 or M4)
- **Total: $500-$900** (vs. $1,000+ for logic board repairs)

---

### Option B: Fix Both Machines (Parallel Logic Board Repairs)

**Rationale:** Keep existing machines; avoid migration friction.

**wendy-pro (Logic Board Replacement):**

- **Cost:** $200-$350 (independent micro-soldering shop)
- **Timeline:** 5-7 business days
- **Risk:** Water damage is confirmed (early boot failure + GPU anomalies). Logic board failure is likely power management IC corrosion. Success probability: ~70-80%
- **Outcome if successful:** M2 MacBook Pro (2022) with fresh logic board; restore from NAS backup
- **Outcome if fails:** Machine is gone; proceed to Option A anyway

**michael-pro (Logic Board Replacement):**

- **Status:** Currently disassembled (battery extraction paused 2026-06-23). Logic board is accessible.
- **Cost:** $200-$350 (micro-soldering shop OR self-service if you attempt it)
- **Timeline:** 5-7 business days (if outsourced); unknown if reassembling locally
- **Risk:** 2020 Intel machine; out of warranty; thermal issues even before water damage (battery degraded to 1,500 cycles)
- **Outcome if successful:** Limping Intel machine; not an improvement over wolf-air for Michael
- **Outcome if fails:** Adds $200-$350 sunk cost to a machine already problematic

**Problem with Option B:**

- Both repairs run in parallel = 5-7 days wait for results
- If wendy-pro succeeds but michael-pro fails (or vice versa), mismatch in outcomes
- Cost ($400-$700 for two boards) approaches Option A's total ($500-$900 for one new machine)
- michael-pro remains an Intel machine even if repaired; no improvement in OS support or Homebrew warnings

---

## Recommendation: Option A (with Michael flexibility)

**Decision Path for Wendy (definite):**

1. Adopt wolf-air immediately (1-2 days for Time Machine restore)
2. Hunt used M3 or M4 MacBook Air on eBay, Facebook Marketplace, or Swappa
3. Restore to new machine within 1-2 days of purchase

**Decision Path for Michael (two options):**

**Option A1 (Upgrade now -- Recommended):**

- Hunt used M3 or M4 MacBook Air (same search as Wendy, independent)
- Restore within 1-2 days of purchase
- Eliminates Monterey EOL pressure
- Cost: $500-$900

**Option A2 (Defer -- Budget-conscious):**

- Continue using wolf-air for Claude Code + git through mid-2026
- Zero cost now; preserves cash flow
- Plan machine upgrade around June 2026 (Monterey EOL)
- Acceptable if Michael is content with current setup

**Retired machines:**

- wendy-pro: Send SSD to data recovery lab ($600) IF data from past 5 weeks critical. Otherwise, scrap/recycle.
- michael-pro: Attempt disassembly completion + logic board repair as low-priority hobby project (if interested). Otherwise, scrap/recycle.

**Why Option A works:**

- **Speed:** 3-5 days to operational (vs. 7-14 days waiting for repairs)
- **Cost:** $500-$900 (Wendy + Michael upgrade) OR $0-$500 (Wendy only, Michael defers)
- **Certainty:** No repair risk; proven hardware
- **Future-proofing:** Modern silicon + long OS support through ~2030
- **Flexibility:** Michael can defer if cash flow is tight; revisit in 6 months

---

## Path B Assessment: wendy-pro Logic Board Replacement

**Machine status:**

- Boots partially (fan spins, keyboard lights)
- Never reaches network boot (stuck early)
- GPU produces brief pink flash before power-off
- **Diagnosis:** Power management or boot sequencer IC failure (corrosion from water intrusion)

**Repair shop approach:**

- Micro-soldering shop would inspect under microscope
- Identify corroded solder joints or oxidized IC pins on power management rail
- Rework solder joints or replace corroded IC (if replaceable)
- Test power-on sequence before returning

**Success factors:**

- Damage is localized to power management (good; not widespread corrosion)
- Machine showed signs of life (fan, keyboard lights); not complete dead board
- Typical success rate for this failure mode: 70-80% (independent shops report 7 in 10 boards salvageable)
- Failure modes: If damage extends to boot sequencer IC or flash firmware is corrupted, recovery is harder (~50% success)

**Why it's risky:**

- Water damage assessment is imperfect until board is under microscope
- Unknown if corrosion has spread to firmware storage or SoC
- If repair fails midway (shop gets partway into rework), machine may be less salvageable than now

**Timeline if attempted:**

- Diagnosis + quote: 1-2 days
- Repair: 3-5 business days
- Testing: 1 day
- Total: 5-8 business days

**Recommendation:**
If you're committed to keeping wendy-pro as primary: Try Path B (70-80% success, $200-$350 cost is low risk).
If you're willing to accept Wendy on wolf-air temporarily: Skip Path B; cheaper and faster to move to Option A.

---

## Options Summary

| Option              | Path                                                    | Cost      | Timeline  | Risk                                 | Outcome                                      |
|---------------------|---------------------------------------------------------|-----------|-----------|--------------------------------------|----------------------------------------------|
| **A (Recommended)** | Wendy → wolf-air, Michael → M3/M4                       | $500-$900 | 3-5 days  | Low (proven hardware)                | Both users operational; modern machines      |
| **B**               | Fix wendy-pro (logic board), keep michael-pro           | $400-$700 | 7-14 days | Medium (repair may fail)             | Outcome unclear; michael-pro still Intel     |
| **C**               | wendy-pro display replacement (if display-only failure) | $200-$400 | 5-7 days  | N/A (already ruled out; not display) | N/A (logic board is the issue)               |
| **D**               | Data recovery from wendy-pro ($600), then scrap         | $600      | 5-10 days | Low (if data critical)               | Wendy data archived; still need new machines |

---

## Wolf-air Caveats (Wendy's interim machine)

**What works:**

- All cloud services (Zoom, ChatGPT, Sheets, Docs, iCloud, GitHub web)
- Safari (though 8GB RAM is tight for 50+ tabs; manageable with tab discipline)
- Mail.app, Notes.app, Calendar.app
- Amazon Prime streaming

**What doesn't work:**

- New macOS versions (stuck at Monterey 12.7.6)
- Homebrew package installation nags (Intel deprecation warnings; non-fatal)
- Security patches end ~mid-2026 (Monterey reaches EOL)

**Mitigation:**

- Wendy is SaaS-first; Monterey EOL is manageable short-term (3-6 months acceptable)
- Safari tab management: Suggest tab grouping / "Later" feature to reduce open tab count
- Accept Intel deprecation warnings as cosmetic until upgrade window

**Success probability:** ~95% (standard migration, no hardware risk)

---

## Machine Analysis Files

Detailed per-user hardware recommendation matrices:

- **[wendy-options.md](wendy-options.md)** -- Wendy's independent hardware choices (M5, M4, M3, M2, wolf-air analysis)
- **[michael-options.md](michael-options.md)** -- Michael's hardware choices, including Claude Code compatibility analysis

**Key findings:**

- Wendy: M3 Air 16GB recommended ($500-$700)
- Michael: M3 Air 16GB recommended ($500-$700); **wolf-air cannot run Claude Code (Monterey < macOS 13 requirement)**

---

## Backup Dates (Updated 2026-08-04)

**Correction:** NAS Time Machine backups are dated **2026-06-27** (38 days / ~5.5 weeks ago), not 3 weeks.

- wendy-pro: 2026-06-27
- michael-pro: 2026-06-27 (likely)
- wolf-air: 2026-06-27 (likely)

**Implication:** Both Wendy and Michael restore from same baseline. Data loss is minimal (SaaS users; code loss acceptable for Michael).

---

## Next Steps

1. **Confirm NAS backup freshness:** Verify both wendy-pro and michael-pro backups dated 2026-06-27 are mounted/accessible
2. **Hunt used M3/M4:** Search eBay, Facebook Marketplace, Swappa for 13-14 inch M3 or M4 MacBook Air; target $500-$900 with 16GB RAM
3. **Wendy migration prep:** Back up wolf-air's current user data (if any) before Time Machine restore; erase and restore from wendy-pro backup
4. **Michael migration prep:** Prepare NAS credentials / backup access for fresh machine setup
5. **Optional:** If data from wendy-pro's past 3 weeks is critical, send SSD to recovery lab after reshuffle ($600); otherwise skip

---

## Security Practices (Wolf-air + Michael Going Forward)

**Wendy's threat model (SaaS-first, Monterey):**

- Risk: Old OS means unpatched vulnerabilities in system libraries
- Mitigation:
  - Use strong passwords in Safari (already does with iCloud Keychain)
  - Enable 2FA on all cloud services (Gmail, iCloud, GitHub, etc.)
  - Avoid untrusted WiFi (stick to home/known networks)
  - Don't download/run untrusted binaries
- Acceptable trade-off: Short-term (3-6 months) Monterey EOL is fine for SaaS user

**Michael's threat model (Claude Code + git, any machine):**

- Risk: Lower priority; focus on preventing credential leaks in shell history / git config
- Mitigation:
  - Never commit `.env` or credentials to git (use `.gitignore`)
  - Keep SSH private key passphrased (even though machine is personal)
  - Use GitHub personal access tokens (PATs) instead of passwords for git clone/push
  - Avoid storing plaintext passwords in config files
- Non-critical: Don't stress about OS patching delays on personal machine (not a server)

**General:**

- Both users: Enable FileVault (full disk encryption) on machines
- Both users: Regular NAS backups (already doing; good)
- Michael: Keep Claude Code and git updated (for security patches)
- Wendy: Accept Monterey as interim; upgrade to modern OS (Tahoe+) when switching to new machine

---

## Files to Update

- `equipment_computing.md` -- Update wendy-pro and michael-pro status; list wolf-air as Wendy's primary (interim)
- `CONTEXT.md` -- Update device ownership: wendy-pro (archived), wolf-air → Wendy (temp), michael-pro (disassembled/TBD)
- Create this project: `project-macbook-x2-reshuffle/notes.md` ✓

---

## Timeline

### Wendy (Definite)

| Date                  | Action                                                                |
|-----------------------|-----------------------------------------------------------------------|
| 2026-08-05            | Migrate to wolf-air (Time Machine restore from wendy-pro, 2026-06-27) |
| 2026-08-05-2026-08-12 | Hunt M3 Air 16GB on eBay/Marketplace                                  |
| 2026-08-12-2026-08-15 | Purchase M3 Air; Time Machine restore                                 |
| 2026-08-16 onwards    | Operational on M3 Air (permanent)                                     |

### Michael (Two Options)

#### Option A1: Upgrade Now (Recommended)

| Date                  | Action                                |
|-----------------------|---------------------------------------|
| 2026-08-05-2026-08-12 | Hunt M3 Air 16GB (independent search) |
| 2026-08-12-2026-08-15 | Purchase M3 Air; Time Machine restore |
| 2026-08-16 onwards    | Operational on M3 Air (permanent)     |

#### Option A2: Defer (Budget-Conscious)

| Date            | Action                                                      |
|-----------------|-------------------------------------------------------------|
| Now-2026-06     | Continue using wolf-air for Claude Code + git               |
| 2026-06         | Begin hunting M3/M4 Air as Monterey EOL approaches          |
| 2026-07-2026-08 | Migrate to new machine before Monterey security patches end |

### Retired Machines (Either Timeline)

| Date               | Action                                                                               |
|--------------------|--------------------------------------------------------------------------------------|
| 2026-08-20 onwards | Optional: Send wendy-pro SSD to recovery ($600) if data critical; else scrap/recycle |
| 2026-08-20 onwards | michael-pro: attempt logic board repair (hobby) or scrap/recycle                     |
