# iperf3 Guide for Real-World Network Diagnosis

## Why iperf3 Instead of speedtest?

**speedtest problems**:

- Reports raw Mbps but doesn't tell you if it's good for Zoom/web/movies
- Tests internet, not local network path
- Doesn't measure latency under load (the real problem)
- Can show "great" speeds but still have sluggish UX

**iperf3 advantages**:

- Tests actual network path (machine-to-machine or to server)
- Can measure latency under load (similar to responsiveness/RPM)
- Shows jitter, packet loss, and retransmissions
- Industry standard, reliable results

---

## Quick Start: Testing Between michael-pro and wolf-air

### Step 1: Start Server on wolf-air

```bash
# SSH to wolf-air and run:
iperf3 -s -p 5201
```

**What this does**: Starts iperf3 server listening on port 5201, waiting for connections.

### Step 2: Run Client Test on michael-pro

```bash
# On michael-pro, test download (server → client)
iperf3 -c wolf-air.local -p 5201 -t 30 -i 1 -w 1M

# Test upload (client → server)
iperf3 -c wolf-air.local -p 5201 -t 30 -i 1 -w 1M -R

# Test bidirectional (both directions simultaneously)
iperf3 -c wolf-air.local -p 5201 -t 30 -i 1 -w 1M --bidir
```

**Parameters explained**:

- `-c wolf-air.local`: Connect to wolf-air
- `-p 5201`: Use port 5201
- `-t 30`: Run for 30 seconds
- `-i 1`: Report every 1 second
- `-w 1M`: Window size 1MB (helps with latency measurement)
- `-R`: Reverse direction (server sends to client)
- `--bidir`: Test both directions at once

---

## Understanding iperf3 Output for Real-World Use

### Basic Output Example

```text
Connecting to host wolf-air.local, port 5201
[  5] local 192.168.8.100 port 54321 connected to 192.168.8.101 port 5201
[ ID] Interval           Transfer     Bitrate         Retr  Cwnd
[  5]   0.00-1.00   sec  1.20 MBytes  10.1 Mbits/sec    0    1.41 MBytes
[  5]   1.00-2.00   sec  1.15 MBytes  9.65 Mbits/sec    0    1.41 MBytes
[  5]   2.00-3.00   sec  1.18 MBytes  9.90 Mbits/sec    0    1.41 MBytes
[  5]   3.00-4.00   sec  1.22 MBytes  10.2 Mbits/sec    0    1.41 MBytes
[  5]   4.00-5.00   sec  1.19 MBytes  10.0 Mbits/sec    0    1.41 MBytes
[  5]   0.00-5.00   sec  5.94 MBytes  9.97 Mbits/sec    0

[ ID] Interval           Transfer     Bitrate         Retr
[  5]   0.00-5.00   sec  5.94 MBytes  9.97 Mbits/sec    0    sender
[  5]   0.00-5.00   sec  5.94 MBytes  9.97 Mbits/sec    0    receiver
```

**Key metrics**:

- **Transfer**: Data transferred in this interval
- **Bitrate**: Speed (Mbits/sec) - similar to speedtest
- **Retr**: Retransmissions (packet loss indicator)
- **Cwnd**: Congestion window (TCP flow control)

### What to Look For

**Good signs**:

- Consistent bitrate (not jumping around)
- Retr = 0 (no retransmissions = no packet loss)
- Stable Cwnd (congestion window stable)

**Bad signs**:

- Retr > 0 (packet loss = retransmissions)
- Highly variable bitrate (jitter in throughput)
- Cwnd shrinking (congestion detected)

---

## Measuring Latency Under Load (The Real Problem)

This is what speedtest misses - **latency when the network is busy**.

### Test with Latency Reporting

```bash
# Server side (wolf-air)
iperf3 -s -p 5201

# Client side (michael-pro) - with latency measurement
iperf3 -c wolf-air.local -p 5201 -t 30 -i 1 -w 1M --logfile iperf3_results.txt
```

### Better: Use UDP for Latency Testing

UDP shows jitter and packet loss more clearly:

```bash
# Server
iperf3 -s -p 5201

# Client - UDP test with latency reporting
iperf3 -c wolf-air.local -p 5201 -u -b 10M -t 30 -i 1 -w 1M
```

**UDP output includes**:

- **Jitter**: Variation in latency (critical for Zoom)
- **Lost/Total**: Packet loss percentage
- **Latency**: Round-trip time

**Example UDP output**:

```text
[ ID] Interval           Transfer     Bitrate         Jitter    Lost/Total Datagrams
[  5]   0.00-1.00   sec  1.19 MBytes  10.0 Mbits/sec  0.123 ms  0/1521 (0%)
[  5]   1.00-2.00   sec  1.19 MBytes  10.0 Mbits/sec  0.145 ms  0/1521 (0%)
[  5]   2.00-3.00   sec  1.19 MBytes  10.0 Mbits/sec  0.167 ms  0/1521 (0%)
```

**Key metrics**:

- **Jitter**: Should be < 10ms for good Zoom calls
- **Lost/Total**: Should be 0% (or very close)
- **Bitrate**: Consistent = good

---

## Interpreting Results for Real-World Use Cases

### For Web Browsing

**What matters**:

- **Latency**: < 50ms = excellent, < 100ms = good, > 200ms = sluggish
- **Packet loss**: < 0.1% = good, > 1% = problematic
- **Throughput**: > 5 Mbps = fine for most web

**Test command**:

```bash
iperf3 -c wolf-air.local -p 5201 -t 10 -i 1 -w 1M
```

**Good web browsing**:

- Consistent bitrate
- Retr = 0
- No large latency spikes

### For Zoom/Video Calls

**What matters**:

- **Jitter**: < 10ms = excellent, < 30ms = acceptable, > 50ms = choppy
- **Packet loss**: < 0.1% = good, > 0.5% = audio/video issues
- **Latency**: < 100ms = good, > 200ms = noticeable delay
- **Throughput**: > 1 Mbps upload/download = sufficient

**Test command**:

```bash
# UDP test (more realistic for video)
iperf3 -c wolf-air.local -p 5201 -u -b 2M -t 30 -i 1
```

**Good Zoom performance**:

- Jitter < 30ms
- Packet loss < 0.5%
- Consistent bitrate

### For Streaming (Netflix, YouTube)

**What matters**:

- **Throughput**: > 5 Mbps = HD, > 25 Mbps = 4K
- **Consistency**: Stable bitrate (no buffering)
- **Packet loss**: < 0.1% = smooth playback

**Test command**:

```bash
iperf3 -c wolf-air.local -p 5201 -t 60 -i 1 -w 2M
```

**Good streaming**:

- Sustained high bitrate (> 5 Mbps)
- Retr = 0 or very low
- No large drops in throughput

---

## Advanced: Measuring Responsiveness (Like networkQuality RPM)

### TCP Latency Under Load Test

This simulates what networkQuality measures - latency when network is busy:

```bash
# Server
iperf3 -s -p 5201

# Client - measure latency while transferring data
iperf3 -c wolf-air.local -p 5201 -t 30 -i 1 -w 1M --logfile results.txt

# Then analyze latency from log file
```

### Better: Use iperf3's Built-in Latency Test

```bash
# Server
iperf3 -s -p 5201

# Client - with zero-copy and latency reporting
iperf3 -c wolf-air.local -p 5201 -t 30 -i 1 -w 1M --zerocopy --get-server-output
```

---

## Practical Test Script

Create this script to run comprehensive tests:

```bash
#!/bin/bash
# iperf3_comprehensive_test.sh

SERVER="wolf-air.local"
PORT=5201
DURATION=30

echo "=== iperf3 Comprehensive Network Test ==="
echo "Server: $SERVER"
echo "Duration: $DURATION seconds"
echo ""

echo "1. TCP Download Test (like downloading files)"
iperf3 -c $SERVER -p $PORT -t $DURATION -i 1 -w 1M | tee tcp_download.log

echo ""
echo "2. TCP Upload Test (like uploading files)"
iperf3 -c $SERVER -p $PORT -t $DURATION -i 1 -w 1M -R | tee tcp_upload.log

echo ""
echo "3. UDP Test (like Zoom/Video calls)"
iperf3 -c $SERVER -p $PORT -u -b 2M -t $DURATION -i 1 | tee udp_test.log

echo ""
echo "4. Bidirectional Test (like general web browsing)"
iperf3 -c $SERVER -p $PORT -t $DURATION -i 1 -w 1M --bidir | tee bidirectional.log

echo ""
echo "=== Test Complete ==="
echo "Check log files for detailed results"
```

**Save as**: `iperf3_comprehensive_test.sh`
**Make executable**: `chmod +x iperf3_comprehensive_test.sh`
**Run**: `./iperf3_comprehensive_test.sh`

---

## Interpreting Results: Good vs Bad

### Good Network (for web/Zoom/streaming)

**TCP Test**:

- Bitrate: Consistent (varies < 10%)
- Retr: 0 (no retransmissions)
- Cwnd: Stable or growing

**UDP Test**:

- Jitter: < 10ms
- Packet loss: 0%
- Bitrate: Consistent

**What this means**: Network is healthy, should work well for all use cases.

### Problematic Network

**TCP Test**:

- Bitrate: Highly variable (> 50% swings)
- Retr: > 0 (packet loss)
- Cwnd: Shrinking (congestion)

**UDP Test**:

- Jitter: > 30ms
- Packet loss: > 0.5%
- Bitrate: Inconsistent

**What this means**: Network has issues - will cause sluggish UX even with "good" speedtest numbers.

---

## Comparison: What Each Tool Tells You

| Tool            | What It Measures                    | Good For                          | Limitations                                          |
|-----------------|-------------------------------------|-----------------------------------|------------------------------------------------------|
| **speedtest**   | Internet speed (Mbps)               | Quick check                       | Doesn't show latency under load, jitter, or local network issues |
| **networkQuality** | Responsiveness (RPM), latency   | Apple ecosystem, real-world simulation | HTTP/2 bug on Sequoia, macOS only                |
| **iperf3**      | Raw throughput, jitter, packet loss | Detailed diagnosis, cross-platform | Doesn't measure "responsiveness" directly            |
| **mtr**         | Path analysis, latency per hop      | Finding where problems occur      | Doesn't measure throughput                           |

---

## Recommended Testing Workflow

### For Diagnosing Sluggish UX Despite Good Speedtest

1. **Run iperf3 UDP test** (most revealing):

   ```bash
   iperf3 -c wolf-air.local -p 5201 -u -b 2M -t 30 -i 1
   ```

   - Look for jitter > 30ms = Zoom will be choppy
   - Look for packet loss > 0.5% = will cause issues

2. **Run iperf3 TCP test** (shows congestion):

   ```bash
   iperf3 -c wolf-air.local -p 5201 -t 30 -i 1 -w 1M
   ```

   - Look for Retr > 0 = packet loss
   - Look for variable bitrate = congestion

3. **Run mtr** (find where problems occur):

   ```bash
   mtr -ezbw -i 1 -c 60 1.1.1.1
   ```

   - Shows which hop has high latency/loss

4. **Compare with networkQuality -f h1** (if available):

   ```bash
   networkQuality -f h1 -v
   ```

   - Gives RPM metric (responsiveness)
   - Can correlate with iperf3 results

---

## Quick Reference: What Numbers Mean

### Latency (Round-Trip Time)

- **< 20ms**: Excellent (LAN)
- **20-50ms**: Very good (local network)
- **50-100ms**: Good (internet)
- **100-200ms**: Acceptable (some delay noticeable)
- **> 200ms**: Poor (sluggish, noticeable delay)

### Jitter (Latency Variation)

- **< 10ms**: Excellent (smooth video calls)
- **10-30ms**: Good (acceptable for Zoom)
- **30-50ms**: Fair (some choppiness)
- **> 50ms**: Poor (choppy video, audio issues)

### Packet Loss

- **0%**: Perfect
- **< 0.1%**: Excellent
- **0.1-0.5%**: Good (minor issues)
- **0.5-1%**: Fair (noticeable problems)
- **> 1%**: Poor (significant issues)

### Throughput (Speed)

**For web browsing**:

- **> 5 Mbps**: Fine
- **> 10 Mbps**: Good
- **> 25 Mbps**: Excellent

**For Zoom**:

- **> 1 Mbps**: Minimum
- **> 2 Mbps**: Recommended
- **> 5 Mbps**: Excellent

**For streaming**:

- **> 5 Mbps**: HD quality
- **> 25 Mbps**: 4K quality

---

## Example: Diagnosing "Good Speedtest but Sluggish UX"

**Scenario**: speedtest shows 25 Mbps, but web browsing feels slow.

**Step 1: Run iperf3 UDP test**:

```bash
iperf3 -c wolf-air.local -p 5201 -u -b 2M -t 30 -i 1
```

**Results**:

- Jitter: 45ms (BAD - should be < 30ms)
- Packet loss: 1.2% (BAD - should be < 0.5%)
- Bitrate: Variable (BAD - should be consistent)

**Diagnosis**: Network has high jitter and packet loss. Even though speedtest shows good throughput, the jitter and packet loss cause sluggish UX.

**Solution**: Investigate router/switch configuration, check for bufferbloat, consider SQM/QoS.

---

## Tips for Best Results

1. **Test multiple times**: Network conditions vary, average results
2. **Test at different times**: Peak hours vs off-peak
3. **Test both directions**: Upload and download can differ
4. **Use UDP for real-time apps**: More realistic for Zoom/video
5. **Compare with networkQuality**: Use both tools for complete picture
6. **Test to local server first**: Rule out internet issues
7. **Test to internet server**: Check end-to-end performance

---

## Troubleshooting Common Issues

### "Connection refused"

- Server not running: Start `iperf3 -s` on server machine
- Firewall blocking: Check firewall settings on server

### "No route to host"

- Network connectivity issue: Check if machines can ping each other
- Wrong hostname/IP: Verify server address

### "Inconsistent results"

- Background traffic: Close other apps, wait for syncs to finish
- Network congestion: Test at different times
- WiFi interference: Try Ethernet if possible

---

## End of Guide
