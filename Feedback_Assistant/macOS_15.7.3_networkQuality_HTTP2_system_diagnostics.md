# System Diagnostics

## networkQuality HTTP/2 Performance Bug

## macOS 15.7.3 (Sequoia)

**Back to**: [Main Bug Report](./macOS_15.7.3_networkQuality_HTTP2_bug_report_Feedback_Assistant.md)

---

## System Information

### macOS Version

```text
ProductName:  macOS
ProductVersion:  15.7.3
BuildVersion:  24G419
```

### Kernel Information

```text
Kernel Version: Darwin 24.6.0
Boot Volume: Macintosh HD
Boot Mode: Normal
Secure Virtual Memory: Enabled
System Integrity Protection: Enabled
Time since boot: 2 days, 6 hours, 39 minutes
```

### Hardware Information

```text
Model Name: MacBook Pro
Model Identifier: MacBookPro16,2
Processor Name: Quad-Core Intel Core i5
Processor Speed: 2 GHz
Number of Processors: 1
Total Number of Cores: 4
L2 Cache (per Core): 512 KB
L3 Cache: 6 MB
Hyper-Threading Technology: Enabled
Memory: 16 GB
System Firmware Version: 2094.40.1.0.0 (iBridge: 23.16.12048.0.0,0)
OS Loader Version: 583~2317
```

### User Information

```text
Computer Name: michael-pro
User Name: Michael R. Wolf (michael)
```

---

## Network Configuration

### Active Network Interface

- **Interface**: en0 (WiFi)
- **Test Endpoint (HTTP/2)**: usmia1-edge-fx-032.aaplimg.com
- **Test Endpoint (HTTP/1.1)**: usmia1-edge-fx-002.aaplimg.com

### Network Tools Versions

**curl**:

```text
curl 8.7.1 (x86_64-apple-darwin24.0)
libcurl/8.7.1 (SecureTransport)
LibreSSL/3.3.6
zlib/1.2.12
nghttp2/1.64.0
Release-Date: 2024-03-27
Protocols: dict file ftp ftps gopher gophers http https imap imaps ipfs ipns ldap ldaps mqtt pop3 pop3s rtsp smb smbs smtp smtps telnet tftp
Features: alt-svc AsynchDNS GSS-API HSTS HTTP2 HTTPS-proxy IPv6 Kerberos Largefile libz MultiSSL NTLM SPNEGO SSL threadsafe UnixSockets
```

**networkQuality**:

- Location: `/usr/bin/networkQuality`
- Type: Mach-O universal binary (x86_64, arm64e)
- Framework: NetworkQualityServices.framework (private)

---

## Security Software

### Firewall Status

**LuLu Firewall**: Active

- Main process: Running (PID 91810)
- System extension: Active (PID 327)
- Location: `/Applications/LuLu.app`
- System extension: `/Library/SystemExtensions/ECEF2EFD-04A4-42F7-96C7-32EA2512EC4B/`

**Note**: Issue persists even when LuLu firewall is disabled, so LuLu is not the root cause.

---

## Test Results

### HTTP/2 Test Results (Broken)

**Command**: `networkQuality -f h2 -v`

**Output**:

```text
==== Verbose Results ====
---
Capacity:
---
   Uplink capacity: 12.578 Mbps
      Accuracy: Medium
      Uplink bytes transferred: 32.500 MB
      Uplink Flow count: 16
   Downlink capacity: 2.325 Mbps
      Accuracy: High
      Downlink bytes transferred: 11.647 MB
      Downlink Flow count: 16
---
Latency:
---
   Idle Latency:
      1319 RPM (45.469 milliseconds)
         Transport: 2840 RPM (21.125 milliseconds)
         Security: 649 RPM (92.375 milliseconds)
         HTTP: 2619 RPM (22.906 milliseconds)
      Accuracy: High
   Responsiveness: Low
      13 RPM (4.457 seconds)
         Transport: 1068 RPM (56.167 milliseconds)
         Security: 149 RPM (402.292 milliseconds)
         HTTP: 710 RPM (84.458 milliseconds)
         HTTP loaded: 4 RPM (12.241 seconds)
      Accuracy: Low
---
Protocols Used:
---
    HTTP/2: 100%
---
Transport-layer info:
---
    ECN Disabled: 100%, L4S Disabled: 100%
---
Other Info:
---
   Test Endpoint: usmia1-edge-fx-032.aaplimg.com
   Interface: en0
   Start: 2025-12-24 14:52:27.614
   End: 2025-12-24 14:53:15.420
   OS Version: Version 15.7.3 (Build 24G419)

==== SUMMARY ====
Uplink capacity: 12.578 Mbps
Downlink capacity: 2.325 Mbps
Responsiveness: Low (4.457 seconds | 13 RPM)
Idle Latency: 45.469 milliseconds | 1319 RPM
```

**Key Metrics**:

- Responsiveness: **13 RPM (Low)** - extremely poor
- HTTP loaded: **4 RPM (12.241 seconds)** - primary bottleneck
- Test duration: ~48 seconds
- Accuracy: Low (due to poor performance)

### HTTP/1.1 Test Results (Working)

**Command**: `networkQuality -f h1 -v`

**Output**:

```text
==== Verbose Results ====
---
Capacity:
---
   Uplink capacity: 13.022 Mbps
      Accuracy: Medium
      Uplink bytes transferred: 38.000 MB
      Uplink Flow count: 16
   Downlink capacity: 2.060 Mbps
      Accuracy: High
      Downlink bytes transferred: 8.609 MB
      Downlink Flow count: 16
---
Latency:
---
   Idle Latency:
      1036 RPM (57.883 milliseconds)
         Transport: 2696 RPM (22.250 milliseconds)
         Security: 511 RPM (117.250 milliseconds)
         HTTP: 1757 RPM (34.149 milliseconds)
      Accuracy: High
   Responsiveness: Medium
      472 RPM (127.084 milliseconds)
         Transport: 85 RPM (699.634 milliseconds)
         Security: 106 RPM (564.561 milliseconds)
         HTTP: 335 RPM (178.829 milliseconds)
      Accuracy: Low
---
Protocols Used:
---
    HTTP/1.1: 100%
---
Transport-layer info:
---
    ECN Disabled: 100%, L4S Disabled: 100%
---
Other Info:
---
   Test Endpoint: usmia1-edge-fx-002.aaplimg.com
   Interface: en0
   Start: 2025-12-24 14:52:30.012
   End: 2025-12-24 14:53:15.351
   OS Version: Version 15.7.3 (Build 24G419)

==== SUMMARY ====
Uplink capacity: 13.022 Mbps
Downlink capacity: 2.060 Mbps
Responsiveness: Medium (127.084 milliseconds | 472 RPM)
Idle Latency: 57.883 milliseconds | 1036 RPM
```

**Key Metrics**:

- Responsiveness: **472 RPM (Medium)** - normal performance
- HTTP loaded: **N/A** - component doesn't exist
- Test duration: ~45 seconds
- Accuracy: High for most components

### Comparison Summary

| Component | HTTP/2 | HTTP/1.1 | Ratio |
| --- | --- | --- | --- |
| **Responsiveness** | 13 RPM | 472 RPM | **36x worse** |
| **HTTP loaded** | 12.241s | N/A | **N/A** |
| **Idle Latency** | 1319 RPM | 1036 RPM | 1.27x better |
| **Transport (Idle)** | 2840 RPM | 2696 RPM | 1.05x better |
| **Security (Idle)** | 649 RPM | 511 RPM | 1.27x better |
| **HTTP (Idle)** | 2619 RPM | 1757 RPM | 1.49x better |

**Critical Finding**: The "HTTP loaded" component (12.2 seconds) is the primary cause of poor HTTP/2 responsiveness. This component does not exist in HTTP/1.1 tests.

---

## System Load

### CPU Information

- **Load Average**: Not captured during test (system was idle)
- **CPU Usage**: Normal (system was not under heavy load)
- **Thermal Status**: Normal

### Memory Information

- **Total RAM**: 16 GB
- **Memory Pressure**: Normal (not a factor)

---

## Network Stack Configuration

### TCP Settings

- **TCP sendspace**: 131072 bytes (128 KB)
- **TCP recvspace**: 131072 bytes (128 KB)
- **TCP congestion control**: CUBIC (default)
- **MTU**: 1500 (standard)

### DNS Configuration

- System default DNS (no custom configuration)
- No proxy settings

### Network Extensions

- **LuLu firewall**: Active (but issue persists when disabled)
- **No VPN**: Active
- **No system proxies**: Configured

---

## Related System Components

### Framework Versions

- **NetworkQualityServices.framework**: Private framework (version info not available)
- **Network.framework**: Version 4277.140.33
- **Foundation.framework**: Version 3603.0.0
- **CoreFoundation.framework**: Version 3603.0.0

### networkQuality Binary Information

```text
/usr/bin/networkQuality:
 /usr/lib/libnetquality.dylib (compatibility version 1.0.0, current version 147.140.5)
 /System/Library/PrivateFrameworks/NetworkQualityServices.framework/Versions/A/NetworkQualityServices (compatibility version 1.0.0, current version 0.0.0)
 /System/Library/Frameworks/Network.framework/Versions/A/Network (compatibility version 1.0.0, current version 4277.140.33)
 /System/Library/Frameworks/Foundation.framework/Versions/C/Foundation (compatibility version 300.0.0, current version 3603.0.0)
```

---

## Additional Context

### curl HTTP/2 Test (Works Fine)

**Command**: `curl -I --http2 https://www.apple.com`

**Result**: Success

- HTTP/2 200 response received
- Connection established successfully
- No delays or errors

**Conclusion**: HTTP/2 protocol stack is functional. The issue is specific to networkQuality's HTTP/2 test implementation.

### Comparison with Other Systems

- **macOS Monterey (12.7.6)**: HTTP/2 performance reported as 1245 RPM (High) on wolf-air system
- **macOS Sequoia (15.7.3)**: HTTP/2 performance is 13 RPM (Low) on michael-pro system
- **Note**: Direct comparison not possible due to different hardware/network conditions, but suggests possible Sequoia regression

---

## Diagnostic Commands Reference

```bash
# System version
sw_vers

# Hardware info
system_profiler SPHardwareDataType

# Software info
system_profiler SPSoftwareDataType

# networkQuality HTTP/2 test
networkQuality -f h2 -v

# networkQuality HTTP/1.1 test
networkQuality -f h1 -v

# CFNetwork logs
log show --predicate 'subsystem == "com.apple.CFNetwork" AND process == "networkQuality"' --last 2h --style compact

# curl HTTP/2 test
curl -I --http2 https://www.apple.com

# Network interface info
ifconfig en0

# TCP settings
sysctl net.inet.tcp
```

---

## End of System Diagnostics
