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

| Site              | MAC Suffix | Distance (ft) | Bearing (°) | Observed Channels | Status         | Notes                                             |
|-------------------|------------|---------------|-------------|-------------------|----------------|---------------------------------------------------|
| Site 3            | TBD        | 210           | 0           | Multiple (5 GHz)  | ⚠️ Unconfirmed | Visible in RF scan; location needs field visit    |
| Dirt Circus       | TBD        | 657           | 135         | Multiple (5 GHz)  | ⚠️ Unconfirmed | Visible in RF scan; location needs field visit    |
| Pump House        | TBD        | 1,392         | 270         | Multiple (5 GHz)  | ⚠️ Unconfirmed | Visible in RF scan; location needs field visit    |
| Barn Farm Antenna | TBD        | --            | --          | --                | ⚠️ Reserved    | Inside barn (south side), if exists; location TBD |

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
- **Windows:** North and south sides (signal penetration points)
- **Effect on Signal:** Welcome Antenna (:38) broadcasts 5 GHz primary; Barn Equipment Panel (:93) penetrates via north window with reduced signal (-45 to -72 dBm variability due to window proximity and metal shielding)

### Bearing Convention

Bearings are measured from Welcome Antenna in the standard compass convention:

- 0° = North (N)
- 45° = Northeast (NE)
- 90° = East (E)
- 135° = Southeast (SE)
- 180° = South (S)
- 225° = Southwest (SW)
- 270° = West (W)
- 315° = Northwest (NW)

---

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

## Next Steps

1. **Site Visit:** Locate Site 3, Dirt Circus, Pump House antennas physically
2. **MAC Mapping:** Confirm MAC addresses for each antenna found
3. **PtP Verification:** If Site 3 ↔ Pump House PtP link is intended, verify both locations and confirm LoS
4. **loco-bridge Siting:** Once locations confirmed, choose optimal 5 GHz AP target for loco-bridge connection
