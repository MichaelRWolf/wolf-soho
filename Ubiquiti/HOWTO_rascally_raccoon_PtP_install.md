# HOWTO_rascally_raccoon_PtP_install.md

## Purpose

Physical installation of the Ubiquiti airMAX PtP link and RV Wi‑Fi distribution for the **Rascally Raccoon** winter site.

---

## System Topology

```text
House Router
 → PoE Injector
 → Indoor Ethernet
 → Wall RJ45 (Inside)
 → Wall RJ45 (Outside / Porch)
 → Surge Protector (bonded)
 → Outdoor Ethernet (CMX or UniFi Outdoor)
 → PtP Radio (House)

PtP Radio (House) ))) ~460 ft RF~ ((( PtP Radio (RV)
                                        ↓
                                      PoE
                                        ↓
                                      UAP
                                        ↓
                                   RV Wi‑Fi
```

---

## Mounting Guidelines

### Height & Line of Sight

* Clear Fresnel zone more important than raw height
* 8–12 ft above ground is usually sufficient
* Avoid people regularly walking through the beam

### Co‑mounting PtP + UAP

* Same pole/tree is fine
* Vertical separation: **≥ 3 ft preferred**, ≥ 1 ft minimum
* Aim PtP precisely; UAP is omnidirectional

---

## Alignment Process

1. Power both radios
2. Log into either radio → **Status** page
3. Watch:

   * Signal strength (dBm)
   * Noise floor
   * SNR / airMAX Quality
4. Adjust **one side at a time**
5. Pause 5–10s between movements
6. Tighten when metrics peak and stabilize

---

## Power Strategy

### Recommended

* PoE injectors **at ground level** in weatherproof box
* Run **Ethernet up the tree/pole**, not AC

Reasons:

* Lower energy
* Easier surge protection
* Fewer safety issues

---

## Surge Protection (House Side)

### Placement

* At **porch exterior RJ45**, before outdoor run

### Bonding

* Bond surge protector to **house grounding system**
* Use 12–14 AWG copper
* Keep bond ≤ ~6 ft, straight

### Do NOT Bond To

* Tree
* Rebar
* Nails
* Deck hardware
* Separate ground rods

---

## RV / Tree Side

* No separate ground rod
* Do not bond to tree
* Optional surge protector only if bonded to same system (usually skip)

---

## RF Safety

* Power levels are low (Wi‑Fi class)
* No eye hazard at normal distances
* Do not stand directly in beam at <1 ft for extended time

---

## Weatherproofing

* Drip loops on all cables
* UV‑rated ties
* Seal wall penetrations
* Desiccant in enclosures

---

## Final Checklist

* Radios labeled
* Surge protector bonded
* Cables strain‑relieved
* Alignment verified
* Throughput test passed

---

END
