# Summary of Chat: LTE Performance, WiFi Options, and Starlink Expectations

## 1. LTE at Your Location (Crystal River, FL – Rascally Raccoon Refuge)

- Your AT&T LTE signal shows:
  - RSRP ~ -111 dBm (weak)
  - RSRQ ~ -13 dB (poor)
  - SINR ~ 5 dB (bad)
- Speedtest results:
  - Download: 41 Mbps (fine)
  - Upload: 1.45 Mbps (too low for stable Zoom)
  - Latency spikes: 63 → 720 → 1504 ms (catastrophic)
  - Jitter: 36 ms (Zoom-unfriendly)
- Diagnosis: **LTE at the RV is not viable for Zoom**, regardless of hotspot/router.

---

## 2. Why LTE Performs Poorly

- Edge-of-cell signal.
- AT&T Band 2 is high-frequency (1900 MHz), doesn’t penetrate trees well.
- Congested sector (snowbird season).
- LTE scheduler adds bufferbloat under load.
- Trees + distance degrade uplink power → bad uploads and jitter.

---

## 3. Tests Recommended

### Test 1 – At RV

- Run 3 Speedtests back-to-back.
- Look for upload ≥ 2 Mbps and stable latency.

### Test 2 – Walk Test

- 50 ft toward house → Speedtest
- 50 ft toward street → Speedtest
- Purpose: detect RF shadow or dead pocket.

### Test 3 – Carrier Comparison

- Borrow Verizon/T-Mobile phone.
- Run 1 Speedtest at RV.
- If upload ≥ 3–5 Mbps and jitter < 20–30 ms → that carrier is viable.

---

## 4. Using the Nighthawk With Beryl

- Beryl cannot improve the LTE link itself.
- It *can* improve LAN stability (WiFi quality) but not WAN (LTE).
- USB/Ethernet doesn’t fix radio issues.
- Chrome blocks Nighthawk admin UI (HSTS, expired Netgear domains). Safari works.

---

## 5. Starlink Expectations (Realistic)

### Typical real-world performance

- Download: 75–220 Mbps
- Upload: 10–40 Mbps
- Latency: 20–60 ms
- Very good for Zoom, screenshare, remote work.

### Winter/Snowbird Congestion

- Starlink is shared medium → can degrade during peak times.
- Reports in FL + RV parks:
  - Evening slowdowns
  - Occasional latency spikes
  - Sometimes <10 Mbps during heavy congestion
- Still much better than your current LTE.

### Practical outcome

- Daytime: excellent.
- Evenings: may have jitter/slowdowns but usually workable.
- Overall: **3.5–4 stars out of 5** for rural remote work during winter.

---

## 6. Recommended Strategy

- Use Starlink as primary.
- Keep house-to-RV NanoStation link as backup (fastest and lowest-latency option).
- Consider multi-carrier SIM (Verizon/TMO) if future redundancy is needed.
