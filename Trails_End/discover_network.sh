#!/usr/bin/env bash
# Minimal network topology discovery
# Usage: ./discover_network.sh

echo "=== Current Interface ==="
ifconfig | grep -A 5 "en0\|en1"

echo ""
echo "=== Routing (Internet Path) ==="
netstat -rn | grep default

echo ""
echo "=== Known Devices (ARP Table) ==="
arp -a | grep -E "192.168|10\."

echo ""
echo "=== Device Connectivity Check ==="
echo "Beryl (192.168.8.1):"
ping -c 1 -W 1 192.168.8.1 >/dev/null && echo "  ✓ UP (ping)" || echo "  ✗ DOWN"

echo "NAS (192.168.8.129):"
timeout 1 bash -c 'echo > /dev/tcp/192.168.8.129/445' 2>/dev/null && echo "  ✓ UP (SMB)" || echo "  ✗ DOWN"

echo "EAP (192.168.8.130):"
timeout 1 bash -c 'echo > /dev/tcp/192.168.8.130/80' 2>/dev/null && echo "  ✓ UP (HTTP)" || echo "  ✗ DOWN"

echo "Trails End Mesh (192.168.1.1):"
ping -c 1 -W 1 192.168.1.1 >/dev/null && echo "  ✓ UP (ping)" || echo "  ✗ DOWN"

echo ""
echo "=== Current WiFi Network ==="
/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I | grep -E "SSID|RSSI|state"
