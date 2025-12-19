# Ubiquiti UniFi AC Mesh Management

## Overview

This directory contains management documentation for the Ubiquiti UAP-AC-M-US device (`wolfden-mesh`).

## Device Status

- **Model**: UAP-AC-M-US
- **Status**: New device, integration pending
- **Target Use**: WiFi client bridge for Trails End campground networks

## Management Files

### [Device Information](device_info.md)

- Device specifications and hardware features
- Operating modes and power requirements
- Network integration overview

### [Configuration Guide](configuration_guide.md)

- Step-by-step setup process
- Web interface and SSH configuration
- Troubleshooting procedures
- Reset and recovery options

### [Network Integration](network_integration.md)

- Integration with existing RV network
- Performance optimization
- Monitoring and maintenance
- Troubleshooting integration issues

### [Setup Guide](ubiquiti_setup.md)

- Comprehensive setup documentation
- Operating modes explanation
- Hardware requirements
- Integration options

## Quick Start

1. Review [Device Information](device_info.md) for specifications
2. Follow [Configuration Guide](configuration_guide.md) for initial setup
3. Use [Network Integration](network_integration.md) for RV network integration
4. Reference [Setup Guide](ubiquiti_setup.md) for detailed procedures

## Key Configuration Points

- **Mode**: Standalone Access Point (not mesh)
- **WiFi Client**: Connect to Trails End networks
- **Network Bridge**: Bridge to RV network (192.168.8.x)
- **IP Address**: 192.168.8.130 (static)
- **Power**: PoE injector required

## Integration Goals

- Better signal reception than current `wolfden-router`
- Outdoor mounting capability
- Seamless integration with existing RV network
- No dependency on Trails End mesh admin access
