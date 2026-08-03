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

## Drying Strategy (48-72 hours total)

### Phase 1: Bulk Moisture Removal (24-48 hours)

**Current setup:** Sun + fan is ideal.

- Sun provides gentle heat (target 100-120°F; prevents adhesive damage above ~140°F)
- Fan accelerates evaporation of moisture reaching open surfaces
- Canned air already removed surface water
- Thermal cycling (sun ↔ shade over hours) helps push out pockets trapped near components

**Monitor:** Feel air vent exhaust. If still noticeably humid after 24h, continue another 12-24h.

**Why this works:** Heat builds vapor pressure inside chassis, pushing trapped moisture out through seals and vents. Together with fan, prevents corrosion formation on the motherboard.

### Phase 2: Mineral Deposit Prevention (~48h onward)

Once case feels dry to the touch, apply 90% isopropyl alcohol:

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

- [ ] **After 48 hours (2026-08-05 evening):** Check case exterior--should feel completely dry to touch (not cool/damp)
- [ ] **After 48-72 hours (2026-08-05 to 2026-08-06):** Apply 90% IPA to water-affected areas (around fan, air port edges, keyboard)
- [ ] **After IPA treatment:** Run fan for 10-15 min, let machine rest 5 minutes, then attempt power-on
- [ ] **If powers on successfully:** Boot into system, run Disk Utility and Activity Monitor to confirm no hardware errors
- [ ] **If does not power on:** Refer to michael-pro procedure for battery disconnection and motherboard inspection

## Comparison to michael-pro Recovery

| Factor         | michael-pro (2026-06-18)      | wendy-pro (2026-08-03)              |
|----------------|-------------------------------|-------------------------------------|
| Water source   | Rain + bag (~2 inches pooled) | Bottle burst (localized)            |
| Amount         | Large (bulk + seepage)        | Smaller, concentrated around fan    |
| Discovery time | ~1.5 hours after incident     | <1 hour (estimated)                 |
| Current drying | Fan + open air (no heat)      | Sun + fan (better; adds heat)       |
| Total timeline | 72 hours (safety margin)      | 48 hours likely sufficient; 72 pref |
| IPA treatment  | 91% at ~36h mark (worked)     | 90% will work identically           |

## References

- [2026-08-03_wendy-pro_water-damage.md](2026-08-03_wendy-pro_water-damage.md) -- Full incident log (redundant with this file; keep for archive)
- [2026-06-18_michael-pro_water-damage.md](../2026-06-18_michael-pro_water-damage.md) -- Reference procedures: battery disconnect, motherboard extraction, corrosion cleaning
- [CONTEXT.md](../CONTEXT.md) -- Device registry (wendy-pro specs)
