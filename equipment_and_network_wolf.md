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
- **NAS**: Synology DS220j
  - Used for Time Machine backups
  - Accessible by fixed local IP
  - Backup share: `Backups`
  - Serves SMB shares, uses `synology-cert`

## Computing Devices
- `michael-pro` (MacBook Pro)
- `wendy-pro` (MacBook Pro)
- `wolf-pro` (MacBook, newer)
- `wolf-air` (MacBook Air)

## Services
- Time Machine backups (quotas discussed)
- NAS uses HTTPS on port 5001
- Self-signed certificates installed and trusted
