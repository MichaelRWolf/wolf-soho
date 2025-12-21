# Transition: LTE → ISP over PtP (Quantitative)

This document is the *quantitative* companion to:

- `Ubiquiti/transition_lte_to_isp_over_ptp_qualitative.md`

Primary goal: provide a table-first ledger for diagnosing and improving macOS `networkQuality -v` **Responsiveness: Low** (loaded-latency / bufferbloat symptoms).

---

## Measurement method (how numbers are gathered)

### Primary tool

- macOS: `networkQuality -v`

### Capture guidance (for repeatability)

- Record whether the client is on:
  - Ethernet to the RV router, or
  - Wi‑Fi (and which SSID/band)
- Record whether any shaping/SQM is enabled (and configured rates).
- Record obvious concurrent traffic (uploads, backups, calls).

---

## Benchmark summary (LTE vs ISP-over-PtP)

The goal of this table is *directional* comparison and establishing that the transport became deterministic after the transition.

| Metric                          | LTE (Before)                | ISP + PtP (After)   | Notes                                          |
|:--------------------------------|:----------------------------|:--------------------|:----------------------------------------------|
| Downlink capacity               | ~10–30 Mbps (variable)      | ~50 Mbps            | Land-based ISP is faster and far more stable   |
| Uplink capacity                 | ~2–10 Mbps (variable)       | ~9 Mbps             | Uplink is still the constraint; now consistent |
| Idle latency                    | Often elevated/inconsistent | ~48 ms              | Predictable after transition                   |
| Responsiveness / loaded latency | Often poor/variable         | ~580–660 ms (Low)   | Primary remaining problem domain               |
| Jitter                          | High/unpredictable          | Lower/more stable   | PtP removes cellular variability               |

---

## Current baseline (ISP-over-PtP) — representative `networkQuality -v`

| Field             | Value                         |
|:------------------|-----------------------------:|
| Downlink capacity |                    ~49.8 Mbps |
| Uplink capacity   |                     ~9.0 Mbps |
| Idle latency      |                        ~48 ms |
| Responsiveness    | Low (~580–660 ms HTTP loaded) |

---

## Experiment log (the driver)

Append rows here as you iterate on SQM / shaping. This table is meant to answer:

- What changed?
- Did `networkQuality` responsiveness improve?
- Under what conditions did it regress?

| Date/time        | Client                | Link_to_router   | SQM_enabled | Shaping_down_Mbps | Shaping_up_Mbps | Concurrent_load      | networkQuality_summary             | Notes |
|:-----------------|:----------------------|:-----------------|:-----------|------------------:|----------------:|:---------------------|:-----------------------------------|:------|
| YYYY-MM-DD HH:MM | wolf-air / michael-pro | Ethernet / Wi‑Fi | On/Off      |                 — |               — | none / upload / call | DL ? / UL ? / idle ? / resp ?      | —     |

---

## Suggested test cases (to populate the log)

| Test_case        | Goal                                 | How                                                                    |
|:-----------------|:-------------------------------------|:-----------------------------------------------------------------------|
| Baseline (quiet) | Establish a stable reference          | No significant background traffic; run `networkQuality -v`             |
| Upload-saturated | Confirm upstream bufferbloat symptoms | Start a large upload; run `networkQuality -v` during sustained upload  |
| SQM tuned        | Validate queue control at the router  | Enable SQM; set shaping below measured rates; re-run tests             |
| Real workflow    | Validate subjective experience        | Video call + background upload; observe responsiveness                 |

---

## Notes / interpretation placeholders

- If Responsiveness improves substantially with SQM, the bottleneck queue is under your control (router-side).
- If Responsiveness remains poor even with conservative shaping, investigate:
  - incorrect choke point (shaping not applied where traffic exits)
  - double-NAT / unexpected path
  - Wi‑Fi airtime contention (test on Ethernet)
  - ISP-side buffering beyond your control (may require lower shaping, different modem/router mode, etc.)
