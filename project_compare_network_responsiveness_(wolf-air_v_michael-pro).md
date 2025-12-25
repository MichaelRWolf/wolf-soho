# Network Responsiveness Comparison: wolf-air vs michael-pro

## Executive Summary (Last Updated: 2025-12-25)

### Where we landed

There are two overlapping realities:

1. **Real network variability / congestion** exists (time-of-day effects), especially on **download**, and SQM rates need to be validated against what the line can actually sustain at that hour.
2. On **michael-pro (macOS Sequoia)**, Apple’s `networkQuality` tool can produce extremely low “Responsiveness” when using **HTTP/2**, while **HTTP/1.1** looks normal. This appears **tool/methodology-specific**, not “HTTP/2 is broken on the internet.”

### Current decisions / status

- **SQM/CAKE is active on Beryl** (OpenWrt) and is the primary control lever for loaded-latency.
  - Current “day” settings we’ve been using: **download 62000 kbit/s**, **upload 8000 kbit/s** (interface `eth0`).
  - Download shaping can be disabled (set to `0`) for experiments; this can help or hurt depending on conditions.
- **Use `bin/beryl_sqm` to view/change SQM** from a Mac without copy/paste:
  - `bin/beryl_sqm status` (read-only)
  - `bin/beryl_sqm <download_kbit> <upload_kbit>`
  - `bin/beryl_sqm day|night`
- **Use `bin/network_test` (curl-based)** as a simple, portable check across macOS versions.
- For Sequoia debugging, treat `networkQuality` results with caution unless forced to HTTP/1.1:
  - Use `networkQuality -f h1 -v` on `michael-pro` when you want a “sanity check” RPM.

### Quick Reference Commands (current)

```bash
# Read-only: show current SQM settings + CAKE counters
bin/beryl_sqm status

# Apply shaping (kbit/s): download upload
bin/beryl_sqm 62000 8000

# Portable curl-based test
bin/network_test

# networkQuality workaround on macOS Sequoia
networkQuality -f h1 -v
```

### System Info

- **michael-pro**: macOS 15.7.3 (Sequoia), WiFi (en0), LuLu firewall active
- **wolf-air**: macOS 12.7.6 (Monterey), WiFi, no LuLu detected  
- **Router**: GL-MT1300 (192.168.8.1) - same for both systems
- **LuLu location**: /Applications/LuLu.app, system extension active

### Notes on this document

- The long “Working Notes” section below is **append-only history**. Some intermediate hypotheses were later falsified (e.g., misreading cumulative nettop counters as instantaneous rates). Prefer the “Current decisions / status” section above for the present state.

### Important Notes

- Both systems use same router (GL-MT1300) - router is NOT the issue
- curl HTTP/2 works fine - issue is specific to networkQuality's CFNetwork implementation
- CPU throttling ruled out - michael-pro has better CPU specs and lower load
- Packet loss was ICMP rate-limiting, not actual data loss
- networkQuality uses CFNetwork (Apple framework), curl uses libcurl - different stacks

---

## Problem Statement

michael-pro consistently shows worse network quality (especially responsiveness) than wolf-air, even though:

- michael-pro is on Ethernet
- wolf-air is on WiFi
- Responsiveness is poor on michael-pro on both WiFi AND Ethernet (ruling out cable/Ethernet-specific issues)

## Current Test Results

**Tool**: `network_test.sh` (uses `curl` - built-in on all macOS versions)

### Comparison Table

| Metric                    | michael-pro         | wolf-air            | Notes                                                    |
|---------------------------|---------------------|---------------------|----------------------------------------------------------|
| **Download**              | 2.59 Mbps           | 2.84 Mbps           | Both very low, upload 2.5-3x higher                      |
| **Upload**                | ~7.5 Mbps           | 7.03 Mbps           | Unusually high relative to download                      |
| **Upload/Download Ratio** | 2.9:1               | 2.5:1               | **⚠️ Anomaly**: Upload > Download (opposite of typical)  |
| **RPM**                   | 68                  | 60                  | michael-pro slightly better                              |
| **Response Time**         | 0.875s              | 0.997s              | michael-pro slightly faster                              |
| **Test Date**             | 2025-12-24T17:43:13 | 2025-12-24T17:46:25 | Same day, 3 minutes apart                                |
|                           |                     |                     |                                                          |

### michael-pro (local, WiFi - en0)

**network_test.sh Results** (2025-12-24T17:43:13-0500):

- **Download**: 2.59 Mbps
- **Upload**: ~7.5 Mbps (983632 bytes/sec)
- **Responsiveness (RPM)**: 68
- **Average Response Time**: 0.875s
- **Tool**: curl (built-in)

### wolf-air (via SSH, WiFi)

**network_test.sh Results** (2025-12-24T17:46:25-0500):

- **Download**: 2.84 Mbps
- **Upload**: ~7.03 Mbps (879143 bytes/sec)
- **Responsiveness (RPM)**: 60
- **Average Response Time**: 0.997s
- **Tool**: curl via network_test.sh

**⚠️ Anomaly Detected**: Both machines show upload speeds 2.5-3x HIGHER than download speeds. This is unusual - typical broadband has download 5-20x faster than upload. See Working Notes for detailed analysis.

**Previous networkQuality Results** (2025-12-24T15:44:02-0500, Tool: `networkQuality`):

- Upload capacity: 2.799 Mbps
- Download capacity: 3.446 Mbps
- Responsiveness: High (1180 RPM)
- Base RTT: 24 ms

---

**Note**: Migrated to `network_test.sh` (curl-based) - simple, built-in tool that works on all macOS versions. Avoids installation issues and HTTP/2 bugs in networkQuality. See Working Notes section for detailed migration notes.

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

### 2025-12-24T12:49:44-0500 - System Load and Background Network Activity

**Machine**: michael-pro and wolf-air

**What**: Checked system load (CPU/memory) and background network activity on both systems using `ps aux`, `lsof -i`, and `nettop`.

**Findings**:

*michael-pro*:

- High CPU usage: WindowServer (28.2%), Daylite (25.6%), Chrome GPU (20.1%), Chrome (14.4%), multiple Cursor processes (4-5% each)
- Significant network activity:
  - rapportd: 19K bytes in, **3.7M bytes out** (very high upload)
  - Multiple Cursor Helper processes: 118K-339K bytes in, 441K-1.7M bytes out each
  - mDNSResponder: 11M bytes in, 6.4M bytes out
  - Google Drive: 28K bytes in, 23K bytes out (multiple processes running)
- Google Drive is running with multiple helper processes
- Many cloud sync processes active

*wolf-air*:

- Lower overall CPU usage
- Network activity:
  - rapportd: 3.5M bytes in, **16K bytes out** (much lower upload)
  - mDNSResponder: 13M bytes in, 3.4M bytes out
  - Python process: 35M bytes in, 508 bytes out (likely monitoring script)
  - Google Chrome Helper: 5.3M bytes in, 1.4M bytes out
  - netbiosd: 897K bytes in, 328K bytes out
- Fewer cloud sync processes
- No Google Drive running

**So what**:

- michael-pro has significantly higher system load (CPU) which could impact network responsiveness
- **Key difference**: rapportd on michael-pro is sending 3.7MB out vs only 16KB on wolf-air - this is a 230x difference in upload traffic
- michael-pro has Google Drive running with multiple processes that could be consuming bandwidth
- Multiple Cursor Helper processes on michael-pro are generating significant network traffic (1.7MB out from one process)
- The high upload traffic from rapportd and Cursor processes could be saturating the upload path, affecting responsiveness

**Now what**:

- Investigate what rapportd is doing on michael-pro that's causing such high upload traffic (230x more than wolf-air)
- Check if Google Drive is actively syncing and consider pausing it temporarily to test impact
- Consider checking network interface settings and QoS to see if upload traffic is being prioritized incorrectly
- Compare macOS versions between systems to check for network stack differences

---

### 2025-12-24T12:54:34-0500 - Detailed Process Investigation and Bandwidth Analysis

**Machine**: michael-pro and wolf-air

**What**: Investigated what each process is, calculated cumulative bandwidth percentages, enumerated all cloud sync processes, and compared total bandwidth usage.

**Process Definitions**:

- **rapportd**: Apple's Rapport Daemon - enables Phone Call Handoff and communication features between Apple devices. Connected to tigger-iphone.local (iPhone) and wolf-air.local.
- **mDNSResponder**: Multicast and Unicast DNS daemon - handles local network name resolution (Bonjour/mDNS).
- **identityservice**: Apple's identity service daemon (no manual page found, likely handles device identity/authentication).
- **Cursor Helper processes**: Multiple renderer and plugin processes for Cursor IDE - these are extension hosts and webview renderers.
- **node**: Node.js process (PID 51819) - appears to be cursor-agent related.

**Bandwidth Analysis - michael-pro**:

Total cumulative bandwidth (1-second snapshot):

- **Total IN**: 14,328,047 bytes (13.66 MB)
- **Total OUT**: 15,972,413 bytes (15.23 MB)

Top Uploaders (OUT) - percentage of total upload:

1. **mDNSResponder**: 6,463,353 bytes (6.16 MB) = **40.47%** of total upload
2. **rapportd**: 3,718,986 bytes (3.55 MB) = **23.28%** of total upload
3. **Cursor Helper (1281)**: 1,236,223 bytes (1.18 MB) = 7.74%
4. **node**: 1,182,435 bytes (1.13 MB) = 7.40%
5. **Cursor Helper (1273)**: 533,630 bytes (0.51 MB) = 3.34%
6. **Cursor Helper (1295)**: 517,997 bytes (0.49 MB) = 3.24%
7. **Cursor Helper (1280)**: 512,797 bytes (0.49 MB) = 3.21%
8. **Cursor Helper (1283)**: 511,413 bytes (0.49 MB) = 3.20%
9. **Cursor Helper (1287)**: 505,398 bytes (0.48 MB) = 3.16%

**Combined Cursor Helper upload**: ~4.2 MB = **26.3%** of total upload

Top Downloaders (IN):

1. **mDNSResponder**: 11,655,144 bytes (11.12 MB) = **81.34%** of total download
2. **node**: 523,367 bytes (0.50 MB) = 3.65%
3. **Cursor Helper processes**: Combined ~1.1 MB = ~7.7%

**Key Finding**: mDNSResponder + rapportd + Cursor Helpers = **89.8% of total upload bandwidth**

**Bandwidth Analysis - wolf-air**:

Total cumulative bandwidth (1-second snapshot):

- **Total IN**: 60,841,494 bytes (58.02 MB) - much higher due to Python monitoring script
- **Total OUT**: 13,959,026 bytes (13.31 MB)

Top Uploaders (OUT):

1. **mDNSResponder**: 3,407,779 bytes (3.25 MB) = 24.4%
2. **Cursor Helper processes**: Combined ~8.5 MB = ~61%
3. **Google Chrome Helper**: 1,418,250 bytes (1.35 MB) = 10.2%
4. **rapportd**: 18,759 bytes (0.02 MB) = 0.13% (230x less than michael-pro!)

**Cloud Sync Processes Enumeration - michael-pro**:

Found 63 processes matching cloud/sync/backup/drive patterns, but many are false positives (driver extensions, ColorSync, etc.). Actual cloud/sync services:

**Google Drive** (13 processes):

- Google Drive (main process)
- Google Drive Helper (GPU)
- Google Drive Helper (Renderer) - 5 instances
- Google Drive Helper (Network Service)
- Google Drive Helper (Storage Service)
- FinderSyncExtension
- DFSFileProviderExtension
- Backup and Sync FinderSyncAPIExtension
- crashpad_handler

**Apple iCloud Services** (15+ processes):

- cloudd (CloudKitDaemon) - 2 instances (user + system)
- cloudphotod (iCloud Photos)
- bird (iCloud Drive)
- iCloudNotificationAgent
- iTunesCloud (iTunes cloud sync)
- PrivateCloudCompute (private cloud compute)
- CloudServices (com.apple.sbd)
- ProtectedCloudKeySyncing
- CloudTelemetryService - 6 instances
- CloudPhotosConfiguration
- CloudKitDaemon
- iCloudDriveCore
- SyncedDefaults (syncdefaultsd)
- CallHistorySyncHelper
- MapsSync (mapssyncd)
- appplaceholdersyncd
- UserPictureSyncAgent
- SafariBookmarksSyncAgent
- CMFSyncAgent (CommunicationsFilter)
- icloudmailagent

**Time Machine Backup** (2 processes):

- backupd
- backupd-helper

**macOS Version Comparison**:

- **michael-pro**: macOS 15.7.3 (Sequoia) Build 24G419
- **wolf-air**: macOS 12.7.6 (Monterey) Build 21H1320

**So what**:

- **mDNSResponder is the largest uploader** on michael-pro at 40.5% of total upload - this is local network traffic (Bonjour/mDNS)
- **rapportd is second largest** at 23.3% - this is Apple device communication (iPhone handoff, etc.)
- **Cursor Helper processes combined** are 26.3% of upload - this is IDE-related network activity
- **Total of top 3 categories = 89.8% of upload bandwidth** - these are all local network or application-specific, not internet traffic
- Google Drive shows minimal network activity (27K in, 22K out) - not actively syncing large amounts
- **Major macOS version difference**: michael-pro is on Sequoia (15.x) vs wolf-air on Monterey (12.x) - 3 major versions apart, significant network stack differences possible
- The high upload traffic appears to be **local network traffic** (mDNS, rapport, Cursor IDE communication) rather than internet traffic, which shouldn't directly affect internet responsiveness tests

**Now what**:

- Investigate why mDNSResponder is generating so much upload traffic (6.16 MB vs 3.25 MB on wolf-air) - could be network discovery/announcement issues
- Check if rapportd is stuck in a loop or misconfigured - why is it sending 230x more data than wolf-air?
- Investigate Cursor Helper processes - what network activity are they doing? Could be extension communication or AI features
- Test networkQuality with Cursor closed to see if Cursor Helper traffic is affecting responsiveness
- Compare mDNSResponder behavior between systems - why is it so much higher on michael-pro?
- Consider that local network traffic shouldn't affect internet responsiveness, so investigate network stack/QoS settings that might be prioritizing local traffic incorrectly

---

### 2025-12-24T12:59:30-0500 - Cursor Helper Network Activity During networkQuality Test

**Machine**: michael-pro

**What**: Ran networkQuality test while Cursor was open and monitored Cursor Helper process network activity before, during, and after the test.

**Test Results**:

- **Uplink capacity**: 9.225 Mbps
- **Downlink capacity**: 2.656 Mbps  
- **Responsiveness**: Low (3.682 seconds | 16 RPM)
- **Idle Latency**: 39.946 milliseconds | 1502 RPM

**Cursor Helper Process Activity**:

- **33 Cursor Helper processes** running
- **1-second snapshot**: Cursor Helper processes generating 4.16 MB upload, 1.05 MB download
- **5-second measurement**: Cursor Helper processes generating **18.15 MB upload** = **29.04 Mbps upload rate**
- **Primary culprit**: PID 1281 (Cursor Helper Plugin: extension-host [6-4]) generating 1.3+ MB upload
- PID 1281 has active connections to:
  - Cloudflare (104.18.18.125:443)
  - Multiple AWS EC2 instances (Amazon Web Services) on HTTPS

**Bandwidth Comparison**:

- **Available uplink capacity**: 9.225 Mbps
- **Cursor Helper upload rate**: 29.04 Mbps
- **Cursor is consuming 3.15x the available upload bandwidth!**

**So what**:

- **CRITICAL FINDING**: Cursor Helper processes are **saturating the upload path** with 29 Mbps of traffic, while only 9.225 Mbps is available
- This is **internet traffic** (Cloudflare, AWS EC2) - not local network traffic as previously thought
- The extension host process (PID 1281) is likely handling Cursor AI features or extension communication with external servers
- This upload saturation would **absolutely cause poor responsiveness** - the upload path is completely saturated, preventing proper bidirectional communication needed for responsiveness tests
- The responsiveness test requires both upload and download to work properly - with upload saturated, responses can't be sent properly, causing the 3.68 second delay and 16 RPM (vs 748 RPM on wolf-air)

**Now what**:

- **Test with Cursor completely closed** to confirm Cursor is the cause of poor responsiveness
- If closing Cursor fixes responsiveness, investigate Cursor settings to:
  - Disable or throttle AI features that require constant server communication
  - Check extension settings that might be causing excessive network usage
  - Look for Cursor network/throttling settings
- Compare Cursor network usage on wolf-air (if Cursor is installed there) to see if this is a configuration issue
- Consider that this might be expected Cursor behavior (AI features require constant communication), but it's incompatible with the limited upload bandwidth available

---

### 2025-12-24T13:03:26-0500 - Test with Cursor Closed and Excess Upload Traffic Analysis

**Machine**: michael-pro

**What**: Attempted to close Cursor completely, ran networkQuality test, and investigated what happens to excess upload traffic when 3.15x capacity is generated.

**Cursor Closure Status**:

- Main Cursor window closed via `osascript`
- **18 Cursor Helper processes still running** (did not fully terminate)
- However, **Cursor network traffic dropped to 0** - processes are idle, not generating traffic

**networkQuality Results with Cursor Closed**:

- **Uplink capacity**: 14.443 Mbps (was 9.225 Mbps with Cursor open) = **56.5% improvement**
- **Downlink capacity**: 2.491 Mbps (was 2.656 Mbps) = slight decrease
- **Responsiveness**: Low (3.172 seconds | 18 RPM) - still poor, but slightly better than 16 RPM
- **Idle Latency**: 47.892 milliseconds | 1252 RPM

**What Happens to Excess Upload Traffic (3.15x Capacity)**:

When an application tries to send 29 Mbps but only 9.225 Mbps is available, the excess traffic doesn't "disappear" - it goes through several stages:

1. **TCP Send Buffer Queue** (128 KB default on macOS):
   - Data is queued in the TCP send buffer (net.inet.tcp.sendspace: 131072 bytes = 128 KB)
   - This buffer can hold ~0.1 seconds of data at 9 Mbps
   - When buffer fills, the application's `write()` calls block or return EAGAIN

2. **TCP Flow Control**:
   - TCP's sliding window mechanism detects the receiver can't keep up
   - The send window shrinks, reducing how much data can be sent before waiting for ACKs
   - TCP automatically throttles the sender to match available capacity

3. **Packet Queuing**:
   - Packets queue in multiple layers:
     - Application buffer → TCP send buffer → Network interface queue → Router/switch buffers
   - Each layer adds latency as packets wait to be transmitted

4. **ACK Delays**:
   - With saturated upload, ACKs from the server are delayed
   - TCP interprets delayed ACKs as potential packet loss
   - This triggers TCP's congestion control algorithms (Reno, CUBIC, etc.)

5. **Congestion Control Response**:
   - TCP reduces the congestion window (cwnd)
   - Sender backs off and sends less data
   - This creates a "sawtooth" pattern of sending bursts, then backing off

6. **Buffer Overflow and Packet Drops**:
   - If queues fill completely, packets are dropped
   - Dropped packets trigger retransmissions
   - Retransmissions consume bandwidth that could be used for new data
   - This creates a feedback loop: more drops → more retransmits → more congestion

7. **Impact on Responsiveness**:
   - **Bidirectional communication breaks down**: Responsiveness tests need to send requests and receive responses quickly. With upload saturated:
     - Request packets queue for seconds before being sent
     - ACKs for responses are delayed
     - The round-trip time (RTT) increases dramatically
   - **Head-of-line blocking**: Important packets (like ACKs) wait behind Cursor's data packets
   - **TCP fairness issues**: Cursor's many connections can starve other applications

**System Observations**:

- TCP retransmit statistics show 0 retransmits currently (good - no packet loss detected)
- TCP send/recv buffers: 128 KB each (relatively small, fills quickly)
- No TCP buffer overflow detected in netstat (buffers managed properly)

**So what**:

- **Cursor was definitely saturating upload**: Closing Cursor (even partially) freed up 5.2 Mbps of upload capacity (56% improvement)
- **Responsiveness still poor**: Even with Cursor closed, responsiveness is Low (18 RPM vs 16 RPM) - only slight improvement
- **Other factors at play**: Since responsiveness is still poor without Cursor, there are likely other issues:
  - mDNSResponder still generating high upload (6+ MB)
  - rapportd still generating high upload (3.7 MB)
  - Network stack configuration issues
  - Possible router/ISP throttling or QoS issues
- **Excess traffic behavior**: The excess upload traffic (3.15x capacity) is handled by TCP's flow control and congestion control, but this creates severe latency spikes and poor responsiveness for all applications

**Now what**:

- **Kill remaining Cursor processes** to fully eliminate Cursor traffic and retest
- **Investigate mDNSResponder** - why is it generating 6+ MB upload? This is local network traffic but shouldn't affect internet tests unless there's a routing/QoS issue
- **Investigate rapportd** - why 3.7 MB upload vs 16 KB on wolf-air? This is Apple device communication
- **Test with both Cursor AND mDNS/rapportd traffic reduced** to isolate the root cause
- Consider that **local network traffic (mDNS, rapport) shouldn't affect internet responsiveness** unless there's a network configuration issue (shared interface, QoS misconfiguration, etc.)

---

### 2025-12-24T13:07:09-0500 - All Cursor Processes Killed (Except cursor-agent)

**Machine**: michael-pro

**What**: Killed all remaining Cursor Helper and Cursor.app processes while preserving cursor-agent (PIDs 51819, 52131) which is required for this AI assistant to function.

**Process Status**:

- **All Cursor Helper processes**: Terminated (no matching processes found)
- **All Cursor.app processes**: Terminated (no matching processes found)
- **cursor-agent processes**: Preserved and running (PIDs 51819, 52131)
- **CursorUIViewService**: Still running (PID 862) - system service for text input, not part of main Cursor app
- **Cursor network traffic**: 0 (confirmed via nettop)

**networkQuality Results with All Cursor Processes Killed**:

- **Uplink capacity**: 10.029 Mbps (was 14.443 Mbps with Cursor partially closed, 9.225 Mbps with Cursor open)
- **Downlink capacity**: 2.698 Mbps (was 2.491 Mbps)
- **Responsiveness**: Low (3.648 seconds | 16 RPM) - **back to original poor performance**
- **Idle Latency**: 49.564 milliseconds | 1210 RPM

**Observations**:

- Uplink capacity decreased from 14.4 Mbps back to ~10 Mbps - suggests other traffic sources are still active
- Responsiveness is still Low (16 RPM) - same as with Cursor open
- **Cursor was not the primary cause** of poor responsiveness, though it was contributing to upload saturation

**So what**:

- **Cursor eliminated**: All Cursor processes killed, network traffic confirmed at 0
- **Responsiveness still poor**: Even without Cursor, responsiveness remains Low (16 RPM)
- **Other traffic sources active**: The decrease in uplink capacity (14.4 → 10 Mbps) suggests other processes are consuming bandwidth:
  - mDNSResponder (6+ MB upload)
  - rapportd (3.7 MB upload)
  - Other background processes
- **Cursor was a contributing factor but not the root cause**: While Cursor was saturating upload (29 Mbps), killing it didn't fix responsiveness, indicating the underlying issue is elsewhere

**Now what**:

- **Investigate mDNSResponder** - why is it generating 6+ MB upload? This is the largest uploader now
- **Investigate rapportd** - why 3.7 MB upload vs 16 KB on wolf-air? This is the second largest uploader
- **Compare total upload traffic** between michael-pro and wolf-air to see if there's a systemic difference
- **Test networkQuality on wolf-air** to establish baseline for comparison
- Consider that **local network traffic (mDNS, rapport) shouldn't affect internet responsiveness** - investigate if there's a network configuration issue causing local traffic to interfere with internet traffic

---

### 2025-12-24T13:13:33-0500 - CRITICAL CORRECTION: Misinterpreted Cumulative Totals as Rates

**Machine**: michael-pro

**What**: Discovered that nettop values are **cumulative totals since boot**, NOT current traffic rates. Re-measured actual current rates using delta calculations over 10-second intervals.

**Measurement Method**:

- Baseline snapshot: mDNSResponder OUT=6,503,809 bytes, rapportd OUT=16,040 bytes
- After 10 seconds: mDNSResponder OUT=6,503,557 bytes, rapportd OUT=16,040 bytes
- **Delta over 10 seconds**: mDNSResponder OUT=-252 bytes (essentially zero), rapportd OUT=0 bytes

**Actual Current Traffic Rates** (10-second delta):

- **mDNSResponder**: ~0 Mbps upload, ~0 Mbps download (essentially idle)
- **rapportd**: 0 Mbps upload, 0 Mbps download (completely idle)
- **identityservice**: 0 Mbps upload, 0 Mbps download (completely idle)

**Previous Incorrect Analysis**:

- Previously interpreted 6.5 MB and 3.7 MB as current rates
- If these were rates: 6.5 MB/s = 52 Mbps (would exceed capacity)
- **These were actually cumulative totals since boot** - reasonable for processes running for hours/days

**Corrected Understanding**:

- **mDNSResponder, rapportd, and identityservice are NOT consuming significant bandwidth currently**
- The 6.5 MB and 16 KB values are total bytes transferred since the system booted
- These processes are essentially idle from a network perspective right now
- **Previous analysis incorrectly blamed these processes for bandwidth consumption**

**So what**:

- **Major error in analysis**: We were looking at cumulative totals, not actual rates
- **mDNSResponder/rapportd are NOT the problem**: They're essentially idle (0 Mbps)
- **Need to identify actual current bandwidth consumers**: Must measure actual rates, not cumulative totals
- **Cursor was the real bandwidth consumer**: When Cursor was running, it was generating 29 Mbps upload (actual rate), which was saturating the 9 Mbps capacity
- **Root cause still unknown**: Since mDNSResponder/rapportd aren't consuming bandwidth, and Cursor is closed, the poor responsiveness must have another cause

**Now what**:

- **Measure actual current rates** for all processes to identify real bandwidth consumers
- **Re-evaluate the entire investigation** - previous conclusions based on cumulative totals may be incorrect
- **Focus on actual current traffic** during networkQuality tests to see what's really consuming bandwidth
- **Compare actual rates** between michael-pro and wolf-air, not cumulative totals
- Consider that **poor responsiveness may not be due to bandwidth saturation** - could be latency, packet loss, routing issues, or other network stack problems

---

### 2025-12-24T13:16:54-0500 - Actual Current Rates During networkQuality Test

**Machine**: michael-pro

**What**: Measured actual current traffic rates (deltas) during a networkQuality test by taking baseline before test and measurement during test.

**Measurement Method**:

- Baseline snapshot before networkQuality
- Started networkQuality test
- Measurement 12 seconds into test
- Calculated deltas and actual rates

**Actual Traffic Rates During networkQuality Test (12-second delta)**:

**networkQuality process**:

- **Upload**: 6,232,955 bytes (5.94 MB) = **3.96 Mbps**
- **Download**: 3,672,515 bytes (3.50 MB) = **2.33 Mbps**

**Other processes** (12-second delta):

- **mDNSResponder**: 0 bytes change (completely idle)
- **rapportd**: 0 bytes change (completely idle)  
- **node.51819** (cursor-agent): ~1,850 bytes OUT = 0.001 Mbps (negligible)

**networkQuality Test Results**:

- Uplink capacity: 15.126 Mbps
- Downlink capacity: 2.573 Mbps
- Responsiveness: Low (3.260 seconds | 18 RPM)
- Idle Latency: 48.834 milliseconds | 1228 RPM

**Bandwidth Usage Analysis**:

- networkQuality used **3.96 Mbps upload** = **26.2% of available upload capacity** (15.126 Mbps)
- networkQuality used **2.33 Mbps download** = **90.7% of available download capacity** (2.573 Mbps)
- **Download path is nearly saturated** during the test (90.7% utilization)

**So what**:

- **mDNSResponder and rapportd are NOT consuming bandwidth** - confirmed idle (0 Mbps)
- **networkQuality itself is the primary bandwidth consumer** during tests
- **Download path is nearly saturated** (90.7%) which could contribute to poor responsiveness
- **Upload path has plenty of headroom** (only 26% used) - not the bottleneck
- **Poor responsiveness persists** even when download is the limiting factor, suggesting the issue may not be simple bandwidth saturation
- **Root cause likely elsewhere**: With download at 90% utilization, responsiveness should still be better than 18 RPM if bandwidth were the only issue

**Now what**:

- **Investigate download path** - why is download capacity so low (2.573 Mbps) compared to upload (15.126 Mbps)?
- **Compare with wolf-air** - what are the actual rates and capacity there?
- **Investigate latency/packet loss** - poor responsiveness with 90% download utilization suggests latency or packet loss issues, not just bandwidth
- **Check networkQuality test methodology** - is it testing correctly? Why such low download vs upload?
- **Consider ISP/throttling** - asymmetric speeds (15 Mbps up, 2.5 Mbps down) are unusual - could indicate throttling or connection issues

---

### 2025-12-24T13:21:26-0500 - Comparison: michael-pro vs wolf-air networkQuality Test

**Machine**: michael-pro and wolf-air

**What**: Ran identical networkQuality tests on both systems and compared actual traffic rates, capacity, and responsiveness.

**Capacity Measurements**:

| Metric            | michael-pro  | wolf-air        | Difference                       |
|-------------------|--------------|-----------------|----------------------------------|
| Upload Capacity   | 15.126 Mbps  | 12.733 Mbps     | +2.393 Mbps (michael-pro higher) |
| Download Capacity | 2.573 Mbps   | 5.149 Mbps      | -2.576 Mbps (wolf-air 2x higher) |
| Responsiveness    | Low (18 RPM) | High (1245 RPM) | -1227 RPM (wolf-air 69x better)  |

**Actual Traffic Rates During Test (12-second delta)**:

| Process        | michael-pro OUT | wolf-air OUT | michael-pro IN | wolf-air IN |
|----------------|-----------------|--------------|----------------|-------------|
| networkQuality | 3.96 Mbps       | 7.11 Mbps    | 2.33 Mbps      | 4.63 Mbps   |

**Bandwidth Utilization During Test**:

| Metric               | michael-pro | wolf-air |
|----------------------|-------------|----------|
| Upload Utilization   | 26.2%       | 55.8%    |
| Download Utilization | 90.7%       | 89.9%    |

**Key Findings**:

1. **Download capacity is the problem**: wolf-air has **2x the download capacity** (5.149 vs 2.573 Mbps)
2. **Both systems have similar download utilization** (~90%), but wolf-air handles it much better
3. **Responsiveness difference is dramatic**: wolf-air is **69x better** (1245 vs 18 RPM) despite similar upload capacity
4. **michael-pro actually has HIGHER upload capacity** (15.126 vs 12.733 Mbps) - upload is not the issue
5. **Download path is the bottleneck**: Both systems saturate download (~90%), but michael-pro's lower capacity causes poor responsiveness

**Other Process Activity**:

- **mDNSResponder**: Both systems showed 0 bytes change (idle) during test
- **rapportd**: Both systems showed 0 bytes change (idle) during test
- **node (cursor-agent)**: Negligible traffic on michael-pro

**So what**:

- **Root cause identified**: **Download capacity is too low on michael-pro** (2.573 Mbps vs 5.149 Mbps on wolf-air)
- **Download saturation is the problem**: Both systems use ~90% of download capacity, but michael-pro's lower capacity causes poor responsiveness
- **Upload is NOT the issue**: michael-pro has higher upload capacity and lower utilization than wolf-air
- **Process-level bandwidth consumption is NOT the issue**: mDNSResponder, rapportd, and other processes are idle
- **The 2.5 Mbps download capacity is abnormally low** - this is likely the root cause of poor responsiveness

**Now what**:

- **Investigate why download capacity is so low on michael-pro**:
  - Check Ethernet interface settings (speed, duplex, MTU)
  - Check router/switch port configuration
  - Check for QoS/throttling on download path
  - Compare network interface configuration between systems
- **Investigate why responsiveness is so poor** even with similar download utilization:
  - Check for packet loss on download path
  - Check latency/jitter differences
  - Compare network stack settings (TCP parameters, buffer sizes)
- **Consider ISP/throttling**: The asymmetric speeds (15 Mbps up, 2.5 Mbps down) are unusual and could indicate:
  - ISP throttling download
  - Router QoS misconfiguration
  - Network interface misconfiguration
  - Cable/connection issues affecting download more than upload

---

### 2025-12-24T13:39:59-0500 - System Performance Analysis: CPU Throttling Investigation

**Machine**: michael-pro and wolf-air

**What**: Investigated whether CPU throttling due to old battery (1500 cycles on 1000 cycle battery) is affecting network performance. Compared system specs, CPU load, thermal status, and memory pressure.

**System Specifications**:

| Metric      | michael-pro                         | wolf-air                      |
|-------------|-------------------------------------|-------------------------------|
| **Model**   | MacBook Pro 16,2                    | MacBook Air 7,2               |
| **CPU**     | Intel Core i5-1038NG7 @ 2.00GHz     | Intel Core i5-5350U @ 1.80GHz |
| **Cores**   | 4 physical / 8 logical              | 2 physical / 4 logical        |
| **Memory**  | 16 GB                               | 8 GB                          |
| **Network** | Ethernet (USB-C adapter, 1000baseT) | WiFi (autoselect)             |
| **Battery** | 100% charged, AC power              | Unknown                       |

**CPU Performance Metrics**:

| Metric              | michael-pro                          | wolf-air       |
|---------------------|--------------------------------------|----------------|
| **Load Average**    | 2.92 2.89 3.57                       | 7.96 5.34 6.30 |
| **Load per Core**   | ~0.36-0.45                           | ~1.33-1.99     |
| **CPU Usage**       | 18.70% user, 14.63% sys, 66.66% idle | Unknown        |
| **CPU Frequency**   | 2.0 GHz (locked at base)             | Unknown        |
| **Thermal Level**   | 56 (scale unknown)                   | Unknown        |
| **Pages Throttled** | 0                                    | Unknown        |

**Memory Status**:

| Metric            | michael-pro    | wolf-air        |
|-------------------|----------------|-----------------|
| **Total RAM**     | 16 GB          | 8 GB            |
| **Swap Used**     | 2.5 GB / 4 GB  | 4.5 GB / 5 GB   |
| **Swap Pressure** | Low (62% free) | High (11% free) |

**Key Findings**:

1. **michael-pro has MORE CPU resources**: 8 logical cores vs 4, higher base frequency (2.0 vs 1.8 GHz)
2. **michael-pro has LOWER load per core**: 0.36-0.45 vs 1.33-1.99 on wolf-air
3. **CPU is NOT heavily loaded**: 66% idle on michael-pro
4. **CPU frequency NOT throttled**: Locked at base 2.0 GHz (not showing dynamic throttling)
5. **No memory throttling**: 0 pages throttled on michael-pro
6. **wolf-air has HIGHER load per core** yet BETTER network performance - contradicts CPU throttling theory
7. **Network interface difference**: michael-pro on Ethernet (USB-C adapter), wolf-air on WiFi

**So what**:

- **CPU throttling is NOT the issue**: michael-pro has more CPU resources, lower load per core, and CPU is 66% idle
- **System performance is NOT the bottleneck**: michael-pro has better CPU specs and lower load than wolf-air, yet worse network performance
- **The problem is network-specific**: Since CPU/system performance is better on michael-pro, the issue must be:
  - Network interface/driver issues (USB-C Ethernet adapter)
  - Network stack configuration
  - Router/switch port configuration
  - ISP/throttling on download path
- **USB-C Ethernet adapter could be the issue**: michael-pro uses a USB-C Ethernet adapter (Belkin USB-C LAN) while wolf-air uses built-in WiFi - USB adapters can have driver/performance issues

**Now what**:

- **Test michael-pro on WiFi** to compare with Ethernet (USB-C adapter) - if WiFi performs better, the USB-C adapter is the issue
- **Check USB-C Ethernet adapter driver/firmware** - update if possible
- **Compare network interface settings** between Ethernet and WiFi on michael-pro
- **Investigate USB-C adapter performance** - check for known issues with Belkin USB-C LAN adapter
- **Consider testing with different Ethernet adapter** if available
- **Focus investigation on network interface/driver** rather than CPU/system performance

---

### 2025-12-24T13:52:22-0500 - WiFi vs Ethernet (USB-C) Comparison Test

**Machine**: michael-pro

**What**: Tested networkQuality on WiFi to compare with Ethernet (USB-C adapter) performance.

**Test Configuration**:

- **Ethernet**: Belkin USB-C LAN adapter (en13), 1000baseT full-duplex
- **WiFi**: Built-in WiFi (en0), autoselect

**networkQuality Results**:

| Metric                | Ethernet (USB-C) | WiFi         | Difference             |
|-----------------------|------------------|--------------|------------------------|
| **Upload Capacity**   | 15.126 Mbps      | 15.536 Mbps  | +0.410 Mbps (similar)  |
| **Download Capacity** | 2.573 Mbps       | 4.580 Mbps   | **+2.007 Mbps (+78%)** |
| **Responsiveness**    | Low (18 RPM)     | Low (18 RPM) | Same (still poor)      |
| **Idle Latency**      | 48.834 ms        | 45.885 ms    | Slightly better        |

**Comparison with wolf-air**:

| Metric                | michael-pro WiFi | wolf-air WiFi   | Difference                |
|-----------------------|------------------|-----------------|---------------------------|
| **Download Capacity** | 4.580 Mbps       | 5.149 Mbps      | -0.569 Mbps (11% lower)   |
| **Upload Capacity**   | 15.536 Mbps      | 12.733 Mbps     | +2.803 Mbps (higher)      |
| **Responsiveness**    | Low (18 RPM)     | High (1245 RPM) | **-1227 RPM (68x worse)** |

**Key Findings**:

1. **USB-C Ethernet adapter IS limiting download**: WiFi download is **78% better** (4.58 vs 2.57 Mbps)
2. **WiFi download still below wolf-air**: 4.58 Mbps vs 5.15 Mbps (11% lower)
3. **Responsiveness still poor on WiFi**: 18 RPM on both interfaces, vs 1245 RPM on wolf-air
4. **Upload capacity similar**: Both interfaces achieve ~15 Mbps upload
5. **The USB-C adapter is a problem, but not the only problem**: Even with WiFi (78% better download), responsiveness is still Low

**So what**:

- **USB-C Ethernet adapter confirmed as download bottleneck**: Download capacity increases 78% when switching to WiFi
- **Additional issues beyond interface**: Responsiveness is still Low (18 RPM) on WiFi, suggesting:
  - Network stack configuration issues
  - Packet loss or latency issues
  - Router/switch configuration differences
  - macOS network stack differences (Sequoia vs Monterey)
- **Download capacity gap**: WiFi (4.58 Mbps) is still 11% lower than wolf-air (5.15 Mbps), but much closer than Ethernet (2.57 Mbps)
- **Responsiveness gap remains huge**: 18 RPM vs 1245 RPM (68x difference) even with similar download capacity

**Now what**:

- **Use WiFi instead of USB-C Ethernet adapter** for better download performance (78% improvement)
- **Investigate why responsiveness is still poor on WiFi**:
  - Compare network stack settings between michael-pro and wolf-air
  - Check for packet loss differences
  - Investigate macOS version differences (Sequoia 15.7.3 vs Monterey 12.7.6)
  - Check router/switch port configuration differences
- **Consider replacing USB-C Ethernet adapter** if Ethernet is needed
- **Investigate why michael-pro responsiveness is 68x worse** than wolf-air even with similar download capacity

---

### 2025-12-24T13:56:17-0500 - CRITICAL: Packet Loss Identified as Root Cause

**Machine**: michael-pro

**What**: Measured packet loss to router and internet to investigate responsiveness issues.

**Packet Loss Measurements**:

| Target                   | Packets Sent | Packets Received | Packet Loss | Latency (min/avg/max/stddev)    |
|--------------------------|--------------|------------------|-------------|---------------------------------|
| **Router (192.168.8.1)** | 20           | 16               | **20%**     | 2.033/46.304/495.441/118.260 ms |
| **Router (192.168.8.1)** | 50           | 46               | **8%**      | 2.004/21.138/310.263/48.845 ms  |
| **Internet (8.8.8.8)**   | 20           | 15               | **25%**     | 19.796/22.545/28.086/2.675 ms   |
| **Internet (8.8.8.8)**   | 50           | 46               | **8%**      | 18.102/35.282/139.050/27.253 ms |

**Key Observations**:

- **Severe packet loss**: 8-25% packet loss is EXTREMELY high (normal is <1%)
- **High jitter**: stddev up to 118ms to router (normal is <10ms)
- **Latency spikes**: Up to 495ms to router (normal is <10ms)
- **Packet loss occurs at router level**: 20% loss to router itself indicates router or WiFi issues
- **Inconsistent loss**: Varies between 8-25% (suggests intermittent congestion or interference)

**Network Interface Statistics**:

- **WiFi interface (en0)**: 0 errors, 0 collisions (interface itself is healthy)
- **TCP statistics**: 0 retransmits, 0 out-of-order packets (TCP layer is handling loss)
- **Router**: console.gl-inet.com (192.168.8.1) - GL-iNet router

**So what**:

- **ROOT CAUSE IDENTIFIED**: **8-25% packet loss is causing poor responsiveness**
- **Packet loss explains 18 RPM vs 1245 RPM**: With 8-25% packet loss, responsiveness tests fail because:
  - Request packets are lost, requiring retransmission
  - Response packets are lost, requiring retransmission
  - High jitter (118ms stddev) causes inconsistent timing
  - Latency spikes (up to 495ms) cause timeouts
- **Packet loss is at router level**: 20% loss to router itself suggests:
  - Router buffer overflow/overload
  - WiFi interference or quality issues
  - Router firmware/configuration problems
  - Network congestion on router
- **This is NOT a michael-pro system issue**: The packet loss is happening in the network path, not on the machine

**Now what**:

- **Investigate router (GL-iNet) status and configuration**:
  - Check router CPU/memory usage
  - Check router buffer settings
  - Check WiFi channel interference
  - Check router firmware version
  - Check for QoS/throttling settings
- **Compare packet loss on wolf-air** (when SSH is available) to see if it's router-wide or michael-pro specific
- **Test from different devices** to isolate if it's michael-pro WiFi or router issue
- **Check WiFi signal strength and channel** on michael-pro
- **Consider router firmware update or reset** if router is overloaded
- **Investigate WiFi interference** - check for channel congestion, neighboring networks

---

### 2025-12-24T14:00:58-0500 - CORRECTION: ICMP Rate Limiting, Not Actual Packet Loss

**Machine**: michael-pro

**What**: Discovered that router (GL-MT1300) is rate-limiting ICMP ping packets, not dropping actual data traffic.

**ICMP Ping Test Results**:

| Test                 | Interval | Packets | Packet Loss | Notes                     |
|----------------------|----------|---------|-------------|---------------------------|
| Fast pings to router | 0.1s     | 10      | **90%**     | Router rate-limiting ICMP |
| Slow pings to router | 0.2s     | 100     | **0%**      | Normal traffic OK         |
| Ping to wolf-air     | 1s       | 20      | 5-10%       | Some loss to other device |
| Ping to internet     | 1s       | 50      | 8%          | Some loss                 |

**Actual Data Traffic Tests**:

- **TCP connections**: All successful (router port 80, internet port 53)
- **HTTP requests**: Fast and reliable (0.1s to router, 0.18s to google.com)
- **TCP statistics**: 0 retransmits, 0 out-of-order packets
- **Network interface**: 0 errors, 0 collisions

**Key Discovery**:

- **Router is rate-limiting ICMP**, not dropping actual data packets
- **TCP/UDP data traffic works fine** - no actual packet loss detected
- **The 8-25% "packet loss" was ICMP throttling**, not real data loss
- **networkQuality uses TCP/UDP**, not ICMP, so ICMP rate-limiting doesn't affect it

**So what**:

- **Previous packet loss analysis was misleading**: ICMP rate-limiting is not the cause of poor responsiveness
- **Actual data traffic is fine**: TCP connections work, HTTP requests are fast
- **Router is NOT the problem**: Both michael-pro and wolf-air use the same router, so router can't explain the difference
- **Need to look elsewhere**: Since router works fine and both machines use it, the 18 RPM vs 1245 RPM difference must be:
  - macOS version differences (Sequoia 15.7.3 vs Monterey 12.7.6)
  - Network stack configuration differences
  - System-level network settings
  - Application-level differences in how networkQuality runs

**Now what**:

- **Focus on macOS/network stack differences** between Sequoia and Monterey
- **Compare networkQuality implementation** - does it behave differently on different macOS versions?
- **Check system network settings** that might affect responsiveness testing
- **Investigate if networkQuality has known issues** on macOS Sequoia
- **Compare actual TCP performance** between systems using iperf3 or similar tools
- **Look for macOS network stack bugs** or configuration issues in Sequoia

---

### 2025-12-24T14:08:35-0500 - Network Stack Settings and networkQuality Verbose Analysis

**Machine**: michael-pro

**What**: Collected network stack settings and ran networkQuality with verbose output to get detailed breakdown of responsiveness components.

**Network Stack Settings - michael-pro**:

| Setting                            | Value                                           |
|------------------------------------|-------------------------------------------------|
| **TCP sendspace**                  | 131072 bytes (128 KB)                           |
| **TCP recvspace**                  | 131072 bytes (128 KB)                           |
| **TCP congestion control**         | CUBIC (95% of sockets)                          |
| **TCP delayed_ack**                | 3                                               |
| **MTU**                            | 1500 (standard)                                 |
| **DNS**                            | System default (none set on WiFi)               |
| **Proxy**                          | Minimal (only .local and 169.254/16 exceptions) |
| **TSO (TCP Segmentation Offload)** | Enabled                                         |
| **Path MTU Discovery**             | Enabled                                         |

**networkQuality Verbose Output Breakdown**:

| Component                  | RPM        | Latency       | Notes                                |
|----------------------------|------------|---------------|--------------------------------------|
| **Overall Responsiveness** | **30 RPM** | 1.979 seconds | **Low**                              |
| Transport                  | 2838 RPM   | 21.140 ms     | **GOOD** - network layer is fast     |
| Security (TLS/SSL)         | 495 RPM    | 121.070 ms    | **SLOW** - TLS handshake bottleneck  |
| HTTP                       | 1575 RPM   | 38.093 ms     | OK                                   |
| **HTTP loaded**            | **14 RPM** | 4.245 seconds | **VERY SLOW** - page load bottleneck |

**Idle Latency Breakdown**:

- Overall: 1104 RPM (54.345 ms) - **High** (good)
- Transport: 2566 RPM (23.375 ms) - Excellent
- Security: 524 RPM (114.500 ms) - Slow TLS
- HTTP: 2384 RPM (25.159 ms) - Good

**Test Details**:

- Test Endpoint: usmia1-edge-fx-018.aaplimg.com
- Interface: en0 (WiFi)
- Protocol: HTTP/2 (100%)
- ECN: Disabled (100%)
- L4S: Disabled (100%)
- OS Version: macOS 15.7.3 (Build 24G419)

**Key Findings**:

1. **Transport layer is FAST**: 2838 RPM (21ms) - network transport itself is not the problem
2. **TLS/SSL handshake is SLOW**: 495 RPM (121ms) - Security layer is a bottleneck
3. **HTTP page load is VERY SLOW**: 14 RPM (4.245 seconds) - This is the main problem
4. **Overall responsiveness dominated by HTTP loaded**: 4.245 seconds out of 1.979 total (wait, that doesn't add up - need to investigate)
5. **Idle latency is good**: 1104 RPM shows the connection itself is healthy

**So what**:

- **Network transport is NOT the problem**: 2838 RPM transport layer shows network is fast
- **TLS/SSL performance is a bottleneck**: 121ms for security handshake is slow
- **HTTP page load is the main issue**: 14 RPM (4.245 seconds) is extremely slow
- **The problem is in the application/HTTP layer**, not the network stack
- **This suggests**:
  - TLS/SSL library performance issues
  - HTTP/2 implementation issues
  - Possible macOS Sequoia-specific TLS/HTTP performance regression
  - Browser/HTTP client performance differences

**Now what**:

- **Compare verbose output with wolf-air** to see if TLS/HTTP performance differs
- **Test with different protocols** (HTTP/1.1, HTTP/3/QUIC) using `-f` flag
- **Investigate TLS/SSL performance** - check for macOS Sequoia TLS regressions
- **Check HTTP/2 implementation** - see if forcing HTTP/1.1 or HTTP/3 improves performance
- **Compare TLS library versions** between systems
- **Test with L4S enabled** (`-f L4S`) to see if it helps
- **Investigate if this is a known macOS Sequoia issue** with TLS/HTTP performance

---

### 2025-12-24T14:12:34-0500 - CRITICAL FINDING: HTTP/2 Performance Issue Identified

**Machine**: michael-pro

**What**: Tested networkQuality with different HTTP protocols to isolate the performance issue.

**Protocol Comparison Results**:

| Protocol               | Responsiveness | RPM         | Latency       | Status          |
|------------------------|----------------|-------------|---------------|-----------------|
| **HTTP/2** (default)   | **Low**        | **30 RPM**  | 1.979 seconds | **POOR**        |
| **HTTP/1.1** (`-f h1`) | **Medium**     | **917 RPM** | 65.429 ms     | **30x BETTER!** |

**HTTP/1.1 Verbose Breakdown**:

- Overall: 917 RPM (65.429 ms) - **Medium** responsiveness
- Transport: 2742 RPM (21.875 ms) - Fast (similar to HTTP/2)
- Security: 653 RPM (91.875 ms) - Faster than HTTP/2 (495 RPM)
- HTTP: 1493 RPM (40.175 ms) - Faster than HTTP/2 (1575 RPM)
- **No "HTTP loaded" component** - test completes faster

**HTTP/3 (QUIC) Test**:

- Test failed or timed out (no results)

**Key Findings**:

1. **HTTP/2 is the problem**: 30 RPM vs 917 RPM with HTTP/1.1 = **30x difference**
2. **HTTP/1.1 works well**: 917 RPM is much closer to wolf-air's 1245 RPM (only 26% difference)
3. **Transport layer is fine**: Both protocols show ~2700 RPM transport (network is not the issue)
4. **HTTP/2 implementation issue**: The problem is specifically with HTTP/2 on macOS Sequoia
5. **This explains the poor responsiveness**: networkQuality defaults to HTTP/2, which performs poorly

**So what**:

- **ROOT CAUSE IDENTIFIED**: **HTTP/2 performance is broken on michael-pro (macOS Sequoia)**
- **HTTP/1.1 works fine**: 985 RPM is reasonable (vs 1245 RPM on wolf-air)
- **This is likely a macOS Sequoia HTTP/2 bug or regression**
- **The 18-30 RPM responsiveness is due to HTTP/2, not network issues**
- **Transport layer is healthy**: ~2700 RPM shows network itself is fine

**Comparison with wolf-air**:

- wolf-air: 1245 RPM (HTTP/2, assumed)
- michael-pro HTTP/1.1: 917 RPM (26% lower, but in same ballpark)
- michael-pro HTTP/2: 30 RPM (41x worse)

**Now what**:

- **Test wolf-air with HTTP/1.1** to confirm it also performs well
- **Investigate macOS Sequoia HTTP/2 issues** - check for known bugs or regressions
- **Check if HTTP/2 can be disabled** system-wide or per-application
- **Report this as a potential macOS Sequoia bug** if confirmed
- **Use HTTP/1.1 for networkQuality tests** to get accurate responsiveness measurements
- **Investigate why HTTP/2 performs so poorly** - is it a client or server issue?

---

### 2025-12-24T14:20:15-0500 - HTTP/2 Performance Breakdown and LuLu Firewall Investigation

**Machine**: michael-pro

**What**: Analyzed HTTP/2 vs HTTP/1.1 verbose output to identify the specific bottleneck, and discovered LuLu firewall is running.

**HTTP/2 Verbose Breakdown** (forced with `-f h2`):

- **Transport**: 2844 RPM (21ms) - **EXCELLENT** - network layer is fine
- **Security (TLS)**: 293 RPM (204ms) - **VERY SLOW** - TLS handshake bottleneck
- **HTTP**: 711 RPM (84ms) - Slow
- **HTTP loaded**: **6 RPM (8.7 seconds)** - **EXTREMELY SLOW** - This is the killer

**HTTP/1.1 Verbose Breakdown** (forced with `-f h1`):

- **Transport**: 2672 RPM (22ms) - **EXCELLENT** - similar to HTTP/2
- **Security (TLS)**: 663 RPM (90ms) - **FASTER** than HTTP/2 (293 RPM)
- **HTTP**: 1427 RPM (42ms) - **FASTER** than HTTP/2 (711 RPM)
- **No "HTTP loaded" component** - test completes without this delay

**Key Difference**:

- **HTTP/2 has "HTTP loaded" component taking 8.7 seconds** - this doesn't exist in HTTP/1.1
- This suggests HTTP/2 is waiting for something that HTTP/1.1 doesn't wait for
- Could be: server push, stream multiplexing, connection establishment, or firewall interference

**System Configuration**:

- **LuLu firewall detected**: Running (PID 1082, system extension active)
- **networkd preferences**: `enable_unified_http = 1`
- **No VPN active**
- **No system proxies configured**
- **curl HTTP/2 works fine**: ALPN negotiation successful, connections work

**So what**:

- **"HTTP loaded" is the problem**: 8.7 seconds in HTTP/2 vs not present in HTTP/1.1
- **LuLu firewall could be interfering**: Firewall might be inspecting/delaying HTTP/2 connections differently than HTTP/1.1
- **TLS handshake is also slow**: 204ms in HTTP/2 vs 90ms in HTTP/1.1 (2.3x slower)
- **curl HTTP/2 works**: Suggests the issue is specific to networkQuality's CFNetwork implementation, not system-wide HTTP/2
- **This is likely LuLu firewall + networkQuality interaction**: LuLu might be interfering with networkQuality's HTTP/2 connections

**Now what**:

- **Test with LuLu firewall temporarily disabled** to see if HTTP/2 performance improves
- **Check LuLu logs** for blocked/delayed connections during networkQuality tests
- **Compare LuLu configuration** - see if HTTP/2 connections are being handled differently
- **Test networkQuality with LuLu disabled** - if HTTP/2 improves, LuLu is the culprit
- **If LuLu is the issue**: Configure LuLu to allow networkQuality or HTTP/2 connections, or find LuLu alternative
- **Research LuLu + HTTP/2 issues** - check if this is a known problem

---

### 2025-12-24T14:28:53-0500 - Test with LuLu Main Process Killed (System Extension Still Active)

**Machine**: michael-pro

**What**: Killed LuLu main application process (PID 1082) and ran HTTP/2 networkQuality test. System extension (PID 327) remains active as it requires System Settings GUI or sudo to disable.

**LuLu Status**:

- **Main application**: Killed (no longer running)
- **System extension**: Still active (PID 327, requires System Settings to disable)

**HTTP/2 Test Results** (with LuLu app killed):

- **Overall Responsiveness**: Low (2.237 seconds | 26 RPM) - still poor
- **Transport**: 2764 RPM (21.705 ms) - **EXCELLENT** - network layer fine
- **Security (TLS)**: 503 RPM (119.136 ms) - Slow (improved from 293 RPM / 204ms)
- **HTTP**: 1533 RPM (39.114 ms) - OK (improved from 711 RPM / 84ms)
- **HTTP loaded**: **13 RPM (4.554 seconds)** - **VERY SLOW** (improved from 6 RPM / 8.7 seconds)

**Comparison with Previous HTTP/2 Test** (LuLu fully active):

| Component              | Previous (LuLu active) | Current (LuLu app killed) | Change          |
|------------------------|------------------------|---------------------------|-----------------|
| Overall Responsiveness | 30 RPM (1.979s)        | 26 RPM (2.237s)           | Slightly worse  |
| Transport              | 2844 RPM (21ms)        | 2764 RPM (21.7ms)         | Similar         |
| Security (TLS)         | 293 RPM (204ms)        | 503 RPM (119ms)           | **72% faster**  |
| HTTP                   | 711 RPM (84ms)         | 1533 RPM (39ms)           | **116% faster** |
| HTTP loaded            | 6 RPM (8.7s)           | 13 RPM (4.55s)            | **48% faster**  |

**Key Findings**:

1. **Partial improvement**: Killing LuLu main app improved TLS, HTTP, and HTTP loaded components
2. **HTTP loaded still very slow**: 4.554 seconds is still extremely slow (should be <100ms)
3. **Overall responsiveness still poor**: 26 RPM vs 917 RPM with HTTP/1.1 (35x worse)
4. **System extension still active**: The LuLu system extension (PID 327) is still running and may still be filtering traffic

**So what**:

- **LuLu main app was contributing to the problem**: Killing it improved performance in TLS, HTTP, and HTTP loaded components
- **System extension may still be interfering**: The LuLu system extension is still active and may be filtering HTTP/2 traffic
- **HTTP/2 performance still broken**: Even with LuLu app killed, HTTP/2 is 35x worse than HTTP/1.1
- **Need to fully disable LuLu**: Must disable the system extension via System Settings to get complete test

**Now what**:

- **Fully disable LuLu system extension** via System Settings → Network → Firewall (or LuLu app settings)
- **Re-run HTTP/2 test** with system extension disabled to see if performance improves further
- **If disabling system extension fixes HTTP/2**: Configure LuLu to allow networkQuality/HTTP/2 or find alternative firewall
- **If HTTP/2 still poor after disabling system extension**: Investigate other causes (macOS Sequoia HTTP/2 bugs, CFNetwork issues, etc.)

---

### 2025-12-24T14:32:00-0500 - Test with LuLu Disabled via App

**Machine**: michael-pro

**What**: Disabled LuLu firewall via the LuLu application and ran HTTP/2 networkQuality test.

**LuLu Status**:

- **Main application**: Running (PID 91810) but firewall disabled via app settings
- **System extension**: Still loaded (PID 327) but filtering disabled

**HTTP/2 Test Results** (with LuLu disabled):

- **Overall Responsiveness**: Low (1.970 seconds | 30 RPM) - still poor
- **Transport**: 2819 RPM (21.279 ms) - **EXCELLENT** - network layer fine
- **Security (TLS)**: 497 RPM (120.674 ms) - Slow
- **HTTP**: 1580 RPM (37.953 ms) - OK
- **HTTP loaded**: **14 RPM (4.080 seconds)** - **VERY SLOW** (improved from 8.7s with LuLu active)
- **Idle Latency**: **1265 RPM (47.411 ms)** - **SIGNIFICANTLY IMPROVED** (was 262 RPM / 228ms with LuLu active)

**Comparison Across All Three Tests**:

| Component              | LuLu Active         | LuLu App Killed     | LuLu Disabled       | Best Result             |
|------------------------|---------------------|---------------------|---------------------|-------------------------|
| Overall Responsiveness | 30 RPM (1.979s)     | 26 RPM (2.237s)     | 30 RPM (1.970s)     | 30 RPM                  |
| Transport              | 2844 RPM (21ms)     | 2764 RPM (21.7ms)   | 2819 RPM (21.3ms)   | Similar (all excellent) |
| Security (TLS)         | 293 RPM (204ms)     | 503 RPM (119ms)     | 497 RPM (121ms)     | **497 RPM** (disabled)  |
| HTTP                   | 711 RPM (84ms)      | 1533 RPM (39ms)     | 1580 RPM (38ms)     | **1580 RPM** (disabled) |
| HTTP loaded            | 6 RPM (8.7s)        | 13 RPM (4.55s)      | 14 RPM (4.08s)      | **14 RPM** (disabled)   |
| **Idle Latency**       | **262 RPM (228ms)** | **262 RPM (228ms)** | **1265 RPM (47ms)** | **1265 RPM** (disabled) |

**Key Findings**:

1. **LuLu was significantly impacting idle latency**: Disabling LuLu improved idle latency from 262 RPM (228ms) to 1265 RPM (47ms) - **4.8x improvement**
2. **HTTP loaded improved but still very slow**: Reduced from 8.7s to 4.08s (53% improvement), but still extremely slow
3. **Overall responsiveness still poor**: 30 RPM vs 917 RPM with HTTP/1.1 (30x worse)
4. **LuLu was NOT the root cause**: While disabling LuLu helped, HTTP/2 performance is still broken

**So what**:

- **LuLu was contributing to the problem**: Disabling it improved idle latency dramatically and reduced HTTP loaded delay
- **HTTP/2 performance still broken**: Even with LuLu disabled, HTTP/2 is 30x worse than HTTP/1.1 (30 RPM vs 917 RPM)
- **Root cause is NOT LuLu**: The HTTP/2 "HTTP loaded" component taking 4.08 seconds suggests a deeper issue:
  - macOS Sequoia HTTP/2 implementation bug
  - CFNetwork HTTP/2 handling issue
  - Server-side HTTP/2 behavior difference
  - Network stack configuration issue specific to HTTP/2

**Now what**:

- **Test wolf-air with HTTP/2** to confirm it performs well (1245 RPM was likely HTTP/2)
- **Compare HTTP/2 verbose output** between michael-pro and wolf-air to identify specific differences
- **Investigate macOS Sequoia HTTP/2 bugs** - check for known issues or regressions
- **Test with different HTTP/2 endpoints** to see if issue is server-specific
- **Consider using HTTP/1.1** for networkQuality tests on michael-pro until HTTP/2 issue is resolved
- **Report as potential macOS Sequoia bug** if confirmed

---

### 2025-12-24T14:34:28-0500 - Confirmation: HTTP/2 Still Broken, curl HTTP/2 Works Fine

**Machine**: michael-pro

**What**: Confirmed HTTP/2 performance issue persists and verified that curl HTTP/2 works fine, confirming the issue is specific to networkQuality's CFNetwork implementation.

**HTTP/2 Test Results** (LuLu disabled, different endpoint):

- **Overall Responsiveness**: Low (2.423 seconds | 24 RPM) - still poor
- **HTTP loaded**: 8 RPM (7.078 seconds) - still extremely slow (variability: 4.08s-7.08s)
- **curl HTTP/2 test**: **Works perfectly** - HTTP/2 200 response from apple.com

**Key Confirmation**:

1. **HTTP/2 itself works**: curl successfully uses HTTP/2, confirming the protocol stack is functional
2. **Issue is networkQuality/CFNetwork specific**: The problem is isolated to networkQuality's use of CFNetwork for HTTP/2
3. **HTTP loaded component is the killer**: Consistently takes 4-7 seconds, doesn't exist in HTTP/1.1
4. **LuLu was contributing but not root cause**: Even with LuLu disabled, HTTP/2 performance is 30x worse than HTTP/1.1

**So what**:

- **Root cause confirmed**: macOS Sequoia's CFNetwork HTTP/2 implementation has a bug affecting networkQuality
- **Workaround available**: Use `networkQuality -f h1` to get accurate responsiveness measurements (917 RPM)
- **Not a general HTTP/2 issue**: curl HTTP/2 works fine, so this is specific to CFNetwork's HTTP/2 handling
- **LuLu impact**: LuLu was making it worse (8.7s → 4.08s improvement), but core issue remains

**Now what**:

- **Use HTTP/1.1 for networkQuality tests** on michael-pro: `networkQuality -f h1 -v` gives accurate results (917 RPM)
- **Test wolf-air when SSH available** to compare HTTP/2 performance (macOS Monterey vs Sequoia)
- **Monitor for macOS updates** that might fix CFNetwork HTTP/2 issue
- **Consider reporting to Apple** if wolf-air (Monterey) shows good HTTP/2 performance, confirming Sequoia regression

---

### 2025-12-24T14:41:34-0500 - Deep Research: Is This a Widespread Bug?

**Machine**: michael-pro

**What**: Investigated whether this HTTP/2 performance issue is a widespread macOS/CFNetwork bug or specific to networkQuality tool.

**Key Clarifications**:

1. **HTTP/2 is NOT the most recent version**:
   - HTTP/3 (QUIC) is newer (released 2022)
   - HTTP/2 is still widely used (released 2015, standardized 2015)
   - HTTP/1.1 is older (1997, updated 2014)

2. **CFNetwork vs Other HTTP/2 Implementations**:
   - **CFNetwork**: Apple's networking framework used by many macOS/iOS apps (Safari, Mail, etc.)
   - **libcurl/nghttp2**: Used by curl (version 8.7.1 with nghttp2/1.64.0) - **works fine**
   - **networkQuality**: Uses NetworkQualityServices framework + Network framework, not directly CFNetwork

3. **System Log Analysis**:
   - CFNetwork logs show HTTP/2 tasks marked as **"failure"** even when `response_status=200` (successful)
   - Transaction durations: 30-44 seconds for HTTP/2 tasks
   - Many tasks show `response_duration_ms=0` despite successful responses
   - This suggests networkQuality may be timing out or canceling HTTP/2 tasks prematurely

4. **Scope of the Issue**:
   - **curl HTTP/2 works perfectly** - confirms HTTP/2 protocol stack is functional
   - **Issue is specific to networkQuality tool**, not general HTTP/2
   - **Other apps using CFNetwork** (Safari, Mail, etc.) may or may not be affected - not tested

**Why This Might NOT Be Widely Reported**:

1. **networkQuality is a diagnostic tool**, not used by most users:
   - Most users don't run `networkQuality` directly
   - They experience network through apps (Safari, Mail, etc.)
   - If Safari/Mail HTTP/2 works fine, users wouldn't notice

2. **The "HTTP loaded" component may be test-specific**:
   - networkQuality's test methodology may wait for specific HTTP/2 features
   - Real-world apps may not trigger the same code path
   - The 4-7 second delay might only affect networkQuality's test, not actual browsing

3. **HTTP/1.1 fallback works**:
   - If CFNetwork HTTP/2 has issues, apps may silently fall back to HTTP/1.1
   - Users wouldn't notice unless they specifically test HTTP/2

4. **This could be a networkQuality bug, not CFNetwork**:
   - networkQuality uses NetworkQualityServices framework
   - The "HTTP loaded" delay might be a bug in networkQuality's test implementation
   - CFNetwork itself may work fine for real-world usage

**Evidence This Is Tool-Specific, Not System-Wide**:

- curl HTTP/2 works fine (uses libcurl/nghttp2, not CFNetwork)
- Other CFNetwork-based apps (Safari, Mail) not tested - may work fine
- networkQuality logs show tasks marked "failure" even when successful (suggests test methodology issue)
- HTTP/1.1 works perfectly in networkQuality (917 RPM)

**So what**:

- **This is likely a networkQuality tool bug**, not a widespread macOS/CFNetwork HTTP/2 bug
- **If it were a system-wide CFNetwork HTTP/2 bug**, we'd expect:
  - Safari/Mail to be slow
  - Widespread complaints on forums/Reddit
  - Apple to have fixed it already
- **The "HTTP loaded" component** taking 4-7 seconds is likely networkQuality's test waiting for something that real apps don't wait for
- **CFNetwork HTTP/2 may work fine** for actual application usage, just not for networkQuality's specific test

**Now what**:

- **Test Safari/Mail HTTP/2 performance** to see if real-world apps are affected
- **Search Apple Developer Forums** for networkQuality HTTP/2 issues
- **Check if this is a known networkQuality bug** (tool-specific, not system-wide)
- **Report to Apple as networkQuality bug** if confirmed (not CFNetwork bug)
- **Use HTTP/1.1 for networkQuality tests** until fixed: `networkQuality -f h1 -v`

---

### 2025-12-24T14:46:52-0500 - networkQuality Ownership and Bug Reporting

**Machine**: michael-pro

**What**: Investigated who owns networkQuality tool and how to submit bug reports.

**Ownership**:

- **Owner**: Apple Inc.
- **Location**: `/usr/bin/networkQuality` (system binary)
- **Framework**: Uses `NetworkQualityServices.framework` (private Apple framework)
- **Bundle ID**: `com.apple.networkQuality`
- **Part of**: Darwin/macOS system tools
- **Man page**: References Apple support documentation (<https://support.apple.com/kb/HT212313>)

**Bug Reporting Options**:

1. **Feedback Assistant** (macOS built-in):
   - Location: `/System/Library/CoreServices/Applications/Feedback Assistant.app`
   - Launch: `open -a "Feedback Assistant"` or search Spotlight for "Feedback Assistant"
   - Requires Apple ID login
   - Can attach system diagnostics and logs
   - Best for: General macOS/system tool bugs

2. **Apple Developer Bug Reporting**:
   - URL: <https://developer.apple.com/bug-reporting/>
   - Requires Apple Developer account (free or paid)
   - Best for: Developer-focused issues, framework bugs
   - Can file bugs against specific frameworks/components

3. **Apple Feedback** (Public):
   - URL: <https://www.apple.com/feedback/>
   - General feedback form
   - Less structured than Feedback Assistant
   - Best for: User-facing issues

4. **Apple Support Documentation**:
   - networkQuality man page references: <https://support.apple.com/kb/HT212313>
   - May contain reporting instructions or known issues

**Recommended Approach**:

1. **Use Feedback Assistant** (most appropriate for system tool bugs):
   - Launch: `open -a "Feedback Assistant"`
   - Category: "macOS" → "System Tools" or "Networking"
   - Include:
     - Description of HTTP/2 performance issue
     - Comparison: HTTP/1.1 (917 RPM) vs HTTP/2 (30 RPM)
     - System logs showing CFNetwork HTTP/2 task failures
     - macOS version: 15.7.3 (Sequoia)
     - Workaround: Use `-f h1` flag

2. **Attach Diagnostic Information**:
   - System logs: `log show --predicate 'subsystem == "com.apple.CFNetwork"' --last 2h`
   - networkQuality verbose output: `networkQuality -f h2 -v`
   - Comparison output: `networkQuality -f h1 -v`

**So what**:

- **networkQuality is an Apple system tool** - owned and maintained by Apple
- **Feedback Assistant is the primary bug reporting mechanism** for macOS system tools
- **Can also use Apple Developer Bug Reporting** if you have a developer account
- **Should report this as a networkQuality tool bug**, not a general CFNetwork bug

**Now what**:

- **Prepare bug report** with:
  - Clear description of HTTP/2 performance issue
  - Comparison data (HTTP/1.1 vs HTTP/2)
  - System logs showing the issue
  - Workaround (use `-f h1` flag)
- **Submit via Feedback Assistant** with appropriate category and diagnostics
- **Consider also posting** to Apple Developer Forums to see if others have encountered this

---

### 2025-12-24T15:44:28-0500 - Updated RPM Measurements

**Machine**: michael-pro and wolf-air

**What**: Ran networkQuality tests on both machines to update recent RPM measurements.

**michael-pro HTTP/2 Test Results**:

- Uplink capacity: 8.995 Mbps
- Downlink capacity: 4.438 Mbps
- Responsiveness: Low (2.675 seconds | **22 RPM**)
- Idle Latency: 73.958 milliseconds | 811 RPM
- HTTP loaded: 9 RPM (6.089 seconds) - still very slow
- Transport: 2760 RPM (21.738 ms) - excellent
- Security: 470 RPM (127.548 ms) - slow TLS
- HTTP: 1603 RPM (37.429 ms) - OK

**michael-pro HTTP/1.1 Test Results**:

- Uplink capacity: 15.155 Mbps
- Downlink capacity: 4.443 Mbps
- Responsiveness: Medium (65.778 milliseconds | **912 RPM**)
- Idle Latency: 44.958 milliseconds | 1334 RPM
- Transport: 2487 RPM (24.122 ms) - excellent
- Security: 476 RPM (125.902 ms) - slow TLS
- HTTP: 1262 RPM (47.537 ms) - OK
- **No "HTTP loaded" component** - test completes without this delay

**wolf-air Test Results** (macOS 12.7.6, no `-f` flag support):

- Upload capacity: 2.799 Mbps
- Download capacity: 3.446 Mbps
- Responsiveness: High (**1180 RPM**)
- Base RTT: 24 ms
- Protocol: Likely HTTP/2 (default for networkQuality)

**So what**:

- **HTTP/2 performance still broken on michael-pro**: 22 RPM vs 912 RPM with HTTP/1.1 (**41x worse**)
- **HTTP/1.1 performance stable**: 912 RPM (similar to previous 917 RPM measurement)
- **wolf-air performance excellent**: 1180 RPM (slightly lower than previous 1245 RPM, but still excellent)
- **HTTP loaded component persists**: Still taking 6.089 seconds in HTTP/2, confirming the issue
- **Gap between machines**: michael-pro HTTP/2 (22 RPM) vs wolf-air (1180 RPM) = **54x difference**
- **HTTP/1.1 brings michael-pro closer**: 912 RPM vs wolf-air 1180 RPM = only **23% difference** (much better than 54x)

**Now what**:

- **Continue using HTTP/1.1 for networkQuality tests** on michael-pro: `networkQuality -f h1 -v` gives accurate results (912 RPM)
- **Monitor for macOS updates** that might fix CFNetwork HTTP/2 issue
- **Consider reporting to Apple** if HTTP/2 performance doesn't improve in future macOS updates

---

### 2025-12-24T15:45:00-0500 - curl Validation: HTTP/2 Works Fine, Issue is Tool-Specific

**Machine**: michael-pro and wolf-air

**What**: Validated networkQuality measurements using curl with timing to test HTTP/1.1 vs HTTP/2 performance on both machines.

**Test Methodology**:

- Used `curl` with `-w` flag to measure timing breakdown
- Tested both HTTP/1.1 (`--http1.1`) and HTTP/2 (`--http2`)
- Ran 5 requests per protocol per machine to <www.apple.com>
- Measured: DNS lookup, Connect, SSL handshake, Time to First Byte (TTFB), Total time, Speed

**michael-pro HTTP/1.1 Results** (5 tests):

- Total time: 0.565s, 0.718s, 0.877s, 0.918s, 0.808s
- **Average: 0.777 seconds**
- TTFB: 0.161s, 0.122s, 0.187s, 0.156s, 0.128s (avg 0.151s)
- Speed: 482-337 KB/s (avg ~361 KB/s)
- All successful (HTTP 200)

**michael-pro HTTP/2 Results** (5 tests):

- Total time: 0.505s, 0.534s, **5.934s**, 1.255s, 0.526s
- **Average: 1.751 seconds** (with outlier), **0.705 seconds** (without outlier)
- TTFB: 0.105s, 0.129s, 0.096s, 0.599s, 0.119s (avg 0.210s)
- Speed: 539-46 KB/s (variable due to outlier)
- All successful (HTTP 200)
- **Note**: One outlier at 5.9s (similar to networkQuality's "HTTP loaded" delay)

**wolf-air HTTP/1.1 Results** (5 tests):

- Total time: 0.539s, 0.518s, 0.502s, 0.589s, 0.506s
- **Average: 0.531 seconds**
- TTFB: 0.150s, 0.121s, 0.108s, 0.198s, 0.115s (avg 0.138s)
- Speed: 505-463 KB/s (avg ~515 KB/s)
- All successful (HTTP 200)

**wolf-air HTTP/2 Results** (5 tests):

- Total time: 1.323s, 0.552s, 0.775s, 0.883s, 0.844s
- **Average: 0.875 seconds**
- TTFB: 0.464s, 0.119s, 0.114s, 0.114s, 0.121s (avg 0.186s)
- Speed: 206-494 KB/s (avg ~336 KB/s)
- All successful (HTTP 200)

**Key Findings**:

1. **HTTP/2 works fine with curl on both machines**: Both michael-pro and wolf-air successfully use HTTP/2 with curl (libcurl/nghttp2), confirming HTTP/2 protocol stack is functional

2. **michael-pro HTTP/2 performance is acceptable with curl**: Average 0.705s (excluding outlier) vs HTTP/1.1 average 0.777s - **HTTP/2 is actually slightly faster**

3. **One HTTP/2 outlier on michael-pro**: One request took 5.9s (similar to networkQuality's "HTTP loaded" delay), but this is intermittent, not consistent

4. **wolf-air HTTP/2 performs well**: Average 0.875s vs HTTP/1.1 average 0.531s - slightly slower but still acceptable

5. **The problem is tool-specific, not network-wide**:
   - curl HTTP/2 works fine (0.7s average on michael-pro)
   - networkQuality HTTP/2 is broken (22 RPM = 2.675s average, with 6s "HTTP loaded" delay)
   - This confirms the issue is with **networkQuality's CFNetwork HTTP/2 implementation**, not the network or HTTP/2 protocol itself

6. **Validation of networkQuality HTTP/1.1**:
   - networkQuality HTTP/1.1: 912 RPM (65.8ms = 0.066s)
   - curl HTTP/1.1: 0.777s average
   - Different test methodologies (networkQuality does multiple requests, curl is single request), but both show HTTP/1.1 works well

**So what**:

- **HTTP/2 protocol is NOT broken**: curl successfully uses HTTP/2 on both machines with good performance
- **networkQuality's CFNetwork HTTP/2 implementation has a bug**: The tool-specific "HTTP loaded" delay (4-7 seconds) doesn't occur with curl
- **The issue is isolated to networkQuality**: Real-world applications using HTTP/2 (via curl/libcurl) work fine
- **networkQuality HTTP/1.1 is accurate**: 912 RPM (65.8ms) is reasonable and validates the tool works correctly with HTTP/1.1

**Now what**:

- **Continue using HTTP/1.1 for networkQuality tests**: `networkQuality -f h1 -v` provides accurate measurements
- **HTTP/2 is fine for real applications**: curl and other libcurl-based tools work correctly with HTTP/2
- **Report as networkQuality tool bug**: The issue is specific to networkQuality's CFNetwork HTTP/2 test implementation, not a system-wide problem
- **Monitor for networkQuality updates**: Apple may fix the CFNetwork HTTP/2 issue in future macOS updates

---

### 2025-12-24T16:08:18-0500 - Tool Migration: Switching from networkQuality to speedtest (Ookla)

**Machine**: michael-pro and wolf-air

**What**: Logging final networkQuality values and switching to speedtest (Ookla Speedtest CLI) - the industry-standard tool used by network engineers.

**Reason for Switch**:

- networkQuality has HTTP/2 bugs on macOS Sequoia (22 RPM vs 912 RPM with HTTP/1.1)
- networkQuality is Apple-specific and not widely used by network engineers
- speedtest (Ookla) is the industry standard, reliable, and works consistently
- speedtest provides comprehensive metrics: download, upload, latency, jitter, packet loss

**Final networkQuality Values** (Tool: `networkQuality`):

**michael-pro** (macOS 15.7.3, WiFi - en0):

- **HTTP/2 Test** (2025-12-24T15:42:13-0500):
  - Upload: 8.995 Mbps
  - Download: 4.438 Mbps
  - Responsiveness: 22 RPM (Low)
  - Idle Latency: 73.958 ms (811 RPM)
- **HTTP/1.1 Test** (2025-12-24T15:43:03-0500):
  - Upload: 15.155 Mbps
  - Download: 4.443 Mbps
  - Responsiveness: 912 RPM (Medium)
  - Idle Latency: 44.958 ms (1334 RPM)

**wolf-air** (macOS 12.7.6, WiFi):

- **Test** (2025-12-24T15:44:02-0500):
  - Upload: 2.799 Mbps
  - Download: 3.446 Mbps
  - Responsiveness: 1180 RPM (High)
  - Base RTT: 24 ms

**Initial speedtest Values** (Tool: `speedtest` - Ookla Speedtest CLI v1.2.0.84):

**michael-pro** (2025-12-24T21:09:11Z):

- **Download**: 5.51 Mbps
- **Upload**: 4.50 Mbps
- **Latency**: 15.56 ms
- **Jitter**: 1.84 ms
- **Packet Loss**: 0%
- **Server**: Spectrum, Tampa, FL (tampfl-speedtest-ookla-01.st.charter.com)
- **ISP**: Spectrum
- **Interface**: en0 (WiFi), IP: 192.168.8.124

**wolf-air**:

- speedtest not yet installed (needs installation)

**Comparison: networkQuality vs speedtest (michael-pro)**:

| Metric   | networkQuality (HTTP/1.1) | speedtest | Difference                   |
|----------|---------------------------|-----------|------------------------------|
| Download | 4.443 Mbps                | 5.51 Mbps | +24% (speedtest higher)      |
| Upload   | 15.155 Mbps               | 4.50 Mbps | -70% (networkQuality higher) |
| Latency  | 44.958 ms (idle)          | 15.56 ms  | -65% (speedtest lower)       |

**So what**:

- **Download speeds are similar**: 4.44 Mbps (networkQuality) vs 5.51 Mbps (speedtest) - within reasonable variance
- **Upload discrepancy**: networkQuality shows 15.155 Mbps vs speedtest 4.50 Mbps - significant difference, needs investigation
- **Latency much better with speedtest**: 15.56 ms vs 44.96 ms idle latency - speedtest shows better network performance
- **speedtest provides more metrics**: Includes jitter and packet loss, which networkQuality doesn't report clearly
- **Tool migration complete**: Moving forward, all bandwidth/latency measurements will use speedtest

**Now what**:

- **Install speedtest on wolf-air**: `brew install speedtest` (or equivalent)
- **Run speedtest on wolf-air** to get baseline measurements
- **Use speedtest for all future measurements** - discontinue use of networkQuality
- **Investigate upload discrepancy** - why networkQuality shows 15 Mbps upload vs speedtest 4.5 Mbps
- **Update Current Test Results section** to use speedtest values going forward

---

### 2025-12-24T17:43:13-0500 - Final Tool Migration: curl-based network_test.sh

**Machine**: michael-pro and wolf-air

**What**: Migrated from speedtest to `network_test.sh` (curl-based script) due to installation difficulties on wolf-air.

**Reason for Final Migration**:

- speedtest installation was painful on wolf-air (different macOS version)
- curl is built-in on all macOS versions (no installation needed)
- network_test.sh script provides both bandwidth and RPM measurements
- Simple, reliable, works via SSH without dependencies
- Avoids HTTP/2 bugs in networkQuality
- Avoids installation issues with speedtest

**Tool Details**:

- **Script**: `bin/network_test.sh`
- **Underlying Tool**: `curl` (built-in, macOS 12+)
- **Tests**:
  - Download bandwidth: Downloads 10MB file from Cloudflare CDN
  - Upload bandwidth: Uploads 1MB test data
  - Responsiveness (RPM): 10 HTTP requests to <www.apple.com>, calculates average and RPM

**Initial network_test.sh Results**:

**michael-pro** (2025-12-24T17:43:13-0500):

- **Download**: 2.59 Mbps
- **Upload**: ~7.5 Mbps (983632 bytes/sec)
- **Responsiveness (RPM)**: 68
- **Average Response Time**: 0.875s
- **Tool**: curl via network_test.sh

**wolf-air**:

- Test pending - script ready to run via SSH

**Comparison with Previous Tools**:

| Tool                      | Download (michael-pro) | Upload (michael-pro) | RPM (michael-pro) | Installation          |
|---------------------------|------------------------|----------------------|-------------------|-----------------------|
| networkQuality (HTTP/1.1) | 4.443 Mbps             | 15.155 Mbps          | 912               | Built-in              |
| speedtest                 | 5.51 Mbps              | 4.50 Mbps            | N/A               | Requires brew install |
| network_test.sh (curl)    | 2.59 Mbps              | ~7.5 Mbps            | 68                | Built-in (curl)       |

**So what**:

- **curl-based approach is simplest**: No installation, works on all macOS versions
- **Download speeds vary**: Different tools/test endpoints show different results (2.59-5.51 Mbps)
- **RPM measurement differs**: networkQuality shows 912 RPM vs curl shows 68 RPM - different methodologies
- **Tool is ready for both machines**: Script can be run via SSH without installation
- **Final tool choice**: network_test.sh (curl) - simple, reliable, no dependencies

**Now what**:

- **Run network_test.sh on wolf-air** via SSH to get baseline measurements
- **Use network_test.sh for all future measurements** - discontinue networkQuality and speedtest
- **Document RPM methodology differences** - networkQuality vs curl measure different things
- **Update all future test results** to use network_test.sh values

---

### 2025-12-24T17:47:27-0500 - wolf-air Measurements and Upload/Download Anomaly Analysis

**Machine**: michael-pro and wolf-air

**What**: Ran network_test.sh on wolf-air and compared results with michael-pro. Identified unusual pattern where download speeds are fractions of upload speeds (opposite of typical broadband).

**wolf-air network_test.sh Results** (2025-12-24T17:46:25-0500):

- **Download**: 2.84 Mbps
- **Upload**: 7.03 Mbps (879143 bytes/sec)
- **Responsiveness (RPM)**: 60
- **Average Response Time**: 0.997s
- **Tool**: curl via network_test.sh

**michael-pro network_test.sh Results** (2025-12-24T17:43:13-0500):

- **Download**: 2.59 Mbps
- **Upload**: ~7.5 Mbps (983632 bytes/sec)
- **Responsiveness (RPM)**: 68
- **Average Response Time**: 0.875s
- **Tool**: curl via network_test.sh

**Comparison: michael-pro vs wolf-air**:

| Metric                    | michael-pro | wolf-air  | Difference                  |
|---------------------------|-------------|-----------|-----------------------------|
| **Download**              | 2.59 Mbps   | 2.84 Mbps | +9.7% (wolf-air higher)     |
| **Upload**                | ~7.5 Mbps   | 7.03 Mbps | -6.3% (michael-pro higher)  |
| **Upload/Download Ratio** | 2.9:1       | 2.5:1     | Both show upload > download |
| **RPM**                   | 68          | 60        | +13% (michael-pro higher)   |
| **Response Time**         | 0.875s      | 0.997s    | -12% (michael-pro faster)   |

**CRITICAL FINDING: Download is Fractions of Upload (Unusual Pattern)**:

Both machines show **upload speeds 2.5-3x HIGHER than download speeds**, which is the **opposite** of typical broadband connections where download is usually 5-20x higher than upload.

**Possible Explanations**:

1. **ISP Throttling/Prioritization**:
   - ISP may be throttling download bandwidth during peak hours or based on usage patterns
   - Upload path may have less congestion or different QoS policies
   - Could be intentional ISP policy (unlikely but possible)

2. **Router/Network Configuration**:
   - Router QoS settings may prioritize upload traffic
   - Bandwidth limiting rules may be misconfigured
   - Router firmware bugs affecting download path

3. **WiFi Interference/Channel Congestion**:
   - Download path may be experiencing more interference
   - WiFi channel congestion affecting download more than upload
   - Neighboring networks causing interference on download frequencies

4. **Test Methodology Limitations**:
   - Cloudflare CDN endpoint may have rate limiting or geographic routing issues
   - Download test (10MB file) may hit different bottlenecks than upload test (1MB)
   - Different test endpoints may have different capacity

5. **Network Stack/TCP Issues**:
   - TCP receive window scaling issues affecting download
   - Download path buffer bloat or queuing delays
   - Network interface driver issues affecting download performance

6. **ISP Connection Type**:
   - If using LTE/cellular backup, upload may be prioritized
   - Satellite or fixed wireless may have asymmetric characteristics
   - Cable modem issues affecting download more than upload

7. **Time-of-Day/Network Congestion**:
   - Tests run during peak hours when download is more congested
   - ISP network capacity issues affecting download path
   - Regional network congestion

**Evidence Supporting Each Theory**:

- **ISP Throttling**: Both machines show same pattern (2.5-3x upload advantage) - suggests network-wide issue
- **Router Configuration**: Both use same router (GL-MT1300) - router could be the common factor
- **WiFi Issues**: Both on WiFi - interference could affect both similarly
- **Test Methodology**: Different file sizes and endpoints - could explain some variance
- **Network Stack**: Different macOS versions (15.7.3 vs 12.7.6) but similar results - less likely

**Most Likely Causes** (in order):

1. **Router QoS/Bandwidth Limiting**: GL-MT1300 router may have misconfigured QoS or bandwidth limits affecting download
2. **ISP Throttling**: ISP may be throttling download bandwidth (common during peak hours or high usage)
3. **WiFi Channel Congestion**: Download path experiencing more interference/congestion than upload
4. **Test Endpoint Limitations**: Cloudflare CDN may have rate limiting or routing issues affecting download tests

**So what**:

- **Both machines show same unusual pattern**: Upload 2.5-3x faster than download
- **This is NOT normal**: Typical broadband has download 5-20x faster than upload
- **Pattern is consistent**: Both machines, multiple tests show same ratio
- **Suggests network-wide issue**: Router or ISP-level problem, not machine-specific
- **Download speeds are very low**: 2.5-3 Mbps download is quite slow for modern broadband

**Now what**:

- **Check router QoS/bandwidth settings**: Review GL-MT1300 router configuration for download throttling
- **Test with different endpoints**: Try other CDNs or test servers to rule out Cloudflare-specific issues
- **Test at different times**: Run tests at off-peak hours to check for ISP throttling
- **Check router firmware**: Update or review GL-MT1300 firmware for known issues
- **Test with Ethernet**: If possible, test michael-pro on Ethernet to rule out WiFi-specific issues
- **Contact ISP**: If router checks out, contact ISP about download throttling or capacity issues
- **Compare with other devices**: Test from other devices on same network to confirm pattern
- **Monitor over time**: Track download/upload ratios over days/weeks to identify patterns

---

### 2025-12-24T18:04:45-0500 - ROOT CAUSE IDENTIFIED: Router QoS Configuration

**Machine**: Router (GL-MT1300)

**What**: Discovered router QoS bandwidth limits that explain the upload/download anomaly.

**Router QoS Settings** (GL-MT1300):

- **Download Limit**: 6000 kbps (6 Mbps)
- **Upload Limit**: 8000 kbps (8 Mbps)
- **QoS Discipline**: CAKE (Common Applications Kept Enhanced)

**Analysis**:

The router has bandwidth limits configured where **upload limit (8 Mbps) is HIGHER than download limit (6 Mbps)**. This is unusual - typical configurations have download limits 5-20x higher than upload.

**Measured vs Configured Limits**:

| Direction    | Configured Limit | Measured Speed | Utilization      |
|--------------|------------------|----------------|------------------|
| **Download** | 6 Mbps           | 2.5-2.8 Mbps   | ~42-47% of limit |
| **Upload**   | 8 Mbps           | 7.0-7.5 Mbps   | ~88-94% of limit |

**Key Findings**:

1. **Upload is hitting the limit**: Measured upload (7-7.5 Mbps) is close to the configured limit (8 Mbps), suggesting the limit is active
2. **Download is well below limit**: Measured download (2.5-2.8 Mbps) is only ~42-47% of the configured limit (6 Mbps), suggesting other factors are limiting download
3. **CAKE QoS discipline**: CAKE is a modern, sophisticated QoS algorithm that manages bandwidth fairly - the limits are being enforced
4. **Configuration is backwards**: Upload limit (8 Mbps) > Download limit (6 Mbps) is opposite of typical broadband

**Why Download is Below Limit**:

Even though the router allows 6 Mbps download, we're only getting 2.5-2.8 Mbps. Possible reasons:

- ISP may be providing less than 6 Mbps actual capacity
- WiFi interference/congestion reducing effective download speed
- Other network bottlenecks between router and internet
- CAKE QoS may be prioritizing upload traffic, leaving less for download

**So what**:

- **Root cause confirmed**: Router QoS settings explain why upload > download
- **Configuration is unusual**: Upload limit higher than download is atypical
- **Download underperforming**: Getting only 42-47% of configured download limit suggests other bottlenecks
- **Upload performing well**: Getting 88-94% of configured upload limit

**Recommendations**:

1. **Adjust Router QoS Settings** (if download capacity is available):
   - **Recommended**: Set download limit to 2-3x upload limit (typical broadband ratio)
   - Example: Download 20-24 Mbps, Upload 8 Mbps (if ISP provides this capacity)
   - Or: Download 12 Mbps, Upload 8 Mbps (if ISP provides ~12 Mbps)
   - **Check ISP plan first**: Verify actual download capacity before increasing limits

2. **Investigate Why Download is Below Limit**:
   - Test download speed directly connected to router (bypass WiFi) to rule out WiFi issues
   - Check ISP plan - may only provide 3-4 Mbps download despite router allowing 6 Mbps
   - Test at different times to check for ISP throttling
   - Check router logs for download path errors or drops

3. **Optimize CAKE QoS Settings**:
   - Review CAKE configuration - may need adjustment for your use case
   - Consider if CAKE is prioritizing upload too aggressively
   - Check if CAKE "ingress" (download) vs "egress" (upload) settings need tuning

4. **Verify ISP Capacity**:
   - Contact ISP to confirm actual download/upload capacity
   - If ISP provides more than 6 Mbps download, increase router limit accordingly
   - If ISP only provides 3 Mbps download, router limit of 6 Mbps is fine (other factors limiting)

5. **Test After Changes**:
   - After adjusting QoS limits, re-run network_test.sh on both machines
   - Verify download speeds improve if limits were too restrictive
   - Monitor for any negative impacts on upload performance

**Suggested Configuration** (assuming ISP provides adequate capacity):

- **Download**: 20-24 Mbps (or match ISP plan, typically 3-4x upload)
- **Upload**: 8 Mbps (keep current if working well)
- **Discipline**: CAKE (keep - it's a good choice)
- **Rationale**: Typical broadband has download 3-5x upload. If ISP provides 20+ Mbps download, set limit accordingly.

**Now what**:

- **Check ISP plan capacity**: Verify what download speed ISP actually provides
- **Adjust router QoS limits**: Set download limit to 2-3x upload limit (if ISP capacity allows)
- **Re-test after changes**: Run network_test.sh to verify improvements
- **Monitor performance**: Track speeds over time to ensure stable performance
