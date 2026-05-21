# WiFi Bridge System (House → RV)

## End‑to‑End Design Notes, Rationale, and Background

This document summarizes the full reasoning, trade‑offs, and design decisions behind building a **point‑to‑point (PtP) WiFi bridge** from a house to an RV ~460–500 ft away, including early exploratory discussions and discarded options.

---

## 1. Original Problem Statement

- RV parked ~460 ft from house
- Clear visual line of sight, but **pine trunks in between**
- Cellular LTE (AT&T) unreliable:
  - High latency and jitter
  - Unstable upload
  - Zoom and voice calls unusable
- RV and pole location **cannot rely on AC power**
- Desire for:
  - Reliable Zoom/voice/screen sharing
  - Low latency over raw throughput
  - Minimal infrastructure complexity
  - Off‑grid capable solution

---

## 2. Early Options Considered (and Why They Failed)

### 2.1 LTE / Cellular Hotspot (Netgear Nighthawk)

Observed performance:

- Downlink: ~40 Mbps
- Uplink: ~1–1.5 Mbps
- Latency: 60 ms → 1500+ ms spikes
- Jitter: 30–40 ms

LTE radio metrics:

- RSRP ≈ –111 dBm (weak)
- RSRQ ≈ –13 dB (poor quality)
- SINR ≈ 5 dB (marginal)

Root problems:

- **Tower congestion**
- **Scheduler delay**
- **Bufferbloat inside LTE network**
- No control over upstream queues

Conclusion:
> LTE performance is structurally unsuitable for real‑time human communication at this location, regardless of router tuning.

---

### 2.2 LTE Antennas and Boosters

Explored ideas:

- MIMO flat‑panel antennas (TS9)
- LTE signal boosters

Why rejected:

- Antennas improved signal *strength* but not **quality**
- SINR remained low
- Boosters amplify noise and interference as well as signal
- LTE towers increasingly refarmed for 5G, reducing LTE priority

Conclusion:
> Antennas cannot fix congestion, scheduling latency, or refarmed LTE spectrum.

---

### 2.3 Inserting a Local Router (Beryl) Between Devices

Hypothesis:

- Add traffic shaping or SQM between Nighthawk and clients

Reality:

- Bufferbloat was **not local**
- Queues lived in:
  - LTE modem firmware
  - Carrier scheduler
  - Tower uplink
- No local router can shorten queues upstream

Conclusion:
> Local shaping cannot solve upstream cellular queueing.

---

## 3. Concept Shift: Stop Using Cellular Entirely

Key realization:
> The house already has a stable, wired Internet connection.  
> The real problem is **distance**, not bandwidth.

This reframed the problem as:

- How to extend the house LAN ~500 ft outdoors
- With minimal latency
- With no trenching
- With minimal power draw

---

## 4. PtP Bridge as “Air Ethernet”

A PtP bridge functions as:
> A transparent Layer‑2 Ethernet cable through the air

Properties:

- No NAT
- No routing
- No LTE scheduler
- No carrier buffering

Advantages over cellular:

- Predictable latency (~5–10 ms)
- Stable upload
- Zero tower congestion
- Full control of radios and power

---

## 5. Hardware Path Chosen

### 5.1 PtP Radios: NanoStation Loco 5AC (×2)

Reasons:

- Designed for short‑to‑medium PtP links
- Forgiving beamwidth for partial obstruction (tree trunks)
- Very low power (~8 W)
- 5 GHz avoids crowded 2.4 GHz band

Roles:

- House unit: **AP Bridge**
- RV unit: **Station Bridge**

---

### 5.2 RV‑Side WiFi: UniFi UAP‑AC‑M

Reasons:

- Already owned
- Good outdoor coverage
- Low power (~8–9 W)
- Separates PtP link from client WiFi

Design choice:
> PtP radios should not also serve client WiFi.

---

## 6. Power Design Evolution

### 6.1 Constraints

- No AC at pole
- Desire for independence from RV wiring
- Continuous 24/7 operation

### 6.2 Power Budget (at RV)

| Component        | Power                |
|------------------|----------------------|
| NanoStation Loco | ~8 W                 |
| UAP‑AC‑M         | ~9 W                 |
| DC/PoE losses    | ~3 W                 |
| **Total**        | **~20 W continuous** |

Daily energy:

- ~480 Wh/day

---

### 6.3 Battery Options Discussed

#### Car Starter Battery (Junkyard)

- Works short‑term
- Poor cycle life
- ~10–18 hrs usable before deep discharge
- Suitable for **testing only**

#### Deep Cycle / Marine Battery (Recommended)

- Designed for daily cycling
- Much longer service life
- 100 Ah provides ~30 hrs usable buffer

---

### 6.4 Solar Sizing Logic

Winter insolation (Crystal River, FL):

- ~4.5–5 peak sun hours/day

Required panel:

- 480 Wh / (5 h × 0.7 efficiency) ≈ 140 W

Chosen recommendation:

- **150–200 W solar**

---

## 7. PoE and Power Distribution Concepts

### 7.1 Passive PoE vs 802.3af

- NanoStation: **24 V passive only**
- UAP‑AC‑M: accepts passive or 802.3af

802.3af negotiation:

- Detection → classification → power‑on
- Prevents accidental powering of non‑PoE devices

Passive PoE:

- Always‑on voltage
- Simple and efficient
- Preferred for solar/DC systems

---

### 7.2 Final Power Architecture

- 12 V battery
- Solar charge controller
- 12 V → 24 V DC‑DC converter
- 2‑port passive PoE injector board
- Ethernet only up the pole

No AC. No inverter. Minimal loss.

---

## 8. Final Network Topology

```text
House Router
   |
   | Ethernet
   v
24V PoE Injector
   |
   '-- NanoStation Loco (House)
          ))))  500 ft PtP  ((((
   '-- NanoStation Loco (RV)
            |
            +--> Passive PoE Panel
                   |        |
                   |        '--> UAP‑AC‑M → RV WiFi
                   '--> Nano Loco
```

---

## 9. Why This Design Wins

- Solves the **root cause**, not symptoms
- Removes cellular from the equation
- Predictable latency
- Solar‑powered, off‑grid
- Modular and repairable
- Minimal ongoing cost

---

## 10. Summary

The PtP WiFi bridge emerged after systematically eliminating cellular‑based options. Once reframed as a distance problem instead of a bandwidth problem, the solution became straightforward.

This design provides:

- House‑quality Internet at the RV
- Reliable Zoom and voice
- Independence from cellular congestion
- A clean, understandable system
