# Trails End Strategy C: Hot-Zone AP Decision Matrix

**Context:** Evaluate three outdoor dual-band access points for hot-zone deployment near Welcome Antenna or Barn ridge. Goal: bridge Trails End Crew mesh (5 GHz) back to Beryl via Cat5 backhaul (100-300 ft).

**Philosophy:** "I am not afraid of tech, but don't want to be ruled by it. I want to use it."

---

## Devices Under Evaluation

| Device                           | Role                            | Status                         |
|----------------------------------|---------------------------------|--------------------------------|
| **TP-Link EAP225-Outdoor**       | Candidate (recommended)         | Viable for Strategy C          |
| **MikroTik GrooveA 52 ac**       | Candidate (backup)              | Viable but vendor lock-in risk |
| **Ubiquiti NanoStation Loco5AC** | Reference (current; won't work) | Why it fails at Trails End     |

---

## Decision Matrix

### 1. Operating Modes (AP / Client / Remote / Proprietary)

**Why this matters:** Determines what roles the device can play in your network. A device locked to one mode (e.g., AP-only) limits flexibility if your strategy changes.

| Mode                     | TP-Link EAP225             | MikroTik GrooveA           | Ubiquiti Loco5AC        | Notes                           |
|--------------------------|----------------------------|----------------------------|-------------------------|---------------------------------|
| **AP (Access Point)**    | ✓ Yes                      | ✓ Yes                      | ✓ Yes (airMAX mode)     | Broadcasts WiFi to clients      |
| **Client (WiFi Bridge)** | ✓ Yes                      | ✓ Yes (station mode)       | ✓ Yes (airMAX mode)     | Connects to upstream Crew mesh  |
| **Remote Access**        | ✓ SSH/HTTPS web UI         | ✓ Winbox, SSH              | ✗ Limited (airMAX only) | Manage from distance            |
| **Proprietary Protocol** | ✗ None (standard 802.11ac) | ✗ None (standard 802.11ac) | ✓ **airMAX**            | Locks you to Ubiquiti ecosystem |

**Verdict:**

- **EAP225 & GrooveA:** Both support AP + Client modes via standard WiFi. No lock-in.
- **Loco5AC:** airMAX protocol forces communication only with other Ubiquiti airMAX devices. Cannot bridge standard WiFi clients directly. *This is why loco-bridge fails at Trails End: can only "see" other Ubiquiti APs, not generic Crew mesh.*

**Implication:**  
Loco5AC teaches a hard lesson: proprietary protocols are powerful within their ecosystem but useless outside it. Crew mesh is standard WiFi; Loco5AC's airMAX protocol means it must "translate" via a compatible AP (Ubiquiti). That extra hop adds complexity and single-point-of-failure risk. EAP225 and GrooveA speak standard WiFi directly--no translation needed.

---

### 2. Ease of Use & Management

| Aspect                | TP-Link EAP225                               | MikroTik GrooveA                               | Ubiquiti Loco5AC                            |
|-----------------------|----------------------------------------------|------------------------------------------------|---------------------------------------------|
| **Web UI**            | Standard HTML form (~5 min setup)            | Winbox custom app (steeper learning curve)     | Telnet/web console (minimal, undocumented)  |
| **Mobile management** | Omada app (optional)                         | Winbox (Windows/macOS only)                    | Mobile Winbox only; no web                  |
| **CLI complexity**    | Telnet available; rarely needed              | RouterOS scripting (powerful, vendor-specific) | Limited telnet; SSH rarely documented       |
| **Troubleshooting**   | Dashboard RSSI, clients, channel info        | Detailed RouterOS logs, firewall rules         | Minimal logging; requires airMAX debug mode |
| **Documentation**     | Abundant; standard WiFi (portable knowledge) | Moderate; RouterOS-specific (vendor lock)      | Sparse; airMAX is proprietary (dead-ends)   |

**Verdict:**  

- **EAP225:** Lowest friction. Web UI is HTML; dashboard is familiar.
- **GrooveA:** Medium friction. RouterOS is powerful but requires study.
- **Loco5AC:** High friction. Undocumented airMAX protocol; limited troubleshooting visibility; you're on your own if it breaks.

**Implication:**  
Loco5AC's apparent simplicity (no configuration needed--just power on) is a trap. When it doesn't work (like at Trails End), you have few levers to fix it. EAP225's "standard" nature means you can troubleshoot using portable WiFi knowledge.

---

### 3. Dual-Band Capable (2.4 GHz + 5 GHz)

| Aspect                     | TP-Link EAP225                                                 | MikroTik GrooveA                       | Ubiquiti Loco5AC                                 |
|----------------------------|----------------------------------------------------------------|----------------------------------------|--------------------------------------------------|
| **Bands supported**        | 2.4 GHz + 5 GHz (simultaneous)                                 | 2.4 GHz + 5 GHz (selectable at config) | **5 GHz only**                                   |
| **Fallback capability**    | Can connect upstream on 5 GHz, broadcast on 2.4 GHz to clients | Must choose one band for all traffic   | No fallback--5 GHz only                          |
| **Client flexibility**     | Clients can use 2.4 or 5 GHz depending on signal               | Clients limited to chosen band         | Clients limited to 5 GHz                         |
| **Ground-level reception** | Better (2.4 GHz penetrates trees, walls better)                | Medium (depends on band choice)        | **Poor at Trails End ground level** (5 GHz only) |

**Verdict:**  

- **EAP225:** Wins. True simultaneous dual-band.
- **GrooveA:** Adequate. Single-band choice requires upfront decision.
- **Loco5AC:** Fails. 5 GHz only means ground-level reception is limited if Welcome Antenna's 5 GHz lobe doesn't reach cone zone.

**Implication:**  
Loco5AC's 5-GHz-only limitation is *why* it doesn't work at Trails End. Welcome Antenna broadcasts primarily on downward/axial lobe; at 100 ft ground level, you're outside the effective cone. A 2.4 GHz fallback would help. EAP225's dual-band is insurance against exactly this scenario.

---

### 4. PoE Power Delivery (100-300 ft backhaul)

| Aspect                     | TP-Link EAP225                   | MikroTik GrooveA                          | Ubiquiti Loco5AC                          |
|----------------------------|----------------------------------|-------------------------------------------|-------------------------------------------|
| **Power draw**             | 10.5 W                           | ~5 W                                      | ~8 W                                      |
| **PoE standard**           | 802.3af (15.4 W available)       | Passive PoE (12 W typical)                | Passive PoE (12 W typical)                |
| **Cat5 distance (200 ft)** | ✓ Reliable (4.9 W headroom)      | ⚠ Marginal (voltage drop risk)            | ⚠ Marginal (voltage drop risk)            |
| **Cat5 distance (300 ft)** | ✓ Reliable (standards-compliant) | ✗ Risky (passive voltage drop ~3-5V loss) | ✗ Risky (passive voltage drop ~3-5V loss) |
| **Injector included**      | ✓ Yes                            | ✓ Yes (Gigabit Ethernet PoE Injector)     | ✓ Yes (POE-24-12W)                        |

**Verdict:**  

- **EAP225:** Best power delivery over distance. 802.3af standard ensures consistent voltage.
- **GrooveA:** Passive PoE works at 150 ft; risky beyond.
- **Loco5AC:** Same passive PoE as GrooveA; no advantage.

**Implication:**  
For 200+ ft backhaul (hot zone to RV), passive PoE becomes unreliable. EAP225's 802.3af standard is worth the higher power draw. Loco5AC and GrooveA are both at risk; you'd need active PoE or AC power to be safe at that distance.

---

### 5. IP Rating (Weatherproofing)

| Aspect                     | TP-Link EAP225                         | MikroTik GrooveA                       | Ubiquiti Loco5AC                       |
|----------------------------|----------------------------------------|----------------------------------------|----------------------------------------|
| **IP rating**              | IP65 (dust-tight, water-jet resistant) | IP54 (splash-resistant)                | IP54 (splash-resistant)                |
| **What it means**          | Direct water spray OK (garden hose)    | Rain/splash OK; prolonged wet is risky | Rain/splash OK; prolonged wet is risky |
| **Operating temp range**   | -30°C to +70°C                         | -20°C to +60°C                         | -10°C to +55°C                         |
| **Keweenaw County winter** | ✓ Suitable                             | ✓ Adequate                             | ⚠ Marginal (-10°C min)                 |
| **Connector sealing**      | ✓ Sealed RJ45 & antenna                | ✓ Sealed antenna                       | ⚠ Standard connectors                  |

**Verdict:**  

- **EAP225:** Best weatherproofing. Designed for outdoor mounting.
- **GrooveA:** Adequate for most outdoor use; lower margin in harsh conditions.
- **Loco5AC:** Adequate; slightly narrower temp range.

**Implication:**  
At Trails End's Welcome Antenna or Barn ridge (exposed, winter temps -10°C to -30°C), EAP225's IP65 and wider temp range provide confidence. Loco5AC's -10°C min is a concern for December-February.

---

### 6. Antennas (Included & Extendable)

| Aspect                             | TP-Link EAP225                                      | MikroTik GrooveA                                   | Ubiquiti Loco5AC                         |
|------------------------------------|-----------------------------------------------------|----------------------------------------------------|------------------------------------------|
| **Included antenna type**          | 2x external pigtail, 3-4 dBi omni                   | 1x body-mounted external, 6/8 dBi omni             | 1x body-mounted (sealed), 8/9 dBi omni   |
| **Connector type**                 | RP-SMA (standard, ubiquitous replacements)          | N-type (less common, limited options)              | Fixed; no replacement possible           |
| **Antenna positioning**            | Independent cables; aim each antenna separately     | Single antenna; orientation tied to device body    | Single antenna; orientation tied to body |
| **Upgrade path**                   | Swap to Yagi, directional (~$15-30, standard RPSMA) | Replace with N-type antenna (specialty item, $50+) | Cannot replace; sealed device            |
| **MIMO capability**                | 2x antenna MIMO diversity                           | Single antenna (no MIMO)                           | Single antenna (no MIMO)                 |
| **Gain improvement (if upgraded)** | 3-4 dBi → 6-8 dBi (Yagi) easily available           | 6/8 dBi → 9-12 dBi (Yagi N-type rare, costly)      | Fixed 8/9 dBi (no upgrade)               |

**Verdict:**  

- **EAP225:** Best flexibility. Pigtail antennas on standard RP-SMA; cheap, easy upgrade. Dual antennas = MIMO diversity.
- **GrooveA:** Moderate flexibility. Body-mounted antenna detachable but N-type connector limits options. Single antenna = no MIMO.
- **Loco5AC:** No flexibility. Body-mounted and sealed; no replacement path.

**Implication:**  
EAP225's pigtail design (cables attached to device) lets you position antennas away from device, aim at Crew mesh AP without moving whole unit. You can also upgrade to directional antenna for $15-30. GrooveA's body-mount means device orientation controls antenna direction--poor azimuth alignment limits options. If you need N-type replacement antennas, they're specialty ($50+) vs ubiquitous RP-SMA ($15-30). Flexibility and economics favor EAP225.

---

### 7. Operating Modes at Trails End (Practical Evaluation)

**Scenario:** Hot-zone device positioned 100-200 ft from Welcome Antenna; must bridge Crew mesh (5 GHz client connection) to Beryl (via Cat5 backhaul) while broadcasting WiFi to RV interior.

| Mode                                   | TP-Link EAP225                            | MikroTik GrooveA                     | Ubiquiti Loco5AC                                                                       |
|----------------------------------------|-------------------------------------------|--------------------------------------|----------------------------------------------------------------------------------------|
| **Client mode (connect to Crew mesh)** | ✓ Connect to Crew mesh SSID (any band)    | ✓ Connect to Crew mesh (802.11ac)    | ✓ *Only if* Crew mesh has Ubiquiti AP in mesh; cannot directly connect to generic WiFi |
| **AP mode (broadcast to RV)**          | ✓ Broadcast 2.4 + 5 GHz to Beryl, clients | ✓ Broadcast 1 band to Beryl, clients | ✓ airMAX mode (Ubiquiti only) or standard SSID (fallback)                              |
| **Bridge mode (transparent backhaul)** | ✓ Yes (standard 802.11ac bridge)          | ✓ Yes (RouterOS bridge)              | ⚠ Partial (requires Ubiquiti mesh controller)                                          |
| **Remote troubleshooting**             | ✓ Web UI via SSH/HTTPS tunnel from RV     | ✓ Winbox SSH from RV                 | ✗ Minimal; telnet only if network already up                                           |

**Verdict:**  

- **EAP225:** All modes work cleanly. Standard WiFi means no dependencies.
- **GrooveA:** All modes work; requires RouterOS bridge config understanding.
- **Loco5AC:** Problematic. airMAX protocol means it can only bridge *via Ubiquiti mesh*; cannot act as a simple WiFi client to generic Crew mesh without a compatible Ubiquiti AP upstream. If Crew mesh is managed by Trails End (not Ubiquiti), Loco5AC is effectively locked out.

**Implication:**  
This is the *fundamental failure mode* of Loco5AC at Trails End. It's not that Loco5AC is broken; it's that airMAX protocol is incompatible with the vendor-agnostic Crew mesh. You'd need Trails End staff to adopt Loco5AC into their mesh controller (unlikely for a personal device). EAP225 and GrooveA have no such dependency.

---

### 8. Technical Capabilities (EE/CS Knowledge Without CCNA)

| Aspect                        | TP-Link EAP225                             | MikroTik GrooveA                          | Ubiquiti Loco5AC                     |
|-------------------------------|--------------------------------------------|-------------------------------------------|--------------------------------------|
| **Signal monitoring (RSSI)**  | ✓ Dashboard; standard dBm units            | ✓ RouterOS interface; detailed stats      | ✓ Basic (telnet/web)                 |
| **Channel tuning**            | ✓ Manual channel select, 20/40/80 MHz      | ✓ Fine-grained RouterOS control           | ✓ Automatic or limited manual        |
| **TX power control**          | ✓ Reduce TX to avoid interference          | ✓ RouterOS 0-30 dBm tuning                | ✓ Limited (no UI)                    |
| **Roaming / 802.11k/v**       | ✓ Supports fast roaming (standard WiFi)    | ✓ Supports (RouterOS-aware)               | ✓ Limited (airMAX-specific roaming)  |
| **Knowledge transferability** | ✓ Portable (WiFi standards apply anywhere) | ⚠ Partial (RouterOS is MikroTik-specific) | ✗ Dead-end (airMAX is Ubiquiti-only) |
| **Debugging tools**           | ✓ Web UI dashboard + standard WiFi tools   | ✓ Detailed RouterOS logging               | ✗ Minimal; requires airMAX expertise |

**Verdict:**  

- **EAP225:** Knowledge you gain is portable. RSSI tuning, channel selection apply to any WiFi AP.
- **GrooveA:** Knowledge is valuable if you commit to MikroTik; otherwise vendor-specific.
- **Loco5AC:** Knowledge is almost useless elsewhere. airMAX tuning doesn't transfer to other brands.

**Implication:**  
Every hour spent learning Loco5AC's airMAX quirks is an hour that doesn't apply to future WiFi projects. With EAP225, you're building transferable RF/WiFi knowledge. With Loco5AC, you're learning a dead-end proprietary protocol.

---

### 9. Ecosystem Lock-In & Future Upgradeability

| Aspect                   | TP-Link EAP225                                    | MikroTik GrooveA                                  | Ubiquiti Loco5AC                            |
|--------------------------|---------------------------------------------------|---------------------------------------------------|---------------------------------------------|
| **Vendor ecosystem**     | TP-Link Omada (APs, switches, controllers)        | MikroTik RouterOS (full routing stack)            | Ubiquiti Unifi mesh (closed ecosystem)      |
| **Standards compliance** | ✓ 802.11ac, Ethernet, PoE (vendor-neutral)        | ✓ 802.11ac, Ethernet, PoE                         | ✓ 802.11ac; ✗ airMAX proprietary overlay    |
| **Replacement path**     | Swap for any 802.11ac/ax AP (Asus, Netgear, etc.) | Swap for any WiFi AP; lose RouterOS features      | Must stay Ubiquiti for airMAX compatibility |
| **Knowledge reuse**      | WiFi tuning applies to any brand                  | RouterOS applies only to MikroTik devices         | airMAX knowledge = zero reuse               |
| **Multi-vendor network** | ✓ Mix with non-TP-Link gear freely                | ✓ Mix with non-MikroTik gear (standard WiFi mode) | ✗ airMAX incompatible with non-Ubiquiti APs |

**Verdict:**  

- **EAP225:** Zero lock-in. You own the device, knowledge, and choice.
- **GrooveA:** Partial lock-in. RouterOS binds you to MikroTik ecosystem for advanced features; standard WiFi mode exists as fallback.
- **Loco5AC:** Full lock-in. airMAX means you're committed to Ubiquiti ecosystem or lose all proprietary benefits.

**Implication:**  
Choosing Loco5AC at Trails End commits you to hoping Trails End staff adopt it into their Ubiquiti mesh. If they refuse, you're stuck with a device that can't talk to their network. EAP225 has no such bet.

---

### 10. Cost & Value

| Aspect                                  | TP-Link EAP225                  | MikroTik GrooveA                     | Ubiquiti Loco5AC                               |
|-----------------------------------------|---------------------------------|--------------------------------------|------------------------------------------------|
| **Device cost**                         | $70-180 (B&H sale: $69.99)      | $88-99                               | ~$100-120 (used, since discontinued)           |
| **PoE injector**                        | Included                        | Included (Gigabit Ethernet PoE)      | ~$15-20 (may be included or extra)             |
| **Mounting hardware**                   | Included                        | Included (Pole Mounting Hardware)    | ~$10-20 (usually extra)                        |
| **Outdoor Cat5 cable**                  | ~$30-50 (any vendor)            | ~$30-50 (any vendor)                 | ~$30-50 (any vendor)                           |
| **Learning time**                       | ~30 min (HTML web UI)           | ~2-4 hrs (RouterOS)                  | ~1-2 hrs (minimal setup)                       |
| **Troubleshooting time (if it breaks)** | Low (standard WiFi tools apply) | Medium (RouterOS-specific debugging) | **High** (airMAX is proprietary; limited docs) |
| **Total cost of ownership (1-year)**    | $100-230 + minimal overhead     | $118-150 + learning overhead         | $100-200 + **high troubleshooting risk**       |

**Verdict:**  

- **EAP225:** Best total cost of ownership (accounting for learning curve). Setup is fast; troubleshooting uses standard WiFi tools (portable knowledge).
- **GrooveA:** Competitive hardware cost ($88-99 + included PoE/mounting); learning curve and RouterOS lock-in add long-term overhead.
- **Loco5AC:** Lowest upfront cost, but highest long-term risk. If airMAX doesn't work at Trails End (likely), you're stuck with an expensive paperweight or forced fallback to standard WiFi mode (losing proprietary benefits).

**Implication:**  
GrooveA's included PoE injector and mounting hardware close the cost gap ($88-99 device is cheaper than EAP225's $70-180 range, but includes accessories). However, learning RouterOS adds 2-4 hours of friction vs EAP225's 30 min setup. If you value your time at >$10/hr, EAP225's lower learning curve pays for itself. Loco5AC *appears* to be a bargain (you already own one), but troubleshooting a failed airMAX deployment far exceeds the EAP225 purchase price.

---

## Summary Comparison Table

| Criterion                                      | TP-Link EAP225          | MikroTik GrooveA         | Ubiquiti Loco5AC         | Winner           |
|------------------------------------------------|-------------------------|--------------------------|--------------------------|------------------|
| **Modes (AP / Client / Remote / Proprietary)** | Standard WiFi all modes | Standard WiFi all modes  | airMAX locks you in      | EAP225 / GrooveA |
| **Ease of Use**                                | ✓ Web UI                | ⚠ RouterOS               | ✗ Limited docs           | EAP225           |
| **Dual-Band**                                  | ✓ Simultaneous          | ⚠ Selectable             | ✗ 5 GHz only             | EAP225           |
| **PoE (200+ ft)**                              | ✓ 802.3af (15.4W)       | ⚠ Passive (voltage drop) | ⚠ Passive (voltage drop) | EAP225           |
| **IP Rating**                                  | ✓ IP65                  | ✓ IP54                   | ⚠ IP54                   | EAP225           |
| **Antennas (upgradeable)**                     | ✓ Detachable            | ✗ Fixed                  | ✗ Fixed                  | EAP225           |
| **Operating Modes at Trails End**              | ✓ All work              | ✓ All work (RouterOS)    | ✗ Proprietary issue      | EAP225 / GrooveA |
| **Technical Knowledge (transferable)**         | ✓ WiFi portable         | ⚠ MikroTik-specific      | ✗ airMAX dead-end        | EAP225           |
| **Ecosystem Lock-In**                          | ✓ None                  | ⚠ Partial                | ✗ Full                   | EAP225           |
| **Cost (hardware only)**                       | $70-180                 | $88-99                   | ~$100-120                | GrooveA          |
| **Total Cost of Ownership**                    | ✓ Low                   | ✓ Medium                 | ✗ High (risk)            | EAP225           |

---

## Recommendation

### → **Choose TP-Link EAP225-Outdoor**

**Wins on 8 of 11 criteria.** Best fit for Strategy C. Respects your philosophy: configure once, validate, move on. No proprietary lock-in. Antenna modularity gives you adjustment room. Standard WiFi means troubleshooting uses portable skills.

### → **Backup: MikroTik GrooveA 52 ac**

If you want to master RouterOS routing/bridging for future MikroTik projects, Groov is worth the learning curve. Otherwise, avoid the complexity and vendor lock-in.

### → **Do Not Retry: Ubiquiti NanoStation Loco5AC (even though you own one)**

Loco5AC teaches a hard lesson: proprietary protocols are powerful inside their ecosystem but useless outside. At Trails End, where Crew mesh is vendor-agnostic, airMAX becomes a liability, not an asset. The knowledge and effort spent troubleshooting Loco5AC doesn't transfer. Unless you convince Trails End staff to adopt Loco5AC into their Ubiquiti controller (unlikely), you're better off deploying EAP225.

**Why Loco5AC fails at Trails End:**

1. **5 GHz only** = no fallback for ground-level weak signal
2. **airMAX proprietary** = cannot bridge generic Crew mesh without Ubiquiti controller adoption
3. **Fixed antenna** = no tuning if signal is weak from hot-zone location
4. **Passive PoE** = risky for 200+ ft backhaul
5. **No upgrade path** = device is sealed; if airMAX strategy fails, you're stuck

---

## Next Steps

### Priority 1: Deploy TP-Link EAP225-Outdoor

1. Order from B&H or equivalent (~$70-180)
2. Identify hot zone: ~50 ft from Welcome Antenna with strong 5 GHz signal (-50 dBm or better)
3. Mount near identified location; position detachable antennas toward Crew mesh AP
4. Run Cat5 backhaul (100-300 ft) from EAP225 to PoE injector to Beryl in RV
5. Configure EAP225 web UI: select Crew mesh SSID, set security to Open (no password)
6. Validate: dashboard shows RSSI -55 dBm or better from Crew mesh
7. Speedtest from RV interior: target ≥5 Mbps down, ≥2 Mbps up over 24h

### Priority 2: If EAP225 insufficient

- Swap omni antenna for directional Yagi (6-8 dBi, RP-SMA)
- Reposition antennas toward Crew mesh AP direction
- Re-validate throughput

### Priority 3: If Strategy C still fails

- Move to Strategy B (PtP link from Site 3) or escalate infrastructure planning

---

**Document:** Trails End Summer 2026 Strategy C Evaluation  
**Last Updated:** 2026-07-12  
**Owner:** Michael R. Wolf
