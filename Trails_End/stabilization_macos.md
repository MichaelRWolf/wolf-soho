<!-- markdownlint-disable MD013 -->
# macOS Stabilization Playbook (formerly "Remediation")

> Goal: increase responsiveness and session resilience for Zoom/Cursor on variable campground uplinks (Starlink/Pasty), trading a bit of raw Mbps for stability.

---

## A. Quick Wins (Do First)

- **Use Beryl SSID, not campground SSID directly.** Keeps your tuning separate from CG gear.
- **DNS:** set to Cloudflare (1.1.1.1) or Google (8.8.8.8) in Network > Advanced > DNS.
- **Disable flaky VPNs** during calls; if needed, prefer **WireGuard** over OpenVPN.
- **Close bulk transfers** (cloud sync, OS updates) during calls.

---

## B. Responsiveness Monitoring

- **Apple `networkQuality` (RPM)**

  ```bash
  networkQuality -v
  ```

  - Run periodically; watch **Responsiveness (RPM)** and **Idle Latency**.

- **Scheduled logging (launchd)**
  - Save plist to `~/Library/LaunchAgents/com.wolf.nq.plist`:

  ```xml
  <?xml version="1.0" encoding="UTF-8"?>
  <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
  <plist version="1.0"><dict>
    <key>Label</key><string>com.wolf.nq</string>
    <key>ProgramArguments</key>
    <array>
      <string>/bin/bash</string>
      <string>-lc</string>
      <string>echo "=== $(date '+%F %T') ===" >> ~/nq.log; networkQuality -v >> ~/nq.log</string>
    </array>
    <key>StartInterval</key><integer>300</integer>
    <key>StandardOutPath</key><string>/tmp/com.wolf.nq.out</string>
    <key>StandardErrorPath</key><string>/tmp/com.wolf.nq.err</string>
    <key>RunAtLoad</key><true/>
  </dict></plist>
  ```

  - Load it:

  ```bash
  launchctl load ~/Library/LaunchAgents/com.wolf.nq.plist
  ```

- **`mtr` path telemetry**

  ```bash
  brew install mtr
  sudo mtr -ezbw -i 1 -c 60 1.1.1.1
  ```

  - Confirms where loss/jitter starts (LAN vs upstream) and catches handoff stalls.
  - **Alternative**: if ICMP looks weird, try TCP/UDP variants:

    ```bash
    sudo mtr -T -P 443 -ezbw -i 0.5 -c 40 -r 1.1.1.1   # TCP
    sudo mtr -u -P 33434 -ezbw -i 0.5 -c 40 -r 1.1.1.1  # UDP
    ```

---

## C. Uplink Identity & Path Logging (already built)

- Use the repo tools we made:

  ```bash
  uplink-short       # one-liner: Pasty vs Starlink + IP
  uplink-describe    # includes traceroute
  nohup uplink-monitor ~/uplink_log.txt 300 &
  ```

- Optional: add a daily cron/launchd to rotate `uplink_log.txt`.
- **Event marker** for NSURLError -1005 during network issues:

  ```bash
  echo "EVENT -1005 $(date '+%F %T')" >> ~/uplink_log.txt; uplink-describe >> ~/uplink_log.txt
  ```

---

## D. TCP Resilience (timeouts/keepalives)
>
> Helps when stalls are short (<10s). Won’t fix full 20–60s blackouts.

- **Test profile (temporary)**

  ```bash
  cat > ~/tcp_keepalive_test.sh <<'EOS'
  #!/bin/bash
  sudo sysctl -w net.inet.tcp.keepidle=20000   # 20s idle
  sudo sysctl -w net.inet.tcp.keepintvl=5000   # 5s between probes
  sudo sysctl -w net.inet.tcp.keepcnt=5        # 5 tries (≈45s total)
  EOS
  chmod +x ~/tcp_keepalive_test.sh
  ./tcp_keepalive_test.sh
  ```

- **Rollback profile**

  ```bash
  cat > ~/tcp_keepalive_reset.sh <<'EOS'
  #!/bin/bash
  sudo sysctl -w net.inet.tcp.keepidle=7200000
  sudo sysctl -w net.inet.tcp.keepintvl=75000
  sudo sysctl -w net.inet.tcp.keepcnt=8
  EOS
  chmod +x ~/tcp_keepalive_reset.sh
  ./tcp_keepalive_reset.sh
  ```

- **Make persistent (optional)** using a launchd script at login; keep test first.

---

## E. Wi‑Fi Hygiene on Mac

- Prefer **5 GHz** over 2.4 GHz; sit closer to the Beryl AP.
- Turn off **Auto-Join** to the campground SSID; stay on Beryl.
- For Apple Silicon, consider **disable Wi‑Fi power saving** during calls:

  ```bash
  sudo pmset -a tcpkeepalive 1
  ```

---

## F. Optional: “Jitter‑friendly” VPN

- If corporate VPN is mandatory, prefer **WireGuard**. Many users see fewer disconnects across LEO handoffs vs OpenVPN/TCP tunnels.

---

## G. What to Watch

- **Zoom**: increase in latency/jitter/loss in Zoom’s stats panel; audio starts to wobble before hard failure.
- **Cursor**: requests that time out ≈10–30s into a "thinking" period → indicative of TCP/WebSocket timeout during a handoff.

---

## H. Exit Criteria

- `networkQuality` **RPM > 200** during busy hours.
- `mtr` shows no multi‑second loss on the first public hop during calls.
- Zoom no longer drops audio; Cursor stops timing out mid‑think.
