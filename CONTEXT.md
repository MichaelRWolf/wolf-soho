# Wolfden Device Registry

Standard names for all devices. Use these names in project files and session notes to prevent
ambiguous language. Read this file at the start of any network-related session.

## Network Infrastructure — RV Side

| Name | Device | IP | Notes |
|---|---|---|---|
| `beryl` | GL.iNet Beryl GL-MT1300 (hostname: GL-MT1300-cd7) | 192.168.8.1 | RV primary router; NAT + DHCP for running-wolf-router |
| `loco-station` | Ubiquiti NanoStation Loco5AC | 192.168.1.21 | PtP station (client), RV side; 10/100 Mbps Ethernet |
| `wolfden-hotspot` | Netgear Nighthawk M1 | varies | Cellular/LTE hotspot; backup internet |
| `wolfden-nas` | Synology DS220j (MAC 00:11:32:EA:25:1B) | 192.168.8.129 | NAS; Time Machine; SMB shares |
| `wolfden-mesh` | Ubiquiti UAP-AC-M-US (MAC D8:B3:70:CC:AA:7C) | 192.168.8.130 planned | WiFi AP; integration pending |
| `cheapo-extender` | Generic USB WiFi repeater (Amazon B0DCBYCHR7) | 192.168.11.1 | Portable campground WiFi backup |

## Network Infrastructure — Moe's House Side

| Name | Device | IP | Notes |
|---|---|---|---|
| `loco-ap` | Ubiquiti NanoStation Loco5AC | 192.168.1.20 | PtP access point (master), house side; 10/100 Mbps Ethernet |
| `spectrum-router` | Spectrum SAC2V1A | LAN IP unknown (not 192.168.1.1) | ISP router/modem at Moe's house |

## Computing Devices

| Name | Device |
|---|---|
| `michael-pro` | MacBook Pro (Michael's primary) |
| `wolf-air` | MacBook Air |
| `wendy-pro` | MacBook Pro (Wendy's) |
| `wolf-pro` | MacBook (newer) |

## Accessories

| Name | Device | Notes |
|---|---|---|
| `anker-dongle` | Anker USB-C to Gigabit Ethernet adapter | Used with michael-pro for direct Ethernet access |
| `poe-rv` | Ubiquiti POE-24-12W passive PoE injector | Originally at RV; emitted buzz during 2026-05 diagnosis |
| `poe-moe` | Ubiquiti POE-24-12W passive PoE injector | Originally at Moe's house |
| `tp-link-switch` | TP-Link TL-SF1005D, 5-port 10/100 unmanaged | Ordered 2026-05-04; not yet installed |

## SSIDs

| Canonical name | Actual SSID | Device | Band |
|---|---|---|---|
| `running-wolf-router` | Running Wolf Router | beryl | 2.4 GHz |
| `running-wolf-router-5g` | Running Wolf Router - 5G | beryl | 5 GHz |
| `running-wolf-guest` | Running Wolf Guest | beryl | 2.4 GHz |
| `running-wolf-guest-5g` | Running Wolf Guest - 5G | beryl | 5 GHz |
| `running-wolf-hotspot` | Running Wolf Hot Spot | wolfden-hotspot (Nighthawk M1) | 2.4/5 GHz |
| `running-wolf-ptp` | Running Wolf PtP | loco-ap ↔ loco-station RF link | 5 GHz |
| `spectrum-wifi` | SpectrumSetup-DO | spectrum-router | 2.4/5 GHz |

## RV Cable Inventory — Rascally Raccoon Site

| Name | Description | Verified good |
|---|---|---|
| `cable-black-10ft` | Black Cat6, 10 ft, indoor RV | Yes |
| `cable-green-3ft-a` | Green Cat6, 3 ft, indoor RV | Yes |
| `cable-green-3ft-b` | Green Cat6, 3 ft, indoor RV | Yes |
| `cable-outdoor-50ft` | Cat6, 50 ft, exterior run, RV side | Yes |

Cables verified by: michael-pro → anker-dongle → [cable] → wolfden-hotspot → internet, pinged
1.1.1.1.

## Normal Data Path — Rascally Raccoon Site

```
internet
  → spectrum-router  (LAN IP unknown)
  → [Ethernet: indoor + outdoor run at Moe's house]
  → loco-ap  (192.168.1.20)
  ))) Running Wolf PtP  RF ~460 ft @ 5 GHz )))
  loco-station  (192.168.1.21)
  → poe injector  (PoE port in → LAN port out)
  → cable-outdoor-50ft + indoor cables
  → beryl WAN  (192.168.8.1)
  → beryl LAN
  → RV devices on running-wolf-router / running-wolf-router-5g
```

## Management Access — Loco Radios

Both radios use static IPs on 192.168.1.0/24, independent of beryl and DHCP. To access
management UI, connect michael-pro directly to the PoE injector LAN port with a manual IP of
192.168.1.100/24 (no gateway), or via beryl if routing to 192.168.1.x is confirmed working.

- loco-station: http://192.168.1.21 (Safari only)
- loco-ap: http://192.168.1.20 (reachable via RF bridge when link is up)

SSH requires legacy algorithm flags — see
[Ubiquiti/HOWTO_rascally_raccoon_PtP_config.md](Ubiquiti/HOWTO_rascally_raccoon_PtP_config.md).

## Reference Docs

| Topic | File |
|---|---|
| Physical installation | [Ubiquiti/HOWTO_rascally_raccoon_PtP_install.md](Ubiquiti/HOWTO_rascally_raccoon_PtP_install.md) |
| Logical config / bench setup | [Ubiquiti/HOWTO_rascally_raccoon_PtP_config.md](Ubiquiti/HOWTO_rascally_raccoon_PtP_config.md) |
| Settings reference | [Ubiquiti/ubiquiti_loco_ptp_settings.md](Ubiquiti/ubiquiti_loco_ptp_settings.md) |
| Operations / health check | [Ubiquiti/HOWTO_ubiquiti_loco_ptp_operations.md](Ubiquiti/HOWTO_ubiquiti_loco_ptp_operations.md) |
| beryl SSH / UCI reference | [GL-iNet/beryl-cheat-sheet.md](GL-iNet/beryl-cheat-sheet.md) |
| RV equipment list | [equipment_and_network_wolf.md](equipment_and_network_wolf.md) |
| Active outage project | [PROJECT_raccoon_ethernet_2026-05.md](PROJECT_raccoon_ethernet_2026-05.md) |
