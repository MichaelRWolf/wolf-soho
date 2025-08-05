# Ubiquiti Setup on Trails End - Standalone Mode

## The Crucial Perspective Change

### **From "No-Fucking-Way" to "Hell-Yes":**
The key realization was that **"Trails End Crew" IS the external network** that can be used in standalone mode. 

**Previous Misconception**: Thinking the device needed to join the mesh infrastructure
**Correct Understanding**: The device can connect to "Trails End Crew" as a client (same as Beryl) but with better performance

### **Why This Works:**
1. **"Trails End Crew"** is a WiFi network (not mesh-only)
2. **Ubiquiti can connect** to any WiFi network in client mode
3. **No mesh adoption** required - just WiFi credentials
4. **Better hardware** = better performance than Beryl

### **Verification from Multiple Perspectives:**

#### **Network Perspective:**
- **Current**: Beryl connects to "Trails End Crew" → bridges to RV network
- **New**: Ubiquiti connects to "Trails End Crew" → bridges to RV network
- **Result**: Same network access, better performance

#### **Technical Perspective:**
- **Beryl**: Consumer router with internal antennas
- **Ubiquiti**: Professional device with outdoor mounting capability
- **Advantage**: Better signal reception and stability

#### **Operational Perspective:**
- **No admin access needed** - just WiFi credentials
- **No mesh integration** - pure client mode
- **Same end result** - internet access for RV

## Step-by-Step Setup

### **Step 1: Factory Reset (15-second method)**
```bash
# Power ON device (plug in PoE)
# Within 2-3 seconds, press and hold reset button
# Keep holding for 15 seconds
# Release and wait for boot
```

### **Step 2: SSH Access**
```bash
# Connect via SSH with proper parameters
ssh -o KexAlgorithms=+diffie-hellman-group1-sha1 -o HostKeyAlgorithms=+ssh-rsa ubnt@192.168.1.20
# Password: ubnt
```

### **Step 3: Configure Standalone Mode**
```bash
# Enter configuration mode
mca-cli

# Set to standalone access point mode
set wireless.1.mode ap

# Configure WiFi client connection to Trails End Crew
set wireless.1.ssid "Trails End Crew"
set wireless.1.security wpa2
set wireless.1.key "[TRAILS_END_CREW_PASSWORD]"

# Configure network bridge
set network.lan.proto static
set network.lan.ipaddr 192.168.8.130
set network.lan.netmask 255.255.255.0
set network.lan.gateway 192.168.8.1

# Commit and save
commit
save
```

### **Step 4: Reboot Device**
```bash
# Reboot to apply configuration
reboot
```

### **Step 5: Test Configuration**
```bash
# SSH back into device
ssh -o KexAlgorithms=+diffie-hellman-group1-sha1 -o HostKeyAlgorithms=+ssh-rsa ubnt@192.168.8.130

# Check connection status
mca-status
```

## Expected Results

### **Network Flow:**
```
Trails End Crew WiFi → Ubiquiti (client mode) → Running Wolf Router → Local Devices
```

### **Performance Improvements:**
- **Better signal strength** due to outdoor mounting
- **More stable connection** due to professional hardware
- **Higher speeds** due to better signal quality
- **Reduced disconnections** during Zoom meetings

## Verification Checklist

### **Before Starting:**
- [ ] Device is factory reset and accessible via SSH
- [ ] "Trails End Crew" WiFi credentials are available
- [ ] RV network uses 192.168.8.x subnet
- [ ] PoE injector is available and compatible

### **After Configuration:**
- [ ] Device connects to "Trails End Crew" successfully
- [ ] RV devices can access internet through Ubiquiti
- [ ] Signal strength is better than current Beryl setup
- [ ] Zoom meetings are stable and professional

## Why This Will Work

### **1. Same Network Access:**
- Uses same "Trails End Crew" network as Beryl
- No mesh integration required
- Standard WiFi client mode

### **2. Better Hardware:**
- Professional-grade antennas
- Outdoor mounting capability
- Higher transmit power
- Better signal processing

### **3. Same Configuration:**
- Client mode connection
- Network bridge to RV
- Static IP assignment
- Standard routing

### **4. Proven Technology:**
- Ubiquiti devices designed for this use case
- WiFi client mode is standard functionality
- No experimental or untested features

## Conclusion

This setup will work because:
- **"Trails End Crew" is accessible WiFi** (not mesh-only)
- **Ubiquiti can connect as client** (same as Beryl)
- **Better hardware** provides performance improvement
- **No mesh adoption** required - just WiFi credentials

The device replaces Beryl's role with better performance, not a different network access method.