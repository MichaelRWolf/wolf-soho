# networkQuality Alternatives and Version Information

## Current networkQuality Version

**michael-pro (macOS 15.7.3 Sequoia)**:

- **Version**: NetworkTester-147.140.5 (embedded in binary)
- **Location**: `/usr/bin/networkQuality`
- **Build Date**: Nov 22 03:17 (from file timestamp)
- **Library**: libnetquality.dylib version 147.140.5
- **Framework**: NetworkQualityServices.framework (private, version 0.0.0)

**Note**: networkQuality doesn't have a `--version` flag, but version info is embedded in the binary.

## Can You Get Same Version on Both Computers?

**Short Answer**: No, not easily.

**Why**:

- networkQuality is a **system tool** bundled with macOS
- Version is tied to macOS version (Sequoia vs Monterey)
- Cannot easily copy binaries between systems (different architectures, dependencies)
- Would require downgrading/upgrading macOS to match versions

**Workaround**: Use HTTP/1.1 on both systems:

```bash
networkQuality -f h1 -v  # Forces HTTP/1.1, avoids HTTP/2 bug
```

## Alternative Tools

### 1. **iperf3** (Already Installed) ⭐ Recommended

**What it does**: Measures raw TCP/UDP throughput and latency

**Pros**:

- Industry standard, widely used
- Works across platforms (macOS, Linux, Windows)
- Measures actual network performance, not HTTP-specific
- No HTTP/2 bugs
- Can test between your two machines directly

**Cons**:

- Doesn't measure "responsiveness" (RPM) like networkQuality
- Requires a server (can run on one machine, test from other)
- More complex setup

**Installation**: Already installed (`/usr/local/bin/iperf3`)

**Basic Usage**:

```bash
# On server machine (e.g., wolf-air)
iperf3 -s

# On client machine (e.g., michael-pro)
iperf3 -c wolf-air.local -t 30 -i 1
```

**Advanced Usage** (measures latency under load - similar to responsiveness):

```bash
# Server
iperf3 -s

# Client - bidirectional test with latency reporting
iperf3 -c wolf-air.local -t 30 -i 1 --bidir --logfile iperf3_results.txt
```

### 2. **mtr** (Already Installed) ⭐ Good for Path Analysis

**What it does**: Combines traceroute + ping, shows path quality

**Pros**:

- Shows where latency/packet loss occurs
- Real-time updates
- Works great for diagnosing network path issues
- No HTTP dependencies

**Cons**:

- Doesn't measure throughput
- Doesn't measure "responsiveness" (RPM)
- Uses ICMP (may be rate-limited)

**Basic Usage**:

```bash
mtr -ezbw -i 1 -c 60 1.1.1.1
```

### 3. **speedtest-cli** (Available via Homebrew)

**What it does**: Tests against Ookla Speedtest servers

**Pros**:

- Simple, well-known tool
- Tests real-world internet performance
- No HTTP/2 dependencies
- Easy to compare results

**Cons**:

- Doesn't measure "responsiveness" (RPM)
- Tests internet, not local network
- Results vary by server location

**Installation**:

```bash
brew install speedtest-cli
```

**Usage**:

```bash
speedtest-cli --simple
speedtest-cli --json  # Machine-readable output
```

### 4. **curl-based Custom Script** ⭐ Best for Responsiveness Testing

**What it does**: You can create a custom script that measures HTTP responsiveness

**Pros**:

- Full control over test methodology
- Can test HTTP/1.1, HTTP/2, HTTP/3 separately
- Can measure round-trip times
- No bugs from Apple's tool

**Example Script**:

```bash
#!/bin/bash
# Test HTTP/1.1 responsiveness
for i in {1..10}; do
  time curl -s -o /dev/null -w "%{time_total}\n" \
    --http1.1 https://www.apple.com
done | awk '{sum+=$1; count++} END {print "Average:", sum/count, "seconds"}'
```

### 5. **Flent** (Network Testing Suite)

**What it does**: Comprehensive network testing, includes bufferbloat testing

**Pros**:

- Specifically designed for responsiveness/bufferbloat testing
- Measures loaded latency (similar to RPM concept)
- Industry standard for network quality testing
- Open source

**Cons**:

- More complex setup
- Requires Python
- May need server component

**Installation**:

```bash
pip3 install flent
# Or via Homebrew (if available)
```

**Usage**:

```bash
flent rtt_fair_up -H 1.1.1.1 -t "Test Name"
```

## Recommended Approach

### For Comparing michael-pro vs wolf-air

### Option 1: Use networkQuality with HTTP/1.1 (Simplest)

```bash
# On both machines
networkQuality -f h1 -v
```

- **Pros**: Same tool, same methodology, avoids HTTP/2 bug
- **Cons**: Still using Apple's tool (but HTTP/1.1 works fine)

### Option 2: Use iperf3 (Most Reliable)

```bash
# On wolf-air (server)
iperf3 -s

# On michael-pro (client)
iperf3 -c wolf-air.local -t 30 -i 1 --bidir
```

- **Pros**: Industry standard, no HTTP/2 bugs, direct machine-to-machine test
- **Cons**: Doesn't measure "responsiveness" (RPM), measures throughput/latency

### Option 3: Use mtr for Path Analysis

```bash
# On both machines
mtr -ezbw -i 1 -c 60 1.1.1.1
```

- **Pros**: Shows where problems occur in the path
- **Cons**: Doesn't measure throughput or responsiveness

### For Responsiveness Testing (RPM equivalent)

**Best Alternative**: Create custom script using `curl`:

```bash
#!/bin/bash
# responsiveness_test.sh - Measures HTTP responsiveness similar to RPM

URL="https://www.apple.com"
ITERATIONS=60
TIMEOUT=5

echo "Testing HTTP/1.1 responsiveness..."
times_h1=()
for i in $(seq 1 $ITERATIONS); do
  start=$(date +%s.%N)
  curl -s -o /dev/null --http1.1 --max-time $TIMEOUT "$URL" 2>/dev/null
  end=$(date +%s.%N)
  elapsed=$(echo "$end - $start" | bc)
  times_h1+=($elapsed)
done

# Calculate RPM (round trips per minute)
total_time=$(printf '%s\n' "${times_h1[@]}" | awk '{sum+=$1} END {print sum}')
rpm=$(echo "scale=0; $ITERATIONS * 60 / $total_time" | bc)
avg_time=$(echo "scale=3; $total_time / $ITERATIONS" | bc)

echo "HTTP/1.1: $rpm RPM (average: ${avg_time}s per request)"
```

## Comparison Table

| Tool                | Measures RPM?          | HTTP/2 Bug?            | Cross-Platform? | Setup Complexity |
|---------------------|------------------------|------------------------|-----------------|------------------|
| networkQuality -f h1 | ✅ Yes                 | ❌ No (uses HTTP/1.1)  | ❌ macOS only    | ⭐ Easy          |
| networkQuality -f h2 | ✅ Yes                 | ✅ **YES**             | ❌ macOS only    | ⭐ Easy          |
| iperf3              | ❌ No                  | ❌ No                  | ✅ Yes           | ⭐⭐ Medium       |
| mtr                 | ❌ No                  | ❌ No                  | ✅ Yes           | ⭐ Easy          |
| speedtest-cli       | ❌ No                  | ❌ No                  | ✅ Yes           | ⭐ Easy          |
| Custom curl script  | ✅ Yes (can calculate) | ❌ No                  | ✅ Yes           | ⭐⭐ Medium       |

## Recommendation

**For your use case** (comparing michael-pro vs wolf-air):

1. **Primary**: Use `networkQuality -f h1 -v` on both machines
   - Same tool, same methodology
   - HTTP/1.1 works correctly
   - Gives you RPM (responsiveness) metric

2. **Secondary**: Use `iperf3` for raw network performance
   - Direct machine-to-machine test
   - No HTTP dependencies
   - Industry standard

3. **Tertiary**: Use `mtr` for path analysis
   - Shows where latency occurs
   - Helps diagnose routing issues

**Bottom Line**: `networkQuality -f h1` is your best bet - it's the same tool, avoids the HTTP/2 bug, and gives you the RPM metric you need for comparison.
