# RV Network

The RV LAN always runs behind `beryl` (192.168.8.1). This file documents the different
WAN uplink configurations (variants) used at different locations.

## Common LAN (all variants)

```text
beryl LAN (192.168.8.0/24)
  wolfden-nas   192.168.8.129
  → RV devices via running-wolf-router / running-wolf-router-5g
```

**Note:** wolfden-mesh (192.168.8.130) was an experimental mesh backhaul that did not work; removed.

## Variant: Rascally Raccoon

WAN source: Spectrum ISP at Moe's house via Ubiquiti PtP link (~460 ft, 5 GHz).

### Data Path

```text
internet
  → spectrum-router (192.168.1.1)
  -> indoor cable
  -> poe-moe 
  -> flat cable
  -> coupler
  -> outdoor cable
  → loco-ap (192.168.1.20) (Moe's porch)
  → RF ~460 ft @ 5 GHz (SSID: Running Wolf PtP)
  → loco-station (192.168.1.21) (Tree near RV
  → cable-outdoor-50ft
  → poe-rv (PoE in → LAN out)
  → indoor cables
  → beryl WAN (192.168.8.1)
```

### Loco Radio Management

Both radios: static IPs on 192.168.1.0/24, independent of beryl DHCP.

To access management UI: connect michael-pro directly to poe-rv LAN port with manual IP
192.168.1.100/24 (no gateway, no DNS). Wi-Fi off.

- loco-ap: <http://192.168.1.20> (Safari only)
- loco-station: <http://192.168.1.21> (Safari only)

SSH requires legacy algorithm flags -- see
[Ubiquiti/HOWTO_rascally_raccoon_PtP_config.md](Ubiquiti/HOWTO_rascally_raccoon_PtP_config.md).

### Cable Inventory

See [equipment_portable.md](equipment_portable.md) for cable specs and verification status.

## Variant: Trails End (Historical -- 2025)

WAN source: campground WiFi repeated into beryl via cheapo-extender (wolfden-mesh experiment did not work).

### Observed SSIDs at Trails End

- `906AT STARLINK`
- `ch_pasty_289-8068` (Copper Harbor's PastyNet)
- `Lake Effect Farm` (2.4 GHz and 5 GHz, password protected)
- `Trails End Crew` (5G, password protected)
- `Trails End WiFi` (5G)

### Uplink Path (2025)

```text
campground WiFi
  → cheapo-extender (client/repeater mode)
  → beryl WAN (repeater mode)
  → beryl LAN
```

Docs: [Trails_End/](Trails_End/)

---

## Variant: Trails End 2026 Summer

**Current Location:** Site 1 (moved from barn area Monday, July 7)

**Status:** Signal mapping in progress; uncertain antenna configuration.

### Site 1 Geographic Layout (Google Maps measurements)

```text
                        Barn
                      (217 ft NW)
                          *
                         /
                        /
                    RV *----------* Registration Antenna
              (Site 1)  \        (60 ft N/NE)
                         \
                          \
                           * Site 3 Pole
                         (172 ft E/SE)
```

| Landmark                     | Distance | Direction | Notes                                                |
|------------------------------|----------|-----------|------------------------------------------------------|
| Barn (Starlink/Pasty uplink) | ~217 ft  | NW        | Primary WAN source                                   |
| Registration antenna         | ~60 ft   | N/NE      | Trails End Wifi broadcast; poor signal indoors at RV |
| Site 3 pole                  | ~172 ft  | E/SE      | Possible PtP link or secondary AP                    |

### Network at Trails End (2026 Summer)

**Campground Infrastructure:**

- **Barn roof:** Starlink dish + Pasty.net ISP uplink (dual WAN source, ~217 ft NW of Site 1)
- **Registration station antenna:** likely 5G; broadcasts Trails End Wifi; coverage weak at Site 1 despite proximity
- **Site 3 pole:** unknown (possible PtP link to barn or secondary AP)
- **New CG Manager:** Stenar

**Observed SSIDs at Site 1:**

- `Trails End WiFi` (5G) -- currently connected; poor indoor signal; likely from registration antenna
- `Trails End Crew` (5G, password protected) -- source unknown; not yet tested
- `906AT STARLINK` -- source unknown; not yet tested
- `ch_pasty_289-8068` (PastyNet) -- source unknown
- `Lake Effect Farm` (2.4 GHz, 5 GHz) -- source unknown

**Signal Issue at Site 1 (Observations):**

- Connected to: Trails End Wifi (5G)
- **Highly variable performance:**
  - Test 1: 9 Mbps down / 4 Mbps up
  - Test 2: 0.3 Mbps down / 0.1 Mbps up (severe drop)
- **Problem:** poor indoor speeds despite ~60 ft proximity to registration antenna
- **Hypotheses:**
  - Foliage blocking registration antenna path (~3-ft tree near antenna; line-of-sight question)
  - Registration antenna inactive or misconfigured
  - Heavy interference or multipath
  - Barn uplink has better signal (217 ft, but no foliage blocking?)
- **Historical clue (Sept 2025):** bucket-on-roof test showed better signal, suggesting barn path advantage or foliage impact at registration antenna

**Signal Mapping Plan (Today):**

- Test locations: RV (baseline), Registration antenna, Site 3 pole, Barn direction
- Method: auto-logging speedtest script (3 tests per location, log to CSV)
- Goal: determine if signal improves at different locations/antennas
- Outcome: inform decision on whether to propose network optimization to Stenar

### Uplink Path (2026)

```text
Current: campground WiFi (Trails End Wifi SSID)
  → beryl WAN (repeater mode)
  → beryl LAN
  → RV devices
  
Possible alternatives (to be tested):
  - Trails End Crew (5G, source/quality unknown)
  - Site 3 pole link (if PtP or AP)
  - Barn-routed Starlink/Pasty (if range permits or external antenna)
```

**Next Steps:**

1. Run signal map (speedtest grid at RV, Registration, Site 3, Barn) -- Today, July 7
2. Analyze results; decide whether to approach Stenar with optimization proposal
3. If pursuing: draft proposal (antenna reposition, external AP, SSID migration, etc.)

**Project Log:** [2026-Summer.md](../../trails-end-campground/2026-Summer.md)

## Variant: On The Road

WAN source: cellular -- michael-iphone or wendy-iphone hotspot, or running-wolf-hotspot
(Netgear Nighthawk M1). Used while driving interstate, Cracker Barrel stops, etc.

### Data Path Options

```text
Netgear hotspot:
  running-wolf-hotspot (Nighthawk M1, LTE)
  → beryl WAN (WiFi uplink; wired future option)

iPhone tethering:
  michael-iphone or wendy-iphone (Personal Hotspot)
  → beryl WAN (WiFi uplink or USB tether)
```

### Notes

- No fixed IPs; all DHCP from cellular carrier
- iPhone hotspot SSID and password set on device
- running-wolf-hotspot may overheat on long drives; ice pack workaround
