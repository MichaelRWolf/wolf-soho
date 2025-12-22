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

### Snapshot: observations (as of 2025-12-21 19:37)

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

## Raw outputs (optional, paste blocks)

### Context header format (for every chunk)

```text
host: <michael-pro|wolf-air>
enabled_interfaces: <example: WiFi=en0(on), BelkinUSBCLAN=en13(off)>
default_route: <example: 1.1.1.1 via gw=192.168.8.1 iface=en0>
```

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
