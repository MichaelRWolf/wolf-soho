# Trails End Network Topology -- SSID → BSSID → Site Mapping

**Last Updated:** 2026-07-18  
**Source:** NetSpot scan + Beryl LuCI status page, live observation  
**Purpose:** Complete reference for SSID/BSSID associations by site, band, and channel. Used by `wifi_field_test.py` and field documentation.

---

## Key Insight: Three SSIDs, One Radio Per Site

Each physical antenna site at Trails End broadcasts **three separate SSIDs** from the **same radio hardware**:

- `Trails End Wifi`
- `Trails End Crew`
- `Lake Effect Farm`

These are distinguished by SSID name only; they share identical BSSID prefix (MAC suffix) and channel. The three-SSID pattern is consistent across Welcome Antenna (`:38`) and Barn North Antenna (`:C1`), confirming this is intentional configuration, not accidental interference.

---

## SSID → BSSID Lookup Table

| Site                         | SSID                            | BSSID               | Band      | Channel   | Notes                                                             |
|------------------------------|---------------------------------|---------------------|-----------|-----------|-------------------------------------------------------------------|
| Welcome Antenna (:38)        | Trails End Wifi                 | 7A:AC:B9:CB:36:38   | 5 GHz     | 44        | Primary outdoor AP                                                |
| Welcome Antenna (:38)        | Trails End Wifi                 | 7A:AC:B9:CA:36:38   | 2.4 GHz   | 11        |                                                                   |
| Welcome Antenna (:38)        | Trails End Crew                 | 7E:AC:B9:CB:36:38   | 5 GHz     | 44        |                                                                   |
| Welcome Antenna (:38)        | Trails End Crew                 | 7E:AC:B9:CA:36:38   | 2.4 GHz   | --        | Not observed in this scan                                         |
| Welcome Antenna (:38)        | Lake Effect Farm                | 74:AC:B9:CB:36:38   | 5 GHz     | 44        |                                                                   |
| Welcome Antenna (:38)        | Lake Effect Farm                | 74:AC:B9:CA:36:38   | 2.4 GHz   | 11        |                                                                   |
| ---------------------------- | ------------------------------- | ------------------- | --------- | --------- | ----------------------------------------------------------------- |
| Barn North Antenna (:C1)     | Trails End Wifi                 | 7A:AC:B9:CB:3B:C1   | 5 GHz     | 44        | Outdoor ridge, north roof                                         |
| Barn North Antenna (:C1)     | Trails End Wifi                 | 7A:AC:B9:CA:3B:C1   | 2.4 GHz   | 1         |                                                                   |
| Barn North Antenna (:C1)     | Trails End Crew                 | 7E:AC:B9:CB:3B:C1   | 5 GHz     | 44        |                                                                   |
| Barn North Antenna (:C1)     | Trails End Crew                 | 7E:AC:B9:CA:3B:C1   | 2.4 GHz   | 1         |                                                                   |
| Barn North Antenna (:C1)     | Lake Effect Farm                | 74:AC:B9:CB:3B:C1   | 5 GHz     | 44        |                                                                   |
| Barn North Antenna (:C1)     | Lake Effect Farm                | 74:AC:B9:CA:3B:C1   | 2.4 GHz   | 1         |                                                                   |
| ---------------------------- | ------------------------------- | ------------------- | --------- | --------- | ----------------------------------------------------------------- |
| Barn Equipment Panel (:93)   | (all three)                     | unconfirmed         | --        | --        | Inside barn, north window; needs in-barn scan                     |
| ---------------------------- | ------------------------------- | ------------------- | --------- | --------- | ----------------------------------------------------------------- |
| Unconfirmed Site (:A1)       | Trails End Wifi                 | FA:E2:C6:24:B3:A1   | 2.4 GHz   | 1         | Unknown location; candidates: Site 3 / Dirt Circus / Pump House   |
| Unconfirmed Site (:A1)       | Trails End Crew                 | FE:E2:C6:24:B3:A1   | 2.4 GHz   | 1         |                                                                   |
| Unconfirmed Site (:A1)       | Lake Effect Farm                | F4:E2:C6:24:B3:A1   | 2.4 GHz   | 1         |                                                                   |
| ---------------------------- | ------------------------------- | ------------------- | --------- | --------- | ----------------------------------------------------------------- |
| Beryl (RV)                   | Running Wolf Router - 5G        | 94:83:C4:11:9C:DA   | 5 GHz     | 44        | Michael's RV gateway; 2.4G radio currently disabled               |
| Beryl (RV)                   | Running Wolf Router             | *radio disabled*    | 2.4 GHz   | --        | Disabled in current config                                        |
| ---------------------------- | ------------------------------- | ------------------- | --------- | --------- | ----------------------------------------------------------------- |
| EAP225 Repeater              | Trails End Wifi - Site 1 - 5G   | 18:69:45:38:A2:F3   | 5 GHz     | 157       | Position varies during field testing                              |
| EAP225 Repeater              | Trails End Wifi - Site 1        | 18:69:45:38:A2:F2   | 2.4 GHz   | 11        | Position varies during field testing                              |

---

## Notes for wifi_field_test.py Integration

1. **KNOWN_BSSIDS constant**: Script seeds all confirmed BSSIDs (seeded to antenna/site name) and uses this table for auto-fill. Unconfirmed entries (`:93`, `:A1`, Beryl 2.4G) are marked as TODO comments in the dict.

2. **Auto-detection logic**: When the script detects a connected BSSID in this table, it auto-fills the antenna/site name without requiring manual `--eap` input. Only the EAP225 (which wanders) and unrecognized BSSIDs require explicit location.

3. **Future maintenance**: As new sites are discovered (e.g., Barn Equipment Panel `:93` confirmed, or `:A1` physically located), this table should be updated first, then the `KNOWN_BSSIDS` dict in the script updated to match.

---

## Related Files

- [antenna_survey.md](antenna_survey.md) -- Physical location reference (distance, bearing, confirmed antennas)
- [wifi_field_test.py](wifi_field_test.py) -- Field test script (uses KNOWN_BSSIDS seeded from this table)
- [equipment_networking.md](../equipment_networking.md) -- Device specs (Beryl, EAP225-Outdoor, loco-bridge)
