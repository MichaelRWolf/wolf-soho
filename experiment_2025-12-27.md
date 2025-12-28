# Experiment: 2025-12-27

## Notes

### ~13:20 — Begin tuning during Collette seminar

What:

- `networkQuality` (user-reported): 8 down, 23 up
- SQM reset (user action): download=10000 kbit/s, upload=6400 kbit/s
- `bin/beryl_sqm` output after reset:

```text
=== SQM section (and interface) ===
eth1
sqm.eth1.interface='eth0'

=== Speed Limits ===
Download: 10000 (  156% of upload)
Upload:    6400 (   64% of download)

=== Shaping (ifb4eth0 / download, if present) ===
qdisc cake 8011: root refcnt 2 bandwidth 10Mbit besteffort triple-isolate nonat wash no-ack-filter split-gso rtt 100.0ms noatm overhead 0
 Sent 44288486 bytes 59397 pkt (dropped 64, overlimits 46386 requeues 0)
 backlog 123b 1p requeues 0
  pk_delay        8.0ms
  av_delay        2.4ms
  drops              64

=== Shaping (eth0 / upload) ===
qdisc cake 8010: root refcnt 2 bandwidth 6400Kbit besteffort triple-isolate nonat nowash no-ack-filter split-gso rtt 100.0ms noatm overhead 0
 Sent 1830909 bytes 10084 pkt (dropped 13, overlimits 2885 requeues 0)
 backlog 0b 0p requeues 0
  pk_delay        8.5ms
  av_delay        1.2ms
  drops              13
 Sent 43649685 bytes 59659 pkt (dropped 0, overlimits 0 requeues 0)
 backlog 0b 0p requeues 0
```

- `networkQuality -fh1`:

```text
==== SUMMARY ====
Uplink capacity: 19.856 Mbps
Downlink capacity: 7.090 Mbps
Responsiveness: High (46.815 milliseconds | 1281 RPM)
Idle Latency: 49.369 milliseconds | 1215 RPM
```

- Symptom: Zoom incoming gets choppy; user observed an apparent 1000–2000ms “break in download”.
- Observation during symptom: trying to run `bin/beryl_sqm` in status mode “freezes” (does not start) until the Zoom freeze ends.

So what:

- The experienced stall is not showing up in CAKE `av_delay`/`pk_delay` at the moment it’s checked (at least via `tc -s qdisc` sampling).
- When the stall is present, even SSH to Beryl can be delayed, so any “after the fact” CAKE snapshot may miss the event.

Now what:

- Apply more conservative SQM as a test: `bin/beryl_sqm 6000 6400`.
- During the next freeze, run concurrent pings (LAN + internet) to determine whether the stall is local (Mac↔Beryl) or upstream.

### ~13:3x — Apply SQM 6000/6400 (immediately after)

What:

- Applied SQM shaping: download=6000 kbit/s, upload=6400 kbit/s
- `bin/beryl_sqm` output immediately after:

```text
=== SQM section (and interface) ===
eth1
sqm.eth1.interface='eth0'

=== Speed Limits ===
Download:  6000 (   93% of upload)
Upload:    6400 (  106% of download)
⚠️ WARNING: download less than upload

=== Shaping (ifb4eth0 / download, if present) ===
qdisc cake 8015: root refcnt 2 bandwidth 6Mbit besteffort triple-isolate nonat wash no-ack-filter split-gso rtt 100.0ms noatm overhead 0 
 Sent 1331770 bytes 1754 pkt (dropped 2, overlimits 1472 requeues 0) 
 backlog 2733b 3p requeues 0
  pk_delay        9.7ms
  av_delay        3.2ms
  drops               2

=== Shaping (eth0 / upload) ===
qdisc cake 8014: root refcnt 2 bandwidth 6400Kbit besteffort triple-isolate nonat nowash no-ack-filter split-gso rtt 100.0ms noatm overhead 0 
 Sent 39738 bytes 229 pkt (dropped 1, overlimits 26 requeues 0) 
 backlog 0b 0p requeues 0
  pk_delay        4.6ms
  av_delay        179us
  drops               1
 Sent 1443298 bytes 1929 pkt (dropped 0, overlimits 0 requeues 0) 
 backlog 0b 0p requeues 0
```

- `networkQuality` summary immediately after:

```text
==== SUMMARY ====
Uplink capacity: 14.385 Mbps
Downlink capacity: 4.117 Mbps
Responsiveness: Medium (69.692 milliseconds | 860 RPM)
Idle Latency: 48.437 milliseconds | 1238 RPM
```

- Symptom update: still experiencing ~1000–2000ms gaps (but not ~4000ms).

So what:

- This setting appears to reduce worst-case stalls (tentative), but does not eliminate the 1–2s gaps.
- Downlink measured by `networkQuality` is very low (~4.1 Mbps) at this moment; a higher downlink shaper would not have controlled the bottleneck.

Now what:

- During the next observed gap, run `ping 192.168.8.1` and `ping 1.1.1.1` concurrently to determine whether the gap is LAN-local or upstream.

### 14:37 — gping shows RTT spikes (not multi-second), but Zoom feels multi-second

What:

- Used `gping` (instead of `ping`) to track RTT to:
  - `192.168.8.1` (Beryl LAN)
  - `1.1.1.1` (internet)
- Graph window shows spikes into the ~150–300ms range for `1.1.1.1` (and smaller spikes to Beryl).
- `gping` stats in the graph (approx):
  - `192.168.8.1`: last ~2.3ms, min ~1.5ms, max ~135ms
  - `1.1.1.1`: last ~36ms, min ~17ms, max ~155ms
- Subjective experience during Zoom: “freezes” feel like 1000s of ms (1–2s gaps), not 100s of ms.

So what:

- RTT graphs can look “fine” even when an app experiences multi-second stalls:
  - Short control packets (ICMP ping) may not share the same bottleneck as sustained downlink video/media.
  - Multi-second “gaps” are often packet loss / delivery pauses, not just elevated RTT; depending on tool settings, loss can show up as missing points rather than a 1000ms value.

Now what:

- Adjust the probe so it can reveal gaps/loss more clearly (higher frequency, larger payload), and capture loss explicitly.

### 14:43:24–14:43:54 — gping stats snapshot (timeouts present)

What:

- `gping` running against:
  - `192.168.8.1` (Beryl)
  - `1.1.1.1` (internet)
- Screenshot stats (as shown by `gping`):
  - `192.168.8.1`: last 2.24ms, min 1.573ms, max 202.133ms, avg 8.482ms, jtr 1.671ms, p95 56.808ms, t/o 29
  - `1.1.1.1`: last 29.136ms, min 17.134ms, max 145.973ms, avg 30.256ms, jtr 1.082ms, p95 86.819ms, t/o 28

So what:

- Even though max RTT is only ~150–200ms, the presence of **many timeouts** means there are genuine delivery gaps; those gaps are a better match for “Zoom freezes feel like seconds” than RTT alone.

Now what:

- Correlate the exact timeout moments with a Zoom freeze (if possible) and determine whether timeouts hit `192.168.8.1` (LAN/local) at the same time as `1.1.1.1` (upstream).

### ~14:4x — Ping shows ~4s break (timeouts burst)

What:

- Screenshot shows a timeout burst (target in that screenshot was later clarified as `1.1.1.1`, not `192.168.8.1`):
  - `Request timeout for icmp_seq` 172–187
  - Replies resume at `icmp_seq=188` (first reply shown: ~30.131ms), then typically returns to ~2–4ms
- Additional loss moments observed (user note):
  - next loss at seq 400
  - then seq 629–649
  - then seq 845–868

So what:

- This is consistent with “multi-second gaps” being **timeouts/loss**, not huge RTT values.
- Timeouts to an internet target alone do **not** imply LAN/local problems; need a concurrent LAN target (`192.168.8.1`) to attribute where the gap originates.

Now what:

- If this was on Wi‑Fi, repeat the same test on Ethernet-only (Wi‑Fi disabled) to see whether LAN timeouts persist; that cleanly separates Wi‑Fi contention from upstream impairment.

### ~14:5x — Concurrent ping shows gaps to 1.1.1.1 and 192.168.8.1 at the same time

What:

- User observation while running both targets:
  - When there's a gap/timeouts to `1.1.1.1`, there is also a gap/timeouts to `192.168.8.1` (about the same duration).
  - Sometimes `1.1.1.1` stops first, but both resume at the same time.

So what:

- Gaps affecting `192.168.8.1` point to a **local issue** (Mac↔Wi‑Fi, Wi‑Fi airtime/interference, Mac network stack stall, or router responsiveness), not purely upstream ISP impairment.
- This also explains why CAKE `av_delay`/`pk_delay` can look normal: during a local stall, packets may not reach the shaper at all (no queueing to measure).

Now what:

- Repeat the concurrent ping test on **Ethernet-only** (disable Wi‑Fi entirely) to see if LAN gaps disappear; if they do, it’s Wi‑Fi/airtime. If they persist, investigate router CPU/load or a broader local network stall.

### ~15:0x — Switch to Ethernet-only; Belkin+blue cable fails; Anker+black cable works

What:

- Attempted Ethernet-only using previously-used gear:
  - Belkin USB Ethernet adapter
  - blue Ethernet cable
- Result: not working today (consistent with prior suspicion).
- Swapped to different gear:
  - Anker USB Ethernet adapter
  - black Ethernet cable
- Result: works.
- Anker adapter LEDs: solid red, solid green, flashing blue.

So what:

- Belkin adapter and/or blue cable is unreliable; treat as “dead for now” and exclude from experiments to avoid confusing results.

Now what:

- Continue Ethernet-only tests using Anker+black cable as the known-good baseline.

### ~15:xx — Two-client observation: wolf-air-only gaps (Wi‑Fi suspect)

What:

- Setup:
  - wolf-air: Wi‑Fi, pinging `192.168.8.1` and `1.1.1.1`
  - michael-pro: pinging `192.168.8.1` and `1.1.1.1` at the same time
- Observations:
  - wolf-air gaps (both targets): seq 1039–1062
  - wolf-air gaps (both targets): seq 1324–1352
  - wolf-air gaps (both targets): seq 2175–2196
  - michael-pro: no corresponding gaps observed during those windows

So what:

- This points strongly toward a Wi‑Fi/client-side issue affecting wolf-air (airtime/interference/driver/power-save/roam), rather than an upstream impairment that would hit both machines at the same time.

Now what:

- Confirm from Beryl’s perspective by pinging each client from Beryl at the same time, and by collecting per-station Wi‑Fi stats (signal, bitrate, retries, disconnects) during a gap.

### ~15:xx — Beryl can’t ping wolf-air, but TCP/SSH is reachable

What:

- From Beryl:
  - Can ping michael-pro.
  - Cannot ping wolf-air.
  - `nc` to wolf-air indicates host is reachable (TCP works).
- On wolf-air: firewall reported “off”.

So what:

- This suggests ICMP echo requests/replies are being dropped/ignored for wolf-air specifically (or are being filtered on the path), while general IP connectivity remains OK.
- For “watching from Beryl”, do not rely on `ping` alone; use Wi‑Fi station stats and packet captures to observe the link.

Now what:

- Use `tcpdump` on Beryl during a `ping` attempt to confirm whether ICMP replies return.

### ~15:xx — Beryl stays healthy while wolf-air (Wi‑Fi) drops; `iw dev` returned no output

What:

- Environment:
  - Only 2.4 GHz Wi‑Fi in use (no 5 GHz).
- Observation:
  - When wolf-air (Wi‑Fi) stops seeing `192.168.8.1` and `1.1.1.1`, Beryl can still reach michael-pro on Ethernet during the same window.
  - This points away from “Beryl is wedged” and toward “wolf-air Wi‑Fi link/client is stalling”.
- Attempted on Beryl: `iw dev` produced no output (empty).

So what:

- If Beryl can still communicate with an Ethernet client while a single Wi‑Fi client is stalling, the offender is likely the Wi‑Fi link (airtime/interference/AP↔client) or wolf-air’s Wi‑Fi stack, not upstream ISP and not general router CPU collapse.
- Since `iw dev` didn’t help, use OpenWrt-native interfaces (`iwinfo`, `wifi status`, `ubus`) to inspect wireless state.

Now what:

- On Beryl, use `ip link`/`iwinfo`/`ubus` to identify the active Wi‑Fi interface and collect per-station stats during a stall.

### ~15:xx — Beryl wireless status: 5GHz AP on `ra0`, uplink STA on `apclix0` (2.4GHz); `iw dev` empty

What:

- Beryl reports OpenWrt `19.07.8`.
- Tools present:
  - `/usr/sbin/iw` (5.0.1) but `iw dev` returned no output.
  - `/usr/bin/iwinfo` present and reports multiple wireless ifnames.
- `iwinfo` / `wifi status` highlights (selected):
  - `ra0`: **Mode: Master (AP)**, SSID `"Running Wolf Router - 5G"`, Channel 44 (5.220 GHz), Type `mtk`, HW `MT7615E`.
  - `apclix0`: **Mode: Client (STA)**, SSID `"Running Wolf Hot Spot"`, Channel 7 (2.442 GHz), network `wwan`.
- `ip -br link` shows `ra0` and `br-lan` UP; `apclix0` shows `NO-CARRIER` and `UP` (interface exists but link state may flap).
- Follow-up correction (user): “Running Wolf Hot Spot” is not powered on (battery removed). Beryl is connected by Ethernet to the PtP radio for upstream.

So what:

- `apclix0` appears to be configured as a STA in config, but with the hotspot unpowered and `NO-CARRIER`, it’s likely not an active uplink (stale config / down link).
- There *is* a 5 GHz AP on Beryl (`ra0`) per `iwinfo` output; verify which band wolf-air is actually associated to from the client side.
- `iw dev` being empty suggests this build/driver stack may not expose nl80211 interfaces in the way `iw` expects; for station visibility, prefer `iwinfo` + `ubus`.

Now what:

- Use `iwinfo ra0 assoclist` (and `logread -f`) during a gap to see if wolf-air’s station entry shows rate drops / retries / disassoc events.

### ~14:4x — Ping to 1.1.1.1 shows 1–2s late replies after timeouts (1208-byte payload)

What:

- Screenshot shows a long timeout run:
  - `Request timeout for icmp_seq` 174–204
- Then late replies arrive for earlier sequence numbers with large `time=` values (selected lines shown):
  - `icmp_seq=196 time=1980.060 ms`
  - `icmp_seq=197 time=1776.117 ms`
  - `icmp_seq=198 time=1574.735 ms`
  - `icmp_seq=199 time=1369.763 ms`
  - `icmp_seq=200 time=1168.898 ms`
  - `icmp_seq=201 time=968.406 ms`
  - `icmp_seq=202 time=767.157 ms`
  - `icmp_seq=203 time=562.411 ms`
- Additional gap ranges observed afterwards (user note):
  - seq 390–425
  - seq 629–649

So what:

- This captures the “1000s of ms” directly: packets are either not delivered for multiple seconds (timeouts), or delivered so late that the app effectively experiences a stall.
- The “late replies after timeout” pattern suggests the path is intermittently stalling/buffering, not merely adding 100–200ms jitter.

Now what:

- Run the same style of ping simultaneously to `192.168.8.1` and `1.1.1.1` (same interval/payload) to see whether the multi-second behavior also hits LAN, or only WAN.

### ~15:xx — Assertion: offender is Wi‑Fi leg (client/AP/airtime), not PtP/ISP

What:

- Working assertion for the rest of this experiment session:
  - The primary offender causing 1–2s (sometimes ~4s) stalls is on the Wi‑Fi leg (wolf-air client, Beryl AP, or 5 GHz airtime), not the PtP/ISP/internet path.

Evidence (so far):

- Beryl → internet (`1.1.1.1`) shows no gaps when tested from Beryl, even while Wi‑Fi clients experience 2000–2500ms stalls.
- Beryl → NAS path that requires Wi‑Fi traversal can show sequence gaps (even if `ping` output doesn’t print explicit “timeout” lines every time).
- wolf-air over Wi‑Fi shows gaps to both `192.168.8.1` and `1.1.1.1`.
- michael-pro over Ethernet remains fine during the same windows where wolf-air shows gaps.
- Two-client test: wolf-air-only gaps (both targets) with no corresponding gaps on michael-pro.
- Concurrent ping test: when `1.1.1.1` gaps, `192.168.8.1` also gaps; both resume together.

Now what:

- During a captured gap, collect Beryl-side Wi‑Fi telemetry to distinguish “wolf-air client” vs “AP/airtime”:
  - `iwinfo ra0 assoclist`
  - `logread -f | egrep -i 'hostapd|wlan|wifi|deauth|disassoc|disconnect|sta'`

### 16:53–16:56 — Beryl kernel logs show DFS/CAC “Enable MAC TX” events during stalls

What:

- Symptom: Beryl-side “watch loops” (run via `ssh root@beryl ...` from michael-pro) pause for ~4000–5000ms, then resume with normal output; “bad output” is hard to capture because the whole loop stops during the stall.
- During each stall/resume window, `logread -f` emits a new block of kernel warnings (pasted):

```text
Sat Dec 27 16:53:40 2025 kern.warn kernel: [ 5851.654123] [DfsCacNormalStart] Normal start. Enable MAC TX
Sat Dec 27 16:53:40 2025 kern.warn kernel: [ 5851.679420] Start Seq = 00000a0d
Sat Dec 27 16:53:40 2025 kern.warn kernel: [ 5851.686368] Start Seq = 00000061
Sat Dec 27 16:53:40 2025 kern.warn kernel: [ 5851.791205] Start Seq = 00000933
Sat Dec 27 16:53:41 2025 kern.warn kernel: [ 5852.054638] Start Seq = 00000e60
Sat Dec 27 16:54:25 2025 kern.warn kernel: [ 5896.860539] [DfsCacNormalStart] Normal start. Enable MAC TX
Sat Dec 27 16:54:26 2025 kern.warn kernel: [ 5897.115897] Start Seq = 00000012
Sat Dec 27 16:54:26 2025 kern.warn kernel: [ 5897.123022] Start Seq = 00000f28
Sat Dec 27 16:54:26 2025 kern.warn kernel: [ 5897.642381] Start Seq = 00000371
Sat Dec 27 16:54:26 2025 kern.warn kernel: [ 5897.697078] Start Seq = 00000adf
Sat Dec 27 16:54:26 2025 kern.warn kernel: [ 5897.704215] Start Seq = 00000bd3
Sat Dec 27 16:54:29 2025 kern.warn kernel: [ 5900.787976] Start Seq = 00000bf1
Sat Dec 27 16:55:10 2025 kern.warn kernel: [ 5942.028442] [DfsCacNormalStart] Normal start. Enable MAC TX
Sat Dec 27 16:55:13 2025 kern.warn kernel: [ 5944.217927] Start Seq = 00000931
Sat Dec 27 16:55:55 2025 kern.warn kernel: [ 5986.581797] [DfsCacNormalStart] Normal start. Enable MAC TX
Sat Dec 27 16:55:56 2025 kern.warn kernel: [ 5987.217233] Start Seq = 000001eb
Sat Dec 27 16:55:56 2025 kern.warn kernel: [ 5987.223968] Start Seq = 00000763
Sat Dec 27 16:55:56 2025 kern.warn kernel: [ 5987.770443] Start Seq = 0000091b
Sat Dec 27 16:56:13 2025 kern.warn kernel: [ 6004.751374] Start Seq = 000007b7
Sat Dec 27 16:56:13 2025 kern.warn kernel: [ 6004.758379] Start Seq = 00000ff2
```

So what:

- These look like the Wi‑Fi driver is repeatedly transitioning through a DFS/CAC-related state (or radio restart) and re-enabling TX.
- That would plausibly cause brief, periodic “everyone on Wi‑Fi pauses for a few seconds” events while Ethernet clients remain fine.

Now what:

- Confirm whether these log bursts correlate 1:1 with the observed ping gaps on wolf-air (and/or NAS-over-Wi‑Fi).
- Identify the active AP interface and channel at the moment of the events (and whether the AP is on a DFS channel).

### 16:57:37 — “All good” snapshot: `iwinfo ra0 assoclist`

What:

```text
Sat Dec 27 16:57:37 EST 2025
D6:A2:15:0B:FF:4E  -71 dBm / -95 dBm (SNR 24)  5475000 ms ago
 RX: 450.0 MBit/s                               16098 Pkts.
 TX: 450.0 MBit/s                               36755 Pkts.
 expected throughput: unknown

10:94:BB:E8:88:D4  -52 dBm / -95 dBm (SNR 43)  1209000 ms ago
 RX: 450.0 MBit/s                              401105 Pkts.
 TX: 450.0 MBit/s                              869055 Pkts.
 expected throughput: unknown

4A:6B:0C:7A:A4:53  -60 dBm / -95 dBm (SNR 35)  5452000 ms ago
 RX: 450.0 MBit/s                               11587 Pkts.
 TX: 450.0 MBit/s                               16037 Pkts.
 expected throughput: unknown

CE:F8:B8:B9:0C:C8  -56 dBm / -95 dBm (SNR 39)  5447000 ms ago
 RX: 450.0 MBit/s                              745439 Pkts.
 TX: 450.0 MBit/s                             3174936 Pkts.
 expected throughput: unknown
```

So what:

- Next step is to map these MACs to actual hostnames/IPs (`/tmp/dhcp.leases`, `ip neigh`) so we can watch wolf-air’s specific station entry during a stall.

### ~17:0x — wolf-air NSS/MCS/Tx rate fluctuate; NAS turned off

What:

- Observation source: macOS Wi‑Fi menu (Option-click) on wolf-air.
- NSS flips between 1 and 2:
  - When NSS=1: MCS ~4–5 and Tx rate ~50–450 Mbps.
  - When NSS=2: MCS ~9 and Tx rate ~700+ Mbps.
- This 1↔2 behavior does not appear to correlate with outages or ping spikes.
- NAS was still on during earlier tests; NAS is now turned off to remove it as a confounder.

So what:

- NSS/MCS/Tx rate changes can be normal rate adaptation; the lack of correlation suggests it is not the primary driver of the multi-second stalls.
- Turning off the NAS is a good control to rule out local LAN traffic causing airtime starvation.

Now what:

- Re-run the “wolf-air pinging 192.168.8.1 + 1.1.1.1” test with NAS off and note whether gaps still occur.

### 17:49 — Change: force 5 GHz AP to channel 36 @ 40 MHz (avoid DFS/CAC churn)

What:

- In LuCI (`/cgi-bin/luci/admin/network/wireless`), changed the 5 GHz AP settings:
  - Channel width: 40 MHz
  - Channel: 36 (from 44)
- Motivation: repeated kernel warnings `[DfsCacNormalStart] Normal start. Enable MAC TX` were occurring roughly every ~45–50 seconds and appeared correlated with multi-second Wi‑Fi stalls.

So what:

- This is a causality test: if DFS/CAC/radio state churn is driving the 4–5s gaps, forcing a stable non-DFS channel/width should reduce or eliminate the stalls (and the log spam).

Now what:

- Validate:
  - On wolf-air: continue pinging `192.168.8.1` and `1.1.1.1` and note whether multi-second gaps persist.
  - On Beryl: confirm channel and check for DFS/CAC log lines:
    - `iwinfo ra0 info`
    - `logread | tail -n 200 | egrep -i 'DfsCac|dfs|cac|radar|Enable MAC TX'`

### 17:49–17:50 — Post-change: DFS/CAC log spam persists (~45s cadence) and gaps still occur

What:

- After forcing channel 36 @ 40 MHz, Beryl continues emitting `[DfsCacNormalStart] Normal start. Enable MAC TX` roughly every ~45 seconds.
- Observed gap (user note): seq 0390–0405.
- Sample logs after the 17:49 change (pasted):

```text
Sat Dec 27 17:49:19 2025 kern.warn kernel: [ 9190.286535] [DfsCacNormalStart] Normal start. Enable MAC TX
Sat Dec 27 17:49:19 2025 kern.warn kernel: [ 9190.482328] Start Seq = 0000004b
Sat Dec 27 17:49:20 2025 kern.warn kernel: [ 9191.433789] wifi_sys_open(), wdev idx = 13
Sat Dec 27 17:49:20 2025 kern.warn kernel: [ 9191.475419] Caller: wlan_operate_init+0xf4/0x108 [mt_wifi]
Sat Dec 27 17:49:20 2025 kern.warn kernel: [ 9191.540562] Start Seq = 00000000
Sat Dec 27 17:49:22 2025 kern.warn kernel: [ 9193.380279] Start Seq = 00000576
Sat Dec 27 17:50:04 2025 kern.warn kernel: [ 9235.540197] [DfsCacNormalStart] Normal start. Enable MAC TX
Sat Dec 27 17:50:04 2025 kern.warn kernel: [ 9235.560889] Start Seq = 000000c7
Sat Dec 27 17:50:06 2025 kern.warn kernel: [ 9237.043889] Start Seq = 000004a5
Sat Dec 27 17:50:06 2025 kern.warn kernel: [ 9237.050696] Start Seq = 0000005d
Sat Dec 27 17:50:22 2025 kern.warn kernel: [ 9253.061820] Start Seq = 00000304
Sat Dec 27 17:50:44 2025 user.notice mtk-wifi: new_station ce:f8:b8:b9:0c:c8 ra0
Sat Dec 27 17:50:44 2025 kern.warn kernel: [ 9275.324998] Start Seq = 00000000
Sat Dec 27 17:50:44 2025 kern.warn kernel: [ 9275.608606] Start Seq = 00000002
Sat Dec 27 17:50:44 2025 kern.warn kernel: [ 9275.820449] Start Seq = 00000000
Sat Dec 27 17:50:49 2025 kern.warn kernel: [ 9280.708185] [DfsCacNormalStart] Normal start. Enable MAC TX
Sat Dec 27 17:50:49 2025 kern.warn kernel: [ 9280.723291] Start Seq = 00000146
Sat Dec 27 17:50:50 2025 kern.warn kernel: [ 9281.066073] Start Seq = 00000876
Sat Dec 27 17:50:50 2025 kern.warn kernel: [ 9281.074253] Start Seq = 00000418
Sat Dec 27 17:50:52 2025 kern.warn kernel: [ 9283.725772] Start Seq = 000000c9
Sat Dec 27 17:50:53 2025 kern.warn kernel: [ 9284.561304] Start Seq = 000001c4
Sat Dec 27 17:50:53 2025 kern.warn kernel: [ 9284.568721] Start Seq = 00000047
```

So what:

- Channel 36 is normally non-DFS, so repeated “DfsCacNormalStart” at a steady cadence suggests either:
  - the driver is using this message for a broader “radio restarted / TX re-enabled” event (not strictly DFS radar handling), or
  - the AP is not actually staying on the intended channel/width, or
  - the device is repeatedly reinitializing the Wi‑Fi subsystem (`wifi_sys_open` / `wlan_operate_init`).

Now what:

- Verify the radio is truly on channel 36 @ 40 MHz (`iwinfo ra0 info` should show the channel).
- If the spam persists on 36, test another non-DFS channel family (e.g. 149 @ 40 MHz) to see if behavior changes.

### ~18:0x — Channel experiments: CAC/DFS spam persists on 36; 149 unusable; reverting to 44

What:

- Observation: `DfsCacNormalStart` messages continue on channel 36 (reported as “35/36”).
- Attempted channel 149:
  - wolf-air was unable to connect (prompted for password; did not connect successfully).
- Next step: revert to channel 44 (known-working association) to keep testing while investigating the periodic radio/TX reset behavior.

So what:

- Persistence of `DfsCacNormalStart` on a non-DFS channel strengthens the hypothesis that this message is effectively “radio TX re-enabled / Wi‑Fi subsystem restart,” not true DFS radar handling.
- Inability to use 149 suggests a regulatory/driver limitation or a configuration mismatch (but not the primary cause of the periodic resets).

Now what:

- On channel 44, continue correlating ping gaps with the `DfsCacNormalStart` log bursts and look for any accompanying netifd/hostapd/mtk-wifi reset messages.
