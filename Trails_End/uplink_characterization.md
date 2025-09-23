# Uplink at Trails End

In a conversation between ChatGPT and Michael on 2025-09-23, we discussed:

- The Trails End campground network setup (Starlink + Pasty dual uplinks)
- Networking fundamentals crucial for interactive apps like Zoom and Cursor
- Actual test data from `speedtest`, `networkQuality`, and `mtr`
- Why the data shows problems (latency, jitter, satellite handoffs)
- Strategies for remediation on both Beryl router and macOS laptop
- Useful monitoring and debugging commands
- Characterization data: vulnerabilities, benchmarks, and traffic-light thresholds

---

## 1. Context: Trails End Network Setup

- Barn roof: Starlink dish → barn router → Ubiquiti mesh backhaul.  
- Local ISP (Pasty.net) also provides uplink.  
- Campground network flips between **Pasty terrestrial** and **Starlink satellite**.  
- Users see variable latency and responsiveness depending on uplink.

---

## 2. Networking Fundamentals for Zoom and Cursor

- **Throughput vs Responsiveness**: Mbps may look fine, but interactive apps fail if responsiveness is low.  
- **Latency**: round-trip delay in ms. Critical for real-time apps.  
- **Jitter**: variation in latency; spikes cause freezes.  
- **Packet Loss**: dropped packets trigger retransmissions and stalls.  
- **TCP Keepalives**: connections are never fully "idle"; missed ACKs during handoffs cause resets.

---

## 3. Evidence from Actual Data

### Speedtest
- ~23 Mbps down / 18 Mbps up looked healthy.  
- Jitter: up to 909 ms, indicating unstable performance.  

### `networkQuality`
- Idle Latency: ~63 ms (951 RPM).  
- Responsiveness: **Low** — ~45 RPM (1.3s).  
- Much more informative than Speedtest.

### `mtr` Traceroute
- Example Pasty path:  
  `AS27337 i1.pasty.net (199.38.31.1)`  
- Example Starlink path:  
  `OrgName: SpaceX Services, Inc.` with IPv6 address.  
- Logs confirmed flips between Pasty and Starlink within minutes.

### Sample Script Output

```bash
$ ./uplink-short
Uplink: SpaceX Services, Inc. — public IP — IP 2605:59ca:13ad:c910:41f0:638f:7b84:376

michael@michael-pro: (wolf-soho)/Trails_End/bin 
[0] $ networkQuality 
==== SUMMARY ====
Uplink capacity: 3.205 Mbps
Downlink capacity: 7.916 Mbps
Responsiveness: Low (4.184 seconds | 14 RPM)
Idle Latency: 69.627 milliseconds | 861 RPM
```

---

## 4. Why These Problems Arise

- **Satellite Handoffs**: Starlink passes connections between satellites every ~10–15 minutes; handoffs can stall 20–60 seconds.  
- **CGNAT**: Starlink often uses Carrier-Grade NAT (100.64.0.0/10); adds complexity to connections.  
- **Dual Uplinks**: Campground router flips between Pasty and Starlink without notice.  
- **Impact**: Zoom freezes, Cursor timeouts, long stalls when AI should be “thinking.”

---

## 5. Remediation Strategies

### Observation
- Use scripts (`uplink-short`, `uplink-describe`, `uplink-monitor`) to log uplink identity and traceroutes.  
- Correlate flips with Zoom/Cursor issues.  

### Mitigation: Beryl Router
- Enable **SQM (Smart Queue Management)** with **cake/codel** to smooth jitter.  
- Test profiles (e.g., “TCP optimization”) in LuCI; keep a fallback config.  

### Mitigation: macOS
- Use `networkQuality -v` to measure responsiveness (RPM).  
- Run `mtr` for live hop-by-hop loss/jitter.  
- Automate logging with `launchd` to gather continuous data.  
- Scripts in repo (`uplink-lib.sh` + wrappers) give quick context.

---

## 6. Useful Monitoring and Debugging Commands

```bash
# Current uplink, org, and IP
./uplink-short

# Detailed snapshot with traceroute
./uplink-describe

# Continuous logging every 5 minutes
./uplink-monitor ~/uplink_log.txt 300

# Apple’s responsiveness test (RPM)
networkQuality -v

# Hop-by-hop latency & loss (requires sudo)
sudo mtr -ezbw -i 1 -c 50 1.1.1.1

# Quick traceroute (6 hops)
traceroute -n -m 6 1.1.1.1

# Confirm CGNAT range membership
ipcalc -nb 100.64.0.0/10 <IP>
```

---

## 7. Characterization Data

### Vulnerabilities by Application Type

#### Zoom (UDP-based media)
- **Latency**: tolerates up to ~300 ms; above this, conversation flow suffers.
- **Jitter**: highly sensitive to >100 ms spikes; causes audio gaps and video freezes.
- **Packet Loss**: tolerates <1–2% via FEC; noticeable degradation >3–5%.
- **Satellite Handoffs (20–60s)**: video/audio freeze, then possible reconnect.
- **Behavior**: *degrades gradually* — call continues, quality worsens.

#### Cursor (TCP/WebSockets over HTTPS)
- **Latency**: moderate RTT is fine; multi-second stalls (>5–10s) risk TCP timeout.
- **Jitter**: less sensitive to small spikes; long jitter events = stall/disconnect.
- **Packet Loss**: TCP retransmits hide small loss; sustained loss slows throughput.
- **Satellite Handoffs (20–60s)**: WebSocket drops due to keepalive or TCP timeout.
- **Behavior**: *fails hard* — looks fine until sudden timeout/disconnect.

---

### Benchmarks and Thresholds

#### Latency (RTT)
- **< 50 ms**: Excellent, feels instantaneous.
- **50–150 ms**: Usable, minor lag.
- **150–300 ms**: Laggy, double-talk issues.
- **> 300 ms**: Zoom awkward, Cursor slowed.
- **> 800 ms bursts**: Zoom freezes; Cursor retries stall.

#### Jitter (variation in latency)
- **< 20 ms**: Excellent.
- **20–50 ms**: Acceptable.
- **50–100 ms**: Zoom may wobble.
- **> 100 ms spikes**: Zoom stutters; Cursor unaffected unless multi-second.
- **> 200 ms sustained**: Zoom nearly unusable.

#### Packet Loss
- **< 1%**: Normal.
- **1–3%**: Minor Zoom glitches.
- **3–5%**: Zoom freezes/blocks; Cursor laggy.
- **> 5%**: Zoom audio-only fallback; Cursor may timeout.
- **> 10%**: Unusable.

#### Responsiveness (RPM, Apple `networkQuality`)
- **> 400 RPM (~250 ms)**: Smooth.
- **200–400 RPM**: Acceptable.
- **50–200 RPM**: Laggy.
- **< 50 RPM (~1s)**: Behaving badly.
- **< 20 RPM (>3s)**: Zoom freezes, Cursor disconnects.

---

### Traffic Light Table (Quick Reference)

| Metric            | Green (Good) – Smooth UX         | Yellow (Degraded) – Noticeable Issues        | Red (Disconnect risk) – Severe Impact       |
|-------------------|---------------------------------|---------------------------------------------|---------------------------------------------|
| Latency (RTT)     | <150 ms — natural conversation  | 150–300 ms — Zoom lag, Cursor slower         | >300 ms or bursts >800 ms — Zoom awkward, Cursor stalls |
| Jitter            | <50 ms — stable audio/video     | 50–100 ms — Zoom wobbles, minor glitches     | >100 ms spikes / >200 ms sustained — Zoom stutters, Cursor unaffected until disconnect |
| Packet Loss       | <1% — clean streams             | 1–5% — Zoom audio drops, Cursor retries      | >5% sustained / >10% — Zoom fallback audio-only, Cursor disconnects |
| Responsiveness RPM| >200 — fast response            | 50–200 — Zoom laggy, Cursor slow requests    | <50 — Zoom freezes, Cursor timeouts         |

---

## 8. Next Steps

- Run monitoring for at least a week.  
- Compare uplink flips vs Zoom/Cursor issues.  
- Decide if Beryl SQM mitigations are effective.  
- If problems persist, escalate to campground IT or Pasty.

---

## 9. Glossary

- **ACK**: Acknowledgment (TCP control message confirming packet receipt).  
- **AS**: Autonomous System — a large routing domain with its own number (e.g., AS27337 = Pasty.net).  
- **CGNAT**: Carrier-Grade Network Address Translation — ISP technique using 100.64.0.0/10 for shared IPv4.  
- **FEC**: Forward Error Correction — redundancy for recovering lost packets in real-time media.  
- **HTTP**: HyperText Transfer Protocol — foundation for web requests.  
- **HTTPS**: Secure HTTP (with TLS encryption).  
- **IP**: Internet Protocol — addressing and routing layer.  
- **IPv4/IPv6**: Internet Protocol versions 4 and 6.  
- **Jitter**: Variation in packet arrival time.  
- **LuCI**: Web interface for OpenWRT/Beryl routers.  
- **Mbps**: Megabits per second — throughput measure.  
- **mtr**: “My Traceroute,” combines ping and traceroute for live path analysis.  
- **NAT**: Network Address Translation.  
- **RPM**: Round-trips per Minute (Apple’s responsiveness metric).  
- **SQM**: Smart Queue Management — router feature for smoothing bufferbloat and jitter.  
- **TCP**: Transmission Control Protocol — reliable, ordered byte streams.  
- **UDP**: User Datagram Protocol — fast, connectionless, no delivery guarantees.  
- **WebSockets**: Persistent, bidirectional communication channel over a single TCP connection.  

