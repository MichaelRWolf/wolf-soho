# Computing Devices

## `michael-pro` -- MacBook Pro (Michael's primary) [WATER DAMAGED 2026-06-18]

- Model: MacBook Pro 13-inch Late 2020 (A2251) -- MacBookPro16,2
- Chip: Intel Core i5, Quad-Core, 2 GHz
- RAM: 16 GB
- Storage: 256GB SSD
- Serial: Unknown (device destroyed)
- Hardware UUID: `3D9DF3C9-1B29-5FAA-A9E9-859D7316915A`
- macOS: 15.7.3 Sequoia (build 24G419) (2026-05-12, last known state)
- macOS 26 Tahoe: **Compatible** -- last Intel-supported macOS
- Battery connector: ZIF (iFixit guide [MIC2020])
- Notes: [Battery Replacement Project](michael-pro_battery.md); [Water damage incident 2026-06-18](2026-06-18_michael-pro_water-damage.md); Device: unrecoverable; Time Machine backup preserved as `Backups-TM-Michael` on NAS (436GB, do not delete without explicit decision)

## `michael-air` -- MacBook Air (Michael's replacement) [M3, 2024]

- Model: MacBook Air 13-inch M3 (2024, A3383) -- Mac15,12
- Model Number: MC8K4LL/A
- Chip: Apple M3 (8-core: 4 performance + 4 efficiency) -- arm64e
- RAM: 16 GB
- Storage: 245.1 GB (available); 245.1 GB total (256 GB SSD)
- Serial: LFGJ62QR3W
- Hardware UUID: `58ED3E12-7C1A-5473-BD8A-89246A584DCC`
- Platform UUID: `58ED3E12-7C1A-5473-BD8A-89246A584DCC`
- Provisioning UDID: `00008122-0006143411F1001C`
- Boot ROM version: 13822.61.10
- macOS: 15.3.1 Sequoia (build 24D70) (2026-08-18)
- macOS 26 Tahoe: **Compatible**
- Status: **Active replacement** for water-damaged michael-pro; Migration Assistant restore completed 2026-08-13/14
- Network: Primary interface en0 (Wi-Fi); secondary USB-C Ethernet dongles available
- MAC addresses: (documented under Network Interfaces section below)
- Notes: Replacing michael-pro (Intel) following 2026-06-18 water damage. See [project-michael-air/](../project-michael-air/) for setup status and Time Machine strategy. Time Machine backup in progress: `Backups-TM-Michael-Air` (fresh start, separate from legacy `Backups-TM-Michael`)

### Time Machine: michael-pro vs michael-air

- **michael-pro TM backup**: `Backups-TM-Michael` on NAS (436GB, 25 snapshots April 2025-Aug 13 2026) -- **PRESERVED; do not delete** without explicit decision
- **michael-air TM backup**: `Backups-TM-Michael-Air` on NAS (fresh start Aug 2026+) -- user-focused, excludes system files and Intel binaries

## `wendy-pro` -- MacBook Pro (Wendy's) -- ABANDONED

- Model: MacBook Pro 13-inch 2022 M2 (A2338)
- Serial: CO2H519BQ05F
- Chip: Apple M2 (8-core: 4 performance + 4 efficiency)
- RAM: 8 GB
- Storage: 256GB SSD (estimated; 2022 M2 baseline)
- macOS: 15.7.5 Sequoia (build 24G624) (2026-05-12)
- Status: **Water damage 2026-08-03; logic board failure; not viable for recovery**
- Notes: Logic board damage prevents network boot. Repair cost ($200-$1,100) approaches replacement. See [project-wendy-pro-water-2026-08/notes.md](project-wendy-pro-water-2026-08/notes.md)

## `wolf-air` -- MacBook Air

- Model: MacBook Air (MacBookAir7,2)
- Chip: Intel Core i5, 1.8 GHz, dual-core
- RAM: 8 GB
- Storage: 128GB SSD (confirmed via system_profiler 2026-08-05)
- macOS: 12.7.6 Monterey (build 21H1320) (2026-05-12)
- macOS 26 Tahoe: **Not compatible** (max: macOS 12 Monterey)
- mDNS name: wolf-air.local
- Ports: MagSafe (power), Thunderbolt 2 (left), 2x USB-A (rectangular data/charging), 3.5mm headphone jack

## `michael-iphone` -- iPhone (Michael's)

- Model: iPhone SE (3rd generation), 64 GB, Midnight -- MNAF3LL/A
- Chip: Apple A15 Bionic (6-core: 2 performance + 4 efficiency)
- Display: 4.7-inch Retina HD
- Camera: 12 MP rear, 7 MP front
- Connectivity: 5G, Wi-Fi 6 (802.11ax), Bluetooth 5.0, NFC
- Released: March 2022
- Serial: LWCGXJFWLP
- mDNS name: tigger-iphone.local
- MAC: 2a:10:66:ad:ee:f9 (tentative -- confirm via Beryl web UI)

## `wendy-iphone` -- iPhone (Wendy's)

- Model: iPhone SE (3rd generation), 64 GB, Midnight -- MNAF3LL/A
- Chip: Apple A15 Bionic (6-core: 2 performance + 4 efficiency)
- Display: 4.7-inch Retina HD
- Camera: 12 MP rear, 7 MP front
- Connectivity: 5G, Wi-Fi 6 (802.11ax), Bluetooth 5.0, NFC
- Released: March 2022
- Serial: HP19392DKK
- mDNS name: smiley.local
- MAC: 82:45:fa:e3:77:c4 (tentative -- private/random MAC; confirm via Beryl web UI)

---

## Test & Measurement Equipment

### `tds340a` -- Tektronix TDS 340A Oscilloscope

2-channel 100 MHz digital real-time oscilloscope (Tektronix, Beaverton OR, ~1998).
Nameplate confirmed from photo (IMG_0823.heic, 2026-05-20).

| Spec              | Value                                    |
|-------------------|------------------------------------------|
| Channels          | 2                                        |
| Bandwidth         | 100 MHz                                  |
| Sample rate       | 500 MS/s per channel                     |
| Sensitivity       | 2 mV to 10 V/div                         |
| Time base         | 5 ns to 5 s/div                          |
| Max input         | 400V (x10 probe) / 40V (x1 probe)        |
| Auto measurements | 21 built-in                              |
| Analysis          | FFT                                      |
| Storage           | 3.5" floppy (DOS-compatible)             |
| Power             | 65W max, 120VA max                       |
| Voltage range     | 90-132V (47-440 Hz) / 90-250V (47-63 Hz) |
| Fuse              | 3A slow (UL 198G) / 3.15A T (IEC 127)    |
| Power switch      | None -- cord is main power disconnect    |

**Usage note:** Scope ground = chassis ground. Avoid floating ground on DC circuits.
Use x10 probe for signals above 40V.

**Used for:** Bluetti EB70 water damage diagnosis -- see
`../rv-2003-dutchman/PROJECT_bluetti_water_damage_2025/CLAUDE.md`

### ThinkVision E24-10 -- Lenovo 24" Display

24-inch external monitor with DisplayPort and VGA inputs.
Manufactured 2019-04-22.

| Spec         | Value                              |
|--------------|------------------------------------|
| Model        | ThinkVision E24-10                 |
| Type Code    | D17238FE0                          |
| MFM          | 61B7-JAR6-WW                       |
| FRU          | 61B7JAR6WVV904EH75                 |
| Serial       | V9-04EH75                          |
| Chassis      | 790NY1300D00R01                    |
| Display size | 24 inches                          |
| Video inputs | DisplayPort (primary), VGA (D-SUB) |
| Date of Mfg  | 2019-04-22                         |

**Connectors:** DisplayPort input (flat rectangular, corner cut off), VGA (15-pin D-SUB legacy analog). No USB-C input -- video via DisplayPort only.

**Used for:** wendy-pro water damage diagnostics (2026-08-04) -- confirmed logic board + GPU functionality via external display testing.

### Anker Premium 7-in-1 USB-C Hub

USB-C hub with multiple ports for connectivity and peripheral support.
Manufactured by Anker Innovations Limited, China.

| Spec         | Value                                    |
|--------------|------------------------------------------|
| Product name | Premium 7-in-1 USB-C Hub 1H2C2A1S1M      |
| Model        | A8346                                    |
| Serial       | AELQPN0A2430034                          |
| Ports        | 1x HDMI, 2x USB-C, 2x USB-A, SD, microSD |
| Compliance   | CAN ICES-3 (B)/NMB-3(B)                  |
| Manufacturer | Anker Innovations Limited (China)        |

**Note:** HDMI output only. Not compatible for driving Lenovo E24-10 display (which requires DisplayPort input). Wolf-air needs Thunderbolt 2 to DisplayPort adapter to drive Lenovo.

---

## Network Interfaces & MAC Addresses

### `michael-air` Network Configuration

Primary interface (as of 2026-08-18):

- **en0** (Wi-Fi/AirPort): `9c:58:84:6a:4b:30`

Secondary/virtual interfaces:

- en1: `36:20:e9:d4:3e:00` (Thunderbolt 1 bridge)
- en2: `36:20:e9:d4:3e:04` (Thunderbolt 2 bridge)
- en3: `36:23:4b:77:f4:92` (Ethernet Adapter)
- en4: `36:23:4b:77:f4:93` (Ethernet Adapter)
- en6: USB 10/100/1000 LAN Ethernet
- en12: Belkin USB-C LAN Ethernet
- bridge0: `36:20:e9:d4:3e:00` (Thunderbolt Bridge)

**Note:** Multiple virtual/USB interfaces are created during network configuration. Primary data interface is en0. USB Ethernet adapters (en6, en12) are available for wired connectivity via USB-C dock/adapters.

### `michael-pro` Network Configuration

**To be documented** -- water-damaged device; TM backup does not contain network configuration reference.

---

## References

### [MIC2020]

iFixit. (2020). MacBook Pro 13-Inch Two Thunderbolt Ports Late 2020 Battery Replacement. Retrieved from <https://www.ifixit.com/Guide/MacBook+Pro+13-Inch+Two+Thunderbolt+Ports+Late+2020+Battery+Replacement/143286>

### [WEN2022]

iFixit. (2022). MacBook Pro 13-Inch M2 2022 Battery Replacement. Retrieved from <https://www.ifixit.com/Guide/MacBook+Pro+13-Inch+M2+2022+Battery+Replacement/149829>
