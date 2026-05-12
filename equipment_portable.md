# Portable Equipment -- Briefcase & Backpack

## USB-C Ethernet Adapters

### `anker-dongle` -- Anker USB-C to Gigabit Ethernet

- Chip: Realtek RTL8153 (VID 0x0bda / PID 0x8153)
- Firmware version: 30.00
- USB speed: USB 3.1 Gen 1 (5 Gb/s)
- Ethernet: 1 Gbps
- Serial: 000001
- MAC: 00:e0:4c:00:00:93
- Power draw: 288 mA
- Interface: en7 on michael-pro
- Note: USB-C plug and RJ45 plug both have worn latches; cable and dongle taped together

### `belkin-dongle` -- Belkin USB-C to Gigabit Ethernet

- Chip: Realtek RTL8153 (VID 0x0bda / PID 0x8153)
- Firmware version: 31.00
- USB speed: USB 3.1 Gen 1 (5 Gb/s)
- Ethernet: 1 Gbps
- Serial: 0013000001
- MAC: 80:69:1a:8d:ea:8a
- Power draw: 112 mA
- Interface: en13 on michael-pro (when connected)
- macOS: built-in Realtek driver; no system extension needed
- Setup: Network → Add Service on first use per machine

## WiFi Extender

### `cheapo-extender` -- Generic USB WiFi Repeater

- Model: Amazon B0DCBYCHR7
- Purchased: 2025-08-10 for $18
- IP: 192.168.11.1 (management)
- Role: Portable campground WiFi signal extension
- Docs: [cheapo_extender.md](cheapo_extender.md)

## Ethernet Cables

| Name                 | Description                        | Verified good |
|----------------------|------------------------------------|---------------|
| `cable-black-10ft`   | Black Cat6, 10 ft, indoor RV       | Yes           |
| `cable-green-3ft-a`  | Green Cat6, 3 ft, indoor RV        | Yes           |
| `cable-green-3ft-b`  | Green Cat6, 3 ft, indoor RV        | Yes           |
| `cable-outdoor-50ft` | Cat6, 50 ft, exterior run, RV side | Yes           |

Verified by: michael-pro → anker-dongle → [cable] → running-wolf-hotspot → internet (ping 1.1.1.1)
