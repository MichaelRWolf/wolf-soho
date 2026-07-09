# Wolfden Device Registry

Standard names for all devices. Use these names in project files and session notes to prevent
ambiguous language. Read this file at the start of any network-related session.

## Network Infrastructure -- Rascally Raccoon PtP (Winter 2025-2026)

| Name                   | Device                       |
|------------------------|------------------------------|
| `beryl`                | GL.iNet Beryl GL-MT1300      |
| `loco-station`         | Ubiquiti NanoStation Loco5AC |
| `running-wolf-hotspot` | Netgear Nighthawk M1         |
| `wolfden-nas`          | Synology DS220j              |
| `wolfden-mesh`         | Ubiquiti UAP-AC-M-US         |
| `cheapo-extender`      | Generic USB WiFi repeater    |

## Network Infrastructure -- Rascally Raccoon PtP (Winter 2025-2026) -- Moe's House Side

| Name              | Device                       |
|-------------------|------------------------------|
| `loco-ap`         | Ubiquiti NanoStation Loco5AC |
| `spectrum-router` | Spectrum SAC2V1A             |
| `moes-roomba`     | iRobot Roomba i7             |

## Network Infrastructure -- Trails End Campground (Summer 2026)

| Name          | Device                       |
|---------------|------------------------------|
| `loco-bridge` | Ubiquiti NanoStation Loco5AC |

## Computing Devices

| Name             | Device                          |
|------------------|---------------------------------|
| `michael-pro`    | MacBook Pro (Michael's primary) |
| `wendy-pro`      | MacBook Pro (Wendy's)           |
| `wolf-air`       | MacBook Air                     |
| `michael-iphone` | iPhone (Michael's)              |
| `wendy-iphone`   | iPhone (Wendy's)                |

## Test & Measurement

| Name      | Device                          |
|-----------|---------------------------------|
| `tds340a` | Tektronix TDS 340A oscilloscope |

## Accessories

| Name             | Device                                   |
|------------------|------------------------------------------|
| `anker-dongle`   | Anker USB-C to Gigabit Ethernet adapter  |
| `belkin-dongle`  | Belkin USB-C to Gigabit Ethernet adapter |
| `poe-rv`         | Ubiquiti POE-24-12W passive PoE injector |
| `poe-moe`        | Ubiquiti POE-24-12W passive PoE injector |
| `poe-trails-end` | Ubiquiti POE-24-12W passive PoE injector |

## SSIDs

| Canonical name             | Actual SSID                | Device                                | Band   | (GHz)   |
|----------------------------|----------------------------|---------------------------------------|--------|---------|
| `running-wolf-router`      | Running Wolf Router        | beryl                                 | 2.4    |         |
| `running-wolf-router-5g`   | Running Wolf Router - 5G   | beryl                                 |        | 5.0     |
| `running-wolf-guest`       | Running Wolf Guest         | beryl                                 | 2.4    |         |
| `running-wolf-guest-5g`    | Running Wolf Guest - 5G    | beryl                                 |        | 5.0     |
| -------------------------- | -------------------------- | ------------------------------------- | ------ | ------- |
| `running-wolf-hotspot`     | Running Wolf Hot Spot      | running-wolf-hotspot (Nighthawk M1)   | 2.4    | 5.0     |
| -------------------------- | -------------------------- | ------------------------------------- | ------ | ------- |
| `running-wolf-ptp`         | Running Wolf PtP           | loco-ap ↔ loco-station RF link        |        | 5.0     |
| -------------------------- | -------------------------- | ------------------------------------- | ------ | ------- |

## Reference Docs

| Topic                           | File                                                                                             |
|---------------------------------|--------------------------------------------------------------------------------------------------|
| Computing device specs          | [equipment_computing.md](equipment_computing.md)                                                 |
| Networking equipment specs      | [equipment_networking.md](equipment_networking.md)                                               |
| Portable / Briefcase & Backpack | [equipment_portable.md](equipment_portable.md)                                                   |
| RV network variants             | [network_rv.md](network_rv.md)                                                                   |
| Physical PtP installation       | [Ubiquiti/HOWTO_rascally_raccoon_PtP_install.md](Ubiquiti/HOWTO_rascally_raccoon_PtP_install.md) |
| PtP config / bench setup        | [Ubiquiti/HOWTO_rascally_raccoon_PtP_config.md](Ubiquiti/HOWTO_rascally_raccoon_PtP_config.md)   |
| PtP settings reference          | [Ubiquiti/ubiquiti_loco_ptp_settings.md](Ubiquiti/ubiquiti_loco_ptp_settings.md)                 |
| PtP operations / health         | [Ubiquiti/HOWTO_ubiquiti_loco_ptp_operations.md](Ubiquiti/HOWTO_ubiquiti_loco_ptp_operations.md) |
| beryl SSH / UCI reference       | [GL-iNet/beryl-cheat-sheet.md](GL-iNet/beryl-cheat-sheet.md)                                     |
