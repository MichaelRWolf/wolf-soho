# Uplink Responsiveness Ledger (Bufferbloat / `networkQuality` RPM)

This file is the **append-only ledger** for experiments aimed at improving macOS `networkQuality -v` **Responsiveness** (RPM / loaded latency) on the Wolfden **Spectrum → PtP → Beryl** path.

## How to use (minimal)

- Run the **Session Checklist** below.
- Paste outputs into chat **only if the agent can’t run the command from here**.
- Add **one row per run** in the table.

## Note on dual-homing (Wi‑Fi + Ethernet on the same subnet)

If **en0 and en13 are both active with 192.168.8.x addresses**, macOS can behave poorly during tests (ARP/routing ambiguity; “some packets go out the wrong interface”).

**Recommendation for testing:** keep **only one** of Wi‑Fi or Belkin Ethernet enabled at a time.

- Wi‑Fi tests: disable Belkin USB‑C LAN
- Ethernet tests: disable Wi‑Fi

## Session Checklist (copy/paste)

```bash
# 1) Identify hop2 (first upstream router beyond Beryl)
traceroute -n -m 6 1.1.1.1

# 2) Primary metric (includes its own load test)
# Tip: `-c` emits JSON (computer-readable) which is easiest to parse.
networkQuality -c
```

## Data table (append rows)

Columns:

- `link`: `Ethernet` or `WiFi(SSID,band)`
- `hop2`: hop 2 IP from traceroute
- `sqm`: `Off` or `On(cake,d/u_kbps,iface)`
- `nq_dl_mbps`, `nq_ul_mbps`, `nq_idle_ms`
- `nq_resp`: `loaded_ms @ RPM` as shown by `networkQuality -v`
- `ping_*`: ping-under-load results (loss%, avg ms, max ms) to:
  - `ping_A`: Beryl LAN IP (hop1)
  - `ping_B`: hop2 gateway
  - `ping_C`: internet target (`1.1.1.1`)

| ts_local          | host        | link          | hop2         | sqm | nq_dl_mbps | nq_ul_mbps | nq_idle_ms | nq_resp                                   | ping_A_loss | ping_A_avg_ms | ping_A_max_ms | ping_B_loss | ping_B_avg_ms | ping_B_max_ms | ping_C_loss | ping_C_avg_ms | ping_C_max_ms | notes                                           |
|------------------|-------------|---------------|-------------|-----|-----------:|-----------:|----------:|-------------------------------------------|------------:|--------------:|--------------:|------------:|--------------:|--------------:|------------:|--------------:|--------------:|------------------------------------------------|
| 2025-12-21 18:46 | michael-pro | WiFi(en0)      | 192.168.1.1 | Off |     55.641 |     19.640 |    55.357 | 1294ms @ 46 RPM (HTTP_loaded 1813ms @ 33) |             |               |               |             |               |               |             |               |               | baseline from Cursor run; traceroute hop1=192.168.8.1 |
| 2025-12-21 18:50 | michael-pro | WiFi(en0)      | 192.168.1.1 | Off |     50.555 |     18.313 |    49.993 | 1879ms @ 31 RPM                            |        15.0 |         46.753 |       1557.453 |        15.5 |         61.821 |       1560.288 |        17.0 |        130.114 |       1573.337 | ping-under-load during networkQuality; hop1=192.168.8.1 |
| 2025-12-21 18:53 | michael-pro | Ethernet(en13) | 192.168.1.1 | Off |            |            |           |                                           |             |               |               |             |               |               |             |               |               | context-only: default route to 1.1.1.1 via gw=192.168.8.1 iface=en13 (Belkin USB-C LAN); en13_ip=192.168.8.235; en0_ip=192.168.8.124 |
| 2025-12-21 19:03 | michael-pro | Ethernet(en13) | 192.168.1.1 | Off |     82.804 |     13.684 |    54.239 | 251ms @ 238.9 RPM (JSON -c)               |         0.0 |          1.438 |         28.942 |         1.5 |          6.437 |         72.223 |         3.5 |         76.117 |        245.927 | ping-under-load pinned to en13 source IP; `networkQuality -I en13 -c` |
| 2025-12-21 19:08 | michael-pro | Ethernet(en13) | 192.168.1.1 | Off |     77.354 |     12.602 |    96.598 | 265ms @ 226 RPM (HTTP_loaded 414ms @ 144) |             |               |               |             |               |               |             |               |               | `networkQuality -I en13 -v` (human summary) |
| 2025-12-21 19:19 | michael-pro | WiFi(en0)      | 192.168.1.1 | Off |     36.966 |     11.388 |    57.022 | 1789ms @ 33.5 RPM (JSON -c)               |        14.0 |         44.159 |       1561.620 |        15.0 |         59.221 |       1564.681 |        18.0 |         96.795 |        327.923 | Wi‑Fi-only (en13 disabled, default route via en0); ping-under-load pinned to en0 source IP; `networkQuality -I en0 -c` |
| 2025-12-21 19:30 | michael-pro | WiFi(en0)      | 192.168.1.1 | Off |     62.392 |            |    54.591 | 560ms @ 107.2 RPM (dl_only; JSON -c -u)   |        15.5 |         19.080 |       1435.884 |        15.0 |         34.215 |        634.978 |        15.5 |        100.529 |       2153.973 | Wi‑Fi-only download-only (`networkQuality -I en0 -c -u`); `dl_responsiveness` present, `responsiveness` absent |
| 2025-12-21 19:31 | michael-pro | WiFi(en0)      | 192.168.1.1 | Off |            |     14.330 |    57.780 | 4094ms @ 14.7 RPM (ul_only; JSON -c -d)   |        13.5 |         21.739 |        942.106 |        14.5 |         19.726 |        741.480 |        14.0 |         98.884 |        959.445 | Wi‑Fi-only upload-only (`networkQuality -I en0 -c -d`); `ul_responsiveness` present, `responsiveness` absent |
| 2025-12-21 19:37 | michael-pro | Ethernet(en13) | 192.168.1.1 | Off |            |     17.967 |    61.048 | 3454ms @ 17.4 RPM (ul_only; JSON -c -d)   |         0.0 |          1.342 |         20.235 |         1.0 |          2.994 |         42.978 |         0.5 |         53.928 |        285.982 | Ethernet-only upload-only (`networkQuality -I en13 -c -d`); Wi‑Fi disabled; `ul_responsiveness` present |
| 2025-12-21 20:29 | michael-pro | Ethernet(en13) | 72.31.129.125 | Off |     72.394 |     19.345 |    63.314 | 209ms @ 286.9 RPM (direct_to_loco; JSON -c) |         0.0 |          3.032 |         19.725 |         1.4 |         35.371 |        253.247 |         0.9 |         45.947 |        387.692 | Direct-to-loco-station (Beryl bypass); gw=192.168.1.1; ping_A=gw, ping_B=hop2 |
| 2025-12-21 20:30 | michael-pro | Ethernet(en13) | 72.31.129.125 | Off |            |     25.472 |    51.374 | 3329ms @ 18.0 RPM (ul_only; direct_to_loco; JSON -c -d) |         0.0 |          2.685 |         55.426 |         0.0 |         57.979 |        296.401 |         0.0 |         68.073 |        313.943 | Direct-to-loco-station (Beryl bypass); gw=192.168.1.1; upload-only still bad while gw ping stays clean |
| 2025-12-21 20:55 | michael-pro | Ethernet(en13) | 72.31.129.125 | Off |            |            |    47.132 | baseline: gw 2.2ms, hop2 14.3ms, inet 25.5ms |         0.0 |          2.218 |         17.013 |         0.0 |         14.263 |         33.776 |         0.0 |         25.511 |         58.319 | Direct-to-loco baseline pings only (no induced load) |
| 2025-12-21 20:57 | michael-pro | Ethernet(en13) | 72.31.129.125 | Off |            |     14.165 |    53.879 | 3877ms @ 15.5 RPM (ul_only; direct_to_loco; JSON -c -d) |         0.0 |          2.709 |         79.724 |         0.0 |         48.196 |        186.324 |         0.0 |         57.984 |        195.361 | Direct-to-loco upload-only; gw stays low while hop2/inet inflate |
| 2025-12-21 20:58 | michael-pro | Ethernet(en13) | 72.31.129.125 | Off |     86.474 |            |    47.132 | 102ms @ 588.3 RPM (dl_only; direct_to_loco; JSON -c -u) |         1.8 |          3.190 |         47.498 |         2.7 |         14.538 |         61.978 |         1.8 |         24.840 |         50.435 | Direct-to-loco download-only; responsiveness excellent |
| 2025-12-22 21:40 | michael-pro | WiFi(en0)      | 192.168.1.1   | On(cake,6000/8000,eth0) |      4.554 |     13.433 |   140.656 | 2462ms @ 24 RPM (full; HTTP_loaded 4255ms @ 14) |             |               |               |             |               |               |             |               |               | Overnight crater: downlink collapsed and responsiveness unusable; Wi‑Fi to Beryl |
| 2025-12-22 21:?? | michael-pro | WiFi(en0)      | 192.168.1.1   | On(cake,6000/8000,eth0) |      4.692 |            |    49.803 | 2154ms @ 27 RPM (dl_only)                    |             |               |               |             |               |               |             |               |               | Downlink-only with download shaping 6000 |
| 2025-12-22 21:?? | michael-pro | WiFi(en0)      | 192.168.1.1   | On(cake,6000/8000,eth0) |            |     10.559 |    46.563 | 111ms @ 542 RPM (ul_only)                     |             |               |               |             |               |               |             |               |               | Uplink-only remained good with upload shaping 8000 |
| 2025-12-22 21:?? | michael-pro | Ethernet(en13) | 192.168.1.1   | On(cake,6000/8000,eth0) |      4.538 |            |    59.621 | 2120ms @ 28 RPM (dl_only)                     |             |               |               |             |               |               |             |               |               | Ethernet confirms downlink crater is upstream (not Wi‑Fi) |
| 2025-12-22 21:?? | michael-pro | Ethernet(en13) | 192.168.1.1   | On(cake,3000/8000,eth0) |      2.212 |            |    80.736 | 4043ms @ 14 RPM (dl_only)                     |             |               |               |             |               |               |             |               |               | Download shaping 3000 reduced throughput but did not improve dl responsiveness |
| 2025-12-22 21:?? | michael-pro | Ethernet(en13) | 192.168.1.1   | On(cake,2000/8000,eth0) |      1.398 |            |    98.244 | 5519ms @ 10 RPM (dl_only)                     |             |               |               |             |               |               |             |               |               | Download shaping 2000 worsened dl throughput and reported dl responsiveness |
| 2025-12-22 22:57 | michael-pro | Ethernet(en13) | 192.168.1.1   | (unknown) |      4.826 |            |    71.873 | 1950ms @ 30.8 RPM (dl_only; JSON -c -u)       |         0.0 |          3.558 |         36.738 |         0.0 |          6.318 |         23.584 |         0.0 |         27.210 |         86.096 | Agent-run: baseline pings clean; under dl load pings stayed low/no loss despite low dl RPM |

### Snapshot: observations (as of 2025-12-22)

- 18:46 — Wi‑Fi full test: **Responsiveness Low (~46 RPM)** despite good throughput.
- 18:50 — Wi‑Fi under load: **high loss + >1.5s spikes even to Beryl** → local Wi‑Fi path collapses under contention.
- 19:03 — Ethernet under load: **router path clean** and **Responsiveness good (~239 RPM)** → Wi‑Fi is a major driver of “Low”.
- 19:08 — Ethernet full test: **Responsiveness Medium (~226 RPM)** → usable baseline without Wi‑Fi.
- 19:19 — Wi‑Fi-only (no dual-homing): still **~14–18% loss to Beryl/hop2** and **Low RPM (~33)** → not an Ethernet/Wi‑Fi confusion artifact; Wi‑Fi itself is unstable under load.
- 19:30 — Wi‑Fi download-only: **dl_responsiveness ~107 RPM** (still degraded) and **loss persists** → download load hurts, but less than upload.
- 19:31 — Wi‑Fi upload-only: **ul_responsiveness ~14.7 RPM (~4.1s)** → upload is the worst case on Wi‑Fi.
- 19:37 — Ethernet upload-only: **ul_responsiveness still low (~17.4 RPM)** while **LAN pings are clean** → uplink queueing is also a separate issue (beyond the local Ethernet link).
- 20:29 — Direct-to-loco full: **Responsiveness good (~287 RPM)** → Beryl not required to get good full-test responsiveness on wired path.
- 20:30 — Direct-to-loco upload-only: **ul_responsiveness still low (~18 RPM)** while **gateway ping stays clean** → queueing is beyond Mac↔gateway (upstream/ISP-side).
- 20:55 — Direct-to-loco baseline: **gw ~2ms / hop2 ~14ms / inet ~26ms** with 0% loss → baseline path is healthy.
- 20:57 — Direct-to-loco upload-only: **ul_responsiveness ~15.5 RPM (~3.9s)**; **gw stays low** but hop2/inet inflate → bottleneck queue is beyond `192.168.1.1` LAN, likely gateway WAN/ISP.
- 20:58 — Direct-to-loco download-only: **dl_responsiveness ~588 RPM (~102ms)** → the pathological direction is upload, not download.
- 22:31 — SQM/CAKE configured in LuCI on WAN; SQM logs show “started successfully,” but `networkQuality -d` still exceeded cap → SQM not yet attached to real egress queue.
- 22:39 — SSH verification: `tc` showed egress wasn’t shaped on `eth0.2`; switching SQM interface to **`eth0`** fixed CAKE attachment.
- 23:00 — With SQM attached at 11000 kbit/s, `networkQuality -d -v` showed uplink ≈ 10 Mbps but still Low RPM → cap was above instantaneous bottleneck; needed lower upload shaping.
- 23:19 — Upload shaping at **8000 kbit/s** produced repeatable Medium/High uplink responsiveness in repeated `networkQuality -d` runs (hundreds–thousands RPM).
- 23:33 — Full `networkQuality -v` sometimes still reported overall Responsiveness Low due to downlink collapsing (~3–6 Mbps during test); direction split confirmed upload-only High while download-only Low.
- 2025-12-22 (night) — Downlink cratered to **~4–5 Mbps** and stayed **Low (~24–31 RPM)** across **Wi‑Fi and Ethernet**, while uplink could still be **Medium/High** with SQM upload shaping.
- 2025-12-22 — Lowering download shaping to **3000 → 2000 kbit/s** reduced measured downlink capacity (**2.2 → 1.4 Mbps**) without improving the downlink RPM metric.
- 2025-12-22 22:57 — Under a downlink-only test on Ethernet, **concurrent pings remained clean** (0% loss; WAN RTT stayed in the tens of ms) despite low `networkQuality -u` RPM → this points more toward **true upstream downlink impairment / low capacity** (or the way `networkQuality` scores downlink on very low Mbps) than classic “download bufferbloat on our LAN.”

## Raw outputs (optional, paste blocks)

### Context header format (for every chunk)

```text
host: <michael-pro|wolf-air>
enabled_interfaces: <example: WiFi=en0(on), BelkinUSBCLAN=en13(off)>
default_route: <example: 1.1.1.1 via gw=192.168.8.1 iface=en0>
```

### 2025-12-22 21:40 — Wi‑Fi full test (downlink crater)

```text
host: michael-pro
enabled_interfaces: WiFi=en0(active), BelkinUSBCLAN=en13(inactive)
path: Wi‑Fi → Beryl (192.168.8.1) → hop2 192.168.1.1
sqm: On(cake,down=6000,up=8000,iface=eth0) (as configured at the time)

==== SUMMARY ====
Uplink capacity: 13.433 Mbps
Downlink capacity: 4.554 Mbps
Responsiveness: Low (2.462 seconds | 24 RPM)
Idle Latency: 140.656 milliseconds | 426 RPM
```

So what: downlink collapsed to ~4.6 Mbps and overall responsiveness became unusable (24 RPM). This is not the “normal” PtP day behavior.

Now what: confirm whether the crater is Wi‑Fi-only or persists on Ethernet (it persisted), then treat as upstream downlink impairment; keep SQM upload shaping (works) and avoid using `networkQuality -u` alone as the KPI for download tuning.

### 2025-12-22 21:?? — Direction split with SQM (download 6000, upload 8000)

```text
host: michael-pro
sqm: download shaping 6000, upload shaping 8000

==== SUMMARY ====
Downlink capacity: 4.692 Mbps
Downlink Responsiveness: Low (2.154 seconds | 27 RPM)
Idle Latency: 49.803 milliseconds | 1204 RPM

==== SUMMARY ====
Uplink capacity: 10.559 Mbps
Uplink Responsiveness: Medium (110.578 milliseconds | 542 RPM)
Idle Latency: 46.563 milliseconds | 1288 RPM
```

So what: SQM upload shaping is still doing its job (uplink Medium, 542 RPM). Downlink remains the bottleneck and is scoring Low.

Now what: focus on keeping uplink stable for calls; treat downlink as “upstream/ISP event” until proven otherwise.

### 2025-12-22 21:?? — Ethernet confirms downlink crater

```text
host: michael-pro
enabled_interfaces: WiFi=en0(inactive), BelkinUSBCLAN=en13(active)

==== SUMMARY ====
Downlink capacity: 4.538 Mbps
Downlink Responsiveness: Low (2.120 seconds | 28 RPM)
Idle Latency: 59.621 milliseconds | 1006 RPM
```

So what: the crater persists on Ethernet, so this is not “Beryl Wi‑Fi melting.” It’s upstream (house gateway / Spectrum / ISP node) or a transient contention source beyond the RV.

Now what: any “fix” we can do locally is limited to prioritizing interactive traffic (SQM) and/or waiting out the upstream impairment.

### 2025-12-22 21:?? — Download shaping experiments (3000, then 2000)

```text
download shaping 3000

==== SUMMARY ====
Downlink capacity: 2.212 Mbps
Downlink Responsiveness: Low (4.043 seconds | 14 RPM)
Idle Latency: 80.736 milliseconds | 743 RPM

download shaping 2000

==== SUMMARY ====
Downlink capacity: 1.398 Mbps
Downlink Responsiveness: Low (5.519 seconds | 10 RPM)
Idle Latency: 98.244 milliseconds | 610 RPM
```

So what: lowering the download cap reduced measured downlink capacity and did not improve the downlink “responsiveness” score. This suggests the event is dominated by low/unstable upstream downlink rather than a controllable local queue on the RV side.

Now what: stop tuning download shaping off of `networkQuality -u` alone during a downlink crater; instead, use ping-under-download-load as the guardrail and keep SQM upload shaping for Zoom stability.

### 2025-12-22 22:56–22:57 — Ethernet downlink-only under load + pings (agent-run)

```text
host: michael-pro
enabled_interfaces: WiFi=en0(inactive), BelkinUSBCLAN=en13(active)
default_route: 1.1.1.1 via gw=192.168.8.1 iface=en13
hop2: 192.168.1.1

Baseline pings (no induced load):
gw (192.168.8.1):     0.0% loss, rtt min/avg/max = 0.718/1.618/21.697 ms
hop2 (192.168.1.1):   0.0% loss, rtt min/avg/max = 1.692/3.152/19.874 ms
inet (1.1.1.1):       0.0% loss, rtt min/avg/max = 20.052/25.425/42.208 ms

Download-only under load (`networkQuality -I en13 -c -u`):
dl_mbps: 4.826
base_rtt_ms: 71.873
dl_responsiveness_rpm: 30.8  (~1.95s per round trip)

Pings during the downlink-only load:
gw (192.168.8.1):     0.0% loss, rtt min/avg/max = 0.804/3.558/36.738 ms
hop2 (192.168.1.1):   0.0% loss, rtt min/avg/max = 1.705/6.318/23.584 ms
inet (1.1.1.1):       0.0% loss, rtt min/avg/max = 19.191/27.210/86.096 ms
```

So what: even while downlink-only “responsiveness” scored Low, the pings stayed relatively stable with 0% loss. That’s inconsistent with classic download bufferbloat on the local path and more consistent with an upstream downlink impairment / low-goodput condition (or `networkQuality`’s scoring behavior when downlink Mbps is very low).

Now what: treat “downlink RPM” as secondary when the ISP is in a crater; instead, use ping-under-load and real app behavior. Keep upload SQM in place (it demonstrably helps Zoom), and plan for a dedicated AP later to remove the local Wi‑Fi failure mode when the ISP is healthy again.

### traceroute

```text
traceroute to 1.1.1.1 (1.1.1.1), 6 hops max, 40 byte packets
 1  192.168.8.1  25.532 ms  4.059 ms  2.791 ms
 2  192.168.1.1  5.546 ms  5.034 ms  5.063 ms
 3  72.31.129.125  145.687 ms  17.619 ms  16.423 ms
 4  71.46.25.177  149.667 ms  15.371 ms  18.052 ms
 5  72.31.119.184  143.482 ms  33.813 ms  541.551 ms
 6  72.31.119.188  1164.431 ms  17.601 ms  18.796 ms
```

So what: hop2 is `192.168.1.1` (an upstream gateway/router) beyond Beryl; the WAN path is not “Beryl direct-to-modem.”

Now what: keep targeting the choke point (likely Beryl WAN egress and/or upstream `192.168.1.1`); SQM on Beryl is still worthwhile, but upstream gear may also matter.

### networkQuality

```text
==== SUMMARY ====
Uplink capacity: 19.640 Mbps
Downlink capacity: 55.641 Mbps
Responsiveness: Low (1.294 seconds | 46 RPM)
Idle Latency: 55.357 milliseconds | 1083 RPM
```

So what: “Low” responsiveness exists even when throughput is good; this is a loaded-latency / queueing symptom, not a raw Mbps problem.

Now what: split by medium (Ethernet vs Wi‑Fi) and by direction (upload vs download) to localize the queue.

### ping-under-load (2025-12-21 18:50)

```text
host: michael-pro
enabled_interfaces: WiFi=en0(on), BelkinUSBCLAN=en13(on)
default_route: (not captured; likely via gw=192.168.8.1 iface=en0)

ping_A (192.168.8.1): 15.0% loss, rtt min/avg/max = 1.997/46.753/1557.453 ms
ping_B (192.168.1.1): 15.5% loss, rtt min/avg/max = 3.573/61.821/1560.288 ms
ping_C (1.1.1.1):     17.0% loss, rtt min/avg/max = 20.438/130.114/1573.337 ms

networkQuality summary (same window):
Uplink capacity: 18.313 Mbps
Downlink capacity: 50.555 Mbps
Responsiveness: Low (1.879 seconds | 31 RPM)
Idle Latency: 49.993 milliseconds | 1200 RPM
```

So what: during `networkQuality` load, there is severe loss and multi-second jitter even to the router (`192.168.8.1`) → the local Wi‑Fi/LAN path is unstable under load.

Now what: reproduce with a single active interface (avoid dual-homing), then compare against Ethernet; if Ethernet is clean, focus on Wi‑Fi airtime/queue management.

### Ethernet confirmation + ping-under-load (2025-12-21 19:03)

```text
host: michael-pro
enabled_interfaces: WiFi=en0(on), BelkinUSBCLAN=en13(on)
default_route: 1.1.1.1 via gw=192.168.8.1 iface=en13

Default route:
gateway: 192.168.8.1
interface: en13
en13 hardware port: Belkin USB-C LAN
en13_ip: 192.168.8.235

ping_A (192.168.8.1):  0.0% loss, rtt min/avg/max = 0.670/1.438/28.942 ms
ping_B (192.168.1.1):  1.5% loss, rtt min/avg/max = 1.963/6.437/72.223 ms
ping_C (1.1.1.1):      3.5% loss, rtt min/avg/max = 16.553/76.117/245.927 ms

networkQuality JSON summary (`networkQuality -I en13 -c`):
dl_mbps: 82.804
ul_mbps: 13.684
base_rtt_ms: 54.239
responsiveness_rpm: 238.9  (0.251s)
```

So what: pinned to Ethernet, ping to router is clean (0% loss, ~1.4ms avg) and responsiveness is good (~239 RPM) → Wi‑Fi is a major contributor to “Responsiveness: Low.”

Now what: for “Medium→High,” prefer Ethernet for critical work; for Wi‑Fi, treat it as an optimization target (airtime, channel width, QoS/SQM).

### networkQuality verbose (2025-12-21 19:08)

```text
host: michael-pro
enabled_interfaces: WiFi=en0(on), BelkinUSBCLAN=en13(on)
default_route: 1.1.1.1 via gw=192.168.8.1 iface=en13 (bound explicitly to en13)

==== SUMMARY ====
Uplink capacity: 12.602 Mbps
Downlink capacity: 77.354 Mbps
Responsiveness: Medium (265.325 milliseconds | 226 RPM)
Idle Latency: 96.598 milliseconds | 621 RPM
```

So what: on Ethernet, Apple reports Responsiveness **Medium (~226 RPM)**; this is the baseline “smoking connection” without touching router configs.

Now what: keep this as the pre-change baseline when we later test SQM/CAKE on Beryl.

### Wi‑Fi-only ping-under-load + networkQuality JSON (2025-12-21 19:19)

```text
host: michael-pro
enabled_interfaces: WiFi=en0(on), BelkinUSBCLAN=en13(off)
default_route: 1.1.1.1 via gw=192.168.8.1 iface=en0
en0_ip: 192.168.8.124

ping_A (192.168.8.1): 14.0% loss, rtt min/avg/max = 1.974/44.159/1561.620 ms
ping_B (192.168.1.1): 15.0% loss, rtt min/avg/max = 3.351/59.221/1564.681 ms
ping_C (1.1.1.1):     18.0% loss, rtt min/avg/max = 18.722/96.795/327.923 ms

networkQuality JSON summary (`networkQuality -I en0 -c`):
dl_mbps: 36.966
ul_mbps: 11.388
base_rtt_ms: 57.022
responsiveness_rpm: 33.5  (1.789s)
```

So what: even with dual-homing removed, Wi‑Fi still shows ~14–18% loss and huge jitter to the router/hop2 under load, with very low RPM (~33) → this is a real Wi‑Fi contention/queueing failure mode.

Now what: treat Wi‑Fi as a separate problem domain (airtime, channel width, client isolation); validate any improvements by re-running this exact block.

### Wi‑Fi-only download-only (2025-12-21 19:30)

```text
host: michael-pro
enabled_interfaces: WiFi=en0(on), BelkinUSBCLAN=en13(off)
default_route: 1.1.1.1 via gw=192.168.8.1 iface=en0
en0_ip: 192.168.8.124

ping_A (192.168.8.1): 15.5% loss, rtt min/avg/max = 2.165/19.080/1435.884 ms
ping_B (192.168.1.1): 15.0% loss, rtt min/avg/max = 3.115/34.215/634.978 ms
ping_C (1.1.1.1):     15.5% loss, rtt min/avg/max = 21.778/100.529/2153.973 ms

networkQuality JSON summary (`networkQuality -I en0 -c -u`):
dl_mbps: 62.392
base_rtt_ms: 54.591
dl_responsiveness_rpm: 107.2  (0.560s)
```

So what: download-only load is still bad (loss persists) but the responsiveness number is much better than upload-only (107 RPM vs ~15 RPM) → upload is the more destructive direction.

Now what: prioritize uplink management (SQM/CAKE) and Wi‑Fi airtime fairness; deprioritize “more download Mbps” tuning.

### Wi‑Fi-only upload-only (2025-12-21 19:31)

```text
host: michael-pro
enabled_interfaces: WiFi=en0(on), BelkinUSBCLAN=en13(off)
default_route: 1.1.1.1 via gw=192.168.8.1 iface=en0
en0_ip: 192.168.8.124

ping_A (192.168.8.1): 13.5% loss, rtt min/avg/max = 1.806/21.739/942.106 ms
ping_B (192.168.1.1): 14.5% loss, rtt min/avg/max = 2.619/19.726/741.480 ms
ping_C (1.1.1.1):     14.0% loss, rtt min/avg/max = 21.112/98.884/959.445 ms

networkQuality JSON summary (`networkQuality -I en0 -c -d`):
ul_mbps: 14.330
base_rtt_ms: 57.780
ul_responsiveness_rpm: 14.7  (4.094s)
```

So what: upload-only is catastrophic on Wi‑Fi (ul_responsiveness ~14.7 RPM) while also showing loss to the router/hop2 → Wi‑Fi upstream contention is a major culprit for interactive pain.

Now what: next step before SSH/LuCI is confirming whether the same upload-only collapse happens on Ethernet (it does, see 19:37), which isolates a second WAN-side queueing problem.

### Ethernet-only upload-only (2025-12-21 19:37)

```text
host: michael-pro
enabled_interfaces: WiFi=en0(off), BelkinUSBCLAN=en13(on)
default_route: 1.1.1.1 via gw=192.168.8.1 iface=en13
en13_ip: 192.168.8.235

ping_A (192.168.8.1):  0.0% loss, rtt min/avg/max = 0.690/1.342/20.235 ms
ping_B (192.168.1.1):  1.0% loss, rtt min/avg/max = 1.629/2.994/42.978 ms

ping_C (1.1.1.1):      0.5% loss, rtt min/avg/max = 15.787/53.928/285.982 ms

networkQuality JSON summary (`networkQuality -I en13 -c -d`):
ul_mbps: 17.967
base_rtt_ms: 61.048
ul_responsiveness_rpm: 17.4  (3.454s)
```

So what: Ethernet keeps LAN/gateway clean (near-zero loss to router/hop2), yet upload-only responsiveness is still very low (~17 RPM) → the remaining issue is **uplink/WAN queueing**, not the Mac↔Beryl cable.

Now what: this is the exact symptom SQM/CAKE is designed to fix; the next “separate HOWTO + ledger” experiment is enabling SQM on the true uplink interface and tuning rates.

### Direct-to-loco-station (Beryl bypass) — topology and hop map

```text
host: michael-pro
enabled_interfaces: WiFi=en0(inactive), BelkinUSBCLAN=en13(active)
default_route: 1.1.1.1 via gw=192.168.1.1 iface=en13
en13_ip: 192.168.1.221

traceroute to 1.1.1.1 (1.1.1.1), 6 hops max
 1  192.168.1.1
 2  72.31.129.125
 3  71.46.25.177
 4  72.31.119.184
 5  72.31.119.188
 6  66.109.6.42 / 66.109.9.114
```

So what: with Beryl removed, the gateway is now **192.168.1.1** and hop2 is **72.31.129.125**; the path is stable/low-latency at idle.

Now what: run the same full + upload-only `networkQuality` tests and compare ping-under-load to the gateway vs hop2 to see where queueing inflates.

### Direct-to-loco full (2025-12-21 20:29)

```text
host: michael-pro
enabled_interfaces: WiFi=en0(inactive), BelkinUSBCLAN=en13(active)
default_route: 1.1.1.1 via gw=192.168.1.1 iface=en13
en13_ip: 192.168.1.221
targets: A(gateway)=192.168.1.1 B(hop2)=72.31.129.125 C(inet)=1.1.1.1

ping_A_gw:   0.0% loss, rtt min/avg/max = 1.413/3.032/19.725 ms
ping_B_hop2: 1.4% loss, rtt min/avg/max = 6.336/35.371/253.247 ms
ping_C_inet: 0.9% loss, rtt min/avg/max = 16.023/45.947/387.692 ms

networkQuality JSON summary (`networkQuality -I en13 -c`):
dl_mbps: 72.394
ul_mbps: 19.345
base_rtt_ms: 63.314
responsiveness_rpm: 286.9  (0.209s)
```

So what: full-test responsiveness is **good (~287 RPM)** with Beryl bypassed → Beryl is not required for good responsiveness on wired traffic.

Now what: compare upload-only, because that’s where bufferbloat/queueing dominates.

### Direct-to-loco upload-only (2025-12-21 20:30)

```text
host: michael-pro
enabled_interfaces: WiFi=en0(inactive), BelkinUSBCLAN=en13(active)
default_route: 1.1.1.1 via gw=192.168.1.1 iface=en13
en13_ip: 192.168.1.221
targets: A(gateway)=192.168.1.1 B(hop2)=72.31.129.125 C(inet)=1.1.1.1

ping_A_gw:   0.0% loss, rtt min/avg/max = 1.352/2.685/55.426 ms
ping_B_hop2: 0.0% loss, rtt min/avg/max = 9.457/57.979/296.401 ms
ping_C_inet: 0.0% loss, rtt min/avg/max = 16.214/68.073/313.943 ms

networkQuality JSON summary (`networkQuality -I en13 -c -d`):
ul_mbps: 25.472
base_rtt_ms: 51.374
ul_responsiveness_rpm: 18.0  (3.329s)
```

So what: even with Beryl removed, upload-only responsiveness is still **very low (~18 RPM)** while ping to the local gateway stays clean → the bloated queue is **upstream of the gateway** (or at the gateway’s WAN edge), not on the Mac or the USB/Ethernet hop.

Now what: if we want to fix upload-only responsiveness without touching Moe’s router, the practical move is to reinsert Beryl as a **shaper** (Ethernet uplink) and enable SQM/CAKE; otherwise, the fix is upstream (Moe’s gateway QoS/SQM, or ISP-side behavior).

### Direct-to-loco baseline + direction split (2025-12-21 20:55–20:58)

```text
host: michael-pro
enabled_interfaces: WiFi=en0(inactive), BelkinUSBCLAN=en13(active)
default_route: 1.1.1.1 via gw=192.168.1.1 iface=en13
en13_ip: 192.168.1.221
hop2: 72.31.129.125

Baseline pings (no induced load):
gw (192.168.1.1):      0.0% loss, rtt min/avg/max = 1.369/2.218/17.013 ms
hop2 (72.31.129.125):  0.0% loss, rtt min/avg/max = 4.581/14.263/33.776 ms
inet (1.1.1.1):        0.0% loss, rtt min/avg/max = 15.361/25.511/58.319 ms

Upload-only under load (`networkQuality -I en13 -c -d`):
ul_responsiveness_rpm: 15.5  (3.877s)
gw ping:   0.0% loss, avg 2.709ms (max 79.724ms)
hop2 ping: 0.0% loss, avg 48.196ms (max 186.324ms)
inet ping: 0.0% loss, avg 57.984ms (max 195.361ms)

Download-only under load (`networkQuality -I en13 -c -u`):
dl_responsiveness_rpm: 588.3  (0.102s)
gw/hop2/inet: small loss (1.8–2.7%), modest RTT changes
```

So what: upload-only creates large latency inflation **after the gateway** (hop2/inet rise) while gateway RTT remains low → the queue/bottleneck sits at the gateway WAN edge or beyond (ISP), not on the local LAN.\n\nDownload-only behaves well (high RPM), so the pathological direction is upload.

Now what: the fastest non-invasive fix is to put a shaper you control (Beryl SQM/CAKE) *in front of* the gateway so the queue forms on the shaper, not at the gateway/ISP.

## Shaping numbers: what to type into SQM (pre-SQM summary)

This section translates the observed `networkQuality` **throughput** numbers into a conservative first-pass SQM configuration.

### Standard words (so we talk consistently)

- **Downlink / Download**: Internet → you (receive).
- **Uplink / Upload**: you → Internet (send). This is the direction that is currently pathological.
- **Measured throughput**: what `networkQuality` reported for capacity/throughput at that moment (Mbps).
- **Bottleneck rate**: the *lowest sustained* throughput you can rely on (use the low end of observed wired measurements, not the best-case peak).
- **Shaping rate** (SQM setting): the cap you configure (kbit/s) so the queue forms on your device (CAKE) instead of upstream.
- **Headroom**: the intentional reduction (typically 10–20%) so you stay below the true bottleneck.

Rule of thumb:

- Pick a **bottleneck rate** from the **low end** of your wired measurements.
- Set the SQM **shaping rate** to **80–90%** of that bottleneck rate.

### Observed wired throughput ranges (this repo session)

These are the wired numbers that matter for shaping (Wi‑Fi numbers are excluded because Wi‑Fi is a separate failure mode).

| Path / vantage point | Observed downlink (Mbps) | Observed uplink (Mbps) | Notes |
|---|---:|---:|---|
| Wired behind Beryl (en13, gateway `192.168.8.1`) | 77.354–82.804 | 12.602–17.967 | Includes full + upload-only runs |
| Beryl bypass (direct-to-loco, en13, gateway `192.168.1.1`) | 72.394–86.474 | 14.165–25.472 | Includes full + upload-only runs |

### Recommended starting SQM shaping rates (safe first pass)

Pick the conservative “bottleneck” values:

- **Uplink bottleneck (conservative)**: **12.6 Mbps** (lowest observed wired uplink)
- **Downlink bottleneck (conservative)**: **72.4 Mbps** (lowest observed wired downlink)

Then apply headroom (start at ~85%):

| Direction | Bottleneck basis (Mbps) | Headroom | Start shaping (Mbps) | Start shaping (kbit/s) |
|---|---:|---:|---:|---:|
| Uplink (upload) | 12.6 | 85% | 10.7 ≈ **11** | **11000** |
| Downlink (download) | 72.4 | 85% | 61.5 ≈ **62** | **62000** |

Practical tuning guidance:

- If responsiveness is still bad on upload: lower **uplink shaping** by another 10–15% and retest.
- If everything feels great but bandwidth feels unnecessarily capped: raise shaping in 0.5–1 Mbps steps.
- Keep the shaping rate below what you see at the worst times of day (the low end is what matters).

### End-of-day wrap (2025-12-21): SQM enabled + first tuning

What:

- Built a baseline with `networkQuality` + ping-under-load and proved topology/hops (Beryl `192.168.8.1` → Moe gateway `192.168.1.1`).
- Proved with Beryl bypass (Mac → loco-station) that upload-only responsiveness was still catastrophic while gateway RTT stayed low → upstream/WAN queueing was real.
- Enabled SQM/CAKE and debugged attachment issues:
  - SQM “started” on `eth0.2` but didn’t shape egress (tc showed `noqueue`).
  - Switching SQM to `eth0` produced an actual `qdisc cake ... bandwidth ...` on egress.
- Tuned upload shaping using repeated `networkQuality -d` runs (fast proxy for “Zoom + browsing under contention”).

So what:

- Pre-SQM we had two separate issues:
  - Wi‑Fi could collapse under load (loss/spikes even to the router), so Ethernet is the stable baseline.
  - Upload-only queueing lived beyond the LAN (gateway WAN edge / ISP), so shaping must be done on a device we control.
- SQM/CAKE is now genuinely active and enforcing a cap (confirmed by `tc` showing CAKE + overlimits/drops during load).
- Upload shaping around **7.5–8.0 Mbps** yields **Medium/High** uplink responsiveness (hundreds–thousands RPM) in repeated `networkQuality -d` runs.
- Overall “Responsiveness” can still show Low when the downlink side collapses during the combined test; direction-split showed upload-only High but download-only Low when downlink fell to ~3–6 Mbps (likely transient congestion/background downloads).

Now what:

- Keep today’s “working” settings as the baseline:
  - SQM interface: **`eth0`**
  - Qdisc/script: **CAKE + `piece_of_cake.qos`**
  - Upload shaping tried: **11000 → 8500 → 8000 → 7500** (best observed stability today: **8000**, fallback **7500**)
  - Download shaping: **62000** (may need to come down temporarily if `networkQuality -u` stays ~3–6 Mbps)
- Next steps to try later:
  - If downlink-only stays Low: temporarily set download shaping near observed bottleneck (e.g., **5000–12000 kbit/s**) to see if downlink responsiveness stabilizes.
  - Use `nettop` to identify background downloaders before downlink tests (avoid chasing transient contention).

## Next up (tomorrow): test directly on Moe’s Spectrum gateway (Ethernet)

Goal: determine whether the **downlink crater (~1–5 Mbps + Low RPM)** is coming from **Spectrum / Moe gateway side** versus our **PtP/Beryl/RV** path.

### Setup (lowest-risk)

- Plug `michael-pro` into Moe’s Spectrum gateway LAN via Ethernet/USB adapter.
- Disable Wi‑Fi (keep the test single-homed).
- Do **not** change any router settings; this is read-only measurement.

### Capture (copy/paste into a new raw-output block)

```bash
date '+%F %T'
route -n get 1.1.1.1 | egrep 'gateway:|interface:'
traceroute -n -m 2 1.1.1.1

# Primary metrics (direction split)
networkQuality -c -u
networkQuality -c -d

# Impairment check (idle)
ping -c 200 1.1.1.1
```

Optional (only if you want a “real app” proxy):

- Run a downlink load while watching latency:

```bash
ping -i 0.2 1.1.1.1
networkQuality -u
```

### Decision rules (what the results mean)

- If Moe-gateway Ethernet shows **normal downlink** (tens of Mbps) and decent loaded behavior:
  - The crater is likely **between gateway ↔ RV** (PtP alignment/interference, cable/power issues, Beryl path, or local contention).
- If Moe-gateway Ethernet also shows **~1–5 Mbps downlink** and/or high idle latency:
  - It’s an **upstream Spectrum / gateway / node** event. Local tuning won’t “fix” bandwidth; keep SQM upload shaping for Zoom stability and wait/escalate to ISP if persistent.

### What to log

- Add a new table row with `link=Ethernet(on_Moe_gateway)` and `hop2` from traceroute.
- Include the `networkQuality -c` JSON blobs in the raw section so we can compare apples-to-apples.
