# Trails End Campground Antenna Survey

**Survey Date:** 2026-07-10  
**Method:** Google Maps distance/bearing measurement + RF scan (NetSpot)  
**Zero Point Reference:** Welcome Antenna (MAC suffix :38)

---

## Confirmed Antennas

| Antenna              | MAC Suffix | Distance (ft) | Bearing (°) | Channels (5 GHz) | Position                              | Status |
|----------------------|------------|---------------|-------------|------------------|---------------------------------------|--------|
| Welcome Antenna      | :38        | 0             | --          | 36, 44           | Outdoor, primary reception point      | ✅      |
| Barn North Antenna   | :C1        | 200           | 45          | 44               | Outdoor ridge, north roof edge        | ✅      |
| Barn Equipment Panel | :93        | 227           | 15          | 149              | Inside barn (north side, near window) | ✅      |

---

## Unconfirmed Candidate Locations

| Site               | MAC Suffix | Distance (ft) | Bearing (°) | Observed Channels | Status         | Notes                                               |
|--------------------|------------|---------------|-------------|-------------------|----------------|-----------------------------------------------------|
| Site 3             | TBD        | 210           | 0           | Multiple (5 GHz)  | ⚠️ Unconfirmed | Visible in RF scan; location needs field visit      |
| Dirt Circus        | TBD        | 657           | 135         | Multiple (5 GHz)  | ⚠️ Unconfirmed | Visible in RF scan; location needs field visit      |
| Pump House         | TBD        | 1,392         | 270         | Multiple (5 GHz)  | ⚠️ Unconfirmed | Visible in RF scan; location needs field visit      |
| Unknown Site (:A1) | A1         | ?             | ?           | 2.4 GHz (ch 1)    | ⚠️ Unconfirmed | NetSpot 2026-07-18 found this site; not yet located |
| Barn Farm Antenna  | TBD        | --            | --          | --                | ⚠️ Reserved    | Inside barn (south side), if exists; location TBD   |

**BSSID Details:** See [network_topology.md](network_topology.md) for complete SSID→BSSID→site mapping table (preferred reference going forward).

---

## Point-to-Point (PtP) Link Candidate

**Primary Candidate:** Site 3 ↔ Pump House

| Parameter | Value                                                              |
|-----------|--------------------------------------------------------------------|
| Distance  | 1,254 ft (382 m)                                                   |
| Bearing   | ~260° (Site 3 → Pump House)                                        |
| Status    | ⚠️ Candidate only; needs confirmation once locations are confirmed |

---

## Physical Context

### Barn Characteristics

- **Dimensions:** ~100 ft (N-S) × 75 ft (E-W)
- **Construction:** Metal exterior (Faraday cage effect)
- **Windows:** North and West sides (signal penetration points)
- **Garage Doors:** North and South sides (signal penetration points)
- **Effect on Signal:** Barn Equipment Panel (:93) only detected inside the barn

### Bearing Convention

## Siting Considerations for loco-bridge

1. **5 GHz Only:** NanoStation Loco5AC cannot operate on 2.4 GHz under any configuration. All antenna siting must verify 5 GHz availability.

2. **Signal Survey Method:**
   - Use dual-band client (MacBook Air, MacBook Pro, iPhone) with NetSpot
   - Scan for 5 GHz signal strength at candidate siting locations
   - Do NOT chase 2.4 GHz signal strength
   - Verify target SSID broadcasts on 5 GHz

3. **Line-of-Sight (LoS):**
   - Welcome Antenna is primary reference; Barn North Antenna has ridge elevation advantage
   - Barn Equipment Panel signal attenuated by Faraday cage effect (north window penetration only)
   - Unconfirmed sites (Site 3, Dirt Circus, Pump House) require field verification for LoS to primary APs

---

## Testing Ground-Level Coverage

To verify which antenna actually reaches ground level at your loco-bridge location, use MAC locks to test individual APs:

### Test 1: Welcome Antenna (:38)

Connect loco-bridge to Trails End Crew with MAC lock to one of:

- `7E:AC:B9:CA:36:38` (channels 36, 44)
- `7E:AC:B9:CB:36:38` (channels 36, 44)

**Measure at ground level:** Signal strength, stability, latency

### Test 2: Barn North Antenna (:C1)

Connect loco-bridge to Trails End Crew with MAC lock to one of:

- `7E:AC:B9:CA:3B:C1` (channel 44)
- `7E:AC:B9:CB:3B:C1` (channel 44)

**Measure at ground level:** Signal strength, stability, latency

**Compare results** to identify which antenna provides reliable coverage at your siting location (ground level, not elevated).

---

## Next Steps

1. **Ground-Level Testing:** Use MAC locks above to verify actual coverage at loco-bridge location
2. **Site Visit:** Locate Site 3, Dirt Circus, Pump House antennas physically
3. **MAC Mapping:** Confirm MAC addresses for each antenna found
4. **PtP Verification:** If Site 3 ↔ Pump House PtP link is intended, verify both locations and confirm LoS
5. **loco-bridge Siting:** Once locations confirmed, choose optimal 5 GHz AP target for loco-bridge connection
