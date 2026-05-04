# Project: Rascally Raccoon Ethernet Outage — 2026-05

## Context

PtP internet link between Moe's house and RV stopped working Sunday 2026-05-04 between 02:00
and 09:00. Working at 02:00 (Netflix). Failed by 09:00 (email check). Half inch of rain
Saturday evening.

Device names and IPs: [CONTEXT.md](CONTEXT.md)
Physical topology: [Ubiquiti/HOWTO_rascally_raccoon_PtP_install.md](Ubiquiti/HOWTO_rascally_raccoon_PtP_install.md)
Normal data path: see CONTEXT.md

---

## CLI Quick Reference — michael-pro Anker Adapter

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
- Confirmed loco-station alive and reachable at 192.168.1.21 — direct connection test
- Confirmed loco-ap alive and reachable at 192.168.1.20 — via RF bridge
- Confirmed PtP RF link healthy — 302 Mbps capacity, signal -55 dBm, noise -87 dBm (32 dB SNR)
- Confirmed loco-ap configuration correct — ACCESS POINT: On, PTP MODE: On
- Confirmed loco-station configuration correct — ACCESS POINT: Off, PTP MODE: On
- Confirmed spectrum-router WAN port active (green LED — internet present at Moe's house)
- Confirmed loco-ap Ethernet physically connected to spectrum-router — port 1 shows yellow
  blinking (100 Mbps active; yellow vs green is expected for loco-ap's 10/100 port)
- Confirmed poe-moe installed at Moe's house powering loco-ap (Michael walked it up)
- Ordered tp-link-switch (TP-Link TL-SF1005D, 5-port 10/100) from Amazon — 2026-05-04

---

## WAITING

- **tp-link-switch delivery** — Amazon, ordered 2026-05-04

---

## TODO

After tp-link-switch arrives:

1. Insert tp-link-switch between injector LAN port and beryl WAN port
2. Confirm beryl WAN shows cable detected
3. Confirm beryl WAN gets DHCP/WAN IP from spectrum-router through PtP bridge
4. Ping 1.1.1.1 from RV device on running-wolf-router
5. Confirm 192.168.1.20 and 192.168.1.21 accessible from michael-pro via beryl (normal
   management path)
6. Reassemble full production chain and monitor for 24 hours

---

## Known

### Cables — all verified good

Test method for each: michael-pro → anker-dongle → [cable under test] → wolfden-hotspot →
internet; pinged 1.1.1.1.

- **cable-black-10ft** passes network ✓
- **cable-green-3ft-a** passes network ✓
- **cable-green-3ft-b** passes network ✓
- **cable-outdoor-50ft** passes network ✓

### PoE Injectors — both verified functional as pass-through

Test method: wolfden-hotspot → cable → injector LAN → injector PoE → cable → anker-dongle →
michael-pro; pinged 1.1.1.1. Tested both with injector powered and unpowered.

- **poe-rv** passes network inline ✓ (emitted audible buzz during Sunday diagnosis; swapped
  with poe-moe for testing; no functional difference observed)
- **poe-moe** passes network inline ✓

### loco-station

- **Alive and reachable at 192.168.1.21** — test: michael-pro (manual IP 192.168.1.100/24) →
  anker-dongle → injector LAN → injector PoE → loco-station; pinged 192.168.1.21 ✓
- **anker-dongle detects cable from injector/loco-station chain** — link established, ping
  worked ✓
- **beryl does NOT detect cable from injector/loco-station chain** — tested on both beryl WAN
  and beryl LAN ports; neither showed cable detected. wolfden-hotspot does show cable on beryl
  using the same cables. The variable is the device on the far end of the cable from beryl.

### loco-ap

- **Reachable at 192.168.1.20** via RF bridge from michael-pro at 192.168.1.100 ✓
- **airOS web UI accessible** at http://192.168.1.20 in Safari ✓
- **PtP RF link: Connected** — 302 Mbps capacity, -55 dBm signal, -87 dBm noise, 32 dB SNR
- **Ethernet physically connected to spectrum-router** — port 1 on spectrum-router shows yellow
  blinking (100 Mbps active) ✓
- **Management radio temporarily active** — ~3-hour countdown timer in airOS; triggered during
  today's diagnosis; will expire automatically; not a configuration error; does not affect PtP
  operation
- **airView disabled on loco-ap** (red "i" bubble) — expected: loco-ap has ACCESS POINT On and
  is actively transmitting; passive scanning cannot run while transmitting. loco-station shows
  blue/green airView spectrum because it has ACCESS POINT Off (passive).

### beryl

- **LAN functional** — michael-pro received 192.168.8.249 from beryl DHCP ✓
- **WAN does not detect cable from loco-station via injector** (see loco-station section above)
- **WAN does detect cable from wolfden-hotspot** — same cable-green-3ft used in both tests

### spectrum-router

- **Internet port active** — green LED on WAN port ✓
- **LAN IP is not 192.168.1.1** — could not ping 192.168.1.1 from michael-pro at
  192.168.1.100/24; actual LAN IP unknown
- **Port 1 (to loco-ap) active at 100 Mbps** — yellow blinking LED ✓

---

## Root Cause Hypothesis

**beryl WAN port magnetics degraded by accidental passive PoE exposure.**

A few days before the outage, the injector PoE output port was accidentally connected to beryl
WAN (cables swapped at the injector). Passive 24V PoE has no device detection — it puts 24V
unconditionally on pins 4,5,7,8 (spare pairs). The beryl WAN port is gigabit; gigabit PHYs
drive signals on all 4 pairs including spare pairs. The transformer magnetics in Ethernet ports
are rated for millivolt-level DC; 24V can saturate or permanently damage them.

The beryl WAN continued working for a few days after the accident. The Sunday power event at
Moe's (loco-ap flapping or down) likely caused loco-station to crash, producing a transient
that pushed the already-degraded beryl WAN below threshold.

Result: strong signals (wolfden-hotspot gigabit) still register on beryl WAN; weak signals
(loco-station 100 Mbps through injector) do not.

**Fix:** tp-link-switch (10/100 only) inserted between injector LAN and beryl WAN. The switch
regenerates a clean, strong signal on the beryl side. Because the switch is 10/100-only, it
never drives signals on spare pairs (4,5,7,8) on the injector side, avoiding the PoE voltage
entirely.

---

## Unknown

- Whether tp-link-switch fully resolves beryl WAN detection (expected: yes)
- Whether beryl WAN port is permanently degraded or marginal (tp-link-switch test will reveal)
- Exact nature of Sunday power event at Moe's house
- Whether loco-station firmware crashed Sunday due to RF link instability, or loco-station
  Ethernet degraded independently
- spectrum-router LAN IP (not 192.168.1.1)
- Whether Moe's devices had internet Sunday AM (never confirmed)
- Whether poe-rv is degraded vs normal behavior (buzz observed; not load-tested independently)
- Current physical state of full RV chain (system partially disassembled for testing as of
  2026-05-04)
