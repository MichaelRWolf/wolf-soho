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
