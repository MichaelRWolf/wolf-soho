# Transition: LTE → ISP over PtP (Qualitative)

This document captures the *qualitative* effects of moving from LTE to a land-based ISP reached via a Ubiquiti point-to-point (PtP) wireless bridge.

Primary goal: create a stable baseline so we can focus on improving macOS `networkQuality -v` reporting **Responsiveness: Low** (bufferbloat / queueing under load).

---

## Scope and non-goals

### What changed

- Internet source moved from **LTE** to a land-based **ISP** connection.
- The RV reaches that ISP via a **Ubiquiti airMAX PtP bridge** that behaves like transparent Layer-2 Ethernet.

### What did not change (the important part)

- The ISP uplink is still limited (currently ~9 Mbps observed).
- If uploads saturate that uplink, **queues form** somewhere (router and/or ISP), and interactive traffic suffers.

---

## Topology snapshot (after)

- ISP (currently: Spectrum cable)
- House-side PtP radio: Ubiquiti NanoStation Loco5AC (AP)
- RV-side PtP radio: Ubiquiti NanoStation Loco5AC (Station)
- RV router: GL.iNet Beryl (GL-MT1300)
- Clients: macOS laptops

The PtP link is treated as a boring wire:

- Layer-2 bridge
- No NAT
- Not the bottleneck when aligned/stable

---

## What got better (and why)

- Consistency and stability
  - Cellular variability (tower load, handoffs, signal swings) is removed.
  - The PtP hop is deterministic compared to LTE.
- Idle latency
  - Typically lower and more predictable once LTE is out of the path.
- Debuggability
  - Problems become separable:
    - LAN/Wi‑Fi
    - PtP bridge
    - ISP uplink / queueing behavior
- Operational stability
  - Static management IPs on the radios; fewer “discovery/DHCP” failure modes.

---

## What did not improve (and why)

### Symptom

- `networkQuality -v` shows good idle latency but **Responsiveness: Low** (high HTTP loaded latency).

### Root cause class (most likely)

- **Uplink congestion / bufferbloat** on the constrained upstream.

PtP improves the middle of the network but cannot change:

- ISP uplink capacity
- Router queue behavior
- ISP-side buffering

---

## Interpreting `networkQuality` “Responsiveness: Low”

Working definition for this project:

- Idle latency is fine.
- Under load, interactive requests (HTTP/TCP) experience high latency.

In other words, the connection is fast enough in throughput terms, but **not well-behaved under contention**.

With LTE removed, this becomes a queue management problem first, not an RF/alignment problem.

---

## Hypotheses to test (bufferbloat-focused)

- Upload saturation is filling a single FIFO queue (router or ISP), delaying small interactive packets.
- Multiple concurrent upstream flows (cloud sync, backups, calls) amplify queueing.
- Wi‑Fi airtime/contention may contribute, but if Responsiveness is still Low on Ethernet, WAN queueing dominates.

---

## Experiment plan (step-by-step)

### 1) Establish a reproducible baseline

- Pick a consistent test posture:
  - Same client machine
  - Prefer Ethernet to RV router for baseline (then repeat on Wi‑Fi)
  - Minimize background uploads/downloads
- Capture:
  - `networkQuality -v` output
  - What else was happening on the network (calls, sync, streaming)

### 2) Confirm it’s uplink-driven

- Re-run `networkQuality -v` while intentionally saturating upload (e.g., large upload, cloud backup).
- If idle latency remains good but loaded latency worsens, that’s classic upstream bufferbloat.

### 3) Add queue management (SQM) at the correct choke point

Principle: shape where you control the queue (typically the WAN egress of your router).

- Enable SQM (CAKE or fq_codel) on the WAN router if available.
- Start with conservative shaping rates below the measured ISP rates.

### 4) Iterate rates until “loaded latency” improves

- Lower uplink shaping rate until loaded latency meaningfully drops.
- Then tune downlink shaping only if needed.

### 5) Validate in real workflows

- Video call + background upload
- Interactive shells/SSH
- Typical browsing while uploads are active

---

## Decision criteria

- Primary: loaded-latency/Responsiveness improves in `networkQuality -v` and in real interactive use.
- Secondary: avoid sacrificing more throughput than necessary.

---

## Related documents

- Quantitative measurements and experiment log:
  - `Ubiquiti/transition_lte_to_isp_over_ptp_quantitative.md`
- Radio settings checklist:
  - `Ubiquiti/ubiquiti_loco_ptp_settings.md`
