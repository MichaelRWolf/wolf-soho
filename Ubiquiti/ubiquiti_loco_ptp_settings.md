# Ubiquiti Loco5AC PtP Settings Checklist

Settings reference for the Wolfden point-to-point wireless bridge.
Each section corresponds to a 1Password entry.

> **Status:** Configuration complete. PtP is production-ready and set-and-forget.

---

## Wolfden – Ubiquiti Loco5AC – AP PtP

### Common to Loco5AC

- Model: Ubiquiti NanoStation Loco5AC
- SSID: `Running Wolf PtP`
- Security: WPA2 Personal (PSK), AES
- Band: 5 GHz
- Channel Width: 40 MHz
- Frequency: Fixed (match both sides)
- PtP Mode: Enabled
- airMAX: Enabled
- Bridging: Layer-2 transparent
- Regulatory Domain: US
- Power: 24V passive PoE (POE-24-12W)

### Unique to AP

- Hostname: loco-ap
- MAC: 1C:6A:1B:CA:EF:9B
- Role: Access Point (AP ON, PtP ON)
- IP: 192.168.1.20 /24 (static, no gateway, no DNS)

---

## Wolfden – Ubiquiti Loco5AC – Station PtP

### Common to Loco5AC

- Model: Ubiquiti NanoStation Loco5AC
- SSID: `Running Wolf PtP`
- Security: WPA2 Personal (PSK), AES
- Band: 5 GHz
- Channel Width: 40 MHz
- Frequency: Fixed (match both sides)
- PtP Mode: Enabled
- airMAX: Enabled
- Bridging: Layer-2 transparent
- Regulatory Domain: US
- Power: 24V passive PoE (POE-24-12W)

### Unique to Station

- Hostname: loco-station
- MAC: 1C:6A:1B:C6:E5:A3
- Role: Station (AP OFF, PtP ON)
- IP: 192.168.1.21 /24 (static, no gateway, no DNS)
- Lock to AP MAC: 1C:6A:1B:CA:EF:9B

---

## Wolfden – Running Wolf PtP – WPA2 Link Key

- Authentication: WPA2 Personal (PSK)
- Encryption: AES
- Passphrase: (stored in 1Password)
