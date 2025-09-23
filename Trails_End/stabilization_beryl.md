<!-- markdownlint-disable MD013 -->
# Beryl Stabilization Playbook (formerly "Remediation")

> Goal: shape queues and improve resilience to jitter/blackouts when the campground flips between Pasty and Starlink.

---

## A. Prep

- Connect Mac to **Beryl SSID** (not campground SSID).
- SSH to Beryl (default `root@192.168.8.1`).
- Update package lists:

  ```bash
  opkg update
  ```

---

## B. Enable SQM with CAKE

> This is the single highest‑impact change.

1. **Install SQM UI & daemon**

   ```bash
   opkg install luci-app-sqm sqm-scripts
   ```

2. **Interface**: set to the **WAN uplink** the Beryl uses to reach the campground AP (often `wlan-sta` or `wwan0`).
3. **Queue discipline**: `cake` (default).
4. **Bandwidth**: set to \~85–90% of your *stable* low‑end rates:
   - Downlink: if you see 15 Mbps → set **13 Mbps**.
   - Uplink: if you see 6 Mbps → set **5.2 Mbps**.
5. **Advanced**:
   - **Per‑host isolation**: *on* (fairness).
   - **DiffServ**: `diffserv4` (prioritize interactive/VoIP/gaming).
   - **ACK/ECN**: leave ECN off initially; enable later if stable.
6. **Save & Apply** via LuCI: *Services → SQM QoS*.

Validate

```bash
tc -s qdisc show dev $(route -n | awk '/UG/ {print $8; exit}')
```

Look for `qdisc cake` counters increasing, and drops/marks not exploding.

---

## C. Instrumentation on Router (recommended)

- **Statistics & graphs**

  ```bash
  opkg install luci-app-statistics collectd-mod-ping collectd-mod-rrdtool
  ```

  LuCI → *Statistics → Graphs*: add pings to `1.1.1.1`, `8.8.8.8`, and the **first upstream hop**.

- **mtr on the router** (clean vantage point)

  ```bash
  opkg install mtr
  mtr -ezbw -i 1 1.1.1.1
  ```

- **Watchdog (optional)**

  ```bash
  opkg install luci-app-watchcat
  ```

  Use to log/alert on extended outages (don’t auto‑reboot unless necessary).

- **Smokeping (optional, heavier)**

  ```bash
  opkg install smokeping
  ```

---

## D. Uplink Selection Awareness

- Keep the macOS scripts (`uplink-short`, `uplink-describe`, `uplink-monitor`) running.
- If you want the **router** to log uplink flips, adapt those scripts in `/root/` and run from cron.

---

## E. Wi‑Fi Backhaul Tips

- **Positioning**: place Beryl where it gets the strongest campground AP signal.
- **5 GHz preferred** to upstream AP (if CG AP supports it); otherwise 2.4 GHz with least‑used channel.
- **Avoid double‑NAT churn** beyond necessity; Beryl as simple client/repeater is fine.

---

## F. Troubleshooting Flow

1. \`\`\*\* shows loss at hop 1 (Beryl)\*\* → local Wi‑Fi/RF issue.
2. **Clean hop 1–2, spikes downstream** → upstream (Starlink/Pasty) jitter/congestion.
3. **Short total loss (10–60s)** → satellite handoff or uplink flip.
4. **RPM < 50** on Mac while SQM on → lower SQM rates another 10–15% and retest.

---

## G. Rollback Plan

- SQM can be disabled in one click: LuCI → *Services → SQM QoS* → **Disable**.
- Keep a LuCI **backup**: *System → Backup / Flash Firmware* → **Generate archive** after working config.

---

## H. Success Criteria

- `networkQuality` RPM consistently **> 200** during busy times.
- Zoom stops freezing; Cursor stops timing out mid‑think.
- `mtr` on router shows minimal downstream loss and fewer >5s stalls.
