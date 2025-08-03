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

## Computing Devices
- `michael-pro` (MacBook Pro)
- `wendy-pro` (MacBook Pro)
- `wolf-pro` (MacBook, newer)
- `wolf-air` (MacBook Air)

## Services
- Time Machine backups (quotas discussed)
- NAS uses HTTPS on port 5001
- Self-signed certificates installed and trusted

## How-To

### Synology Certificate Management

#### Creating Self-Signed Certificates
Use the `create_synology_cert` script to generate certificates for the NAS:

```bash
./create_synology_cert
```

**What the script does:**
- Creates certificates in `~/Desktop/synology-cert/`
- Generates certificates valid for 10 years (3650 days)
- Includes multiple DNS names and IP addresses:
  - `wolfssynology.synology.me`
  - `wolfsynology.direct.quickconnect.to`
  - `wolfden-nas` (local hostname)
  - `192.168.8.129` (NAS static IP)

**Output files:**
- `synology.crt` - Certificate file
- `synology.key` - Private key file

#### Installing Certificates
1. **On Synology NAS:**
   - Go to Control Panel → Security → Certificate
   - Import the generated certificate and key
   - Set as default certificate for DSM

2. **On Mac devices:**
   - Double-click the `.crt` file to open in Keychain Access
   - Add to System keychain
   - Set trust to "Always Trust" for SSL

#### Troubleshooting Certificate Issues
- **Chrome certificate errors**: Use `--ignore-certificate-errors` flag
- **DNS cache issues**: Flush DNS cache occasionally
- **Trust issues**: Reinstall certificate and set trust level in Keychain Access
