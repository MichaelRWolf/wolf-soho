# HOWTO: Campground WiFi Repeater Setup (NanoStation Loco5AC)

Bridges "Trails End Wifi" from the mesh cone zone back to RV via Cat5 + Beryl local broadcast.

---

## Overview

**Topology:**

```text
Ubiquiti Mesh (20 ft up, ~100 ft away)
        ↓ (WiFi signal into cone zone)
        ↓ 
NanoStation Loco5AC [Station mode, Bridge]
        ↓ (PoE-powered, Cat5 100 ft back to RV)
        ↓
Beryl [in RV]
        ↓ (broadcasts locally via WiFi)
        → RV interior ground-level coverage
```

**Hardware Required:**

- 1× `loco-bridge` (Ubiquiti NanoStation Loco5AC, configured in Station mode to join "Trails End Wifi")
- 1× `poe-trails-end` (Ubiquiti POE-24-12W injector, PoE power for loco-bridge)
- Cat5/Cat6 cable, ~100 feet (from cone zone to RV)
- 1× `beryl` (in RV, acts as local AP)
- `michael-pro` or `wolf-air` with `belkin-dongle` (USB-C Ethernet adapter, for bench config)

*See CONTEXT.md for device registry.*

---

## Config Backup & Recovery

**Before modifying loco-bridge for Trails End**, save its current configuration in case you need to restore it later (returning to winter setup at Moe's or RV).

### Export Config via Web UI

1. Navigate to **System → Backup** in the NanoStation web UI
2. Click **Download Configuration Backup**
3. Save the `.tar.gz` file to your laptop with a descriptive name:

   ```bash
   loco-bridge-trails-end-backup-2026-07-09.tar.gz
   ```

### Import Config via Web UI

When returning to the previous setup:

1. Navigate to **System → Backup**
2. Click **Choose File** and select your saved `.tar.gz` backup
3. Click **Upload & Restore**
4. Device reboots and restores all previous settings

### Default IP After Factory Reset

If you factory reset loco-bridge and need to access it during recovery:

- **Ubiquiti factory default IP** is **192.168.1.20** (may vary by firmware)
- **In this setup**, loco-bridge is configured at **192.168.1.22** (not the factory default)
- After factory reset, the device will be at **192.168.1.20** temporarily
- Once you reconfigure it to 192.168.1.22, use: `ssh admin@192.168.1.22` (or `ssh loco-bridge`)
- For recovery/diagnosis at factory default: `ssh admin@192.168.1.20` (password: `ubiquiti`)
- Or access via web UI: `http://192.168.1.20` (Safari only)
- If neither works, check device logs or try mDNS: `ssh admin@nanostation.local`

**Note:** Avoid confusing loco-bridge (192.168.1.22, Trails End repeater) with loco-ap (192.168.1.20, Moe's PtP) or loco-station (192.168.1.21, RV PtP).

---

## Bench Setup (Before Deployment)

### System WiFi Configuration (System-Wide)

Before starting bench setup, disable WiFi globally. This setting applies to **all locations**, not just the Ubiquiti-Setup location.

- **Menu bar:** Click WiFi icon → **Turn WiFi Off**
- *(It stays off across location switches until you toggle it back on)*

### Network Location Configuration (Location-Specific)

Create and configure a new network location. These settings are saved **per location** -- switching locations changes them automatically.

1. System Settings → Network → Location → **Add Location**
2. Name: `Ubiquiti-Setup`
3. In the right pane, configure services:
   - **Belkin USB-C LAN / Thunderbolt Ethernet:** Enabled (selected in list)
   - All other services: Disabled (not in list or unselected)
4. Click **Belkin USB-C LAN** to edit its IPv4 settings:
   - IPv4 Configuration: **Configure Manually**
   - IP Address: `192.168.1.100`
   - Subnet Mask: `255.255.255.0`
   - Router: *(leave blank)*
   - DNS: *(leave blank)*
5. Apply and save location

### Wiring (Bench)

```text
MacBook → USB-C Ethernet → PoE LAN (⚡) → PoE PoE (⇄) → NanoStation Loco5AC
```

- **LAN/⚡ port:** Connect to Mac
- **PoE/⇄ port:** Connect to NanoStation

### Access the Device

- **SSH:** `ssh admin@192.168.1.20`
- **Web UI:** `http://192.168.1.20` (Safari only; Chrome blocks HTTP)
- **Password:** *(See 1Password)*

---

## NanoStation Configuration (Station Mode)

### UI Settings: Network

Navigate to: **System → Network**

| Setting               | Value           |
|-----------------------|-----------------|
| NETWORK MODE          | **Bridge**      |
| MANAGEMENT IP ADDRESS | **Static**      |
| IP ADDRESS            | `192.168.1.22`  |
| NETMASK               | `255.255.255.0` |
| GATEWAY               | *(leave blank)* |
| DNS                   | *(leave blank)* |

### UI Settings: Wireless → Basic Wireless Settings

Navigate to: **Wireless → Basic Wireless Settings**

| Setting       | Value                                                       |
|---------------|-------------------------------------------------------------|
| ACCESS POINT  | **Off** *(Off means Station mode, not AP)*                  |
| PTP MODE      | **Off** *(using WiFi client mode, not PtP)*                 |
| SSID          | `Trails End Wifi` *(exactly as broadcast by Ubiquiti mesh)* |
| WIRELESS MODE | **802.11ac**                                                |
| CHANNEL WIDTH | **40 MHz**                                                  |
| FREQUENCY     | Auto *(or manual if Ubiquiti is on fixed channel)*          |

### UI Settings: Wireless → Security

Navigate to: **Wireless → Security**

**If "Trails End Wifi" is open/unencrypted** (no password):

The web UI does not expose an "Open" security option -- you must disable WPA2 via CLI first.

#### Disable WPA2 via Telnet (Required for Open SSID)

1. From your macOS terminal:

   ```bash
   telnet 192.168.1.22
   ```

2. Once connected (prompt: `BusyBox v1.00`), run either:

   **sed (text replacement) -- confirmed for NanoStation Loco5AC**

   ```bash
   sed -i 's/aaa.1.wpa.mode=2/aaa.1.wpa.mode=0/g' /tmp/system.cfg
   ```

   *(uci config tool not available on this model)*

3. Reboot the device:

   ```bash
   reboot
   ```

4. Wait 30 seconds for boot, then return to web UI. SECURITY should now show **Open** option.

#### Configure Web UI After WPA2 Disabled

| Setting  | Value                |
|----------|----------------------|
| SECURITY | **Open** or **None** |

**If "Trails End Wifi" is encrypted with WPA2:**

| Setting            | Value                                  |
|--------------------|----------------------------------------|
| SECURITY           | **WPA2 Personal**                      |
| WPA2 PRESHARED KEY | *(same passphrase as Trails End Wifi)* |

### UI Settings: Transmit Power

Navigate to: **Wireless** (may be under **Advanced** in some firmware versions)

| Setting        | Value                                                                   |
|----------------|-------------------------------------------------------------------------|
| TRANSMIT POWER | Leave at **default or maximum** for field deployment *(+20 to +24 dBm)* |
|                | Slider range typically -4 to +25 dBm depending on firmware              |
|                | *(Lower power useful for bench testing; increase for 100 ft+ distance)* |

**Other settings:**

- **ANTENNA GAIN:** Leave default
- **TX/RX CHAINS:** Leave default

---

## Validation (Bench)

**Before starting:** Confirm you're using the `Ubiquiti-Setup` network location (System Settings → Network → Location dropdown shows `Ubiquiti-Setup`). This activates the Belkin USB-C LAN configuration.

1. Power cycle the NanoStation
2. Wait 30 seconds for boot
3. SSH into `192.168.1.20` and check status:

```bash
ssh -o KexAlgorithms=+diffie-hellman-group1-sha1 \
    -o HostKeyAlgorithms=+ssh-rsa \
    -o Ciphers=+aes128-cbc \
    admin@192.168.1.20
```

1. Once connected via SSH:

```bash
# Check device info
cat /etc/board.info

# Check wireless status
cat /tmp/system.cfg | grep wireless

# Check if "Trails End Wifi" is visible
iwlist wlan0 scan | grep -i "trails"
```

1. Via Web UI (**<http://192.168.1.20>**):
   - Go to **Main / Status**
   - **Wireless** section should show:
     - **Mode:** Station
     - **SSID:** Trails End Wifi
     - **Signal Strength:** visible (dBm, negative number)
     - **Link State:** Connected or Connecting

---

## Field Deployment

### Cone Zone Setup (100 feet from Ubiquiti pole)

1. **Mount NanoStation:**
   - Position on tripod or temporary mount in the cone zone (ground level)
   - **Aim antenna upward 15-20°** into the cone (directional antenna, not omnidirectional)
   - This is critical -- the antenna pattern is narrow

2. **Power:**
   - Connect PoE injector
   - Plug Mac or portable battery into PoE LAN port
   - Wait for boot (30 seconds)

3. **Verify Signal:**
   - **Location:** Switch to `Ubiquiti-Setup` location (System Settings → Network → Location)
   - SSH into `192.168.1.20` (via the temporary PoE connection through Belkin USB-C LAN)
   - Check signal strength: `cat /tmp/system.cfg | grep rssi`
   - Should be **-50 to -60 dBm** in the cone zone
   - If weaker, adjust antenna angle slightly

4. **Run Cat5 Cable:**
   - From NanoStation PoE PoE port to RV
   - Secure for weather (conduit, clips)
   - Run 100 feet back to RV

### RV Setup

1. **Connect PoE at RV end:**
   - Run Cat5 into RV
   - Connect to PoE LAN port
   - Plug PoE LAN port into wall power

2. **Separate PoE at RV:**
   - Connect Cat5 from PoE PoE port to Beryl WAN port (or LAN, depending on Beryl mode)

3. **Configure Beryl:**
   - Beryl should pick up network from NanoStation
   - Configure Beryl to **broadcast locally as access point**
   - SSID: "Wolf repeating TE" or "Trails End Wifi" (your choice)
   - Broadcast to cover RV interior and ground level

### Antenna Alignment (Fine-Tuning)

Walk the cone zone with your laptop running NetSpot:

- Adjust NanoStation antenna angle for maximum signal strength
- Small angle changes (5-10°) can mean 10+ dBm difference
- Lock mount once optimal angle is found

---

## Troubleshooting

### NanoStation won't connect to "Trails End Wifi"

- Verify SSID spelling exactly matches (case-sensitive in some configs)
- Verify WPA2 passphrase is correct
- Check if Trails End Wifi is broadcasting on 5 GHz (not 2.4 GHz)
- Try **WIRELESS MODE: 802.11ac + 802.11n** if stuck

### Signal is very weak (-70 dBm or worse)

- **Antenna angle:** Re-aim antenna upward into cone (15-20° elevation)
- **Antenna height:** Move NanoStation higher if possible
- **Location:** Move closer to Ubiquiti pole (cone is ~30 ft diameter)
- **Frequency interference:** Try manually setting to a different 5 GHz channel

### Beryl won't connect to NanoStation via Cat5

- Check PoE injector powers on (LED lights)
- Verify Cat5 cable continuity (test with another device)
- Check Beryl network settings (may need to set WAN port manually)
- Swap LAN/PoE port connections if unclear

### Poor speeds despite good signal

- Check for interference (use NetSpot to scan 5 GHz band)
- Try different channel width (20 MHz instead of 40 MHz)
- Verify no other devices are congesting the link
- Check if Trails End Wifi mesh is congested (time of day dependent)

---

## Performance Expectations

- **Signal in cone zone:** -50 to -60 dBm (excellent)
- **Signal at RV (after Beryl):** Depends on RV obstruction, expect -60 to -70 dBm locally
- **Throughput:** 20-50 Mbps over 100 ft Cat5 link (should be sufficient for texting, email, light browsing)
- **Latency:** 50-100 ms (acceptable for most uses)

---

## One-Minute Health Check (Weekly)

1. SSH into `192.168.1.20` and run:

   ```bash
   cat /tmp/system.cfg | grep -E "rssi|mode|ssid"
   ```

2. Verify:
   - Mode: Station
   - SSID: Trails End Wifi
   - Signal (rssi): -50 to -65 dBm

3. If signal degrades:
   - Check antenna angle hasn't shifted
   - Re-run NetSpot to spot interference
   - Consider seasonal foliage changes affecting signal

---

## References

- NanoStation Loco5AC User Guide: [Ubiquiti Docs](https://dl.ubnt.com/)
- PtP setup (for reference): `HOWTO_rascally_raccoon_PtP_config.md`
- Equipment specs: `equipment_networking.md`

---

END
