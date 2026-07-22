# Computing Devices

## `michael-pro` -- MacBook Pro (Michael's primary)

- Model: MacBook Pro (MacBookPro16,2)
- Chip: Intel Core i5, Quad-Core, 2 GHz
- RAM: 16 GB
- macOS: 15.7.3 Sequoia (build 24G419) (2026-05-12)
- macOS 26 Tahoe: **Compatible** -- last Intel-supported macOS
- Notes: [Battery Replacement Project](michael-pro_battery.md)

### Tahoe Upgrade Recommendation

Eligible but proceed with caution given hardware state:

- Battery is at 1,501 cycles (50% over Apple's 1,000-cycle threshold), already showing thermal throttling under load
- Tahoe is optimized for Apple Silicon; Intel Macs carry more of its background services as CPU work → more heat → more throttling
- A degraded battery compounds this: the machine draws harder from a weakened cell, increasing thermal stress and shortening unplugged runtime further
- **Recommended order:** replace battery first, then evaluate Tahoe -- or accept that sustained-load performance will degrade noticeably on Tahoe without a fresh battery
- Tahoe is the end of the Intel road; staying on Sequoia 15.x remains a valid lower-risk option until the battery is replaced

## `wendy-pro` -- MacBook Pro (Wendy's)

- Model: MacBook Pro (MacBookPro17,1)
- Chip: Apple M1 (8-core: 4 performance + 4 efficiency)
- RAM: 8 GB
- macOS: 15.7.5 Sequoia (build 24G624) (2026-05-12)
- macOS 26 Tahoe: **Compatible**

## `wolf-air` -- MacBook Air

- Model: MacBook Air (MacBookAir7,2)
- Chip: Intel Core i5, 1.8 GHz, dual-core
- RAM: 8 GB
- macOS: 12.7.6 Monterey (build 21H1320) (2026-05-12)
- macOS 26 Tahoe: **Not compatible** (max: macOS 12 Monterey)
- mDNS name: wolf-air.local

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
