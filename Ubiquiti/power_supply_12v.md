# Power Supply for Ubiquiti UAP-AC-M-US from 12V RV Battery

## Overview

This document outlines the power supply requirements and efficiency calculations for running a Ubiquiti UAP-AC-M-US access point from a 12V RV house battery system.

## Device Power Requirements

- **UAP-AC-M-US**: 24V passive PoE, ~6W consumption
- **Input voltage**: 24V DC
- **Power consumption**: 6W (0.25A at 24V)

## Recommended Two-Component Solution (Most Efficient)

### Component 1: 12V to 24V DC-DC Converter

**Model**: Mean Well LDD-350H-24V

- **Input voltage**: 12V DC
- **Output voltage**: 24V DC
- **Output current**: 350mA (8.4W max)
- **Efficiency**: 95%+
- **Power consumption**: ~9W input (6W output + 3W overhead)
- **Cost**: $15-20
- **Size**: 2.4" x 1.2" x 0.6"

### Component 2: 24V Passive PoE Injector

**Model**: Ubiquiti POE-24-24W-G

- **Input voltage**: 24V DC
- **Output**: 24V passive PoE
- **Efficiency**: 90%+
- **Power consumption**: ~1W overhead
- **Cost**: $25-30
- **Size**: 2.8" x 1.8" x 0.8"

### Total System Efficiency

- **DC-DC converter**: 95% efficiency
- **PoE injector**: 90% efficiency
- **Combined efficiency**: ~85%
- **Total power consumption**: ~10W from 12V battery

## Alternative One-Component Solution (Less Efficient)

### 12V PoE Injector

**Model**: Ubiquiti POE-12-24W-G

- **Input voltage**: 12V DC
- **Output**: 24V passive PoE
- **Efficiency**: ~80%
- **Power consumption**: ~12W total
- **Cost**: $35-40

**Recommendation**: Use two-component solution for 5% better efficiency

## Battery Runtime Calculations

### For 100Ah 12V Battery (1200Wh)

- **Two-component solution**: 1200Wh ÷ 10W = **120 hours** (5 days continuous)
- **One-component solution**: 1200Wh ÷ 12W = **100 hours** (4.2 days continuous)

### For 200Ah 12V Battery (2400Wh)

- **Two-component solution**: 2400Wh ÷ 10W = **240 hours** (10 days continuous)
- **One-component solution**: 2400Wh ÷ 12W = **200 hours** (8.3 days continuous)

## Installation Notes

### Wiring Requirements

- **12V input**: 14 AWG wire (up to 10 feet)
- **24V output**: 18 AWG wire (up to 10 feet)
- **Ethernet cable**: Cat5e or better, up to 100m

### Mounting Considerations

- **DC-DC converter**: Mount in weatherproof enclosure
- **PoE injector**: Can be mounted near AP or in equipment box
- **Heat dissipation**: Both components generate minimal heat

### Safety Considerations

- **Fuse protection**: 15A fuse on 12V input line
- **Grounding**: Proper grounding for outdoor installation
- **Weatherproofing**: Use appropriate enclosures for outdoor use

## Cost Comparison

| Solution | Components | Total Cost | Efficiency | Power Draw |
|----------|------------|------------|------------|------------|
| Two-component | DC-DC + PoE | $40-50 | 85% | 10W |
| One-component | 12V PoE | $35-40 | 80% | 12W |

## Solar Panel Requirements

### For 10W Load (Two-component)

- **Minimum panel**: 20W (accounting for 50% efficiency)
- **Recommended panel**: 30W (for cloudy days and battery charging)
- **Charge controller**: 10A PWM or MPPT

### For 12W Load (One-component)

- **Minimum panel**: 24W
- **Recommended panel**: 36W
- **Charge controller**: 10A PWM or MPPT

## Maintenance and Troubleshooting

### Regular Checks

- **Battery voltage**: Monitor 12V input voltage
- **Connections**: Check for corrosion or loose connections
- **Heat**: Ensure adequate ventilation around components

### Common Issues

- **Low voltage**: Check battery charge and connections
- **No power to AP**: Verify 24V output from DC-DC converter
- **Poor performance**: Check Ethernet cable quality and length

## Parts List for Implementation

### Required Components

1. **Mean Well LDD-350H-24V** DC-DC converter
2. **Ubiquiti POE-24-24W-G** PoE injector
3. **15A fuse** and fuse holder
4. **14 AWG wire** (12V input)
5. **18 AWG wire** (24V output)
6. **Cat5e Ethernet cable**
7. **Weatherproof enclosure** (optional)

### Tools Needed

- **Wire strippers**
- **Crimping tool** for RJ45 connectors
- **Multimeter** for voltage testing
- **Drill** for mounting holes

## References

- [Mean Well LDD Series Datasheet](https://www.meanwell.com/Upload/PDF/LDD-H/LDD-H-spec.pdf)
- [Ubiquiti PoE Injector Specifications](https://www.ui.com/accessories/power-over-ethernet/)
- [UAP-AC-M Power Requirements](https://www.ui.com/unifi/unifi-ap-ac-mesh/)

---
*Last updated: [Current Date]*
*Document version: 1.0*
