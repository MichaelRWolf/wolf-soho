# Quality Thresholds by App

This guide defines practical thresholds for *latency* and *capacity* to keep common apps usable without chasing HD video. Values are approximate and conservative.

---

## Zoom (faces in gallery + screen sharing)

| Measure                             | Good (smooth) | Medium (usable) | Poor (frustrating) | Notes                                  |
|-------------------------------------|---------------|-----------------|--------------------|----------------------------------------|
| **Idle latency**                    | < 100 ms      | 100–250 ms      | > 250 ms           | Affects call setup & UI responsiveness |
| **Responsiveness (loaded latency)** | < 200 ms      | 200–800 ms      | > 800 ms           | Key for talking over uploads/downloads |
| **Uplink capacity**                 | ≥ 1 Mbps      | 0.5–1 Mbps      | < 0.5 Mbps         | Enough for faces; not aiming for HD    |
| **Downlink capacity**               | ≥ 3 Mbps      | 1–3 Mbps        | < 1 Mbps           | Receive gallery view + screen share    |
| **Jitter**                          | < 30 ms       | 30–100 ms       | > 100 ms           | Higher jitter ⇒ choppy audio/video     |

---

## Cursor (AI IDE streaming completions/diffs)

| Measure                             | Good (smooth) | Medium (usable) | Poor (frustrating) | Notes                                   |
|-------------------------------------|---------------|-----------------|--------------------|-----------------------------------------|
| **Idle latency**                    | < 100 ms      | 100–250 ms      | > 250 ms           | Lower is snappier for interactive edits |
| **Responsiveness (loaded latency)** | < 300 ms      | 300–1000 ms     | > 1000 ms          | Under load, delays hurt streaming       |
| **Uplink capacity**                 | ≥ 0.5 Mbps    | 0.2–0.5 Mbps    | < 0.2 Mbps         | For edits/uploads/telemetry             |
| **Downlink capacity**               | ≥ 3 Mbps      | 1–3 Mbps        | < 1 Mbps           | Streaming tokens & model results        |
| **Jitter**                          | < 50 ms       | 50–150 ms       | > 150 ms           | Helps keep streams steady               |

---

## Chrome (general web browsing)

| Measure                             | Good (smooth) | Medium (usable) | Poor (frustrating) | Notes                                                 |
|-------------------------------------|---------------|-----------------|--------------------|-------------------------------------------------------|
| **Idle latency**                    | < 100 ms      | 100–250 ms      | > 250 ms           | Page snappiness/TTFB                                  |
| **Responsiveness (loaded latency)** | < 500 ms      | 500–1500 ms     | > 1500 ms          | Affects parallel loads while background transfers run |
| **Uplink capacity**                 | ≥ 0.5 Mbps    | 0.2–0.5 Mbps    | < 0.2 Mbps         | Forms/uploads/sync                                    |
| **Downlink capacity**               | ≥ 5 Mbps      | 1–5 Mbps        | < 1 Mbps           | Scripts/images/fonts; HTTP/2 helps                    |
| **Jitter**                          | < 75 ms       | 75–150 ms       | > 150 ms           | Usually less critical than for real-time apps         |

---

## Wi‑Fi Voice Call (Wi‑Fi Calling / VoIP)

| Measure                             | Good (smooth) | Medium (usable) | Poor (frustrating) | Notes                                     |
|-------------------------------------|---------------|-----------------|--------------------|-------------------------------------------|
| **Idle latency**                    | < 100 ms      | 100–150 ms      | > 150 ms           | >150 ms starts to feel laggy              |
| **Responsiveness (loaded latency)** | < 150 ms      | 150–300 ms      | > 300 ms           | Keeps talk-over natural                   |
| **Uplink capacity**                 | ≥ 0.2 Mbps    | 0.1–0.2 Mbps    | < 0.1 Mbps         | Most voice codecs need <100 kbps each way |
| **Downlink capacity**               | ≥ 0.2 Mbps    | 0.1–0.2 Mbps    | < 0.1 Mbps         | Symmetric matters for call quality        |
| **Jitter**                          | < 20 ms       | 20–50 ms        | > 50 ms            | Jitter buffers can only do so much        |

---

## YouTube (SD / 480p priority)

| Measure                             | Good (smooth) | Medium (usable) | Poor (frustrating) | Notes                                   |
|-------------------------------------|---------------|-----------------|--------------------|-----------------------------------------|
| **Idle latency**                    | < 150 ms      | 150–400 ms      | > 400 ms           | Less critical thanks to buffering       |
| **Responsiveness (loaded latency)** | < 800 ms      | 800–2000 ms     | > 2000 ms          | Impacts startup/resume & quality shifts |
| **Uplink capacity**                 | ≥ 0.2 Mbps    | 0.1–0.2 Mbps    | < 0.1 Mbps         | Minimal; comments/uploads aside         |
| **Downlink capacity**               | ≥ 3 Mbps      | 1–3 Mbps        | < 1 Mbps           | SD stream without frequent stalls       |
| **Jitter**                          | < 75 ms       | 75–150 ms       | > 150 ms           | Buffering hides some jitter             |

---

## Parallel TODOs (run independently)

- [ ] **Enable SQM (Cake/FQ-CoDel) on bottleneck router** to cap at ~90–95% of actual up/down and cut loaded latency.
- [ ] **Re‑run `networkQuality -v` while saturating a download** (e.g., `curl` a large file) to measure responsiveness change.
- [ ] **Check ECN negotiation**: `tcpdump` SYN/SYN‑ACK ECE/CWR with a few HTTPS hosts; note if path marks CE under load.
- [ ] **Zoom test call** with simultaneous file upload to confirm speech remains clear and screen share legible.
- [ ] **Cursor streaming test** (long completion) during background download; confirm <300–500 ms loaded latency feel.
- [ ] **Record results** back into this file (dates + values) to build a before/after log.

> Tip: Prioritize SQM at the *actual uplink bottleneck* (the barn/ISP edge) for the biggest responsiveness win. SQM only helps on the link you control.
