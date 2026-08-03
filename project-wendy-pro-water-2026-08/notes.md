# wendy-pro Water Damage -- Recovery Project

**Device**: `wendy-pro` -- MacBook Pro
**Incident Date:** 2026-08-03 (Trails End Campground, Copper Harbor MI)
**Status**: Drying in progress

## Incident Summary

Water bottle broke in briefcase → liquid contacted laptop → opened back panel → found water intrusion centered around fan (likely air port ingress) → applied canned air → now drying in sun with fan.

**Current state:**

- Power: Off (safe)
- Battery: Assumed connected (unknown if disconnected yet)
- Drying method: Sun + fan
- Timeline: Started 2026-08-03 afternoon

## Drying Strategy

### Phase 1: Trapped Water Displacement (Immediate - now)

Apply 90% isopropyl alcohol NOW to displace trapped water that canned air cannot reach (especially under fan where water hangs on by surface tension). This prevents corrosion from starting while water is still fresh.

**Materials:**

- 90%+ IPA only (91% drugstore or 99% lab grade; avoid 70% IPA--too much water)
- Soft brush or cotton swabs
- Lint-free cloth

**Process:**

1. Douse areas visibly affected by water (around fan, air port, keyboard edges)
2. Brush gently to displace water and break up mineral deposits
3. Tilt machine to let IPA drain off (evaporates in ~5 min)
4. Run fan for 10-15 min after to accelerate evaporation

**Why now:** IPA's low surface tension penetrates crevices that air can't reach. Crucially, it displaces water before mineral residue (calcium, magnesium salts) can form corrosion deposits on solder joints and component legs. Waiting 24-48h gives corrosion more time to start. Fresh water + IPA = faster displacement, less corrosion risk.

### Phase 2: Extended Drying (After IPA, 24-72 hours)

After IPA treatment, continue sun + fan drying to evaporate any residual moisture:

**Setup:** Sun provides gentle heat (target 100-120°F; prevents adhesive damage above ~140°F). Fan accelerates evaporation of moisture reaching open surfaces. Thermal cycling (sun ↔ shade over hours) helps push out pockets trapped near components.

**Monitor:** Feel air vent exhaust. If still noticeably humid after 24h of post-IPA drying, continue another 12-24h.

**Why this works:** Heat builds vapor pressure inside chassis, pushing residual moisture out through seals and vents. Combined with IPA displacement, this prevents corrosion formation on the motherboard.

**Materials:**

- 90%+ IPA only (91% drugstore or 99% lab grade; avoid 70% IPA--too much water)
- Soft brush or cotton swabs
- Lint-free cloth

**Process:**

1. Douse areas visibly affected by water (around fan, air port, keyboard edges)
2. Brush gently to displace water and break up mineral deposits
3. Tilt machine to let IPA drain off (evaporates in ~5 min)
4. Run fan for 10-15 min after to accelerate evaporation

**Why:** IPA's low surface tension reaches crevices. Crucially, it displaces water and prevents mineral residue (calcium, magnesium salts from tap water) from forming white/blue corrosion deposits on solder joints and component legs. This is what would require motherboard extraction and cleaning if neglected.

**Timeline:** michael-pro was treated at ~36h into drying and it worked. Don't wait too long--mineral corrosion deposits start forming immediately.

## Critical Decision: Battery Disconnection

**Should battery be disconnected before IPA treatment?**

- **If `wendy-pro` powers on after drying:** Battery is safe to leave connected during IPA treatment (alcohol won't harm sealed Li+ cells).
- **If `wendy-pro` won't power on:** Consider disconnecting battery before IPA to prevent any risk of shorts during cleanup.

**Recommendation:** Test power after 48h drying. If it boots, no further disassembly needed. If not, refer to michael-pro procedure for battery disconnect (Step 2 in incident log).

## Recovery Checklist

- [ ] **NOW (2026-08-03):** Apply 90% IPA to water-affected areas (around fan, air port edges, keyboard); brush gently; let drain and evaporate
- [ ] **After IPA (2026-08-03 evening):** Run fan for 10-15 min, then begin sun + fan drying
- [ ] **After 24 hours of post-IPA drying (2026-08-04 afternoon):** Check case exterior--should feel completely dry to touch (not cool/damp); continue drying if humid
- [ ] **After 24-72 hours of post-IPA drying (2026-08-04 to 2026-08-05):** Case should be fully dry; attempt power-on
- [ ] **If powers on successfully:** Boot into system, run Disk Utility and Activity Monitor to confirm no hardware errors
- [ ] **If does not power on:** Refer to michael-pro procedure for battery disconnection and motherboard inspection

## Comparison to michael-pro Recovery

| Factor          | michael-pro (2026-06-18)        | wendy-pro (2026-08-03)           |
|-----------------|---------------------------------|----------------------------------|
| Water source    | Rain + bag (~2 inches pooled)   | Bottle burst (localized)         |
| Amount          | Large (bulk + seepage)          | Smaller, concentrated around fan |
| Discovery time  | ~1.5 hours after incident       | 1-2 hours after incident         |
| IPA treatment   | 91% at ~36h mark (delayed)      | 90% immediately (better)         |
| Why immediate   | Material unavailability at time | Prevents corrosion sooner        |
| Post-IPA drying | 72 hours (safety margin)        | 24-72 hours target               |
| Improvement     | Waited → corrosion risk longer  | Displace trapped water first     |

## References

- [2026-08-03_wendy-pro_water-damage.md](2026-08-03_wendy-pro_water-damage.md) -- Full incident log (redundant with this file; keep for archive)
- [2026-06-18_michael-pro_water-damage.md](../2026-06-18_michael-pro_water-damage.md) -- Reference procedures: battery disconnect, motherboard extraction, corrosion cleaning
- [CONTEXT.md](../CONTEXT.md) -- Device registry (wendy-pro specs)
