# In‑Depth Notes: LTE vs PtP vs Starlink for the RV

Location context:  
**The Rascally Raccoon Refuge Inc. · 8459 W Oak St · Crystal River, FL 34428**

You want: reliable Zoom (with screen share), light everyday work, and minimal drama.  
You do **not** care about gaming, 20+ devices, or huge media workloads.

This document explains:

1. The concepts behind the [earlier short summary](file://./Internet_at_Rascally_Raccoon_Refuge.md) (LTE signal quality, bufferbloat, etc.).
2. Why we’re effectively **sunsetting the Nighthawk as a primary WAN**.
3. A design + rationale for a **point‑to‑point (PtP) WiFi link** from house to RV.
4. A comparison table: **Nighthawk LTE vs PtP vs Starlink**.

---

## 1. Conceptual Background

### 1.1 LTE signal quality: RSRP, RSRQ, SINR

LTE has several key radio metrics:

- **RSRP (Reference Signal Received Power)**  
  Roughly: “how strong is the tower’s LTE pilot signal at your device?”  
  - Values are negative dBm; closer to 0 is better.  
  - Example rough scale:
    - > −90 dBm → strong
    - −90 to −100 dBm → okay
    - −100 to −110 dBm → weak
    - < −110 dBm → very weak  
  Your value: **≈ −111 dBm** → very weak/edge‑of‑cell territory.

- **RSRQ (Reference Signal Received Quality)**  
  How “clean” that signal is, relative to the noise and other users.  
  - Typical scale:
    - −3 to −10 dB → acceptable
    - −11 to −14 dB → congested / noisy
    - < −14 dB → very bad  
  Your value: **≈ −13 dB** → strongly suggests congestion or interference.

- **SINR (Signal‑to‑Interference‑plus‑Noise Ratio)**  
  The all‑important “how usable is this signal?” metric.  
  - Rough scale:
    - > 12 dB → excellent (high‑order modulation, good throughput)
    - 8–12 dB → good
    - 5–7 dB → marginal
    - 0–4 dB → bad
    - < 0 dB → useless  
  Your value: **≈ 5 dB** → marginal; barely good enough for basic internet, not for smooth real‑time work at busy times.

Your Nighthawk is also camped on **LTE Band 2 (1900 MHz)**, which:

- Doesn’t bend around/through trees as well as low‑band (700–850 MHz).
- Tends to be more easily attenuated by trunks, RV roofs, etc.
- Is often repurposed/refarmed and can be more congested.

Put simply: the radio environment at the RV is **weak and messy**.

---

### 1.2 Why your Speedtest looks “fast” but feels terrible

Representative test you ran:

- **Download:** ~41 Mbps  
- **Upload:** ~1.45 Mbps  
- **Ping:** 63 → 720 → 1504 ms (three probes in one test)  
- **Jitter:** ~36 ms

#### Download vs upload

Zoom and screen share care far more about **upload** (your outgoing video) than download.  

- 41 Mbps down is great.
- 1.45 Mbps up is borderline. It may drop below 1 Mbps during congestion.

#### Latency and jitter (bufferbloat + tower congestion)

The ping pattern (63 → 720 → 1504 ms) reveals:

- Sometimes the tower and backhaul are quick.
- Under load or in certain bursts, your packets sit in **queues**:
  - In the tower’s scheduler buffers
  - Possibly in carrier core routers
- That deep queuing is called **bufferbloat**: too many packets waiting too long in buffers, instead of being dropped early or paced.

Zoom can tolerate 100–200 ms latency if it’s stable.  
It **cannot** tolerate 60 ms one moment and 1500 ms the next.

So even when speed tests show “okay” download, the **behavioral reality** is:

- Audio dropouts
- Frozen frames
- Screenshare lag
- “Network unstable” warnings

---

### 1.3 Why Beryl or a newer LTE puck can’t fix this

The Beryl (or any good router) can:

- Improve **local WiFi** inside and around the RV.
- Do smart things like:
  - Traffic shaping (so your own devices don’t cause self‑inflicted congestion)
  - Better LAN handling than Nighthawk’s built‑in WiFi.

But it cannot:

- Change the **RSRP/RSRQ/SINR** seen at the Nighthawk.
- Increase the tower’s capacity or reduce the number of snowbirds on the same sector.
- Turn a deeply congested, edge‑of‑cell LTE path into something as stable as cable or fiber.

A **newer LTE hotspot** on the **same band on the same tower** might:

- Improve sensitivity by a few dB.
- Handle some modulation modes more efficiently.

But it **won’t resolve**:

- High congestion
- Bad SINR
- Weak, obstructed signal
- The fact that AT&T’s better bands/5G aren’t reaching your exact patch of ground.

---

## 2. Why We’re Sunsetting the Nighthawk as Primary WAN

“Sunsetting” here is a design decision:  
Stop trying to make this specific AT&T LTE + Nighthawk combination your main workhorse.

### 2.1 Technical reasons

1. **LTE‑only & no usable 5G at this spot**  
   - Your phone rarely shows “5G” here.
   - That strongly suggests: even if you bought a fancy 5G Nighthawk, it would still mostly see the same marginal LTE.

2. **Edge of coverage (RSRP −111, SINR 5 dB)**  
   - These numbers are typical of “fringe” sites where connections are:
     - Fine for lightweight browsing.
     - Not fine for real‑time voice/video reliability.

3. **Tower congestion & refarming**  
   - Snowbird load + carriers re‑arranging spectrum = older LTE bands often get less love.
   - You’re seeing exactly that in the ping and jitter.

4. **Limited upside even with antennas**  
   - A directional antenna might win a few dB and occasionally push SINR into “okay” territory.
   - But it cannot fix congestion or make 5G magically appear.

### 2.2 Ecosystem / maintenance reasons

1. **Browser administration friction**  
   - Old HTTP‑only firmware on the Nighthawk is fighting:
     - Chrome’s HTTPS‑only push
     - HSTS quirks
     - Netgear’s long‑term neglect of certain hostname flows
   - This will get *worse*, not better, over time.

2. **Firmware stagnation**  
   - LTE mobile hotspots of that generation are not getting big feature or security upgrades.
   - Investing time in learning and nursing this platform has diminishing returns.

3. **Better long‑term options exist**  
   - If you’re putting energy anywhere, it’s more rational to invest in:
     - A robust PtP link.
     - A Starlink setup.
     - Or a modern, multi‑carrier 5G router tested with real signal.

### 2.3 Strategic judgment

Given:

- Your workload (Zoom + remote collaboration).
- The RF + congestion data.
- The state of the device ecosystem.

It’s a **strategically sound call** to:

- Demote the Nighthawk from “primary WAN for work” to:
  - Backup WAN.
  - “Nice to have” when moving or in other locations where it might do better.
- Shift main design attention to:
  - **PtP house‑to‑RV link**.
  - **Starlink** (house or RV).

---

## 3. PtP from House to RV – Design & Rationale

### 3.1 Concept: “Air Ethernet”

The idea of a **PtP WiFi link**:

- Two outdoor radios (e.g., Ubiquiti NanoStation Loco) form a focused, directional wireless bridge.
- One at the **house** (“root” side).
- One at the **RV** (“remote” side).
- They act as if you’ve run a long Ethernet cable through the air.

This gives you:

- Latency in the single‑digit milliseconds.
- Dozens of Mbps (often 50–200 Mbps) of throughput if aligned and configured well.
- Independence from cellular and tower congestion.

### 3.2 Why PtP makes sense in your case

1. **You can see the house from the RV**  
   - Some pine trunks, but mostly clear line‑of‑sight.
   - PtP radios excel in this scenario.

2. **500 ft is an easy distance**  
   - Well within comfortable range for NanoStation‑class hardware.
   - Plenty of margin to back off power to reduce interference to neighbors.

3. **You care about *quality*, not raw multi‑user capacity**  
   - A simple PtP link + one AP near the RV gives you:
     - Strong WiFi coverage in and around the RV.
     - A pipe that behaves like a wired connection to the house network.

4. **You can centralize the “hard internets” at the house**  
   - House can host:
     - Starlink dish (best sky view).
     - Any future wired or fixed‑wireless solution.
   - PtP then just “teleports” that connectivity out to the RV without another ISP or extra modem.

### 3.3 High-level design

**At the House:**

- Mount NanoStation (or similar) on the house, aimed at the RV.
  - Use 5 GHz if possible (less crowded, more capacity, but prefers clearer LOS).
- Connect NanoStation to:
  - House router / switch via Ethernet.
  - Power via PoE injector.

**At the RV:**

- Mount second NanoStation pointing back at the house unit.
- Connect to:
  - A small router (Beryl) or directly into an AP.
- Provide local WiFi around/in the RV via:
  - Ubiquiti UAP, or
  - The Beryl’s own WiFi if you prefer.

### 3.4 Rationale and tradeoffs

**Pros:**

- **Latency:** very low; great for Zoom and interactive work.
- **Throughput:** more than enough for your needs.
- **Predictability:** not dependent on cell tower loads.
- **Scalability:** if the house internet improves, RV benefits automatically.

**Cons:**

- Requires some install work:
  - Mounting.
  - Aiming and basic radio config.
- Still subject to:
  - Strong storms.
  - Potential interference from other 5 GHz users (though you can pick channels).

Overall: given your conditions, a PtP solution is one of the *highest‑leverage* improvements you can make.

---

## 4. Starlink – Zoom‑Relevant View

Starlink is a **low Earth orbit (LEO) satellite internet** service.

### 4.1 What it typically delivers (ballpark)

- Download: **~75–200+ Mbps**.
- Upload: **~10–20+ Mbps**.
- Latency: **~20–60 ms**, but may spike at times.
- Jitter: generally acceptable, but can see occasional bursts (especially during satellite hand‑offs or congestion).

For Zoom:

- This is **massively better** than your current LTE upload.
- Latency is usually quite workable.
- Occasional spikes or short outages are possible, but many WFH users run entire workdays on Starlink.

### 4.2 Seasonal & congestion effects

- Florida in winter = high Starlink user load (snowbirds, RV parks).
- That can cause:
  - Evening slowdowns.
  - Latency increases during prime‑video hours.
- In a mildly rural setting like the Refuge (vs a giant RV resort):
  - You’re likely in better shape than the most saturated cells.
  - Still, expect performance to be **“usually good, sometimes cranky”**.

### 4.3 Where Starlink fits in your design

Best roles:

- As the **primary house internet**, feeding the PtP link.
- Or as a **direct RV internet** if mounting and sky view at the RV is better than at the house.

In both cases:

- Starlink replaces LTE as your WAN.
- The PtP link can still be useful for:
  - Sharing connectivity between house and RV.
  - Keeping a consistent local network.

---

## 5. Comparison Table: Nighthawk LTE vs PtP vs Starlink

All numbers are approximate, based on:

- Your real measurements (Nighthawk LTE).
- Typical PtP behavior at ~500 ft LOS.
- Typical Starlink performance in lightly rural areas with some seasonal congestion.

| Feature / Metric          | **Nighthawk (AT&T LTE @ RV)**            | **PtP House→RV (with solid house internet)**      | **Starlink (good mount, some congestion)**        |
|---------------------------|-------------------------------------------|---------------------------------------------------|---------------------------------------------------|
| Download speed (typical)  | 20–40 Mbps (bursty)                      | 50–200 Mbps (limited by house WAN)                | 75–200+ Mbps                                     |
| Upload speed (typical)    | 0.5–2 Mbps                               | 10–40 Mbps (house WAN dependent)                  | 10–20+ Mbps                                      |
| Latency (idle)            | 60–100 ms *sometimes*, but highly noisy  | 5–20 ms over PtP + whatever house WAN has         | 20–60 ms                                         |
| Latency (under load)      | Spikes 700–1500+ ms                      | Slight increase only; usually stays < 50–80 ms    | Occasionally 80–200+ ms during congestion        |
| Jitter                    | High (20–80+ ms)                         | Low (PtP): 5–20 ms; mostly WAN‑driven             | Usually moderate (10–30 ms), occasional spikes   |
| Zoom suitability          | **Poor / fragile**                       | **Excellent**, if house WAN is decent             | **Good to Very Good**, some peak-hour wobble     |
| Reliability over a week   | Variable; prone to bad days              | Very stable once aligned and configured           | Usually stable; subject to weather/congestion    |
| Dependent on cell tower   | Yes (AT&T only)                          | No (only depends on house ISP / Starlink)         | Yes (Starlink “cell” capacity, but not LTE)      |
| Sensitive to snowbird load| Yes (LTE tower congestion)               | No (bypasses LTE)                                 | Yes, but generally less severe than LTE          |
| Hardware you already own  | Nighthawk (yes)                          | NanoStations + AP/Beryl (partly; some you own)    | None (would need Starlink kit)                   |
| Complexity to set up      | Low (already done)                       | Medium: mount + align + configure radios          | Medium: mount dish, configure, manage power draw |
| Ongoing admin friction    | High (old UI vs new browser security)    | Low once in place                                 | Moderate (firmware updates, app, occasional tweaks) |
| Capital cost (one-time)   | Sunk cost                                | Few hundred USD for PtP radios + mounts           | Starlink hardware kit cost                       |
| Monthly cost              | Existing AT&T plan                       | Cost of house ISP or Starlink plan                | Starlink subscription                            |

### Reading the table

- **Nighthawk LTE**:
  - Looks okay on paper (good downloads), but upload + latency/jitter make it a **poor primary for Zoom**.
- **PtP House→RV**:
  - If house WAN is at least “pretty good,” this is the **most stable option** for calls.
  - Essentially gives you “house‑grade internet at the RV.”
- **Starlink**:
  - On its own: a large upgrade vs LTE.
  - As house WAN feeding PtP: potentially the best of all worlds.

---

## 6. Design Philosophy Going Forward

Given all of this, the “sane future design” for your setup looks something like:

1. **Treat Nighthawk LTE as backup or travel‑only.**  
   - Keep it for use when on the move or in other locales where LTE works better.
   - Stop expecting it to sustain your core Zoom workload at the Refuge.

2. **Install a PtP link between house and RV.**  
   - Use NanoStations (or similar) in bridge mode.
   - Feed the RV’s Beryl / UAP from the PtP link.
   - This gives you a dependable LAN extension.

3. **Give the house a robust WAN: ideally Starlink.**  
   - Mount Starlink where sky view is best.
   - Plug it into the house router.
   - Let PtP carry that goodness out to the RV.

4. **Optionally test multi‑carrier cellular as tertiary backup.**  
   - At some point, run the 3‑test protocol with Verizon/T‑Mobile phones.
   - If one is clearly good, a small 5G router on that carrier can be your “Plan C.”

This path aligns with:

- The **physics** of your location.
- The **constraints** of modern LTE and browser security.
- Your **real needs**: stable conversations, not speed‑test trophies.
