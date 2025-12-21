# Ubiquiti airMAX PtP Configuration (DRY Refactor)

This document records the **intended, deployed configuration** for the Wolfden point‑to‑point wireless bridge.  
It is structured to avoid duplication by separating **shared link settings** from **device‑specific differences**.

---

## 1. Shared PtP Link Configuration

These settings **must match exactly** on both devices.

### Link Identity
- Link Name / SSID: `Running Wolf PtP`
- Purpose: House ↔ RV Ethernet bridge
- Distance: ~460–500 feet
- Line of Sight: Yes (tree trunks only; no foliage blockage)

### Wireless Security
- Authentication: WPA2 Personal (PSK)
- Encryption: AES
- Passphrase: Stored in 1Password

**1Password Entry**
```
Wolfden – Running Wolf PtP – WPA2 Link Key
```

### RF Parameters
- Band: 5 GHz
- Channel Width: 40 MHz
- Frequency: Fixed (identical on both sides)
- Output Power: Low / default during alignment

### airMAX / Bridge Behavior
- PtP Mode: Enabled
- airMAX: Implicitly enabled by PtP mode
- Transparent bridging: Enabled (Layer‑2 bridge, no NAT)

### Management & Access
- Admin Interface: HTTP Web UI
- Browser Compatibility: Safari required (Chrome unreliable)
- SSH: Available (may require legacy algorithm flags)
- Country / Regulatory Domain: Set identically on both devices

---

## 2. House‑Side Device — PtP Access Point

### Identity
**1Password Entry**
```
Wolfden – Ubiquiti Loco5AC – House PtP (AP)
```

### Hardware
- Model: Ubiquiti NanoStation Loco5AC
- MAC Address: **1C:6A:1B:CA:EF:9B**
- Power: 24V passive PoE (POE‑24‑12W)

### Role
- Point‑to‑Point **Access Point**
- Initiates PtP link
- No client Wi‑Fi service

### Wireless Role Settings
- Access Point: ON
- PtP Mode: ON

### Management Networking
- Management IP Mode: DHCP
- DHCP Fallback IP: 192.168.1.20 /24
- Static IP: Deferred until link validation complete

### Operational Notes
- Configured on bench via Safari
- Management radio disabled temporarily
- Mounted at house, aimed toward RV

---

## 3. RV‑Side Device — PtP Station

### Identity
**1Password Entry**
```
Wolfden – Ubiquiti Loco5AC – RV PtP (Station)
```

### Hardware
- Model: Ubiquiti NanoStation Loco5AC
- MAC Address: **1C:6A:1B:C6:E5:A3**
- Power: 24V passive PoE (POE‑24‑12W)

### Role
- Point‑to‑Point **Station**
- Associates to House AP
- No client Wi‑Fi service

### Wireless Role Settings
- Access Point: OFF
- PtP Mode: ON  
  *(Station role is inferred from this combination)*

### Management Networking
- Management IP Mode: DHCP
- DHCP Fallback IP: 192.168.1.20 /24 (factory default)
- Static IP: To be assigned after link alignment

### Operational Notes
- Bench‑configured prior to outdoor mounting
- Receives DHCP lease across PtP bridge once link is active
- Mounted near RV, aimed toward house

---

## 4. Alignment & Deployment Assumptions

- Temporary mounts used for alignment
- Low transmit power during alignment to avoid masking mis‑aim
- Fine alignment performed using:
  - Signal strength
  - Noise floor
  - SNR / airMAX quality metrics
- Permanent mounting only after stable link confirmed

---

## 5. Change Control

Any change to the following **must be applied symmetrically** and documented:

- SSID
- WPA2 key
- Channel width
- Frequency
- Regulatory domain
- Management IP mode

This document and the corresponding 1Password entries are the **source of truth**.
