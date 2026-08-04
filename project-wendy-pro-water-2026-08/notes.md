# wendy-pro Water Damage -- Recovery Project

**Device**: `wendy-pro` -- MacBook Pro 13-inch 2022 M2 (A2338)
**Incident Date:** 2026-08-03 (Trails End Campground, Copper Harbor MI)
**Status**: Partial boot, no display; diagnostics in progress

## Incident Summary

Water bottle broke in briefcase → liquid contacted laptop → opened back panel → found water intrusion centered around fan (likely air port ingress) → applied canned air → now drying in sun with fan.

**Current state:**

- Power: Both USB and battery power machine (confirmed 2026-08-04)
- Battery: Connected; powers machine (has water on bottom, not fully inspected)
- Display: Completely dark, no output on built-in screen
- Drying method: Sun (2026-08-03), overnight indoors, fan 2-3h (2026-08-04)
- **IPA applied: 2026-08-03 ~14:30-15:00 (completed)**
- **Reassembled: 2026-08-04 (batteries reconnected, bottom panel screwed)**
- **Power-on test: 2026-08-04 (24h post-IPA)** -- USB and battery both power machine

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
- [x] **2026-08-04 power-on test:** Machine boots on USB and battery (both work); fan on high, keyboard lights; no display output on internal screen.
- [x] **Battery status:** Confirmed working (stops fan when unplugged, restarts when replugged); water on bottom not fully inspected.
- [x] **External USB display test:** Recovery Assistant renders perfectly (graphics, battery indicator, WiFi indicator all functional). Logic board + GPU 100% working.
- [x] **Display behavior on power-off:** Brief red/orange splash observed on external USB display (~1/4 second). Internal Retina display remained completely dark. Splash indicates normal graphics output during shutdown sequence.
- [ ] Clean display cable connectors with 90% IPA + soft brush (address corrosion on hinge-side connectors)
- [ ] Power on and test internal display after connector cleaning
- [ ] If still no display: display cable or assembly replacement needed

## Troubleshooting: No Display (2026-08-04)

### External Display Testing (2026-08-04, afternoon)

**Connected USB-C external display:** Machine boots to Recovery Assistant on external display (full graphics, battery indicator, WiFi indicator, keyboard indicator all functional). Logic board and GPU confirmed working.

**Internal display behavior:** Completely dark during normal boot, but brief red/orange color splash observed when powering off (~1/4 second). Suggests display is receiving signal from logic board but connection is intermittent or degraded.

**Conclusion:** Logic board + GPU + USB display output all functional. Internal Retina display is receiving no signal (or signal is not reaching the panel). Issue is in the display connector, cable, or display assembly itself.

### Diagnostic Strategy: Connector → Cable → Display (Safe Inspection)

**Goal:** Determine root cause without powering a potentially water-damaged display.

### Phase 1: Connector Cleaning (SAFE - no power to display)

- Open back panel, locate display cable connector at hinge
- Disconnect press connector (gentle lift, no screws)
- Inspect connector pins visually (use magnifier) for corrosion, mineral deposits, water residue
- Clean both sides: 90% IPA + soft toothbrush on connector pins and socket
- Allow to dry completely (~5-10 min)
- Reconnect carefully
- Test protocol: Power on, connect external USB display, observe internal Retina display. If display works → problem solved. If not → proceed to Phase 2.

### Phase 2: Display Cable Inspection (SAFE - no power to display)

- With back panel still open and machine powered on (external display in use for visibility):
- Visually inspect the display cable from connector to hinge area
- Look for: water residue, corrosion, bent/damaged pins, disconnected sections
- Gently flex cable at hinge (where water was observed) while watching external display for any signal flicker
- If cable looks corroded: clean with 90% IPA on Q-tip (do NOT soak)
- Allow to dry, test again with external display

### Phase 3: Display Assembly Disassembly (LAST RESORT - must power display to test)

- Only if connectors + cable are clean and display still shows nothing
- Display panel must be powered to verify it's receiving/responding to signal
- Requires: full hinge disassembly, display panel removal
- Once separated, can safely power display (limited test: brief power pulse to confirm response)
- Inspect display connector on panel side for water damage

**Safety principle:** Only power the display after confirming connector/cable are clean and undamaged. If display is powered before cleaning, corrosion may create short circuits or permanent damage to the display IC chips.

**Symptoms:**

- Power: machine boots on both USB and battery (fan stops when USB unplugged, restarts when replugged)
- Keyboard: backlight lights up
- Display: completely black, no Apple logo, no output of any kind
- Audio: no startup sound/chime
- Abnormal fan behavior: starts high after 2-4 seconds (typical boot does not do this)
- Battery: has water on bottom but functions (not fully inspected)

**Likely causes (priority):**

1. Display cable connector corrosion (most common post-water-damage symptom)
2. Display cable (flex cable) internal damage from water exposure
3. Display assembly requiring replacement (if cable is clean but still no display)
4. Logic board display-management IC chips corroded

**Diagnostic steps (order matters):**

1. **External display test:** Connect external USB-C/Thunderbolt display (available) → if external display works, confirms logic board is functional and display/cable is the issue
2. **SMC reset:** Shift+Control+Option+Power for 10s (may reset fan/power state and display driver)
3. **Clean display connectors:** Open back panel, disconnect display cable, use 90% IPA + soft toothbrush to gently clean both connectors (motherboard side + cable side), reconnect and test
4. **If external display works but internal doesn't:** Display cable or assembly replacement needed (iFixit or Apple Authorized Service)
5. **If external display also fails:** Logic board damage; consider professional service

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
