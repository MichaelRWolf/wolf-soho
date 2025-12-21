# Ubiquiti Loco5AC PtP Operations Guide

Operational procedures, health checks, and policies for the Wolfden PtP link.
For settings values, see `ubiquiti_loco_ptp_checklist.md`.

---

## Management Access

- Admin Interface: HTTP Web UI
- Browser: Safari recommended (Chrome unreliable)
- SSH: Available (legacy algorithm flags may be required)
- AP URL: http://192.168.1.20
- Station URL: http://192.168.1.21

---

## Operations Model

- PtP radios are treated as **infrastructure**, not clients
- Management access is via **static IPs**, not DHCP, DNS, or discovery
- Device reachability does **not** depend on:
  - Beryl
  - DHCP server behavior
  - DNS availability
- Management access is preserved via **1Password entries** pointing to static IPs

This avoids outage-mode forensics when checking link status.

---

## Alignment & Deployment

- Temporary mounts used for alignment
- Low transmit power during alignment to avoid masking mis-aim
- Fine alignment performed using:
  - Signal strength
  - Noise floor
  - CINR / Link Potential metrics
- Permanent mounting only after stable link confirmed

---

## Change Control

Any change to the following **must be applied symmetrically** and documented:

- SSID
- WPA2 key
- Channel width
- Frequency
- Regulatory domain
- Management IP addresses

The checklist and corresponding 1Password entries are the **source of truth**.

---

## One-Minute Health Check

Use this when something feels slow, weird, or you just want reassurance.
Do **not** tune. Do **not** optimize. Observe, then stop.

### Step 1: Open the radios

From 1Password:

- `loco-ap` → http://192.168.1.20
- `loco-station` → http://192.168.1.21

Log in to the airOS UI on **either** device.

### Step 2: Check these fields only (Main / Status page)

Look at the **Wireless** section.

- **Link State:** Connected
- **Link Potential:** ≥ 95%
- **CINR / SNR:** Stable and comfortably positive (no rapid swings)
- **Tx/Rx Rate:** Reasonable and not flapping wildly

You do **not** need exact numbers. Stability matters more than peaks.

### Step 3: Decide and stop

- If Link Potential is high and stable → **The PtP link is healthy**
- If CINR is stable → **Alignment and interference are fine**
- If rates are steady → **Throughput issues are elsewhere**

Close the tab.

---

## Explicit Stop Conditions

Do **not**:

- re-aim antennas
- change channel width
- change frequency
- adjust transmit power

Unless:

- Link Potential drops persistently below ~90%, **or**
- The link actually drops.

---

## Mental Model

> **PtP health is about stability, not perfection.**

If it's boring, it's working.
