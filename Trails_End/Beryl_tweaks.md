# 2025-08-13

## ChatGPT discussion

<https://chatgpt.com/c/689c901c-8a40-8327-9c83-0b55325f4fe6>

Heck yes. Here’s a tight, Beryl-focused hardening recipe. Each step = **Do / Why / How it works**. (Assumes GL-MT1300 “Beryl”, GL.iNet firmware v3.x. I note LuCI/SSH paths too.)

---

## 0) Snapshot + basics

**Do:** Back up config (GL.iNet UI → *More Settings → Backup / Restore*).
**Why:** Fast rollback if a tweak misbehaves.
**How it works:** Exports UCI configs so you can restore without re-pairing everything.

---

## 1) Enable SQM (CAKE) on WAN

**Do:** Install & enable SQM; cap to \~85–90% of real uplink/downlink.

* SSH:

  ```bash
  opkg update
  opkg install luci-app-sqm sqm-scripts kmod-sched-cake kmod-ifb
  ```

  LuCI → *Network → SQM QoS* → `Enable` on **WAN** (usually `eth0`/`wwan`), set bandwidth (e.g., if real = 10/2 Mbps, enter 9000/1800 Kbps). Queue: **cake**; Script: **piece\_of\_cake.qos**.
  **Why:** Kills bufferbloat so latency stays stable under load.
  **How it works:** CAKE fairly schedules flows and intentionally “shaves” throughput to prevent the upstream queue from bloating (where you have no control).

---

## 2) Fix MTU/MSS (prevent silent fragmentation)

**Do:** Turn on TCP MSS clamping; set a safe clamp.

* LuCI → *Network → Firewall → General Settings* → **TCP MSS**: *Clamp to PMTU* (or explicit **1420** if you’ll use WireGuard/VPN).
* GL.iNet UI sometimes has **Fix MTU** under VPN.
  **Why:** Campground+CGNAT+VPN often reduce path MTU; mismatched MTU → stalls/ECONNRESET.
  **How it works:** Router rewrites TCP options so endpoints send packets small enough for the narrowest link—no fragmentation surprises.

---

## 3) Add a stable VPN egress (WireGuard → VPS)

**Do:** Stand up a \$5/mo VPS (near Midwest) and make a WireGuard tunnel from Beryl. Route only your Mac through it.

* On VPS (Ubuntu): install WireGuard; create peer keys.
* On Beryl (GL UI): *VPN → WireGuard Client → Add new* (peer, endpoint, `AllowedIPs = 0.0.0.0/0`, **MTU 1420**, **PersistentKeepalive 25**).
* *VPN Policy* → “Only allow the following clients via VPN” → check your Mac’s DHCP reservation.
  **Why:** Gives your flows one clean, consistent public IP and keeps NAT tables warm; masks campground jitter/CGNAT oddities.
  **How it works:** Your Mac’s traffic rides an encrypted UDP tunnel to the VPS. Short, regular keepalives prevent NAT idle timeouts; Cloud services see a steady endpoint.

---

## 4) Dual-uplink failover (optional but clutch)

**Do:** Add LTE/iPhone tether as **backup WAN** and enable failover.

* GL UI → *Network → Multi-WAN* (install plugin if prompted). Primary = Campground Wi-Fi; Secondary = **Tethering** (USB) or **Cellular modem**; Health check every \~5–10s; failback = on.
  **Why:** When the camp link dies, long-lived sessions don’t; WireGuard rides the surviving uplink.
  **How it works:** The router watches pings/DNS to known hosts; on failure, routes the WireGuard underlay over LTE. VPN keeps your app sessions intact.

---

## 5) DNS caching (keep lookups fast when link wobbles)

**Do:** Keep **dnsmasq** as local cache; set multiple upstreams; avoid DoH on a flaky link.

* GL UI → *DNS* → Upstreams: `1.1.1.1`, `8.8.8.8`, `9.9.9.9`. Disable DoH unless your link is stable.
  **Why:** Slow/failed DNS looks like “the internet is broken.” Local cache shields you from transient upstream failures.
  **How it works:** dnsmasq answers repeats from RAM and cycles upstream resolvers if one stalls.

---

## 6) Lock Wi-Fi to be boring and predictable

**Do:** Split SSIDs, fix channels, reduce roam-flap.

* GL UI → *Wireless*: create **separate SSIDs** for 2.4 GHz (range) and 5 GHz (work). Turn off band-steering. Fix 2.4 GHz to **1/6/11** (pick least noisy); fix 5 GHz to a clean non-DFS channel your Mac supports. Place Beryl near a window toward the camp AP.
  **Why:** Band-steering and auto-channel changes cause momentary drops that kill WebSockets.
  **How it works:** Static channels + separate SSIDs stop the client from bouncing bands; better SNR lowers retransmits and jitter.

---

## 7) Rate-limit “elephants” during work hours

**Do:** Put cloud backup/photo sync on a schedule or cap it.

* LuCI → *Network → SQM → Advanced* can give **diffserv** prioritization; simplest: pause heavy sync while coding.
  **Why:** Big uploads inflate latency and blow up interactive flows even with SQM (less so, but still).
  **How it works:** Keeping queues light preserves headroom for ACKs/keepalives.

---

## 8) Keepalive pings so captive/CGNAT doesn’t idle you out

**Do:** Enable network check/keepalive.

* GL UI → *More Settings → Network Check*: ping `1.1.1.1` and `8.8.8.8` every 60–120s (lightweight).
  **Why:** Some public Wi-Fi/CGNAT boxes drop idle mappings; a tiny periodic packet keeps the door open.
  **How it works:** Prevents state expiry in upstream NAT/firewalls; your sessions don’t get surprise RSTs.

---

## 9) Give WireGuard priority over bulk (if available)

**Do:** If your SQM supports per-flow prioritization, mark WG (UDP:51820) high.

* LuCI → *Network → Firewall → Traffic Rules* (mangle/DSCP) or SQM advanced: `diffserv4`.
  **Why:** Ensures the control plane (VPN) stays smooth even when other stuff is busy.
  **How it works:** DSCP marks steer packets into a higher-priority queue inside CAKE.

---

## 10) Quick health dashboard you’ll actually look at

**Do:** On your Mac, run:

* `gping 1.1.1.1 8.8.8.8 <your VPS IP>` while you work.
* `sudo nping --tcp -p 443 api.openai.com` when Cursor feels bad.
  **Why:** Immediate visual on jitter/loss locally vs tunnel vs destination.
  **How it works:** If VPS stays flat but api.openai.com jitters, it’s beyond you; if both jitter, it’s the uplink.

---

### Order of ops (fastest impact first)

1. **SQM (CAKE)** + **MSS clamp**
2. **WireGuard → VPS** with **policy routing** for your Mac
3. **DNS cache** & **Wi-Fi channel/SSID hygiene**
4. **Failover WAN** (tether)
5. **Keepalives** + optional prioritization

If you want, tell me:

* Your GL.iNet firmware (3.x exact),
* WAN interface name it shows for the campground (so I target SQM to the right device),
* The static DHCP IP of your Mac,
  and I’ll give you copy-paste configs (WG, SQM, PBR) tailored to your box.
