# HOWTO_rascally_raccoon_PtP_config.md

## Purpose

Bench configuration of Ubiquiti airMAX PtP link (NanoStation Loco 5AC) for the **Rascally Raccoon** winter site. This document covers *logical* setup only. No ladders.

---

## Hardware in Scope

* 2× NanoStation Loco 5AC (AP + Station)
* 24V passive PoE injectors (POE-24-12W)
* MacBook with USB-C Ethernet adapter

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

## Accessing the Device

* **SSH**: `ssh admin@192.168.1.20` (preferred)
* **Web UI**: `http://192.168.1.20` (Safari only; Chrome blocks HTTP)

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

* MAC Address: **1C:6A:1B:CA:EF:9B**
* Mode: **PTP**
* Role: **Access Point**
* SSID: `Running Wolf PtP`
* Security: **WPA2-Personal**
* Channel width: 40 or 80 MHz
* Frequency: Manual (avoid DFS initially)
* Power: 24V passive PoE (POE-24-12W injector)

---

## RV-Side Radio (Station)

* MAC Address: **1C:6A:1B:C6:E5:A3**
* Mode: **PTP**
* Role: **Station**
* SSID: `Running Wolf PtP`
* Security: WPA2-Personal (AES)
* Lock to AP MAC (recommended)
* Power: 24V passive PoE (POE-24-12W injector)

---

## Using ssh(1)

SSH access requires legacy algorithm support on modern macOS.

### SSH Command

```bash
ssh -o KexAlgorithms=+diffie-hellman-group1-sha1 \
    -o HostKeyAlgorithms=+ssh-rsa \
    -o Ciphers=+aes128-cbc \
    admin@192.168.1.20
```

### SSH Config (recommended)

Add to `~/.ssh/config`:

```ssh-config
Host loco
    HostName 192.168.1.20
    User admin
    HostKeyAlgorithms +ssh-rsa
    KexAlgorithms +diffie-hellman-group1-sha1
    Ciphers +aes128-cbc
```

Then connect with: `ssh loco`

### Useful Commands

```bash
# Show device status
cat /etc/board.info

# Show wireless config
cat /tmp/system.cfg | grep wireless

# Show network config
cat /tmp/system.cfg | grep netconf

# Backup config
cat /tmp/system.cfg > backup.cfg

# Apply changes after editing
cfgmtd -w -p /etc/

# Reboot device
reboot
```

---

## 1Password Notes

Three 1Password entries:

1. **Wolfden – Ubiquiti Loco5AC – House PtP (AP)**
2. **Wolfden – Ubiquiti Loco5AC – RV PtP (Station)**
3. **Wolfden – Ubiquiti Running Wolf PtP – WPA2 Link Key** (linked from #1 and #2)

### Wolfden – Ubiquiti Loco5AC – House PtP (AP)

```text
Role: Point-to-Point bridge – Access Point (AP)
Location: House
Physical Mount: TBD (house-facing RV direction)
Power: 24V passive PoE (POE-24-12W injector)

MAC Address: 1C:6A:1B:CA:EF:9B
Management IP: 192.168.1.20 (DHCP fallback)

Firmware: airMAX (factory)
Band: 5 GHz
Mode: airMAX AP
SSID: Running Wolf PtP
Security: WPA2-Personal (AES)
Peer: RV-side Loco5AC (Station)

Access:
  SSH: ssh -o KexAlgorithms=+diffie-hellman-group1-sha1 -o HostKeyAlgorithms=+ssh-rsa -o Ciphers=+aes128-cbc admin@192.168.1.20
  Web UI: http://192.168.1.20 (Safari only)
```

### Wolfden – Ubiquiti Loco5AC – RV PtP (Station)

```text
Role: Point-to-Point bridge – Station
Location: RV
Physical Mount: TBD (RV-facing house direction)
Power: 24V passive PoE (POE-24-12W injector)

MAC Address: 1C:6A:1B:C6:E5:A3
Management IP: 192.168.1.20 (DHCP fallback)

Firmware: airMAX (factory)
Band: 5 GHz
Mode: airMAX Station
SSID: Running Wolf PtP
Security: WPA2-Personal (AES)
Peer: House-side Loco5AC (AP)

Access:
  SSH: ssh -o KexAlgorithms=+diffie-hellman-group1-sha1 -o HostKeyAlgorithms=+ssh-rsa -o Ciphers=+aes128-cbc admin@192.168.1.20
  Web UI: http://192.168.1.20 (Safari only)
```

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
