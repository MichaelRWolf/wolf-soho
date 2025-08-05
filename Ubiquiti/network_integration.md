# Ubiquiti Network Integration Guide

## Current Network Architecture

### Existing Setup
```
Internet Sources:
├── Trails End WiFi Networks
│   ├── Trails End Crew (password protected)
│   └── Trails End WiFi (public)
├── Mobile Hotspot (wolfden-hotspot)
└── Other Campground WiFi

Current Flow:
Trails End WiFi → wolfden-router (client mode) → Running Wolf Router → Local Devices
```

### Target Integration Options

#### Option 1: Enhanced Bridge (Recommended)
```
Trails End WiFi → wolfden-mesh (client) → wolfden-router → Running Wolf Router → Local Devices
```
**Benefits:**
- Better signal reception with outdoor mounting
- Maintains existing network structure
- wolfden-router continues as primary router
- Easy fallback to existing setup

#### Option 2: Direct Bridge
```
Trails End WiFi → wolfden-mesh (client) → Running Wolf Router (direct) → Local Devices
```
**Benefits:**
- Simplified network path
- Reduced latency
- Single device management
**Considerations:**
- Requires reconfiguring wolfden-router
- May lose some router features

#### Option 3: Parallel Setup
```
Trails End WiFi → wolfden-mesh (client) → Running Wolf Router
Trails End WiFi → wolfden-router (client) → Running Wolf Router (backup)
```
**Benefits:**
- Redundancy and failover
- Load balancing possible
- Gradual migration path

## Integration Steps

### Phase 1: Device Setup
1. **Power and Mount**: Install PoE injector and mount device
2. **Initial Configuration**: Configure standalone mode
3. **WiFi Client Setup**: Connect to Trails End networks
4. **Network Bridge**: Configure to RV network subnet

### Phase 2: Network Integration
1. **IP Assignment**: Assign static IP (192.168.8.130)
2. **Gateway Configuration**: Point to wolfden-router (192.168.8.1)
3. **DNS Setup**: Use wolfden-router as DNS server
4. **Bridge Mode**: Enable network bridging

### Phase 3: Testing and Optimization
1. **Signal Testing**: Test signal strength and stability
2. **Speed Testing**: Compare performance with existing setup
3. **Failover Testing**: Test fallback to existing setup
4. **Load Balancing**: Configure if using parallel setup

## Network Configuration

### Device IP Assignment
- **wolfden-router**: 192.168.8.1 (existing)
- **wolfden-mesh**: 192.168.8.130 (new)
- **wolfden-nas**: 192.168.8.129 (existing)
- **Client devices**: 192.168.8.2-128 (DHCP)

### Subnet Configuration
- **Network**: 192.168.8.0/24
- **Subnet Mask**: 255.255.255.0
- **Gateway**: 192.168.8.1 (wolfden-router)
- **DNS**: 192.168.8.1

### WiFi Client Configuration
```bash
# Primary network (password protected)
SSID: Trails End Crew
Security: WPA2
Password: [campground password]

# Backup network (public)
SSID: Trails End WiFi
Security: Open
```

## Performance Optimization

### Signal Optimization
- **Mounting**: Outdoor mounting for better signal reception
- **Antenna Orientation**: Point toward Trails End WiFi source
- **Height**: Mount as high as practical
- **Line of Sight**: Minimize obstructions

### Network Optimization
- **Band Selection**: Use 5GHz for better performance
- **Channel Selection**: Auto-select or manual for best channel
- **Power Management**: Adjust transmit power as needed
- **QoS**: Configure quality of service if needed

## Monitoring and Maintenance

### Performance Monitoring
```bash
# Check device status
ssh ubnt@192.168.8.130
mca-status

# Check signal strength
mca-cli
show wireless.1.status
```

### Network Monitoring
```bash
# Test connectivity
ping 192.168.8.130
ping 8.8.8.8

# Check network speed
speedtest-cli

# Monitor bandwidth usage
iftop -i eth0
```

### Maintenance Tasks
- **Weekly**: Check device status and signal strength
- **Monthly**: Review performance metrics
- **Seasonal**: Clean device and check mounting
- **As Needed**: Update configuration for new campgrounds

## Troubleshooting Integration

### Common Integration Issues

#### Device Not Connecting to Trails End WiFi
- Verify SSID and password
- Check signal strength
- Ensure device is in client mode
- Test with different Trails End networks

#### Bridge Mode Not Working
- Verify IP configuration
- Check subnet settings
- Ensure no IP conflicts
- Test network connectivity

#### Performance Issues
- Check signal strength and quality
- Verify bandwidth allocation
- Monitor for interference
- Consider alternative mounting locations

#### Network Conflicts
- Verify IP address uniqueness
- Check for duplicate MAC addresses
- Ensure proper subnet configuration
- Test network isolation 