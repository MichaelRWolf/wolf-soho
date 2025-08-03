# Bridging Wolf and Trails End Networks

## Repeater Setup
- `wolfden-router` connects to campground SSID (e.g. `Trails End Crew`)
- Uses client mode to join external network
- Simultaneously broadcasts internal SSID: `Running Wolf Router`

## Power and Wiring
- Discussion of PoE injector inside RV powering UniFi mesh device outside
- Desire to minimize cabling: one Cat5 cable for both power and data

## DNS / Certificate / Trust Considerations
- Self-signed certificate from NAS manually installed and trusted
- Chrome behavior adjusted using `--ignore-certificate-errors` if needed
- Importance of flushing DNS or certificate trust cache occasionally

## Other Integration Notes
- Time Machine backups run over SMB from MacBooks to Synology NAS
- NAS has static IP for consistency even when upstream changes
- SSH and web interfaces are used for debugging and configuration
