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

- Role: Cellular/LTE hotspot; backup/travel internet
- Interfaces: USB tethering and Wi-Fi
- Known issue: overheats; workaround is ice pack
- Specs: TBD (offline at time of writing)

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
