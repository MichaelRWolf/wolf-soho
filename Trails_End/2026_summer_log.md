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
