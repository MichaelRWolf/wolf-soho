# Trails End Summer 2026 Log

**Location**: Trails End Campground (2026-07-08 through October 2026)

## 2026-07-08: WiFi throughput collapse -- good signal, bad uplink pipe

**Time**: ~5:00-6:00 PM (1 hour)
**Symptoms**: Unusably low throughput despite good signal strength

- Download: 0.25 Mbps
- Upload: 0.00 Mbps
- Signal at RV: -60 dBm (good)
- Signal at welcome sign: -55 dBm (good)

**Diagnosis**: Signal strength normal; uplink pipe degraded (ISP/backhaul issue, not local RF)

**Resolution**: Recovered at 6:00 PM on its own; no manual intervention required

**Follow-up @ 17:51**: Speedtest CLI returns `HTTP Error 403: Forbidden` on "Running Wolf Router" SSID.

**Follow-up @ 18:05**: Speedtest works from "Trails End Wifi" SSID:

- Download: 5.56 Mbps
- Upload: 2.49 Mbps
- Latency: 77.826 ms (NCR 153.66.57.242 → Omni Fiber, Columbus OH)

**Finding**: SSID-dependent routing issue. "Running Wolf Router" blocked/misconfigured; "Trails End Wifi" works. Check: beryl DNS/DHCP config for "Running Wolf Router", or WAN path routing asymmetry between SSIDs.

**RECURRENCE @ 6:30 PM**: Complete internet outage -- cannot ping 1.1.1.1 or reach any service. Traceroute to speedtest.net hangs at hop 7; <www.speedtest.net> (Cloudflare) completed at 6:17 PM before collapse.

**Status**: Currently investigating. Need: RF link status, Moe's-side connectivity, beryl WAN state.

**Notes**: Confirms that signal strength alone is not a complete picture of link quality. Future troubleshooting should include backhaul diagnostics (modem stats, carrier signal levels at Moe's).

---

## 2026-07-09: loco-bridge Setup & Authentication Blocker

**Location:** Trails End CG (AM) + downtown park (PM)

**Setup completed:**

- Configured `loco-bridge` (NanoStation Loco5AC) static IP 192.168.1.22
- Created `Ubiquiti-Setup` macOS network location (Belkin USB-C LAN, static 192.168.1.100)
- Disabled WPA2 mode via telnet/sed for open SSID support
- Identified "Trails End Crew" as target Ubiquiti mesh SSID

**Key finding:**

- **"Trails End Crew" is open/unencrypted** (no password). Crew member mentioned password, but network requires no auth.
- loco-bridge was failing to connect because WPA2 was enabled; changed Security setting to Open/None resolves it.
- Tested with public network (GrantTownshipPastyFree at downtown park) confirms both are 802.11n open networks.

**Outstanding:**

- Full Cat5 chain test (loco-bridge → beryl) deferred to next Trails End session (no USB-C Ethernet dongles in park)
- loco-bridge → "Trails End Crew" authentication pending field validation

**Next session:**

1. Change loco-bridge SSID to "Trails End Crew" and Security to Open
2. Verify "Remote: Connected" on dashboard
3. Run Cat5 to beryl, test network access from RV interior
4. Measure signal strength and throughput from cone zone (100 ft from mesh antenna)

---

## Equipment Comparison -- Dual-Band Outdoor APs (Strategy C Candidates)

**Decision Criteria** (from 2026-07-11 log):

- Dual-band (2.4 + 5 GHz)
- Standard WiFi (802.11ac or newer), not proprietary protocols
- Outdoor IP rating
- PoE powered
- Client/AP/bridge modes

### MikroTik GrooveA 52 ac (Reference)

| Spec               | Value                                 |
|--------------------|---------------------------------------|
| **Standard**       | 802.11ac (WiFi 5)                     |
| **Bands**          | 2.4 GHz + 5 GHz (dual-band)           |
| **Throughput**     | ~867 Mbps                             |
| **Antenna**        | Omni 6 dBi (2.4 GHz), 8 dBi (5 GHz)   |
| **PoE**            | Passive PoE in (5W)                   |
| **IP Rating**      | IP54                                  |
| **Ethernet**       | 1x Gigabit RJ45                       |
| **Operating Temp** | -20°C to +60°C                        |
| **Price (USD)**    | $88-99                                |
| **Modes**          | Client, AP, Bridge, Router (RouterOS) |
| **Power Draw**     | ~5 W                                  |
| **Footprint**      | Small outdoor rackmount               |

### TP-Link EAP225-Outdoor (B&H Specs 2026-07-12)

| Spec               | Value                                                  |
|--------------------|--------------------------------------------------------|
| **Standard**       | 802.11ac (WiFi 5)                                      |
| **Bands**          | 2.4 GHz + 5 GHz (dual-band)                            |
| **Throughput**     | 1200 Mbps total (300 Mbps @ 2.4 GHz, 867 Mbps @ 5 GHz) |
| **Antenna**        | 2x external detachable, 3-4 dBi                        |
| **PoE**            | 802.3af (15.4 W) passive PoE injector included         |
| **IP Rating**      | IP65                                                   |
| **Ethernet**       | 1x Gigabit RJ45                                        |
| **Operating Temp** | -30°C to +70°C                                         |
| **Price (USD)**    | ~$150-180 (B&H: $69.99 sale)                           |
| **Modes**          | Access Point (standard WiFi)                           |
| **Power Draw**     | 10.5 W                                                 |
| **Management**     | Omada Controller (cloud or local)                      |
| **Mounting**       | Pole, Wall (kits included)                             |

### Comparison Summary

| Factor                    | GrooveA 52 ac              | EAP225-Outdoor      | Winner      |
|---------------------------|----------------------------|---------------------|-------------|
| **Dual-band**             | ✓ (2.4 + 5)                | ✓ (2.4 + 5)         | Tie         |
| **Standard WiFi**         | ✓ (802.11ac)               | ✓ (802.11ac)        | Tie         |
| **IP Rating**             | IP54                       | **IP65**            | EAP225      |
| **Antenna modularity**    | Fixed omni                 | **2x detachable**   | EAP225      |
| **PoE Power**             | Passive (5W)               | **802.3af (15.4W)** | EAP225      |
| **Operating range**       | -20 to +60°C               | **-30 to +70°C**    | EAP225      |
| **Management complexity** | RouterOS (steep)           | Omada (standard)    | **EAP225**  |
| **Modes available**       | Client, AP, Bridge, Router | **AP only**         | GrooveA     |
| **Cost**                  | $88-99                     | $150-180            | **GrooveA** |
| **Weight/size**           | Compact                    | Larger (wall/pole)  | GrooveA     |
| **Power budget**          | Tight (5W passive PoE)     | Better (15.4W)      | **EAP225**  |

### Assessment

**TP-Link EAP225-Outdoor:**

- Better weatherproofing (IP65 vs IP54)
- Higher power budget (15.4W vs 5W) → can drive external antenna relays, active optics
- Modular antenna design → directional pointing at Trails End Crew mesh AP
- Omada management more familiar than RouterOS
- **Limitation:** AP mode only (no bridge/router functions)
- **Fit for Strategy C:** Excellent; designed as secondary mesh-connected router

**MikroTik GrooveA 52 ac:**

- Lower cost ($88 vs $180)
- Full routing/bridge capabilities via RouterOS
- Passive PoE only (tight power budget for long Cat5 runs)
- Fixed omni antenna (less flexible for directional alignment)
- **Fit for Strategy C:** Good but overkill if AP mode sufficient; RouterOS learning curve

### Next Steps

1. **Trial:** Deploy EAP225-Outdoor at identified hot zone (near Welcome Antenna or Barn ridge)
2. **Power:** Verify PoE injector can deliver 15.4W over planned Cat5 distance (~100-300 ft)
3. **Antenna:** Position detachable antennas toward Trails End Crew mesh, away from RV
4. **Bridge config:** Test Omada controller setup for transparent bridging to Beryl
5. **Fallback:** If EAP225 insufficient, evaluate GrooveA 52 ac for comparison trial
