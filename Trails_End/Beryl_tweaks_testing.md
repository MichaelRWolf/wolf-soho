# Beryl Tweak Testing Plan

This plan lists each recommended tweak, a way to test its effect, and a table to record before/after results.

---

## 1. SQM (CAKE) – Reduce Bufferbloat

**Command to run:**

```bash
ping -c 20 8.8.8.8
```

**What to look for:**

* Average latency (should drop under load)
* Jitter (variation between min and max should be smaller)
  **Before/After Table:**

  | Metric           | Before | After |
  |------------------|--------|-------|
  | Avg latency (ms) |        |       |
  | Min latency (ms) |        |       |
  | Max latency (ms) |        |       |

---

## 2. MSS Clamping – Prevent Fragmentation

**Command to run:**

```bash
ping -c 5 -M do -s 1472 8.8.8.8
```

**What to look for:**

* If this fails before the tweak, find largest `-s` that passes
* After tweak, 1472 (or higher) should pass without fragmentation
  **Before/After Table:**

  | Max passing payload size | Before | After |
  |--------------------------|--------|-------|
  |                          |        |       |

---

## 3. WireGuard to VPS – Stabilize IP & Jitter

**Command to run:**

```bash
gping 1.1.1.1 <your_VPS_IP>
```

**What to look for:**

* VPS line should have less jitter and fewer spikes than direct public IP test
  **Before/After Table:**
  \| VPS jitter range (ms) | Before | After |
  \|-----------------------|--------|-------|
  \| Packet loss %         |        |       |

---

## 4. Dual-WAN Failover – Reduce Dropouts

**Command to run:**

```bash
ping -c 100 1.1.1.1
```

**What to look for:**

* During a forced outage on primary WAN, pings should continue via backup
  **Before/After Table:**
  \| Packet loss during failover | Before | After |

---

## 5. DNS Caching – Speed Repeated Lookups

**Command to run:**

```bash
for i in {1..5}; do time dig +short api.openai.com; done
```

**What to look for:**

* First lookup time vs. subsequent lookup times (cached should be faster)
  **Before/After Table:**
  \| Avg cached lookup time (ms) | Before | After |

---

## 6. Wi-Fi Channel/SSID Hygiene – Reduce Retries

**Command to run:**

```bash
airport -I | grep agrCtlRSSI
```

(run this repeatedly during work)
**What to look for:**

* RSSI should be stable, retries fewer, disconnects rarer
  **Before/After Table:**
  \| RSSI avg (dBm) | Before | After |
  \|----------------|--------|-------|

---

## 7. Keepalive Pings – Maintain NAT Mapping

**Command to run:**

```bash
ping -c 300 <WireGuard_peer_IP>
```

**What to look for:**

* No large gaps or 100% loss streaks during idle periods
  **Before/After Table:**
  \| Longest idle gap without loss | Before | After |
