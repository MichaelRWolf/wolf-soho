# Ubiquiti airMAX PtP Configuration (DRY Refactor)

This document records the **intended, deployed configuration** for the Wolfden point‑to‑point wireless bridge.
It is structured to avoid duplication by separating **shared link settings** from **device‑specific differences**.

> **Status:** Configuration complete. PtP is production‑ready and set‑and‑forget.

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
- Output Power: Default / low during alignment; left unchanged post‑deployment

### airMAX / Bridge Behavior
- PtP Mode: Enabled
- airMAX: Enabled implicitly by PtP mode
- Transparent bridging: Enabled (Layer‑2 bridge, no NAT)

### Regulatory / Country
- Regulatory Domain: **US**
- Country setting verified on both radios
- Management radios disabled after deployment

### Management & Access
- Admin Interface: HTTP Web UI
- Browser Compatibility: Safari recommended (Chrome unreliable)
- SSH: Available (legacy algorithm flags may be required)

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

### Management Networking (Final, Stable)
- IP Mode: **Static**
- Management IP: **192.168.1.20 /24**
- Netmask: 255.255.255.0
- Gateway: **Not set (intentionally empty)**
- DNS: Not set

> Rationale: Infrastructure device. Does not initiate off‑subnet traffic.
> Configuration is independent of any specific router (e.g., Beryl).

### Operational Notes
- Configured via Ethernet using Safari
- Management radio disabled
- Permanently mounted at house, aimed toward RV

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

### Management Networking (Final, Stable)
- IP Mode: **Static**
- Management IP: **192.168.1.21 /24**
- Netmask: 255.255.255.0
- Gateway: **Not set (intentionally empty)**
- DNS: Not set

> Rationale identical to AP‑side device.

### Operational Notes
- Bench‑configured prior to outdoor mounting
- Verified reachable via static IP regardless of DHCP/router changes
- Mounted near RV, aimed toward house

---

## 4. Alignment & Deployment Assumptions

- Temporary mounts used for alignment
- Low transmit power during alignment to avoid masking mis‑aim
- Fine alignment performed using:
  - Signal strength
  - Noise floor
  - CINR / Link Potential metrics
- Permanent mounting only after stable link confirmed

---

## 5. Operations Model (Important)

- PtP radios are treated as **infrastructure**, not clients
- Management access is via **static IPs**, not DHCP, DNS, or discovery
- Device reachability does **not** depend on:
  - Beryl
  - DHCP server behavior
  - DNS availability
- Management access is preserved via **1Password entries** pointing to static IPs

This avoids outage‑mode forensics when checking link status.

---

## 6. Change Control

Any change to the following **must be applied symmetrically** and documented:

- SSID
- WPA2 key
- Channel width
- Frequency
- Regulatory domain
- Management IP addresses

This document and the corresponding 1Password entries are the **source of truth**.

---

## 7. One-Minute Health Check (When You Just Want to Know “Is It Fine?”)

Use this when something feels slow, weird, or you just want reassurance.
Do **not** tune. Do **not** optimize. Observe, then stop.

### Step 1: Open the radios
From 1Password:
- `loco-ap` → http://192.168.1.20
- `loco-station` → http://192.168.1.21

Log in to the airOS UI on **either** device.

---

### Step 2: Check these fields only (Main / Status page)

Look at the **Wireless** section.

- **Link State:** Connected
- **Link Potential:** ≥ 95%
- **CINR / SNR:** Stable and comfortably positive (no rapid swings)
- **Tx/Rx Rate:** Reasonable and not flapping wildly

You do **not** need exact numbers. Stability matters more than peaks.

---

### Step 3: Decide and stop

- If Link Potential is high and stable → **The PtP link is healthy**
- If CINR is stable → **Alignment and interference are fine**
- If rates are steady → **Throughput issues are elsewhere**

Close the tab.

---

### Explicit Stop Conditions (Important)

Do **not**:
- re-aim antennas
- change channel width
- change frequency
- adjust transmit power

Unless:
- Link Potential drops persistently below ~90%, **or**
- The link actually drops.

---

### Mental Model (Write This Down)

> **PtP health is about stability, not perfection.**

If it’s boring, it’s working.

---

