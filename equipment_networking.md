# Networking Equipment

## `beryl` -- GL.iNet Beryl GL-MT1300

- Model: GL-MT1300
- Hostname: GL-MT1300-cd7
- MAC: 94:83:c4:11:9c:d8
- IP: 192.168.8.1 (LAN gateway)
- Role: RV primary router; NAT + DHCP
- SSIDs: running-wolf-router, running-wolf-router-5g, running-wolf-guest, running-wolf-guest-5g
- Docs: [beryl-cheat-sheet.md](GL-iNet/beryl-cheat-sheet.md)

## `Running Wolf PtP` - Ubiquiti PtP Link

- SSID: Running Wolf PtP
- Band: 5 GHz
- Channel width: 40 MHz
- Security: WPA2 Personal (PSK), AES
- Passphrase: 1Password -- "Wolfden -- Ubiquiti Running Wolf PtP -- WPA2 Link Key"
- airMAX: enabled
- PtP mode: enabled on both radios

### `loco-ap` -- Ubiquiti NanoStation Loco5AC

- Model: NanoStation Loco5AC (NanoStation 5AC loco)
- Role: PtP access point (master), house side
- IP: 192.168.1.20 (static, no gateway)
- MAC: 1C:6A:1B:CA:EF:9B
- Firmware: WA.ar934x.v8.7.11.46972.220614.0420 (verified 2026-05-12)
- Power: poe-moe (24V passive PoE)
- Web UI: <http://192.168.1.20> (Safari only)
- SSH: legacy algorithm flags required -- see [HOWTO_rascally_raccoon_PtP_config.md](Ubiquiti/HOWTO_rascally_raccoon_PtP_config.md)

### `loco-station` -- Ubiquiti NanoStation Loco5AC

- Model: NanoStation Loco5AC (NanoStation 5AC loco)
- Role: PtP station (client), RV side
- IP: 192.168.1.21 (static, no gateway)
- MAC: 1C:6A:1B:C6:E5:A3
- Firmware: WA.ar934x.v8.7.11.46972.220614.0420 (verified 2026-05-12)
- Power: poe-rv (24V passive PoE)
- Web UI: <http://192.168.1.21> (Safari only)
- SSH: legacy algorithm flags required -- see [HOWTO_rascally_raccoon_PtP_config.md](Ubiquiti/HOWTO_rascally_raccoon_PtP_config.md)

### PoE Injectors

- `poe-moe`: Ubiquiti POE-24-12W; at Moe's house; powers loco-ap
- `poe-rv`: Ubiquiti POE-24-12W; at RV; powers loco-station

## `wolfden-nas` -- Synology DS220j

- MAC: 00:11:32:EA:25:1B
- IP: 192.168.8.129 (static)
- Role: NAS; Time Machine; SMB shares
- Services:
  - Time Machine backups via HTTPS port 5001
  - SMB share: Backups
  - Self-signed cert: create_synology_cert script
- Docs: [Synology Management Notes](Synology/synology_mananagement.md)

## `running-wolf-hotspot` -- Netgear Nighthawk M1

- Model: Nighthawk M1 (AT&T; full model number TBD -- may be MR1100)
- IMEI: 015240000553847
- MAC (Ethernet LAN): 44:a5:6e:e9:59:26
- Admin IP: 192.168.1.1 (when connected via Ethernet; web UI at <http://192.168.1.1>)
- Firmware: TBD -- browser login to <http://192.168.1.1> → Settings → About needed
- Firmware clues: API verMajor=42 verMinor=0; server banner `httpd/2.7 (Netgear; D86)` (D86 = hardware variant)
- Role: Cellular/LTE hotspot; backup/travel internet
- Interfaces: Wi-Fi (2.4 + 5 GHz) and Ethernet LAN port (also USB tethering)
- SSID (primary, 2.4 GHz): Running Wolf Hot Spot
- SSID (5 GHz): Running Wolf Hot Spot - 5G (confirmed from device API)
- Carrier: AT&T (confirmed)
- SIM ICCID: 89014103334557770959
- SIM IMSI: 310410455780010
- SIM phone number: +1 (984) 381-5800
- LTE IPs (dynamic): IPv4 10.x.x.x / IPv6 2600::/28 block (AT&T)
- Known issue: overheats; workaround is ice pack
- Thermal data (observed): device ~61 °C, battery ~54 °C; battery state reports "Hot" -- confirms overheating

## `wolfden-mesh` -- Ubiquiti UAP-AC-M-US

- Model: UAP-AC-M-US
- Role: WiFi AP; integration pending
- MAC: D8:B3:70:CC:AA:7C
- Serial: EKHAMQ
- IP: 192.168.8.130 (planned)
- Purchased: 2025-07 from Amazon
- Status: integration pending
- Power: 24V passive PoE (POE-24-12W injector, not included)
- Docs: [device_info.md](Ubiquiti/device_info.md)

## `spectrum-router` -- Spectrum SAC2V1A

- Serial: A5L4H956C14029
- MAC: A8:97:CD:70:61:D0
- WAN IPv4: 50.89.8.254
- Firmware: 7.0.1-1-795640-g202508082008-SAC2V1A-prod (verified 2026-05-12)
- Location: Moe's house; upstream ISP gateway
- Admin: Moe (credentials in 1Password if shared)

## Trails End Campground (Summer 2026)

### `loco-bridge` -- Ubiquiti NanoStation Loco5AC

- Model: NanoStation Loco5AC (5 GHz only)
- Role: WiFi client (Station mode); bridges "Trails End Wifi" mesh → Cat5 → Beryl (RV)
- IP: 192.168.1.22 (static, no gateway)
- MAC: TBD (confirm via web UI at <http://192.168.1.22>)
- Power: poe-trails-end (24V passive PoE)
- Web UI: <http://192.168.1.22> (Safari only)
- SSH: legacy algorithm flags required -- see [HOWTO_campground_wifi_repeater_setup.md](Ubiquiti/HOWTO_campground_wifi_repeater_setup.md)
- Docs: [HOWTO_campground_wifi_repeater_setup.md](Ubiquiti/HOWTO_campground_wifi_repeater_setup.md)

### Trails End Mesh Antenna Registry

**Authoritative Source:** [Trails_End/antenna_survey.md](../Trails_End/antenna_survey.md)

**Quick Reference:**

| Antenna              | MAC Suffix | Distance (ft) | Bearing (°) | Status                    |
|----------------------|------------|---------------|-------------|---------------------------|
| Welcome Antenna      | :38        | 0             | --          | ✅ Outdoor, primary        |
| Barn North Antenna   | :C1        | 200           | 45          | ✅ Outdoor ridge           |
| Barn Equipment Panel | :93        | 227           | 15          | ✅ Inside barn, north side |

**Unconfirmed:** Site 3 (210 ft, 0°), Dirt Circus (657 ft, 135°), Pump House (1,392 ft, 270°)

**PtP Link Candidate:** Site 3 ↔ Pump House (1,254 ft, bearing 260°)

**Key Characteristics:**

- **All APs are 5 GHz only** -- loco-bridge cannot connect to 2.4 GHz SSIDs (no firmware mode exists)
- Barn is Faraday cage (metal exterior) except windows; Barn Equipment Panel (:93) penetrates via north window
- **Siting loco-bridge:** Verify 5 GHz signal at candidate location using dual-band client (MacBook Air, MacBook Pro); do not chase 2.4 GHz signal
- Barn dimensions: ~100 ft (N-S) × 75 ft (E-W)

### `eap225-outdoor` -- TP-Link EAP225-Outdoor Wireless AC1200

- Model: EAP225-Outdoor
- Role: Outdoor AP for Strategy C hot-zone deployment
- Power: 15.4W PoE (passive or active)
- Band: Dual-band (2.4 GHz + 5 GHz)
- Standard: WiFi 5 (802.11ac)
- Rating: IP65 (weather-sealed)
- Antenna: Modular (directional pointing toward Trails End Crew mesh)
- Purchased: 2026-07-13 (B&H order #1130629306)
- Expected delivery: 2026-07-15
- Status: On order

### Surge Protectors (Trails End)

- `surge-protector-01`, `surge-protector-02`: Ubiquiti Outdoor Ethernet Surge Protector (10kA, ETH-SP-G2)
- Role: Protect outdoor Cat5 backhaul and device inputs from lightning strikes
- Purchased: 2026-07-13 (B&H order #1130629306, qty 2)
- Expected delivery: 2026-07-15
- Status: On order

### PoE Injector

- `poe-trails-end`: Ubiquiti POE-24-12W; at Trails End cone zone; powers loco-bridge
