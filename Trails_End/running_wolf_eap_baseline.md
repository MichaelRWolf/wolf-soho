# Running Wolf EAP (TP-Link EAP225-Outdoor) -- Baseline Measurements

**Device:** TP-Link EAP225-Outdoor (Omada)  
**MAC:** 18-69-45-38-A2-F2 / :A2-F3 (5 GHz)  
**S/N:** Y263210002286  
**Location:** Cabin 13 - RV Ladder  
**Date:** 2026-07-25

---

## EAP Broadcast Performance (from Cabin 13 location)

| Band    | SSID                  | Channel | SNR (dBm) | Signal (dBm) | Status |
|---------|-----------------------|---------|-----------|--------------|--------|
| 2.4 GHz | Running Wolf EAP      | 11      | -34       | -33          | Strong |
| 5 GHz   | Running Wolf EAP - 5G | 149     | -42       | -40          | Strong |

---

## Trails End Network Baseline (at EAP location)

| Network          | BSSID             | Band  | Channel | Signal (dBm) | Status |
|------------------|-------------------|-------|---------|--------------|--------|
| Trails End Crew  | 7E:AC:B9:CB:36:38 | 5 GHz | 44      | -88          | Weak   |
| Trails End Wifi  | 7A:AC:B9:CB:36:38 | 5 GHz | 44      | -88          | Weak   |
| Barn North (:C1) | 7A:AC:B9:CA:3B:C1 | 5 GHz | 44      | -89          | Weak   |
| Welcome (:38)    | 7E:AC:B9:CB:36:38 | 5 GHz | 36/44   | -40          | Strong |

---

## Next Steps

- [ ] Test throughput from Cabin 13 → EAP → Beryl bridge
- [ ] Measure signal from candidate backhaul antenna (Site 3 / Barn)
- [ ] Document final mounting location and cable run
