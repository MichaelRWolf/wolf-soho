# RV Network

The RV LAN always runs behind `beryl` (192.168.8.1). This file documents the different
WAN uplink configurations (variants) used at different locations.

## Common LAN (all variants)

```text
beryl LAN (192.168.8.0/24)
  wolfden-nas   192.168.8.129
  wolfden-mesh  192.168.8.130 (planned)
  wolf-air      192.168.8.167
  → RV devices via running-wolf-router / running-wolf-router-5g
```

## Variant: Rascally Raccoon

WAN source: Spectrum ISP at Moe's house via Ubiquiti PtP link (~460 ft, 5 GHz).

### Data Path

```text
internet
  → spectrum-router (192.168.1.1)
  → [Ethernet: indoor + outdoor run at Moe's house]
  → loco-ap (192.168.1.20)
  ))) Running Wolf PtP  RF ~460 ft @ 5 GHz )))
  loco-station (192.168.1.21)
  → poe-rv (PoE in → LAN out)
  → cable-outdoor-50ft + indoor cables
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

## Variant: Trails End

WAN source: campground WiFi repeated into beryl via cheapo-extender or wolfden-mesh.

### Observed SSIDs at Trails End

- `906AT STARLINK`
- `ch_pasty_289-8068` (Copper Harbor's PastyNet)
- `Lake Effect Farm` (2.4 GHz and 5 GHz, password protected)
- `Trails End Crew` (5G, password protected)
- `Trails End WiFi` (5G)

### Uplink Path

```text
campground WiFi
  → cheapo-extender or wolfden-mesh (client/repeater mode)
  → beryl WAN (repeater mode)
  → beryl LAN
```

Docs: [Trails_End/](Trails_End/)

## Variant: On The Road

WAN source: cellular -- michael-iphone or wendy-iphone hotspot, or wolfden-hotspot
(Netgear Nighthawk M1). Used while driving interstate, Cracker Barrel stops, etc.

### Data Path Options

```text
Option A -- iPhone tethering:
  michael-iphone or wendy-iphone (Personal Hotspot)
  → beryl WAN (WiFi uplink or USB tether)

Option B -- Netgear hotspot:
  wolfden-hotspot (Nighthawk M1, LTE)
  → beryl WAN (WiFi uplink; wired future option)
```

### Notes

- No fixed IPs; all DHCP from cellular carrier
- iPhone hotspot SSID and password set on device
- wolfden-hotspot may overheat on long drives; ice pack workaround
