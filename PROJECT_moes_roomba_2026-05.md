# Project: Moe's Roomba -- Standalone Operation

---

## STICKY NOTE -- MOE'S CHEAT SHEET

### Start cleaning

1. Press **CLEAN** (big center button)
2. Wait 2 seconds for ring to light up
3. Press **CLEAN** again → it goes

### Send it home while it's running

Press the button with the **house** on it. Wait. It finds the dock itself.
(Did not respond during first post-move run -- blue light mode. Should work normally after that.)

### Cut it loose from Sonia's phone forever

Hold **HOME** (house) + **SPOT** (4 dots) at the same time for **10 seconds** until it beeps.
Done. It's Moe's now. No app, no account, no interference.

---

## Goal

Let Moe use the Roomba like a 2005 robot: press CLEAN, it cleans, it docks. No app, no
account, no phone needed. Sonia is away for months and should not be bothered.

## Device

- **Model:** iRobot Roomba i7 (regulatory model RVB-Y1)
- **FCC ID:** ZW9AXCY1
- **Account:** Registered to Sonia's iRobot HOME account (unknown credentials)
- **Network:** Connected (or previously connected) to `spectrum-wifi` at Moe's house

---

## Recommended Next Action

**Sever WiFi -- do this before handing off to Moe.**

Hold **HOME + SPOT** simultaneously for ~10 seconds until a tone sounds.

- Erases WiFi credentials only
- Maps preserved
- Buttons unchanged
- Eliminates all couplings to Sonia's app (see table below)

| Coupling severed     | Why it matters                                   |
|----------------------|--------------------------------------------------|
| DND schedule         | Her quiet-hours silently block Moe's CLEAN press |
| Scheduled cleans     | Her scheduled runs fire without Moe asking       |
| Remote control       | She can start, stop, cancel from her phone       |
| Firmware push        | iRobot can change behavior remotely              |
| Map/status reporting | She sees when and where it ran                   |

After severance: `moes-roomba` is a $500 Roomba from 2005. Exactly right for Moe.

---

## If Sonia Comes Back

To re-couple to her account:

1. Download **iRobot HOME** app (or she already has it)
2. On the robot: hold **CLEAN** for ~2 seconds until a tone and spinning ring
3. Follow in-app Wi-Fi setup
4. Robot re-registers to her account and her maps/schedules resume

Do NOT factory reset -- her maps survive a WiFi-only reset and will still be there.

---

## Status (2026-05-06)

- Home base was unplugged -- plugged back in
- Roomba placed on base, showed swirling white light around CLEAN button (charging)
- After a few minutes: triumphant startup sound, base light off, unit dark (fully charged / idle)
- Pressed CLEAN: upbeat signal, unit started moving ✓
- **Physical CLEAN button works** -- basic operation confirmed without app

### Wake-from-sleep behavior (confirmed normal)

After sitting in dock fully charged, `moes-roomba` enters sleep mode (ring goes dark). Two presses required:

1. **First press** -- quick high-pitch tone up a half-step; circling white ring appears (robot wakes)
2. **Wait** ~2 seconds for ring to fully illuminate
3. **Second press** -- starts the clean cycle and robot moves

The wait between presses is critical. Press too fast and the second press is ignored. Long-press
by accident and it sends the robot home. iRobot's UX expects you to read the manual.

### Dock relocated (2026-05-06)

Dock moved from **right side of TV** to **left side of TV** -- 90 degrees off, on a separate
wall. TV is in a corner. On first run after move, robot showed blue circling multi-light ring
(remapping/relearning mode) and did forward/back orientation moves before proceeding. Left
running; expected to complete and dock.

Map will self-correct over 2-3 runs from the new position. No app action needed.

---

## Key Facts

The Roomba i7 physical buttons work completely independently of the app, WiFi, and account.

- **CLEAN** (big center) -- start a clean cycle
- **HOME** (house icon) -- send it back to dock mid-clean
- **SPOT** (4 dots) -- clean a small area only

The app is only needed for scheduling, maps, remote start, notifications. Moe needs none of that.
