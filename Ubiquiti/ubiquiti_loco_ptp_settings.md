# Ubiquiti Loco5AC PtP Settings Checklist

Settings reference for the Wolfden point-to-point wireless bridge.
Each section corresponds to a 1Password entry.

Related transition/performance docs (for bufferbloat / `networkQuality` Responsiveness investigation):

- `Ubiquiti/transition_lte_to_isp_over_ptp_qualitative.md`
- `Ubiquiti/transition_lte_to_isp_over_ptp_quantitative.md`

> **Status:** Configuration complete. PtP is production-ready and set-and-forget.

---

## Wolfden – Ubiquiti Loco5AC – AP PtP

### Common to Loco5AC (Station)

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

---

## Rascally Raccoon – Spectrum Router (Moe's)

Upstream internet source for the PtP link. Contact Moe for admin access.

- Model: SAC2V1A (Spectrum Advanced WiFi)
- Serial Number: A5L4H956C14029
- MAC: A8:97:CD:70:61:D0
- FW Version: 7.0.1-1-795640-g202508082008-SAC2V1A-prod
- Location: House side of PtP link
- Admin: Moe (credentials in 1Password if shared)
