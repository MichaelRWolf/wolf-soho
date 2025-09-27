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

### **🎯 MODERN APPROACH: UniFi Network Mobile App**
**No SSH, no wires, no 1990s bullshit!**

#### **Step 1: Download the App**
- **iOS**: Search "UniFi Network" in App Store
- **Android**: Search "UniFi Network" in Google Play
- **Free app** - no subscription needed for standalone mode

#### **Step 2: Power Up Device**
```bash
# 1. Plug in PoE power
# 2. Wait for steady white LED
# 3. Device should broadcast its own WiFi network
```

#### **Step 3: WiFi Connection Strategy**
**Critical**: You need to be on the SAME network as the device for the app to find it.

**Option A: Connect to Device's WiFi (Recommended)**
```bash
# 1. Look for WiFi: UAP-AC-M-XXXXXX (where XXXXXX is device MAC)
# 2. Connect to this WiFi network
# 3. Open UniFi Network app
# 4. App will find device automatically
```

**Option B: Direct Ethernet Connection**
```bash
# 1. Connect computer to PoE injector's LAN port
# 2. Set computer IP to 192.168.1.10 (subnet 255.255.255.0)
# 3. Open UniFi Network app on computer
# 4. App will find device on network
```

#### **How to Set Computer IP to 192.168.1.10:**

**Mac:**
1. **System Preferences** → **Network**
2. **Select Ethernet** (or Thunderbolt Ethernet) from left sidebar
3. **Configure IPv4**: Dropdown → **Manually**
4. **IP Address**: `192.168.1.10`
5. **Subnet Mask**: `255.255.255.0`
6. **Router**: `192.168.1.1` (or leave blank)
7. **DNS**: Leave blank or use `8.8.8.8`
8. **Click "Apply"**

**To Restore Later:**
- Change back to "Using DHCP" in Network settings

**Option C: Same Network as Device**
```bash
# 1. If device is connected to Trails End WiFi, connect to Trails End WiFi
# 2. If device is on its own network, connect to device's network
# 3. App needs to be on same network segment as device
```

#### **Step 4: Configure via App**
```bash
# 1. Open UniFi Network app
# 2. Tap "Add Device" 
# 3. App should auto-discover device
# 4. Wait for "Green-check... UniFi Network Server started"
# 5. Click "Manage Server in Browser"
# 6. Follow setup wizard
# 7. Configure WiFi client mode for "Trails End Crew"
```

#### **What "UniFi Network Server Started" Means:**
- **Device is discovered** and ready for configuration
- **Web interface is available** via browser
- **Server is running** on the device
- **Ready for setup** - you can now configure the device

#### **Web Interface Login Credentials:**
- **URL**: `127.0.0.1:8080/manage/account/login`
- **Username**: `admin`
- **Password**: `admin`
- **If that doesn't work**: Try `ubnt` / `ubnt`
- **If both fail**: Try `root` / `ubnt` or `admin` / `password`
- **Last resort**: Check device label for default credentials

#### **🚨 PROBLEM: Device is in Controller Mode, Not Standalone Mode**
**Both web interface and mobile app are asking for credentials because the device is running UniFi Network Controller software.**

**Why This is Wrong:**
- **No internet connection** - can't authenticate online accounts
- **Direct connection** to device - should use local credentials
- **Controller software** - designed for network management, not device setup
- **Wrong approach** - device should be in standalone mode, not controller mode

**Solution:**
- **Factory reset device** to clear controller configuration
- **Device should boot in standalone mode** (not controller mode)
- **Standalone mode** = no credentials needed, direct device configuration
- **Controller mode** = requires online account authentication (wrong for your use case)

#### **What the UniFi Network App Does:**
- **Auto-discovers** device on network
- **Guides you** through setup step-by-step
- **No SSH** or command line needed
- **Visual configuration** - point and tap
- **Saves settings** automatically
**Goal**: Make device broadcast its own WiFi SSID for web-based configuration

#### **App Configuration Steps:**
1. **Device Discovery**: App will find your Ubiquiti device
2. **Standalone Mode**: Choose "Standalone Access Point" (not mesh)
3. **WiFi Client Setup**: 
   - Add "Trails End Crew" network
   - Enter password
   - Set as primary connection
4. **Network Bridge**: Configure to bridge to RV network (192.168.8.x)
5. **Save and Apply**: App handles all the technical details

#### **What Happens Next:**
- Device connects to "Trails End Crew" automatically
- Bridges internet to your RV network
- No SSH, no command line, no manual IP configuration
- UniFi Network app manages everything for you

#### **If UniFi Network App Doesn't Find Device:**
- Make sure device has steady white LED
- Try scanning QR code on device label
- Check that your phone is on same WiFi network as device
- Restart UniFi Network app if needed

#### **WiFi Connection Troubleshooting:**
**Problem**: Device doesn't broadcast its own WiFi SSID

**🚨 IMMEDIATE FIX: Force Factory Reset**
```bash
# 1. UNPLUG PoE power completely
# 2. Press and hold reset button
# 3. WHILE HOLDING reset button, plug in PoE power
# 4. Keep holding for 30+ seconds (be patient!)
# 5. Release and wait for boot
# 6. Look for UAP-AC-M-XXXXXX WiFi network
```

**Why This Happens:**
- Device has existing configuration (not factory default)
- May be connected to a controller somewhere
- Needs complete factory reset to broadcast its own WiFi
- 30+ second reset ensures complete wipe

**Solution 2: Use Ethernet Connection**
```bash
# 1. Connect computer to PoE injector's LAN port
# 2. Set computer IP to 192.168.1.10
# 3. Use UniFi Network app on computer
# 4. App will find device via network discovery
```

**Solution 3: Check Device Status**
- **Steady white LED**: Device is ready
- **Blue LED**: Device is connected to controller (needs reset)
- **No LED**: Check PoE power connection

#### **Quick Diagnostic:**
**What LED color do you see?**
- **Blue LED** = Device is connected to a controller → **NEEDS RESET**
- **Steady White** = Device is ready but not broadcasting WiFi → **NEEDS RESET**
- **Blinking White** = Device is booting → **Wait for steady light**
- **No Light** = No power → **Check PoE connection**

**The Fix:**
1. **Do the 30+ second reset** (see above)
2. **Wait for steady white LED**
3. **Look for UAP-AC-M-XXXXXX WiFi network**
4. **If still no WiFi, try 60+ second reset**

#### **60-Second Reset: Recovery Mode (Different Reset Type)**
**⚠️ WARNING: This can create a brick if not done carefully!**

**This is NOT a "better" 30-second reset - it's a completely different mode:**

```bash
# 1. UNPLUG PoE power completely
# 2. Press and hold reset button
# 3. WHILE HOLDING reset button, plug in PoE power
# 4. Keep holding for 60+ seconds
# 5. Release and wait for boot
```

**What 60+ Seconds Does:**
- **Recovery Mode**: Forces device into recovery/firmware mode
- **Complete System Reset**: Wipes firmware and configuration
- **Network Reset**: Clears all network associations and IP settings
- **Controller Disassociation**: Breaks ALL controller connections
- **Last Resort**: Only use if 30-second reset doesn't work

**⚠️ BRICK RISK:**
- **Device has built-in firmware** - it can recover without network
- **BUT**: If firmware is corrupted, device may become unusable
- **Recovery requires**: Device to have valid firmware stored internally
- **No network needed**: Device can rebuild from internal firmware

**When to Use 60+ Seconds:**
- Device is "stuck" in controller mode
- 30-second reset didn't clear mesh adoption
- Device won't broadcast its own WiFi
- LED stays blue after 30-second reset
- Device appears "bricked" or unresponsive

**⚠️ SAFETY CHECK:**
- **Only use if 30-second reset failed**
- **Device should have steady white LED** before attempting
- **If device becomes unresponsive**: May need professional recovery

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