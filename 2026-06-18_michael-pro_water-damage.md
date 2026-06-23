# 2026-06-18 michael-pro Water Damage

**Device**: `michael-pro` -- MacBook Pro 13-inch 2020, A2251 (MacBookPro16,2)

## Incident

- Left in canvas bag; rain accumulated ~2 inches of water over ~1.5 hours
- Machine appears to have timed out and powered off before discovery
- Discovered wet; recovery in progress

## Immediate Goal: Disconnect Battery Before Any Drying

Power must stay off and battery must be disconnected before patting dry or using drying methods.
Do NOT attempt to power on.

---

## Step 1 -- Remove Back Panel

**Screwdriver required**: P5 Pentalobe (the screws are pentalobe, not Phillips)

The A2251 has 6 pentalobe screws:

- 4 short screws -- along one edge (bottom/top of the panel)
- 2 longer screws -- opposite side, in the corners

**All 6 screws removed. Panel not yet free.**

If the back panel won't lift after all screws are out:

1. Do NOT pry hard at the hinge end -- ribbon cables run there.
2. Insert a plastic spudger or opening pick into the gap at the **front edge** (opposite the hinge).
3. Slide the pick along the **left and right sides**, gently breaking the adhesive/friction seal.
4. Lift the panel from the front edge -- it hinges up slightly toward the hinge end, then lifts free.
5. Set panel aside.

---

## Step 2 -- Disconnect Battery

Once inside:

1. Locate the **battery connector** -- a small rectangular ZIF connector on the **right side** of the logic board (right side when lid is open/screen facing you), near the battery cells.
2. Use a **plastic spudger** -- do NOT use metal tools near the connector.
3. Gently lever the connector **straight up** to unplug it from its socket on the logic board.
4. Confirm it is fully seated out -- connector should be visibly separated from the socket.

**Do NOT cut any wires.**

---

## Step 3 -- Dry Before Any Power-On

- Pat visible moisture with lint-free cloth
- Allow extended drying time (48-72 hours minimum) before reconnecting battery or powering on
- Consider silica gel packs or dry enclosure

## Drying Notes (2026-06-20, mid-72h)

### Heat

- Fan alone won't help water under keyboard gaskets or speaker covers -- fan air can't reach there
- Heat conducts through chassis and warms trapped water; vapor pressure builds and pushes out through seals
- Target 100--120°F (38--49°C) -- well below adhesive softening (~140°F+)
- Use heat source in open box (airflow but not a direct cooling breeze on the board)
- Fan and heat together fight each other -- alternate: 45 min heat, 15 min fan to flush vapor
- Ambient 75°F / 65% RH (2026-06-20) -- decent vapor pressure deficit; fan effective for open surfaces

### IPA (2026-06-20, ~36h in)

- Good time: bulk water gone, mineral residue forming -- IPA displaces before corrosion sets
- Use 90%+ IPA only (91% drugstore or 99%); 70% has too much water
- Douse and brush visually affected areas; IPA's low surface tension reaches crevices
- Tilt board to let IPA run off carrying dissolved minerals
- Turn fan on after -- IPA evaporates in minutes, no added wait time needed

---

---

---

## Motherboard - Remove and Clean

**Sources**:

- [MacBook Pro 13" Four Thunderbolt Ports 2020 Screen Replacement - iFixit](https://www.ifixit.com/Guide/MacBook+Pro+13-Inch+Four+Thunderbolt+Ports+2020+Screen+Replacement/143619)
- [MacBook Pro 13" Four Thunderbolt Ports 2020 Device Page - iFixit](https://www.ifixit.com/Device/MacBook_Pro_13%22_Four_Thunderbolt_Ports_2020)

### Remove Components Blocking Motherboard Access

Before the motherboard can be lifted free, several components must be disconnected/removed:

1. **Disconnect all flex cables on motherboard**:
   - Locate all ribbon cable connectors (ZIF style) on the logic board
   - Use a plastic spudger; lever each connector upward *straight up* (same as battery connector)
   - Common connectors on the A2251 motherboard (consult iFixit guide for exact locations):
     - Speaker/audio connectors
     - USB board connector
     - Keyboard/trackpad flex cable
     - Display backlight & video flex cables
     - Temperature/sensor flex cables
     - Touch ID flex cable (if present)

2. **Remove SSD (if needed for full board clearance)**:
   - SSD is typically a small M.2 drive mounted on the bottom of the logic board
   - One tiny screw holds it at an angle; remove screw and flip SSD out

3. **Remove thermal pad/spreader** (if blocking access):
   - Some thermal pads may need gentle peeling if they adhere the motherboard to the chassis

4. **Remove logic board screws**:
   - The logic board is held down by multiple small pentalobe screws (P5)
   - Consult iFixit Screen Replacement guide (step 8-12 region) for exact screw locations and count
   - Typical count: 6-8 screws around the board perimeter and near the logic board bracket
   - Remove all screws, storing them in order (different lengths)

5. **Lift motherboard free**:
   - Once all screws and connectors are removed, gently lift the motherboard from the corner opposite any bracket hinges
   - Be aware of any remaining adhesive or thermal interface material
   - Set board aside on an **ESD-safe mat or non-static surface** (clean cardboard works)

### Inspect Top Side for Corrosion

1. **Examine components under direct light**:
   - Look for **white, blue, or green deposits** on:
     - Solder joints near connectors
     - Component legs (resistors, capacitors, inductors)
     - The logic board traces around high-current areas (power delivery, memory, CPU socket region)
   - Water ingress typically pools near battery connector, keyboard flex cable entry, and speaker connections

2. **Document corrosion locations**:
   - Note coordinates or describe location relative to visible landmarks (Touch ID area, USB connector area, etc.)
   - Take photos for reference before cleaning

### Clean Corroded Areas with Distilled Water & 91% IPA

**Tools & Materials**:

- **91% IPA** (isopropyl alcohol) -- use 91% drugstore or higher; 70% IPA contains too much water and will worsen corrosion
- **Distilled water** (to rinse before IPA)
- **Soft brush** (old toothbrush or brass wire brush, non-conductive)
- **Lint-free cloth** (wipe down after cleaning)
- **Small container** for soaking (glass or ceramic, not plastic)
- **Drying fan** (to accelerate evaporation)
- **Clean cardboard or non-conductive mat** (to rest board during drying)

**Cleaning Sequence**:

1. **First rinse with distilled water**:
   - Apply distilled water to corroded areas with a brush or dropper
   - Gently agitate the corroded spots with a soft brush to break up mineral deposits
   - Let water drip off naturally (tilt board as needed)
   - Wipe excess water with lint-free cloth
   - Do NOT soak the entire board in water -- target affected areas only

2. **Follow with 91% IPA wash**:
   - Apply 91% IPA to the same areas immediately after water rinse (IPA displaces water and prevents re-corrosion)
   - Brush gently to dissolve remaining mineral residue
   - IPA's low surface tension penetrates crevices between component legs
   - Allow IPA to drain off; tilt board to channel IPA away from unaffected areas
   - Wipe with fresh lint-free cloth

3. **Repeat if necessary**:
   - If significant corrosion remains, repeat distilled water + IPA sequence
   - Stop if corrosion deposits are visibly gone or only faint staining remains (staining alone does not prevent function if corrosion is gone)

4. **Dry thoroughly**:
   - Position board on clean cardboard, component side up
   - Run a small fan across the board for 15-30 minutes to evaporate all moisture
   - Confirm board is visually dry (no wet sheen on components or traces)
   - IPA evaporates quickly; wait 5 minutes after IPA application before running fan to allow volatilization

### Reassemble

Once board is completely dry and corrosion is cleaned:

1. **Reverse removal steps**:
   - Reinstall all flex cable connectors (ZIF) by inserting each straight down into its socket and sliding the retention lever down until seated
   - Reinstall SSD if it was removed
   - Reinstall all motherboard screws in reverse order
   - Reattach thermal pads/spreaders

2. **Reconnect battery**:
   - Once board is fully seated and all other connectors are installed, reconnect the main battery connector
   - This can be done while the back panel is off, before closing the chassis

---

## TODO: Working Environment on wolf-air

### Email (ATT/Yahoo -- fragile, do in this order)

> **2026-06-20 finding**: Safari completes full browser login (email → password → SMS OTP → inbox).
> Chrome fails at OTP step -- correct 6-digit code entered, page reloads with errorCode=908 (OTP
> rejected server-side). Use Safari for browser-based att.net login until Chrome is resolved.
> See [ATT/password_fuckery.md](ATT/password_fuckery.md) for hypothesis and analysis.

- [ ] Open **Safari** (Chrome fails at OTP as of 2026-06-20): `open -a Safari "https://mail.yahoo.com/"`
- [ ] Sign in with `michaelrwolf@att.net` + ATT password (NOT Secure Mail Key)
- [ ] Confirm inbox loads -- if "It's not you, it's us" see `ATT/password_fuckery.md` for escalation wording
- [ ] Navigate to ATT security settings: `open "https://www.att.com/my/#/profile/security"`
- [ ] Generate a new Secure Mail Key for wolf-air; store in 1Password
- [ ] Open Mail.app on wolf-air -- Add Account -- Yahoo
  - Email: `michaelrwolf@att.net`
  - Password: **Secure Mail Key** (not ATT password)
- [ ] Confirm mail syncing in Mail.app

### Environment Parity (wolf-air vs michael-pro)

- [ ] Audit SSH keys -- confirm wolf-air has keys for GitHub and any servers michael-pro had
- [ ] Check shell config -- `~/.zshrc`, `~/.bashrc`, Portable_Profile repo up to date
- [ ] Verify Homebrew packages match (compare `brew list` outputs)
- [ ] Check dev repos -- confirm all active repos are cloned and up to date on wolf-air
- [ ] Identify any other apps that were michael-pro-exclusive

---

## TODO: Prepare for Pinnacle Interview

- [ ] Find Zoom link for Pinnacle interview
- [ ] Verify Zoom link in calendar event (Google Calendar or Apple Calendar)
- [ ] Verify Zoom link in notes file (Job_Search repo)
- [ ] Create opportunity entry in Job_Search repo for Pinnacle

---

## Status Log

| Time              | Action                                                                                                                                                                  |
|-------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 2026-06-18        | Incident discovered; machine wet, appears off                                                                                                                           |
| 2026-06-18        | Back screws removed (6 of 6); panel not yet free                                                                                                                        |
| 2026-06-18        | Front edge (opposite hinge) lifting; hinge corners still seated                                                                                                         |
| 2026-06-18        | Panel removed                                                                                                                                                           |
| 2026-06-18        | Battery disconnected; electrical tape between connector and socket                                                                                                      |
| 2026-06-18 ~09:30 | Drying begun -- fan blowing across open interior, hinge-down V-orientation, open box                                                                                    |
| 2026-06-21 18:00  | Switched to heat: removed fan; placed 30W incandescent bulb 8 inches from back                                                                                          |
| 2026-06-22 12:30  | Removed light/heat source; inspected board bottom; found 4 locations of white corrosion                                                                                 |
| 2026-06-22 13:30  | Board in strong sun (back black components >110°F); applied 70% IPA; small fan running                                                                                  |
| 2026-06-22 ~14:00 | Discovered IPA was ear drops (50/50 vinegar + 70% IPA); rinsed with well water; moved to shade with fan in driver seat; awaiting distilled water + 91% IPA              |
| 2026-06-22 ~16:30 | Added Step 4 motherboard removal & corrosion cleaning procedure; iFixit references documented; ready for motherboard extraction once distilled water + 91% IPA acquired |
