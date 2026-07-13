# Wolfden Device Registry

Standard names for all devices. Use these names in project files and session notes to prevent
ambiguous language. Read this file at the start of any network-related session.

## Network Infrastructure -- Rascally Raccoon PtP (Winter 2025-2026)

| Name                   | Device                       | IP (Static)  |
|------------------------|------------------------------|--------------|
| `beryl`                | GL.iNet Beryl GL-MT1300      |              |
| `loco-station`         | Ubiquiti NanoStation Loco5AC | 192.168.1.21 |
| `running-wolf-hotspot` | Netgear Nighthawk M1         |              |
| `wolfden-nas`          | Synology DS220j              |              |
| `wolfden-mesh`         | Ubiquiti UAP-AC-M-US         |              |
| `cheapo-extender`      | Generic USB WiFi repeater    |              |

## Network Infrastructure -- Rascally Raccoon PtP (Winter 2025-2026) -- Moe's House Side

| Name              | Device                       | IP (Static)  |
|-------------------|------------------------------|--------------|
| `loco-ap`         | Ubiquiti NanoStation Loco5AC | 192.168.1.20 |
| `spectrum-router` | Spectrum SAC2V1A             |              |
| `moes-roomba`     | iRobot Roomba i7             |              |

## Network Infrastructure -- Trails End Campground (Summer 2026)

| Name                 | Device                                           | IP (Static)  |
|----------------------|--------------------------------------------------|--------------|
| `loco-bridge`        | Ubiquiti NanoStation Loco5AC                     | 192.168.1.22 |
| `eap225-outdoor`     | TP-Link EAP225-Outdoor Wireless AC1200           |              |
| `surge-protector-01` | Ubiquiti Outdoor Ethernet Surge Protector (10kA) |              |
| `surge-protector-02` | Ubiquiti Outdoor Ethernet Surge Protector (10kA) |              |

### Antenna Survey & Location Registry

**Authoritative Source:** [Trails_End/antenna_survey.md](Trails_End/antenna_survey.md)

**Zero Point Reference:** Welcome Antenna (MAC suffix :38)

**Confirmed Antennas:**

- Welcome Antenna (:38) -- 0 ft, primary outdoor reception (channels 36, 44)
- Barn North Antenna (:C1) -- 200 ft, bearing 45° (outdoor ridge, north roof)
- Barn Equipment Panel (:93) -- 227 ft, bearing 15° (inside barn, north window)

**Unconfirmed Candidates (need field verification):**

- Site 3 -- 210 ft, bearing 0°
- Dirt Circus -- 657 ft, bearing 135°
- Pump House -- 1,392 ft, bearing 270°
- Barn Farm Antenna (reserved for south-side inside barn, if exists)

**PtP Link Candidate:** Site 3 ↔ Pump House (1,254 ft, bearing 260°)

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
