# HOWTO_rascally_raccoon_PtP_config.md

## Purpose

Bench configuration of Ubiquiti airMAX PtP link (NanoStation Loco 5AC) for the **Rascally Raccoon** winter site. This document covers *logical* setup only. No ladders.

---

## Hardware in Scope

* 2× NanoStation Loco 5AC (AP + Station)
* 24V passive PoE injectors (POE-24-12W)
* MacBook (Safari preferred for UI access)

---

## Safety / Guardrails

* Do **not** change your primary network location
* Use a temporary macOS Location (e.g. `Ubiquiti-Setup`)
* Configure **one radio at a time**

---

## macOS Setup (Temporary Location)

1. System Settings → Network → Location → **Add Location**
2. Name: `Ubiquiti-Setup`
3. Enable only **Belkin USB‑C LAN / Thunderbolt Ethernet**
4. IPv4: **Configure Automatically (DHCP)**
5. Wi‑Fi: Off

---

## Wiring (Bench)

```text
MacBook → USB‑C Ethernet → PoE LAN (⚡) → PoE PoE (⇄) → Loco
```

* Use the **LAN/⚡** port for the Mac
* Use the **PoE/⇄** port for the radio

---

## Accessing the UI

* Browser: **Safari** (Chrome may block HTTP)
* URL: `http://192.168.1.20` (fallback) or device-assigned IP

---

## Common Settings (Both Radios)

* Firmware: current / matching
* Country: United States
* Management IP: **DHCP**
* DHCP fallback: `192.168.1.20/24`
* airMAX: **Enabled**
* Management radio: Enabled (temporarily)

---

## House-Side Radio (AP / PTP Master)

* Mode: **PTP**
* Role: **Access Point**
* SSID: `Running Wolf PtP`
* Security: **WPA2-Personal**
* Channel width: 40 or 80 MHz
* Frequency: Manual (avoid DFS initially)

---

## RV-Side Radio (Station)

* Mode: **PTP**
* Role: **Station**
* SSID: `Running Wolf PtP`
* Security: WPA2-Personal
* Lock to AP MAC (recommended)

---

## Credentials & 1Password

Create **separate 1Password items**:

1. `RascallyRaccoon – PtP – House (Loco5AC)`
2. `RascallyRaccoon – PtP – RV (Loco5AC)`
3. `RascallyRaccoon – PtP – WPA2 Key` (password-only item)

Link item #3 from #1 and #2.

---

## Validation (Bench)

* Both radios reachable
* Station sees AP
* airMAX Quality > 50%
* Peer MAC matches expected

---

## Before Moving On

* Restore macOS Location to **Automatic**
* Power down radios
* Label radios physically (House / RV)

---

END
