# Trails End Summer 2026 -- Infrastructure Connectivity Plan

**Active Period:** 2026-07-08 through October 2026  
**Location:** Trails End Campground, Site 1 (RV)  
**Status:** In progress; major blocker = loco-bridge siting for stable 5 GHz connection

---

## Context & Problem Statement

**Current Setup:** `loco-bridge` (NanoStation Loco5AC) positioned at cone zone (~100 ft from RV) attempting to bridge Trails End Crew mesh → Cat5 → Beryl (RV main router).

**Blocker (Last Night, 2026-07-10):** Moving loco-bridge to -58 dBm signal (near welcome antenna, better signal) still does not connect as seen on `.22` overview screen. Diagnosed: 5 GHz only (no 2.4 GHz fallback); signal at ground level may be outside cone zone of all known antennas.

**Root Issue:** Trails End Crew antennas are designed for building/elevated coverage; ground-level reception 100+ ft away is degraded or unreliable. Welcome Antenna broadcasts primarily downward/axial; loco-bridge position is neither in radial cone nor at height for axial lobe.

**Emotional State:** Frustrated; taking a step back to evaluate alternatives.

---

## Open TODOs (WIP)

### Phase 1: Site & Equipment Assessment

**Objective:** Locate all known infrastructure and determine feasible options for stable WiFi bridge.

- [x] **1.1:** Find equipment list for Trails End infrastructure  
  _Locations: Networking center, Barn, Site 3, Pump House_  
  _Goal: Identify what's already deployed, power sources, antenna placement_  
  _Status: In progress; cheapo repeater & loco-bridge identified_

- [x] **1.2:** Locate Charlotte's el-cheapo repeater (Dirt Circus)  
  _Reference: `cheapo_extender.md` ($18 USB WiFi repeater, purchased 2025-08-10)_  
  _Goal: Evaluate whether USB repeater approach viable for Trails End environment_  
  _Status: FOUND & TESTED. Repeats "Trails End Wifi" as "Trails End Wifi-Site 1"; iPhone connects; speedtest fails; macOS can't see SSID in selector (visible in network scan)_

- [ ] **1.3:** Find the standalone Ubiquiti device from last summer  
  _Reference: `Ubiquiti/device_modes.md` explains why standalone mode failed_  
  _Goal: Determine current status and condition; evaluate mesh adoption vs. storage_

- [ ] **1.4:** Field verify unconfirmed antenna locations  
  _Sites: Site 3 (210 ft, 0°), Dirt Circus (657 ft, 135°), Pump House (1,392 ft, 270°)_  
  _Barn Farm Antenna (south side, if exists)_  
  _Goal: Confirm physical presence, MAC addresses, signal quality_

---

### Phase 2: Connection Strategy -- Evaluate Three Alternatives

**Objective:** Test and select best path forward for stable RV WiFi.

#### **Strategy A: loco-bridge Siting Optimization** (Current approach -- lowest cost)

**Actions:**

- [ ] **2A.1:** Perform ground-level MAC-locked tests to identify best AP  
  _Reference: `antenna_survey.md` section "Testing Ground-Level Coverage"_  
  _Test MACs: Welcome (:38), Barn North (:C1), Barn Equipment (:93)_  
  _Measure: signal strength, stability, latency at ground level_

- [ ] **2A.2:** Evaluate alternative ground-level positions within 100-200 ft radius  
  _Goal: Find spot where primary AP broadcasts at ground level (not just elevated)_  
  _Tool: wolf-air or michael-pro with NetSpot; measure 5 GHz signal continuously_

- [ ] **2A.3:** If optimal position found, relocate loco-bridge and test Cat5 chain  
  _Cat5 chain: loco-bridge → POE injector → Beryl in RV_  
  _Test: network access from RV interior, throughput, stability over 24h_

**Blocker Risk:** If no ground-level AP target identified, this strategy fails. → Move to Strategy B/C.

---

#### **Strategy B: PtP Link from Site 3 to Site 1** (Rascally Raccoon pattern)

**Actions:**

- [ ] **2B.1:** Confirm Site 3 location and antenna type (if any exists)  
  _Reference: `antenna_survey.md` unconfirmed candidates_  
  _Goal: Determine if Site 3 is high enough / has good LoS to Pump House or other AP_

- [ ] **2B.2:** Evaluate Site 3 → Pump House as secondary PtP link  
  _Distance: 1,254 ft; Bearing: 260° (Site 3 → Pump House)_  
  _Goal: Assess LoS, wind exposure, available mounting points_

- [ ] **2B.3:** If feasible, acquire second pair of NanoStation Loco5AC devices  
  _Cost: ~$200-300 for pair + PoE injectors_  
  _Logistics: Ship to Trails End or acquire locally if available_

- [ ] **2B.4:** Configure Site 3 PtP link (AP mode) and connect to Beryl via Cat5/PoE at RV  
  _Reference: `Ubiquiti/HOWTO_rascally_raccoon_PtP_config.md` for config steps_

**Advantage:** Stable, high-bandwidth dedicated link (if LoS available).  
**Risk:** Requires admin coordination for Site 3 antenna placement; LoS may be blocked by terrain.

---

#### **Strategy C: Deploy Secondary Mesh-Connected Router at Hot Zone** (Hybrid approach)

**Actions:**

- [ ] **2C.1:** Identify "hot zone" -- location with strong 5 GHz signal from known AP  
  _Candidates: within 50 ft of Welcome Antenna, or Barn ridge, if accessible_  
  _Goal: Position router where signal is reliable and AC power is feasible_

- [ ] **2C.2:** Acquire exterior-grade router (Beryl equivalent or UAP-AC-M-US)  
  _Key requirements:_
  - _Station mode (client) capable, not mesh-dependent_
  - _Dual-band (2.4/5 GHz) or at least stable 5 GHz_
  - _Exterior IP rating (IP64 or better) and weather-sealed antenna connectors_
  - _Modular antennas (input antenna toward Welcome/Barn; output antenna toward RV)_
  - _PoE powered (preferred) or AC power + weatherproof enclosure_

- [ ] **2C.3:** Decision: PoE vs AC power for distant router  
  _PoE advantage: Single Cat5 cable, simpler weatherproofing_  
  _AC advantage: No PoE voltage drop over distance; simpler integration_  
  _Action: Consult with staff on available power infrastructure at hot zone_

- [ ] **2C.4:** Run Cat5 from hot-zone router back to Beryl (RV interior)  
  _Distance: likely 100-300 ft depending on hot-zone location_  
  _Route: Underground/duct preferred; above-ground in cable tray if available_  
  _Goal: Stable backhaul, avoid EMI and weathering_

- [ ] **2C.5:** Configure hot-zone router in station mode, bridge to Beryl  
  _Beryl: primary DHCP/NAT; hot-zone router: transparent AP (bridge mode)_  
  _SSID broadcast: From hot-zone router only (not Beryl) to avoid confusion_

**Advantage:** No mesh admin needed; leverages hot zone with known coverage.  
**Risk:** Requires exterior-grade equipment; AC power may be limited or require generator.

---

### Phase 3: Ubiquiti Device Mesh Adoption (Aspirational -- if staff willing)

**Objective:** Propose adoption of standalone Ubiquiti UAP-AC-M-US into Trails End mesh (like Barn/Welcome pattern).

**Reference Documents:**

- `Trails_End/request_to_adopt_my_ap.md` -- two canned request templates
- `Ubiquiti/device_modes.md` -- explains why standalone mode alone doesn't work

**Actions:**

- [ ] **3.1:** Inspect last summer's UAP-AC-M-US device; confirm firmware, condition, MAC  
  _Reference: `Ubiquiti/device_info.md`_  
  _Goal: Ensure device is functional and adoptable_

- [ ] **3.2:** Research mesh adoption model at Barn, Welcome, Site 3, Pump House  
  _Question for staff: Were these APs "adopted" into a central UniFi controller? If so, how/by whom?_  
  _Goal: Understand political/technical path for adoption_

- [ ] **3.3:** Prepare "adopt my AP" proposal (use template from `request_to_adopt_my_ap.md`)  
  _Pitch: One-time adoption step; extends coverage; reduces load on public SSIDs; "set it and forget it"_  
  _Offering: Provide device, PoE injector, label, and mounting hardware_

- [ ] **3.4:** If adoption approved, configure UAP as mesh peer and validate coverage  
  _Target location: Site 1 (RV area), elevated position if possible_  
  _Test: Connect Beryl to adopted AP via mesh backhaul (not client WiFi)_

**Advantage:** Cleaner architecture; leverages mesh infrastructure; may improve overall site coverage.  
**Risk:** Requires admin approval; may be denied if policy-restricted; adoption process may be technical (UniFi controller access).

---

### Phase 4: Power & Infrastructure Planning (Long-term)

**Objective:** Document power sources and exterior equipment requirements for sustainable deployment.

- [ ] **4.1:** Review power supply options for exterior devices  
  _Reference: `Ubiquiti/power_supply_12v.md` -- UAP-AC-M-US from RV battery via DC-DC converter + PoE_  
  _Evaluate: AC 120V service, solar + battery, PoE only_

- [ ] **4.2:** Document exterior-grade router candidates  
  _Search criteria: IP64+ rating, temperature range, antenna modularity_  
  _Examples: Ubiquiti Bullet, MikroTik outdoor APs, GL.iNet Beryl (existing reference)_  
  _Goal: Curate short list with specs for potential purchase_

- [ ] **4.3:** Identify cable routing options for Cat5 backhaul  
  _Locations: Cone zone → Hot zone → RV, or Site 3 → RV (if PtP strategy)_  
  _Constraints: Weather, EMI, staff approval, existing conduit/duct_

- [ ] **4.4:** Create equipment procurement list  
  _Items: PoE injectors, outdoor Cat5 armor cable, antenna cable adapters, weatherproof connectors_  
  _Budget estimate: $200-500 depending on strategy (A/B/C)_

---

## Decision Tree

**Start here:** Run Phase 1 assessment (site/equipment inventory).

```text
Phase 1 Assessment
  ├─ Can locate/access Charlotte's repeater at Dirt Circus?
  │  └─ YES → Test as interim solution (cheap, quick validation)
  │  └─ NO → Continue to alternatives
  │
  ├─ Can find optimal ground-level AP within 100-200 ft? (Phase 2A)
  │  └─ YES → Relocate loco-bridge, test 24h. If stable → DONE (cheapest option)
  │  └─ NO → Proceed to Phase 2B/C
  │
  ├─ Is Site 3 suitable for PtP link? (Phase 2B)
  │  └─ YES (LoS clear, admin willing) → Acquire PtP hardware, configure
  │  └─ NO (LoS blocked, no admin access) → Proceed to Phase 2C
  │
  └─ Can identify/prepare hot zone with AC or PoE? (Phase 2C)
     └─ YES → Deploy exterior router, backhaul to Beryl
     └─ NO → Escalate to staff; may require facility infrastructure work
```

---

## Known Issues & Constraints

### Technical

- **loco-bridge 5 GHz only:** Cannot fall back to 2.4 GHz; limits AP choices to Trails End Crew mesh antennas
- **Ground-level coverage gap:** Welcome Antenna designed for elevated reception; poor performance 100+ ft away at ground level
- **Cat5 distance:** Can run up to 100m (328 ft) with passive PoE; beyond that, active PoE or AC power needed
- **Mesh adoption requires admin:** Cannot adopt device without Trails End controller access

### Organizational

- **Staff coordination:** Any antenna placement requires approval from Trails End management
- **Power availability:** Some locations may not have AC 120V service
- **LoS verification:** Site 3 / Pump House locations not yet confirmed; may be blocked by trees/terrain

---

## Success Criteria

**Goal:** Stable WiFi connection from RV to Trails End Crew mesh supporting:

- Download: ≥ 5 Mbps sustained
- Upload: ≥ 2 Mbps sustained
- Latency: ≤ 100 ms to public DNS
- Stability: No disconnects over 24h continuous operation

---

## Related Documentation

- **antenna_survey.md** -- Confirmed antennas, distances, bearings, unconfirmed candidates
- **2026_summer_log.md** -- Incident log (throughput collapse 2026-07-08, loco-bridge setup 2026-07-09)
- **Trails_End/request_to_adopt_my_ap.md** -- Mesh adoption request templates
- **Ubiquiti/device_modes.md** -- Why standalone Ubiquiti mode fails
- **Ubiquiti/HOWTO_campground_wifi_repeater_setup.md** -- loco-bridge configuration guide
- **cheapo_extender.md** -- $18 USB repeater reference
- **CONTEXT.md** -- Device registry (loco-bridge, antennas, PoE injectors)

---

## Test Results -- 2026-07-11 Afternoon

### Cheapo Repeater (FOUND & TESTED -- BREAKTHROUGH RESULTS)

- **Maintenance SSID:** `Repeater-2827f1` (broadcasted after power-on)
- **Rebroadcast:** Successfully repeated "Trails End Wifi" as "Trails End Wifi-Site 1"
- **iPhone:** Connected; speedtest attempted
- **MacBook:** Initially not visible in WiFi selector; **SOLVED** by manual SSID entry in System Settings → WiFi → Advanced
- **Throughput Test:**
  - **Original signal (loco-bridge location):** 0.15 Mbps down / 0.30 Mbps up
  - **Repeated signal (repeater location):** 6.4 Mbps down / 3.5 Mbps up
  - **Improvement:** ~40x (unexpected; likely repeater in better line-of-sight to Trails End Wifi)
- **Conclusion:** **VIABLE for MacBook work.** $20 repeater bridges coverage gap when positioned correctly. Can add WPA2 password for security.
- **Next:** Determine repeater placement (location with strong Trails End Wifi), validate sustained throughput over 1+ hour

### loco-bridge Maintenance Mode (DISCOVERED)

- **After reboot:** Device broadcasts `Repeater-XXXXXX` maintenance SSID for ~8 hours
- **No dependencies:** Can configure directly from iPhone without bench setup, USB-Ethernet dongle, or second computer
- **Time to config:** ~10 minutes
- **Advantage:** Fast path to testing without waiting for wendy-pro or other gear
- **Updated:** `HOWTO_campground_wifi_repeater_setup.md` section "Maintenance Mode (Recommended Path)"

---

## Next Session Action Items

**Priority 1 (NOW -- Use Maintenance Mode):**

1. Reboot loco-bridge; use maintenance SSID (`Repeater-XXXXXX`) to configure directly from iPhone
   - Select `Trails End Wifi` AP
   - Run speedtest on iPhone to validate throughput
   - If ≥2 Mbps sustained, consider cat5 chain to Beryl for MacBook access

2. Document speedtest results and signal stability over 15-30 minutes

**Priority 2 (If loco-bridge fails via maintenance mode):**
3. Perform MAC-locked ground-level tests at three known APs (Welcome, Barn North, Barn Equipment)
4. Identify alternative siting location with stronger signal
5. Consider cheapo repeater as interim if loco-bridge proves unreliable

**Priority 3 (Longer-term if WiFi path not viable):**
6. Field-verify Site 3, Pump House locations and antennas (PtP link candidate)
7. Identify "hot zone" with strong 5 GHz signal; scout AC/PoE power access
8. Contact staff re: mesh adoption interest

**Priority 4 (Planning):**
9. Curate exterior-grade router candidates and power supply options
10. Create procurement list and budget estimate

---

## Learned (2026-07-11)

- **Trails End uplink is unstable:** 0-6.4 Mbps variance within 30-minute window; ISP path hopping between multiple carriers/routes (Ontario, Ohio, Michigan)
- **Local WiFi optimization won't fix upstream instability:** Repeater/bridge/hot-zone router all downstream of campground uplink problem
- **Cheapo repeater ($20) works:** Successfully repeated "Trails End Wifi" as "Trails End Wifi-Site 1"; iPhone connected; MacBook can connect via "Other Networks" (not manual entry)
- **MacBook WiFi selector limitation:** Many devices don't show in macOS WiFi menu but ARE discoverable via network scans and "Other Networks" picker
- **loco-bridge maintenance mode (Repeater-XXXXXX) is viable 10-minute config path:** No bench setup, USB dongle, or second computer needed; iPhone access only
- **Ubiquiti airMAX and mesh protocols create lock-in:** NanoStation Loco5AC (loco-bridge, loco-ap, loco-station) + UAP-AC-M-US require Ubiquiti controller adoption or cannot interoperate with standard WiFi APs
- **Keweenaw County has zero cellular coverage forever:** Nighthawk M1 is useless; all infrastructure must be WiFi-based

## Decided (2026-07-11)

**Decision: No single-band devices. No vendor-proprietary protocols.**

**Ruling out:**

- **NanoStation Loco5AC** (loco-bridge, loco-ap, loco-station) -- 5 GHz only + airMAX proprietary
- **NanoStation M5 Loco** (airMAX) -- 5 GHz only + airMAX proprietary
- **UAP-AC-M-US** (wolfden-mesh) -- Requires Ubiquiti mesh controller adoption; cannot operate standalone without admin access to Trails End mesh
- **TP-Link CPE210** -- 2.4 GHz only
- **Cheapo repeater** (interim only) -- Low throughput (halved), repeater architecture fragile

**Viable candidates (dual-band, standard WiFi):**

- **MikroTik GrooveA 52 ac** -- WiFi 5 (802.11ac), dual-band (2.4 + 5 GHz), standard WiFi client/AP/bridge, RouterOS (powerful but learning curve)
- **Awaiting:** TP-Link and other dual-band outdoor AP/bridge options

**Rationale:** At Trails End, must use devices that can access standard WiFi on both bands. Cannot rely on Ubiquiti-only frequencies or proprietary protocols (airMAX, mesh adoption) because:

1. Trails End mesh is managed by staff; adoption not guaranteed
2. Standalone Ubiquiti modes don't work (documented in `device_modes.md`)
3. Need vendor-independent solution; can't be locked to Ubiquiti ecosystem
4. Single-band (5 GHz only) exposes ground-level coverage gap; dual-band provides fallback

---

---

## Equipment Research -- TP-Link EAP225-Outdoor vs MikroTik GrooveA 52 ac

**Updated:** 2026-07-12 (B&H copypaste specs)

See **Trails_End/2026_summer_log.md** for full comparison table.

### Quick Take

**TP-Link EAP225-Outdoor** (recommended for Strategy C):

- IP65 (vs GrooveA IP54)
- 15.4W PoE (vs GrooveA 5W) → better for long Cat5 runs
- Modular antennas → directional pointing at Trails End Crew mesh
- Omada management (familiar)
- AP mode only (limitation if router functions needed)
- Price: ~$70-180 depending on sale/retailer

**MikroTik GrooveA 52 ac** (backup option):

- Lower cost ($88-99)
- Full RouterOS bridge/client/routing modes
- IP54 (adequate for most deployment)
- Passive PoE only (tight power budget)
- Fixed omni antenna (less flexible)

### Plan

**Phase 2C Strategy (hot-zone router):**

1. Acquire EAP225-Outdoor and identify hot zone with strong 5 GHz signal
2. Position modular antennas toward Trails End Crew AP; run Cat5 backhaul to Beryl
3. Test Omada controller transparent bridge mode
4. Measure sustained throughput (target: ≥5 Mbps down, ≥2 Mbps up)
5. If EAP225 insufficient, trial GrooveA 52 ac as comparison

**Procurement:**

- TP-Link EAP225-Outdoor (1x) -- $70-180
- Outdoor PoE Cat5 cable, armored, 100-300 ft run -- ~$30-50
- Weatherproof RJ45 connectors -- ~$10
- Mounting hardware (pole, wall bracket) -- included or ~$20

---

**Last Updated:** 2026-07-12 (Equipment comparison added)  
**Owner:** Michael R. Wolf  
**Status:** Ready to trial TP-Link EAP225-Outdoor for Strategy C hot-zone deployment
