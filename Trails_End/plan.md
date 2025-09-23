<!-- markdownlint-disable MD013 -->
# Trails End Uplink Stabilization — Action Plan

This plan ties together the two playbooks and sequences **what to observe** and **what to do**, with clear decision gates and rollback.

Related docs:

- **remediation_macos** (macOS Stabilization Playbook)
- **remediation_beryl** (Beryl Stabilization Playbook)

---

## 0) Assumptions

- You will connect your Mac only to the **Beryl SSID** (not the campground SSID) during tests.
- You have the repo tools installed: `uplink-short`, `uplink-describe`, `uplink-monitor`.
- Goal success criteria (target): **RPM ≥ 200** during busy hours; no Zoom freezes; no Cursor timeouts mid‑think.

---

## 1) Observe First (Instrument for 48–72 hours)

### Uplink Identity & Path

- [ ] Start continuous logging (5‑minute cadence):
  - `./uplink-monitor ~/uplink_log.txt 300`
- [ ] Take detailed snapshots when you notice issues:
  - `./uplink-describe` (appends traceroute to log)

### Responsiveness (Apple `networkQuality`)

- [ ] Run every 15 minutes via launchd (see **remediation_macos**): logs RPM & idle latency to `~/nq.log`.
- [ ] Manual spot checks before/after known issues:
  - `networkQuality -v`

### Path Health (`mtr`)

- [ ] 1–2 live runs per session when issues appear:
  - `sudo mtr -ezbw -i 1 -c 60 1.1.1.1`
- [ ] Note whether first public hop loss/RTT spikes coincide with freezes.

### Correlate

- [ ] Mark Zoom/Cursor event timestamps (freezes, timeouts).
- [ ] After two days, correlate logs: Pasty vs Starlink periods; RPM lows; `mtr` spikes.

**Decision Gate A:** If most problems align with **Starlink periods** or **handoff‑style 10–60 s stalls**, proceed to Step 2 (Do). If problems are LAN‑side (hop 1), fix Wi‑Fi placement first.

---

## 2) Do — High‑Impact Changes (Apply, then re‑observe 24–48 hours)

### Beryl (Primary lever — see **remediation_beryl**)

1. **Enable SQM/CAKE** on the WAN uplink (`wlan-sta`/`wwan0`).
   - Rates: ~85–90% of stable lows (e.g., 13 Mbps down, 5.2 Mbps up).
   - Options: `diffserv4`, per‑host isolation on.
2. **Validate** with `tc -s qdisc` (counters incrementing sensibly).
3. **Re‑run observation** (Step 1) for another day.

**Decision Gate B:** If RPM improves ≥ 200 and Zoom/Cursor stabilize → keep settings. If RPM < 200 or Zoom still freezes, lower SQM rates by another 10–15% and retest.

### macOS (Supportive levers — see **remediation_macos**)

4. **TCP keepalive test profile** (temporary; rollback script ready).
5. **DNS** set to 1.1.1.1 or 8.8.8.8.
6. **Disable VPN** during calls, or switch to **WireGuard** if required.
7. **Wi‑Fi hygiene**: 5 GHz, close to Beryl, disable auto‑join to campground SSID.

**Decision Gate C:** If handoff stalls still cause disconnects despite SQM and keepalives, accept that 20–60 s blackouts are not maskable — focus on detection/avoidance.

---

## 3) Optional Enhancements

- **Router telemetry**: `luci-app-statistics` (collectd graphs), `mtr` on Beryl, watchcat alerts.
- **Smokeping** on Beryl for long‑term jitter/loss graphs.
- **Launchd** job for `networkQuality` with log rotation.

---

## 4) Rollback & Safety

- **Beryl**: disable SQM in LuCI (*Services → SQM QoS → Disable*). Keep a LuCI backup snapshot after each stable config.
- **macOS**: run `tcp_keepalive_reset.sh` or reboot to clear sysctl changes.

---

## 5) Weekly Review Checklist

- [ ] RPM median and 95th‑percentile; goal ≥ 200 median.
- [ ] Count of Starlink vs Pasty periods; fraction of incidents per uplink.
- [ ] Zoom: any audio‑only fallbacks or reconnects?
- [ ] Cursor: any mid‑think timeouts? timestamp & uplink at that time.
- [ ] SQM rates tuned to the lowest stable bandwidth seen that week.

---

## 6) Escalation Path

- If issues occur **only during Starlink windows** and are frequent:
  - Provide campground with timestamps + logs indicating handoff stalls.
  - Suggest pinning guests to the **Pasty uplink** during high‑value calls (policy routing) or scheduling critical calls during historically stable windows.

---

## 7) Quick Reference — What Good Looks Like

- **RPM ≥ 200**, idle latency ≈ 50–90 ms.
- `mtr` shows minimal loss on early hops; no >5 s total stalls.
- Zoom has stable audio/video; Cursor sessions do not timeout mid‑think.
