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

| Time              | Action                                                                                                                                                     |
|-------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 2026-06-18        | Incident discovered; machine wet, appears off                                                                                                              |
| 2026-06-18        | Back screws removed (6 of 6); panel not yet free                                                                                                           |
| 2026-06-18        | Front edge (opposite hinge) lifting; hinge corners still seated                                                                                            |
| 2026-06-18        | Panel removed                                                                                                                                              |
| 2026-06-18        | Battery disconnected; electrical tape between connector and socket                                                                                         |
| 2026-06-18 ~09:30 | Drying begun -- fan blowing across open interior, hinge-down V-orientation, open box                                                                       |
| 2026-06-21 18:00  | Switched to heat: removed fan; placed 30W incandescent bulb 8 inches from back                                                                             |
| 2026-06-22 12:30  | Removed light/heat source; inspected board bottom; found 4 locations of white corrosion                                                                    |
| 2026-06-22 13:30  | Board in strong sun (back black components >110°F); applied 70% IPA; small fan running                                                                     |
| 2026-06-22 ~14:00 | Discovered IPA was ear drops (50/50 vinegar + 70% IPA); rinsed with well water; moved to shade with fan in driver seat; awaiting distilled water + 91% IPA |
