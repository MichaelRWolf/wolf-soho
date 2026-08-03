# 2026-08-03 wendy-pro Water Damage

**Device**: `wendy-pro` -- MacBook Pro

**Location**: Trails End Campground, Copper Harbor MI

## Incident

Water bottle broke in briefcase; liquid contacted computer. User opened back panel and found water intrusion centered around fan area, likely ingress through air port. Already dried with canned air. Currently drying in sun with fan running.

## Immediate Status

- **Power state**: Off (safe)
- **Battery state**: Assumed connected (unknown if disconnected yet)
- **Drying method in progress**: Sun + fan
- **Next action needed**: Determine if battery should be disconnected before continued drying

## Drying Strategy

Based on michael-pro recovery (2026-06-18):

### Phase 1: Bulk Moisture Removal (Current - Next 24-48 Hours)

**Current setup is good:**

- Sun provides gentle heat (target 100-120°F to prevent adhesive damage)
- Fan pushes moisture away from internal components
- Canned air already removed surface water

**Duration:** 24-48 hours minimum in this configuration

**Why this works:** Heat from sun builds vapor pressure inside chassis, pushing trapped moisture out through seals and vents. Fan accelerates evaporation of moisture that reaches open surfaces. Together they prevent corrosion formation on the motherboard.

**Monitor for:** Feel air vent exhaust -- if still noticeably humid after 24h, continue for another 12-24h. Thermal cycling (sun ↔ shade over hours) helps push out pockets of moisture that static heat alone misses.

### Phase 2: Mineral Deposit Prevention (After Bulk Drying)

Once the case feels dry to the touch (~48h), apply 90% isopropyl alcohol:

- **Use 90%+ IPA only** (91% drugstore or 99% lab grade work; 70% IPA is too dilute and carries water)
- Douse areas visibly affected by water (around fan, air port, keyboard edges)
- Brush gently with soft brush or cotton swab to displace water and prevent mineral corrosion
- Tilt machine to let IPA drain off; IPA evaporates quickly (5 min)
- Turn fan on after IPA application

**Why:** IPA's low surface tension reaches crevices water can't. More importantly, it displaces water and prevents the mineral residue (calcium, magnesium salts from tap/rain water) from forming white/blue corrosion deposits on solder joints and component legs. This is what killed michael-pro if left untreated.

## Critical Question: Battery Disconnection

**Should battery be disconnected before Phase 2 IPA treatment?**

- If `wendy-pro` powers on after drying: battery is safe to leave connected during IPA treatment (alcohol won't harm sealed Li+ cells)
- If `wendy-pro` won't power on: consider disconnecting battery before IPA to prevent any risk of shorts during cleanup (same process as michael-pro Step 2)

**Recommendation:** Test power after 48h drying. If it boots, no need to open further. If it doesn't, then disconnecting the battery before IPA treatment is safer.

## Comparison to michael-pro

| Factor            | michael-pro (2026-06-18)       | wendy-pro (2026-08-03)                   |
|-------------------|--------------------------------|------------------------------------------|
| Water source      | Rain + bag; ~2 inches pooled   | Bottle burst; localized to briefcase     |
| Water amount      | Large (bulk + seepage)         | Smaller, but concentrated around fan     |
| Time to discovery | ~1.5 hours                     | Unknown; assume <1 hour                  |
| Current drying    | Fan + open air                 | Sun + fan (better; heat helps)           |
| Drying timeline   | 72 hours for safety margin     | 48 hours likely sufficient; 72 preferred |
| IPA application   | 91% used successfully (36h in) | 90% will work identically                |

---

## TODO Checklist

- [ ] **After 48 hours (2026-08-05 evening):** Check case exterior -- should feel completely dry to touch (not cool/damp)
- [ ] **After 48-72 hours (2026-08-05 to 2026-08-06):** Apply 90% IPA to water-affected areas (around fan, air port edges, keyboard)
- [ ] **After IPA treatment:** Run fan for 10-15 min, let machine rest 5 minutes, then attempt power-on
- [ ] **If powers on successfully:** Boot into system, run diagnostics (Disk Utility, Activity Monitor) to confirm no hardware errors
- [ ] **If does not power on:** Consider battery disconnection and motherboard inspection (see michael-pro procedure for reference)

---

## Reference

- [2026-06-18_michael-pro_water-damage.md](2026-06-18_michael-pro_water-damage.md) -- Full disassembly, battery disconnect, motherboard extraction, and corrosion cleaning procedures
- [CONTEXT.md](CONTEXT.md) -- Device registry (wendy-pro specs, location)
