# Synology Management Notes

## Certificate Steps
1. Generated self-signed cert (`synology-cert`)
2. Uploaded `.crt` and `.key` to DSM
3. Imported into macOS Keychain and trusted
4. Used Chrome with `--ignore-certificate-errors` to test
5. Verified ports using `nc`

## Cert Generation Script
```bash
openssl req -x509 -nodes -days 825 -newkey rsa:2048 \
  -keyout synology-cert.key -out synology-cert.crt \
  -subj "/CN=wolf-nas.local"
```

## Chrome Bypass
```bash
open -na "Google Chrome" --args --ignore-certificate-errors --user-data-dir=/tmp/chrome-test
```

## Notes
- DSM assigns certs to services
- HTTPS port 5001 used for backups

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
