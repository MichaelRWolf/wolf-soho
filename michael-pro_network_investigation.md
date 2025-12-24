# Michael-Pro Network Quality Investigation

## Problem Statement

michael-pro consistently shows worse network quality (especially responsiveness) than wolf-air, even though:

- michael-pro is on Ethernet
- wolf-air is on WiFi
- Responsiveness is poor on michael-pro on both WiFi AND Ethernet (ruling out cable/Ethernet-specific issues)

## Current Test Results

### michael-pro (local, Ethernet)

- Uplink capacity: 9.795 Mbps
- Downlink capacity: 2.477 Mbps
- Responsiveness: Low (3.720 seconds | 16 RPM)
- Idle Latency: 48.277 milliseconds | 1242 RPM

### wolf-air (via SSH, WiFi)

- Upload capacity: 4.069 Mbps
- Download capacity: 5.247 Mbps
- Upload flows: 4
- Download flows: 20
- Responsiveness: Medium (748 RPM)

## Investigation Plan

### Network Infrastructure & Path

- [ ] Compare physical network path each device takes to the internet
- [ ] Check switch port configuration (speed, duplex, VLAN, QoS settings)
- [ ] Check router/switch port health (errors, drops, rate limiting)

### System Configuration

- [ ] Check network interface settings (MTU, offloading, flow control)
- [ ] Compare macOS network settings (service order, DNS, proxy settings)
- [ ] Check system load (CPU/memory usage, background network activity during tests)
- [ ] Compare macOS versions between systems

### Network Stack & Performance

- [ ] Check for background traffic (active connections consuming bandwidth during tests)
- [ ] Compare packet loss, latency, and jitter on both systems
- [ ] Check for firewall/security software interference

### Comparative Testing

- [ ] Run tests simultaneously to check for shared bottlenecks
- [ ] Test michael-pro on WiFi (to confirm it's also bad, isolating Ethernet vs WiFi)
- [ ] Compare results with other test tools (iperf3, speedtest-cli, etc.)

## Notes

- Cable/Ethernet-specific issues ruled out (WiFi also shows poor responsiveness)
- Focus should be on system-level configuration and network stack differences

## Working Notes

### Workflow

Work through issues one at a time. For each investigation step:

1. **What**: What we tried/tested/checked
2. **So what**: What does that indicate or tell us
3. **Now what**: Suggested next step based on findings

Each entry should include:

- Timestamp in ISO8601 format (YYYY-MM-DDTHH:MM:SS±TZ)
- Machine name (michael-pro, wolf-air, or both)
- What/So what/Now what structure

---
