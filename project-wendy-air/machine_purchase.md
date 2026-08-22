# MacBook Air Purchase Guide: M1/M2/M3 Comparison

**Purpose:** Specification guide for purchasing replacement MacBook Air (M-series) for Michael and Wendy.

---

## Quick Specs

| Aspect        | Requirement                                                  |
|---------------|--------------------------------------------------------------|
| **Model**     | MacBook Air (13-inch or larger)                              |
| **Processor** | M1, M2, or M3 (M3 preferred if available)                    |
| **RAM**       | 16 GB minimum (matches michael-air, Wendy's pro)             |
| **Storage**   | 256 GB minimum (Wendy may want 512 GB if higher volume work) |
| **OS**        | macOS Sequoia 15.x (or later)                                |
| **Age**       | 2024 model year preferred; 2023 acceptable                   |

---

## Processor Comparison: M1 vs M2 vs M3

| Feature                       | M1 (Nov 2020)       | M2 (Jul 2022)      | M3 (Mar 2024)                   |
|-------------------------------|---------------------|--------------------|---------------------------------|
| **Cores**                     | 8 (4P+4E)           | 8 (4P+4E)          | 8 (4P+4E)                       |
| **GPU**                       | 7-8 core            | 8-10 core          | 8 core                          |
| **TDP**                       | ~10W                | ~10W               | ~10W                            |
| **Performance gain vs prior** | baseline            | ~20%               | ~30%                            |
| **Availability**              | Limited (refurb)    | Common (used)      | Common (new/refurb)             |
| **Price (eBay typical)**      | $500-650            | $600-800           | $800-1000+                      |
| **Recommendation**            | Acceptable if <$600 | Good middle ground | Preferred (best perf/available) |

---

## Avoid These Models

- **MacBook Air M1 (early 2020)** -- Only 7-core GPU option; rare/expensive
- **MacBook Air Intel (any year)** -- Requires full x86_64 remediation; large cleanup overhead
- **13" base M1/M2/M3 with 256GB** -- Storage fills quickly; consider 512 GB if budget allows
- **MacBook Air 11" (2015 or older)** -- Insufficient specs; avoid

---

## eBay Search Tips

### M3 (2024 -- Recommended)

```text
MacBook Air 13 M3 2024 16GB 256GB
MacBook Air M3 2024 16GB
A3113 MacBook Air  # (model number for 13" 2024)
```

**Look for:**

- Condition: "Like new" or "Very Good"
- Seller rating: 98%+ positive feedback
- Includes charger & box (for resale value if needed)
- Return policy ≥ 30 days

### M2 (2022 -- Fallback)

```text
MacBook Air 13 M2 2022 16GB 256GB
MacBook Air M2 2022 16GB
A2681 MacBook Air  # (model number for 13" 2022)
```

### M1 (2020-21 -- Budget Option)

```text
MacBook Air M1 2020 16GB 256GB
MacBook Air M1 2021 16GB
A2337 MacBook Air  # (model number for 13" 2021)
```

---

## michael-air Purchase Reference

**Machine:** MacBook Air (13-inch, M3, 2024)  
**Model Number:** A3113  
**Specs:**

- Processor: Apple M3 (8-core CPU, 8-core GPU)
- RAM: 16 GB
- Storage: 256 GB SSD
- OS: macOS 15.7 Sequoia

**Purchase Details:**

- Seller: gadgetpickup (eBay, 99.9% feedback)
- Condition: Like new
- Price: [**Update with actual price**]
- Date: 2026-08 (approximately)

**Setup Time (michael-air):**

- Time Machine restore: ~4 hours
- Shell & Homebrew: ~2 hours
- Intel artifact remediation: ~2 hours
- Time Machine exclusions: ~2 hours
- **Total: ~10 hours of active work**

---

## wendy-air Recommended Specs

**Primary option (best value):**

- MacBook Air 13" M3 2024
- 16 GB RAM
- 256 GB storage
- eBay search: `MacBook Air M3 2024 16GB 256GB` or `A3113 MacBook Air`

**Alternative (budget/fallback):**

- MacBook Air 13" M2 2022
- 16 GB RAM
- 256 GB storage
- eBay search: `MacBook Air M2 2022 16GB` or `A2681 MacBook Air`

---

## michael-air vs wendy-air: Minimal Differences

Both machines require:

- ✓ Time Machine restore from water-damaged predecessor
- ✓ Shell fix (Intel binary → ARM64 native)
- ✓ Homebrew rebuild (Intel → ARM64)
- ✓ x86_64 audit + remediation
- ✓ Time Machine exclusion configuration

**Key differences:**

- NAS share name: `Backups-TM-Michael-Air` vs `Backups-TM-Wendy-Air`
- Service account: `tm-michael-air` vs `tm-wendy-air`
- Hostname: `michael-air` vs `wendy-air`
- SSH key comment: `michael@michael-air` vs `wendy@wendy-air`
- 1Password entry: "NAS - TM - tm-michael-air" vs "NAS - TM - tm-wendy-air"

(See [CONTEXT.md](../CONTEXT.md) for canonical device registry)

---

## Setup Process (Same for Both)

1. **Restore** via Time Machine (Migration Assistant) -- See [project-michael-air/TEMPLATE-macbook-air-setup.md](../project-michael-air/TEMPLATE-macbook-air-setup.md)
2. **Identify issues** (Shell, Homebrew, TCC permissions)
3. **Run audit** -- `./x86_64-audit.sh`
4. **Remediate** (remove Intel artifacts, rebuild tools)
5. **Configure Time Machine** with exclusions
6. **Validate** backup contains only intended data

---

## Estimated Total Cost

- **Machine (M3, 13", 16GB/256GB):** $800-1000
- **Shipping & tax:** Variable
- **Total:** $900-1100 per machine
