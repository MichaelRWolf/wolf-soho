# Omada by TP-Link EAP225 Setup Project

**Status**: In progress
**Location**: Trails End Campground, Copper Harbor, MI
**Started**: 2026-07-16
**Equipment**: EAP225-Outdoor + surge protectors

## Objective

Deploy EAP225-Outdoor at Trails End as WiFi-to-Ethernet bridge (repeater mode). Topology:

```text
Trails End Crew WiFi ))) [EAP225-Outdoor on pole] <--Cat5+PoE--> Beryl <--> MacBooks
                                                       192.168.8.130
```

EAP225 connects to Trails End WiFi mesh and bridges connection via Cat5 to Beryl. Does NOT broadcast own SSID (avoids interference). Beryl provides internet via "Running Wolf Router" SSID to client devices.

## Equipment Inventory

- EAP225-Outdoor (qty 1) -- Ordered 2026-07-13; received 2026-07-16; recovered after brief unresponsiveness
- Surge protectors (qty 2) -- Ordered 2026-07-13
- PoE injectors -- TBD
- Ethernet cabling -- TBD

## Setup Phases

### Phase 1: Hardware Setup

- [ ] Unbox and inspect EAP225 units
- [ ] Verify PoE power requirements and injector compatibility
- [ ] Physical placement and mounting
- [ ] Cable routing to controller location

### Phase 2: Controller Configuration

- [ ] Set static IP reservation on Beryl: **192.168.8.130** (MAC: 18-69-45-38-A2-F2)
- [ ] Access EAP at <http://192.168.8.130>
- [ ] Install Omada controller (hardware or software)
- [ ] Initial network configuration
- [ ] Create WiFi network SSID (tentative: `running-wolf-trails-end` or similar)
- [ ] Security settings and authentication

### Phase 3: Integration

- [ ] Connect to Trails End network
- [ ] Test WiFi coverage and performance
- [ ] Link to existing infrastructure (beryl, loco-bridge, etc.)
- [ ] Document new SSID and access credentials in CONTEXT.md

### Phase 4: Documentation

- [ ] Create Trails_End/omada_setup.md with operational procedures
- [ ] Add to CONTEXT.md device registry
- [ ] Document PoE/power layout
- [ ] Add monitoring/health check procedures if needed

## Notes

- Trails End Crew mesh will be evaluated for continued use or replacement
- No cellular fallback available (Keweenaw County zero coverage)
- Coordinate with Trails End Crew operations for minimal downtime

## QR Code References

1. [Device Specs (back): EAP225-Outdoor, Default Access: https://omadaeap.net](Trails_End/omada_eap225/images/eap225_back.jpg)
2. [Configuration Guide (Standalone vs Controller modes)](Trails_End/omada_eap225/images/IMG_5522.JPEG) -- <https://support.omadanetworks.com/document/>
3. [Scan for Standalone Start Guide](Trails_End/omada_eap225/images/IMG_5523.JPEG)
4. [Scan for Omada App](Trails_End/omada_eap225/images/IMG_5524.JPEG)
5. [Scan for Controller Start Guide](Trails_End/omada_eap225/images/IMG_5525.JPEG)
6. [QR Code (unknown target)](Trails_End/omada_eap225/images/IMG_5526.JPEG)
7. [Box Back: Support & Warranty](Trails_End/omada_eap225/images/IMG_5527.JPEG) -- <https://support.omadanetworks.com/> | <www.omadanetworks.com> | S/N:Y263210002286
8. [Unit Label: MAC:18-69-45-38-A2-F2, SSIDs Omada_2.4GHz_38A2F2 / Omada_5GHz_38A2F3](Trails_End/omada_eap225/images/IMG_5528.JPEG)

## References

TP-Link Systems Inc. (n.d.). *Quick Setup Guide for Standalone Omada EAPs*. Retrieved from <https://www.tp-link.com/us/configuration-guides/quick_setup_guide_for_standalone_omada_eaps/?configurationId=18595>

## Related Files

- CONTEXT.md -- Device registry (to be updated)
- Trails_End/ -- Device-specific documentation
- equipment_networking.md -- Network equipment specs
