# Ubiquiti Device Operating Modes

## Overview
The Ubiquiti UAP-AC-M-US device has two primary operating modes, but neither allows it to replace how the Beryl router currently attaches to the Trails End mesh network.

## Mode 1: Mesh Peer Mode (Default)
**Technical Term**: UniFi Mesh Access Point
**Analogy**: "Spray" mode - device becomes part of the mesh and broadcasts signal

### How It Works:
- Device joins existing UniFi mesh network as a peer
- Becomes part of the mesh infrastructure
- Broadcasts mesh SSID to other devices
- Requires UniFi controller access for adoption

### Why It Won't Replace Beryl:
- **Requires admin access** to Trails End mesh controller
- **Cannot be adopted** without mesh administrator privileges
- **Becomes mesh infrastructure** rather than client device
- **No standalone operation** - must be part of mesh

## Mode 2: Standalone Access Point Mode
**Technical Term**: Independent Access Point
**Analogy**: "Suck" mode - device connects to external networks as client

### How It Works:
- Device operates independently of mesh networks
- Can connect to external WiFi networks as client
- Bridges external connection to local network
- No controller access required

### Why It Won't Replace Beryl:
- **Still requires external network** to connect to
- **Cannot join mesh** without admin access
- **Same limitation** as Beryl - needs external WiFi source
- **No mesh integration** - operates as separate network

## The Core Problem

### Current Beryl Setup:
```
Trails End WiFi → Beryl (client mode) → Running Wolf Router
```

### Ubiquiti Options:
```
Option 1: Trails End Mesh → Ubiquiti (mesh peer) → [Requires admin access]
Option 2: Trails End WiFi → Ubiquiti (client mode) → Running Wolf Router
```

### Why Neither Works:
1. **Mesh Peer Mode**: Requires Trails End admin to adopt device
2. **Standalone Mode**: Same limitation as Beryl - needs external WiFi source
3. **No Direct Mesh Access**: Cannot "attach to" mesh without being "adopted by" mesh

## Conclusion
The Ubiquiti device cannot replace the Beryl's current mesh attachment method because:
- **Mesh mode** requires admin privileges we don't have
- **Standalone mode** has the same limitations as current Beryl setup
- **No hybrid mode** exists that allows mesh attachment without admin access

The device is either "spraying" (broadcasting as mesh peer) or "sucking" (connecting as client), but neither mode allows it to replace the Beryl's current role without Trails End mesh administrator intervention. 