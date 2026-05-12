# Wolf Network Equipment (Mobile/RV-Based)

## Network Infrastructure

- **Router**: `wolfden-router` (GL.iNet Beryl GL-MT1300)
  - Functions: Primary router in RV
  - Broadcasts: `Running Wolf Router`
  - Operates in repeater mode at campgrounds
- **Hotspot**: `wolfden-hotspot` (Netgear Nighthawk M1)
  - Used for mobile internet
  - USB tethering and Wi-Fi supported
  - Known to overheat, sometimes placed on an ice pack
- **Mesh AP**: `wolfden-mesh` (Ubiquiti UAP-AC-M-US)
  - Model: UAP-AC-M-US
  - Manufacturer: Ubiquiti (unifi.ui.com)
  - Purchased: 2025-07 from Amazon
  - Status: New device, integration pending
- **NAS**: Synology DS220j
  - Used for Time Machine backups
  - Accessible by fixed local IP
  - Backup share: `Backups`
  - Serves SMB shares, uses `synology-cert`
  - Certificate generation: `create_synology_cert` script
  - **Management**: [Synology Management Notes](Synology/synology_mananagement.md)
- **WiFi Extender**: Cheapo USB WiFi Repeater
  - Model: Generic USB WiFi repeater (Amazon B0DCBYCHR7)
  - Purchased: 2025-08-10 for $18
  - Functions: Portable WiFi signal extension, campground connectivity backup
  - **Documentation**: [Cheapo Extender Setup Guide](cheapo_extender.md)

## Computing Devices

- `michael-pro` (MacBook Pro)
  - **Battery Replacement**: [Battery Replacement Project](michael-pro_battery.md)
- `wendy-pro` (MacBook Pro)
- `wolf-pro` (MacBook, newer)
- `wolf-air` (MacBook Air)

## Briefcase & Backpack

Portable accessories that travel for field use (cable testing, direct Ethernet, diagnostics).

- **`anker-dongle`**: Anker USB-C to Gigabit Ethernet adapter
  - Used with `michael-pro` for direct Ethernet connections
  - Chip: unknown; used to verify cables at Rascally Raccoon 2026-05

- **`belkin-dongle`**: Belkin USB-C to Gigabit Ethernet adapter
  - Chip: Realtek RTL8153 (VID 0x0bda / PID 0x8153)
  - USB speed: USB 3.1 Gen 1 (5 Gb/s); Ethernet: 1 Gbps
  - Serial: 0013000001; MAC: 80:69:1a:8d:ea:8a (en13 on michael-pro)
  - Works on `michael-pro` and `wendy-pro`; macOS built-in driver (no system extension needed)
  - Setup on michael-pro: Network → Add Service → selected "Belkin USB-C LAN"; renamed via
    `networksetup -renamenetworkservice "Belkin USB-C LAN 2" "Belkin USB-C LAN"`

## Services

- Time Machine backups (quotas discussed)
- NAS uses HTTPS on port 5001
- Self-signed certificates installed and trusted
