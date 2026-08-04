# wendy-pro Water Damage -- Recovery Project

**Device**: `wendy-pro` -- MacBook Pro
**Incident Date:** 2026-08-03 (Trails End Campground, Copper Harbor MI)
**Status**: Drying in progress

## Incident Summary

Water bottle broke in briefcase → liquid contacted laptop → opened back panel → found water intrusion centered around fan (likely air port ingress) → applied canned air → now drying in sun with fan.

**Current state:**

- Power: USB-powered (partial boot, no display)
- Battery: Connected; does NOT power machine on its own
- Drying method: Sun (2026-08-03), overnight indoors, fan 2-3h (2026-08-04)
- **IPA applied: 2026-08-03 ~14:30-15:00 (completed)**
- **Reassembled: 2026-08-04 (batteries reconnected, bottom panel screwed)**
- **Power-on test: 2026-08-04 (24h post-IPA)** -- USB powers on, battery does not

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

**Timeline (post-IPA):**

The last 2-3 drops of water in deep pockets are undetectable by human senses or conventional monitoring. The IPA displacement was the critical step; residual slow evaporation is not a boot-prevention problem.

- **After 24h (2026-08-04):** Localized intrusion like wendy-pro likely fully dry by this point. Test power-on.
- **If no boot at 24h:** Problem is not "residual moisture still evaporating"--it's specific damage (corrosion, connector contamination, logic board short). Waiting to 48h won't help. Proceed to diagnosis: disconnect battery, inspect for corrosion, check connectors, consider motherboard extraction + cleaning.
- **After 48h (2026-08-05):** If you chose to wait, absolute latest safe point before assuming the machine won't boot due to water damage. Power on and test.
- **72h:** Only for bulk water scenarios (michael-pro's ~2 inches). Wendy-pro localized → 24-48h sufficient.

**Why this works:** Heat builds vapor pressure inside chassis, pushing residual moisture out through seals and vents. Combined with IPA displacement, this prevents corrosion formation on the motherboard.

## Critical Decision: Battery Disconnection Before IPA

**Should battery be disconnected before IPA treatment (right now)?**

- **Option 1 (simpler):** Battery safe to leave connected during IPA. Machine is off; IPA is non-conductive at 90%+; process is quick (minutes). No electrical risk.
- **Option 2 (safest):** Disconnect battery first. Takes 2 minutes (pentalobe P5 + plastic spudger). Eliminates all electrical concerns if IPA seeps into unexpected places.

**Recommendation:** Option 2. Battery is already accessible with back panel off. Zero cost to disconnect; maximum safety during IPA treatment.

## Recovery Checklist

- [x] **2026-08-03 ~14:30-15:00:** IPA applied to water-affected areas (around fan, air port edges, keyboard); brushed gently; drained and evaporated
- [x] **2026-08-03 ~15:00-15:15:** Extended drying begun (sun + breeze, IPA fully evaporated)
- [x] **2026-08-04 (24h post-IPA):** Machine reassembled (batteries reconnected, bottom panel screwed); air vents feel dry
- [x] **2026-08-04 power-on test:** USB power: machine boots partially (fan on high, keyboard lights); no display output, no Apple logo, no sound. Battery does NOT power machine on.
- [ ] **Pending diagnostics:** Display connector issue vs. GPU damage vs. battery failure
- [ ] **Pending:** SMC reset, display connector inspection, battery diagnostics

## Troubleshooting: No Display (2026-08-04)

**Symptoms:**

- USB power: machine boots (fan on high immediately, keyboard backlight lights up)
- Battery power: no power at all
- Display: completely black, no Apple logo, no output of any kind
- Audio: no startup sound/chime
- Abnormal fan behavior: starts high after 2-4 seconds (typical boot does not do this)

**Likely causes (priority):**

1. Display connector corroded or loose → water intrusion near display ribbon connector
2. GPU/display subsystem damaged by water
3. Battery damaged/failed (explains no battery power)
4. SMC/firmware state from water exposure (less likely given USB power works)

**Next steps:**

1. Try SMC reset (Shift+Control+Option+Power for 10s, then power on) -- may reset fan/power behavior
2. Inspect display connector on logic board (visible with back panel off) for corrosion/moisture
3. If connector looks corroded: disconnect, clean with 90% IPA on cotton swab
4. Check battery connector for corrosion (may explain battery power failure)
5. If still no display: may need motherboard extraction for detailed inspection (reference michael-pro June recovery for procedure)

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

- [2026-06-18_michael-pro_water-damage.md](../2026-06-18_michael-pro_water-damage.md) -- Reference procedures: battery disconnect, motherboard extraction, corrosion cleaning
- [CONTEXT.md](../CONTEXT.md) -- Device registry (wendy-pro specs)
