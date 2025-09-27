# Ubiquiti UniFi AC Mesh Setup

## Device Information

- **Model**: UAP-AC-M-US
- **Manufacturer**: Ubiquiti (unifi.ui.com)
- **Purchased**: 2025-07 from Amazon
- **Status**: New device, needs configuration

## Power-On Reset Timing

| Reset Type | Reset Button Press (seconds) | Explanation |
|------------|------------------------------|-------------|
| **Power Cycle** | 0 | Simple reboot, keeps configuration |
| **Soft Reset** | 10-15 | Clears some config, keeps network settings |
| **Factory Reset** | 15-30 | Factory defaults, clears mesh associations |
| **Recovery Reset** | 60+ | Complete factory reset, last resort |

### Reset Sequence

1. **Power ON** device (plug in PoE)
2. **Within 2-3 seconds** of power-on, press and hold reset button
3. **Keep holding** for specified duration
4. **Release** and let device boot

## Verified Login Sequence

### Factory Reset Method

1. **Reset with 15-second power press** (see table above)
2. **SSH access**:

   ```bash
   ssh -o KexAlgorithms=+diffie-hellman-group1-sha1 -o HostKeyAlgorithms=+ssh-rsa ubnt@192.168.1.20
   ```

3. **Password**: `ubnt`

### Alternative Access Methods

- **Web Interface**: `http://192.168.1.20` (default credentials: `ubnt`/`ubnt`)
- **Device SSID**: Look for `UAP-AC-M-XXXXXX` (where XXXXXX is device MAC)

## Operating Modes

### Mode 1: Mesh Peer (Default)

- Device becomes part of existing UniFi mesh network
- Requires admin access to mesh controller
- **Not suitable** for Trails End CG (no admin access)

### Mode 2: Standalone Client (Target Configuration)

- Device connects to existing WiFi networks as a client
- Acts as a bridge/repeater without joining mesh
- **Suitable** for Trails End CG (no admin access required)

## Configuration Approach

### Standalone Setup (Recommended)

The UAP-AC-M-US can be configured in standalone mode to:

1. Connect to Trails End WiFi networks as a client
2. Bridge the connection to the RV network
3. Provide better signal reception than the current `wolfden-router`

### Setup Steps

#### 1. Initial Device Setup

```bash
# Power on device with PoE injector
# Device will broadcast its own SSID for initial configuration
# SSID format: UAP-AC-M-XXXXXX (where XXXXXX is device MAC)
```

#### 2. Access Device Configuration

- **Option A**: Web interface via device IP (default: 192.168.1.20)
- **Option B**: SSH access (username: ubnt, password: ubnt)
- **Option C**: UniFi Network mobile app (standalone mode)

#### 3. Configure Standalone Mode

1. **Access Point Mode**: Set to "Access Point" (not "Mesh")
2. **WiFi Configuration**:
   - Connect to Trails End SSIDs as client
   - Examples: `Trails End Crew`, `Trails End WiFi`
3. **Network Bridge**: Configure to bridge to RV network
4. **Power**: Use PoE injector for power + data

### Integration with Existing Network

#### Current Setup

```text
Trails End WiFi → wolfden-router (client mode) → Running Wolf Router
```

#### Proposed Setup

```text
Trails End WiFi → wolfden-mesh (client mode) → wolfden-router → Running Wolf Router
```

#### Alternative Setup

```text
Trails End WiFi → wolfden-mesh (client mode) → Running Wolf Router (direct)
```

## Hardware Requirements

### PoE Setup

- **PoE Injector**: Required for power and data
- **Cable**: Single Cat5 cable for power + data
- **Mounting**: Outdoor mounting capability for better signal

### Power Considerations

- PoE injector plugs into RV power
- Device can be mounted outside RV
- Single cable solution (power + data)

## Configuration Commands

### SSH Access

```bash
# Default credentials
ssh ubnt@192.168.1.20
# Password: ubnt

# Check device status
mca-status

# Configure WiFi client mode
mca-cli
```

### Web Interface

- Navigate to device IP (default: 192.168.1.20)
- Configure WiFi client settings
- Set bridge mode for network connection

## Troubleshooting

### Common Issues

1. **Device not broadcasting SSID**: Check PoE power
2. **Can't access web interface**: Verify IP address and network
3. **WiFi client mode not working**: Check credentials and signal strength
4. **Bridge mode issues**: Verify network configuration

### Reset to Factory Defaults

```bash
# SSH into device
ssh ubnt@192.168.1.20

# Reset to factory defaults
syswrapper.sh restore-default
```

## Next Steps

1. Power on device and verify PoE connection
2. Access device configuration interface
3. Configure standalone client mode
4. Test connection to Trails End WiFi networks
5. Integrate with existing RV network setup
