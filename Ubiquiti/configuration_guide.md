# Ubiquiti Configuration Guide

## Initial Setup Process

### Step 1: Power and Network Connection
```bash
# Connect PoE injector to power and network
# Connect device to PoE injector
# Device will boot and broadcast its own SSID
```

### Step 2: Access Device Configuration
**Option A: Web Interface**
- Device default IP: `192.168.1.20`
- Open browser: `http://192.168.1.20`
- Default credentials: `ubnt` / `ubnt`

**Option B: SSH Access**
```bash
ssh ubnt@192.168.1.20
# Password: ubnt
```

**Option C: Device SSID**
- Look for SSID: `UAP-AC-M-XXXXXX` (where XXXXXX is device MAC)
- Connect to this SSID for initial configuration

## SSH Access Issues

### Common SSH Error
When attempting SSH access, you may encounter:
```bash
$ ssh ubnt@192.168.1.20
Unable to negotiate with 192.168.1.20 port 22: no matching host key type found. Their offer: ssh-rsa,ssh-dss
```

### Why This Happens
- **Ubiquiti devices** use older SSH algorithms for compatibility
- **Modern SSH clients** (OpenSSH 8.8+) disable these by default for security
- **The device offers**: `ssh-rsa,ssh-dss` (older algorithms)
- **Your client rejects**: These older, less secure algorithms

### Solutions

#### Option 1: Force SSH to accept older algorithms
```bash
ssh -o KexAlgorithms=+diffie-hellman-group1-sha1 -o HostKeyAlgorithms=+ssh-rsa ubnt@192.168.1.20
```

#### Option 2: Use a more comprehensive approach
```bash
ssh -o KexAlgorithms=+diffie-hellman-group1-sha1 -o HostKeyAlgorithms=+ssh-rsa -o Ciphers=+aes128-cbc ubnt@192.168.1.20
```

#### Option 3: Create an SSH config entry (recommended)
Add this to your `~/.ssh/config`:
```
Host 192.168.1.20
    HostKeyAlgorithms +ssh-rsa
    KexAlgorithms +diffie-hellman-group1-sha1
    Ciphers +aes128-cbc
    User ubnt
```

Then you can simply use:
```bash
ssh 192.168.1.20
```

### Alternative Access Methods
If SSH continues to be problematic, you can also access the device via:
- **Web interface**: `http://192.168.1.20`
- **Device SSID**: Look for `UAP-AC-M-XXXXXX` WiFi network

The web interface is often easier for initial configuration anyway, and you can configure SSH settings from there if needed.

### Step 3: Configure Standalone Mode

#### Web Interface Configuration
1. **Access Point Mode**: Set to "Access Point" (not "Mesh")
2. **WiFi Client Configuration**:
   - Enable WiFi client mode
   - Add Trails End networks:
     - `Trails End Crew` (password protected)
     - `Trails End WiFi` (public)
3. **Network Bridge**: Configure to bridge to RV network
4. **Save Configuration**

#### SSH Configuration
```bash
# SSH into device
ssh ubnt@192.168.1.20

# Check current status
mca-status

# Enter configuration mode
mca-cli

# Configure WiFi client mode
set wireless.1.ssid "Trails End Crew"
set wireless.1.security wpa2
set wireless.1.key "your_password"

# Configure bridge mode
set network.lan.proto static
set network.lan.ipaddr 192.168.8.130
set network.lan.netmask 255.255.255.0

# Commit and save
commit
save
```

## Network Integration Options

### Option 1: Bridge to Existing Router
```
Trails End WiFi → wolfden-mesh (client) → wolfden-router → Running Wolf Router
```

### Option 2: Direct Bridge
```
Trails End WiFi → wolfden-mesh (client) → Running Wolf Router (direct)
```

### Option 3: Enhanced Repeater
```
Trails End WiFi → wolfden-mesh (client) → wolfden-router (enhanced) → Running Wolf Router
```

## Troubleshooting

### Common Issues and Solutions

#### Device Not Broadcasting SSID
```bash
# Check PoE power
# Verify cable connections
# Reset device if needed
syswrapper.sh restore-default
```

#### Can't Access Web Interface
```bash
# Check network connectivity
ping 192.168.1.20

# Try different IP if changed
arp -a | grep ubnt

# Reset to factory defaults if needed
```

#### WiFi Client Mode Not Working
- Verify SSID and password
- Check signal strength
- Ensure device is in standalone mode (not mesh)
- Test with different Trails End networks

#### Bridge Mode Issues
- Verify network configuration
- Check IP address conflicts
- Ensure proper subnet configuration

## Configuration Files

### Default Network Settings
- **IP Address**: 192.168.1.20
- **Subnet**: 255.255.255.0
- **Gateway**: 192.168.1.1
- **DNS**: 8.8.8.8, 8.8.4.4

### Target Network Settings
- **IP Address**: 192.168.8.130 (static)
- **Subnet**: 255.255.255.0
- **Gateway**: 192.168.8.1 (wolfden-router)
- **DNS**: 192.168.8.1

## Reset Procedures

### Factory Reset
```bash
# SSH into device
ssh ubnt@192.168.1.20

# Reset to factory defaults
syswrapper.sh restore-default

# Device will reboot with default settings
```

### Soft Reset (Configuration Only)
```bash
# Reset configuration but keep network settings
mca-cli
delete wireless.1
delete network.lan
commit
save
``` 