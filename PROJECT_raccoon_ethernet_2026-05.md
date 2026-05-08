# Project: Rascally Raccoon Ethernet Outage -- 2026-05

## Context

PtP internet link between Moe's house and RV stopped working Sunday 2026-05-04 between 02:00
and 09:00. Working at 02:00 (Netflix). Failed by 09:00 (email check). Half inch of rain
Saturday evening.

Device names and IPs: [CONTEXT.md](CONTEXT.md)
Physical topology: [Ubiquiti/HOWTO_rascally_raccoon_PtP_install.md](Ubiquiti/HOWTO_rascally_raccoon_PtP_install.md)
Normal data path: see CONTEXT.md

---

## CLI Quick Reference -- michael-pro Anker Adapter

Network service name: `USB 10/100/1000 LAN`

```bash
# Switch to DHCP (to get IP from spectrum-router through bridge)
networksetup -setdhcp "USB 10/100/1000 LAN"

# Check assigned IP and gateway
ipconfig getifaddr en7
ipconfig getoption en7 router

# Switch to manual (to access loco management IPs)
networksetup -setmanual "USB 10/100/1000 LAN" 192.168.1.100 255.255.255.0

# Ping loco management IPs (requires manual 192.168.1.100/24)
ping -c 4 192.168.1.21   # loco-station
ping -c 4 192.168.1.20   # loco-ap (via RF bridge)

# Test internet (requires DHCP address from spectrum-router)
ping -c 4 1.1.1.1
```

---

## DONE

- Confirmed cable-black-10ft, cable-green-3ft-a, cable-green-3ft-b, cable-outdoor-50ft all
  pass network signal individually
- Confirmed poe-rv and poe-moe both pass network signal inline (tested with and without
  injector powered)
- Confirmed loco-station alive and reachable at 192.168.1.21 -- direct connection test
- Confirmed loco-ap alive and reachable at 192.168.1.20 -- via RF bridge
- Confirmed PtP RF link healthy -- 302 Mbps capacity, signal -55 dBm, noise -87 dBm (32 dB SNR)
- Confirmed loco-ap configuration correct -- ACCESS POINT: On, PTP MODE: On
- Confirmed loco-station configuration correct -- ACCESS POINT: Off, PTP MODE: On
- Confirmed spectrum-router WAN port active (green LED -- internet present at Moe's house)
- Confirmed loco-ap Ethernet physically connected to spectrum-router -- port 1 shows yellow
  blinking (100 Mbps active; yellow vs green is expected for loco-ap's 10/100 port)
- Confirmed poe-moe installed at Moe's house powering loco-ap (Michael walked it up)
- Ordered tp-link-switch (TP-Link TL-SF1005D, 5-port 10/100) from Amazon -- 2026-05-04
- Confirmed spectrum-router LAN IP is 192.168.1.1 -- accessed admin UI from Moe's side
  2026-05-06; WAN IPv4 50.89.8.254; model SAC2V1A; S/N A5L4H956C14029; MAC A8:97:CD:70:61:D0
- **ROOT CAUSE FOUND 2026-05-06**: outdoor cable between poe-moe PoE port and loco-ap had
  animal chew damage (hawk/rooster incident site, feathers present near chew marks). Outer
  jacket nicked. Data pairs compromised; power pairs intact → loco-ap had power (blue LED)
  but no Ethernet data path. Replaced with new white cable + coupler. Cable test confirmed:
  michael-pro dongle → white cable → coupler → short black cable → spectrum-router passed data.
- **loco-ap fully restored** -- sub-10ms pings to 192.168.1.20 from Moe's WiFi confirmed.
  loco-ap was unreachable because cable broke its Ethernet data path -- not a firmware crash.
- **Full system restored 2026-05-06** -- internet confirmed working end-to-end:
  michael-pro WiFi → beryl → poe-rv → loco-station → RF → loco-ap → new cable → poe-moe →
  spectrum-router. wolf-air also confirmed. tp-link-switch not needed.
- Note: openwrt.lan at 192.168.1.55 present on Moe's LAN (Moe's own device, unrelated)

---

## WAITING

- ~~tp-link-switch delivery~~ -- system fully working without it; switch may still arrive

---

## TODO

- Monitor for 24 hours -- confirm link remains stable
- Protect new white cable + coupler from weather/animals (cable is now the critical run)
- When tp-link-switch arrives: keep as spare; beryl WAN may still have marginal magnetics

---

## Known

### Cables -- all verified good

Test method for each: michael-pro → anker-dongle → [cable under test] → wolfden-hotspot →
internet; pinged 1.1.1.1.

- **cable-black-10ft** passes network ✓
- **cable-green-3ft-a** passes network ✓
- **cable-green-3ft-b** passes network ✓
- **cable-outdoor-50ft** passes network ✓

### PoE Injectors -- both verified functional as pass-through

Test method: wolfden-hotspot → cable → injector LAN → injector PoE → cable → anker-dongle →
michael-pro; pinged 1.1.1.1. Tested both with injector powered and unpowered.

- **poe-rv** passes network inline ✓ (emitted audible buzz during Sunday diagnosis; swapped
  with poe-moe for testing; no functional difference observed)
- **poe-moe** passes network inline ✓

### loco-station

- **Alive and reachable at 192.168.1.21** -- confirmed ✓
- **beryl detects cable from loco-station chain** -- confirmed working 2026-05-06 after cable
  fix on Moe's side; no tp-link-switch required ✓

### loco-ap

- **Reachable at 192.168.1.20** via RF bridge from michael-pro at 192.168.1.100 ✓
- **airOS web UI accessible** at <http://192.168.1.20> in Safari ✓
- **PtP RF link: Connected** -- 302 Mbps capacity, -55 dBm signal, -87 dBm noise, 32 dB SNR
- **Ethernet physically connected to spectrum-router** -- port 1 on spectrum-router shows yellow
  blinking (100 Mbps active) ✓
- **Management radio temporarily active** -- ~3-hour countdown timer in airOS; triggered during
  today's diagnosis; will expire automatically; not a configuration error; does not affect PtP
  operation
- **airView disabled on loco-ap** (red "i" bubble) -- expected: loco-ap has ACCESS POINT On and
  is actively transmitting; passive scanning cannot run while transmitting. loco-station shows
  blue/green airView spectrum because it has ACCESS POINT Off (passive).

### beryl

- **LAN functional** ✓
- **WAN detects cable from loco-station via injector** -- confirmed working 2026-05-06 ✓
- **Internet confirmed** -- wolf-air and michael-pro both routing through beryl → PtP → spectrum ✓

### spectrum-router

- **Internet port active** -- green LED on WAN port ✓
- **LAN IP confirmed 192.168.1.1** -- accessed admin UI from Moe's side 2026-05-06 ✓
- **WAN IPv4 50.89.8.254** -- internet connected ✓
- **Model SAC2V1A, S/N A5L4H956C14029, MAC A8:97:CD:70:61:D0**
- **Port 1 (to loco-ap) active at 100 Mbps** -- yellow blinking LED ✓ (as of 2026-05-04)

---

## Forensic Post-Mortem -- 2026-05-08

### Physical Inspection

Cable cut open after replacement. Found: **solid green wire (pin 6) nicked** by animal.
Outer jacket had visible chew mark; inner damage was to the solid green conductor only.

### Animal Identification (Revised)

Moe believes **mouse or squirrel**, not hawk. Prior note listed hawk as likely culprit based
on feathers at the site. Feathers were from the earlier hawk/rooster incident; the cable chew
is a separate event by a different animal.

### Why Solid Green = Fatal for Data

T568B wiring (North American standard):

| Pins     | Wires                         | Function                |
|----------|-------------------------------|-------------------------|
| 1, 2     | white/orange + solid orange   | TX+ / TX- (transmit)    |
| **3, 6** | **white/green + solid green** | **RX+ / RX- (receive)** |
| 4, 5     | blue + white/blue             | PoE power               |
| 7, 8     | white/brown + solid brown     | PoE power               |

10/100 Mbps uses only pins 1,2,3,6 for data. PoE rides on 4,5,7,8.
Solid green = pin 6 = RX-. Nicking one wire of a differential pair destroys the pair.

Result: **receive pair dead → no Ethernet data. Power pairs intact → loco-ap stayed powered
(blue LED).** RF radio runs on PoE → RF link to loco-station unaffected. Exactly matches
observed symptoms.

### Why the Groundhog Test Failed

General principle (animals won't chew cable for fun/food) held for scent-neutral environments.
Failure mode here: cable ran through the hawk/rooster kill site. Fat, blood, and feather
residue contaminated the area. Mouse or squirrel investigating food scent gnawed whatever was
in the way. **Scent contamination is the confounding variable** the test doesn't cover.

### Splice Options Considered

Wire nuts and solder work for DC but fail at 100 MHz (100BASE-TX uses 100 MHz differential
signaling). Impedance discontinuities from untwisted wire at splice points cause reflections
that corrupt data. Wire nuts require ~1-2" of untwisted wire -- spec allows ≤0.5" at
termination. Soldering with careful staggering might survive at 10 Mbps; unlikely at 100 Mbps.

**Correct repair: RJ45 coupler** (which is what was done). Two properly crimped ends joined
by a coupler maintains impedance geometry. Spec-legal field repair for this scenario.

---

## Root Cause -- Confirmed

**Chewed cable between poe-moe PoE port and loco-ap broke Ethernet data pairs.**

An animal (likely a hawk -- feathers and chew marks found at same location near where a hawk
caught a rooster months earlier) chewed the outdoor cable running from poe-moe's PoE output
to loco-ap. The outer jacket was nicked but not deeply. The data pairs (pins 1,2,3,6) were
compromised; the power pairs (pins 4,5,7,8) remained intact.

Result: loco-ap received 24V passive PoE and stayed powered (blue LED present), but had no
Ethernet data path to spectrum-router. The bridge was broken at the Ethernet layer.
loco-station's RF association with loco-ap stayed up (RF layer is independent of Ethernet),
but loco-station had no live bridge to sustain proper Ethernet output toward beryl. beryl WAN
-- which may already have slightly weaker magnetics from an earlier passive PoE incident --
could not detect loco-station's weakened/inactive signal, though it could detect wolfden-hotspot
(stronger gigabit signal).

**Fix:** replaced chewed cable with new white cable + coupler. Full chain restored immediately.
tp-link-switch was not needed.

## Prior Hypothesis (superseded)

The earlier hypothesis (beryl WAN magnetics degraded by accidental passive PoE exposure) was
plausible and consistent with observed data at the time, but was not the primary cause.
beryl WAN may still be marginally weaker than spec -- keep tp-link-switch as a spare.

**Conflicting / uncertain data (documented honestly):**

- RF link showed 302 Mbps / -55 dBm even when cable was broken -- not conflicting, RF metrics
  are independent of Ethernet; loco-ap's radio ran fine with broken Ethernet
- beryl detected loco-station without tp-link-switch once cable was fixed -- suggests beryl WAN
  is functional, but signal margin is unknown
- From Ethernet dongle (.100/24), could not reach iPhone at .8 (WiFi client, same /24) --
  possibly real spectrum-router behavior, possibly macOS dongle initialization issue; unresolved

---

## End-of-Day Health Check -- 2026-05-06 17:15 EDT

All systems nominal. Full PtP internet path verified from RV (wolf-air on beryl).

```text
ping 192.168.1.20  →  loco-ap      0% loss  avg 14 ms  (RF bridge hop -- normal)
ping 192.168.1.21  →  loco-station 0% loss  avg  3 ms  (local Ethernet hop -- normal)
ping 1.1.1.1       →  internet     0% loss  avg 27 ms  (normal for Spectrum ISP)
```

Data path confirmed: wolf-air → beryl → poe-rv → loco-station → RF → loco-ap → poe-moe → spectrum-router → internet

---

## Unknown / Unresolved

- Exact nature of Sunday power event at Moe's house
- Whether Moe's devices had internet Sunday AM (never confirmed)
- Whether poe-rv is degraded vs normal behavior (buzz observed; not load-tested independently)
- Whether beryl WAN magnetics are marginally degraded -- functional now, but signal margin
  unknown; tp-link-switch kept as spare in case it becomes an issue again
- **Why loco-station's Ethernet output was insufficient for beryl to detect** when loco-ap's
  cable was broken -- RF association between locos was maintained throughout; mechanism by which
  loco-ap's broken Ethernet affected loco-station's Ethernet output is unresolved (see Root
  Cause section)
