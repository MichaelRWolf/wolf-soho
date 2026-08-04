# Wendy's Machine Options Analysis

**Focus:** Wendy's independent hardware needs. SaaS-first workflow; heavy Safari tab usage is the primary constraint.

**Decision:** Which machine offers best value for Wendy's actual workload?

---

## Workload Constraints

| Factor                | Impact | Notes                                                       |
|-----------------------|--------|-------------------------------------------------------------|
| **Safari tabs (50+)** | HIGH   | RAM is bottleneck, not CPU. Needs 16GB minimum.             |
| **Zoom video calls**  | LOW    | 1080p codec support; any M-series handles trivially         |
| **Cloud apps**        | LOW    | ChatGPT, Sheets, Docs, MailChimp, GoDaddy -- all web-based  |
| **Mail.app (IMAP)**   | LOW    | ATT.net backlog; email is low-CPU workload                  |
| **Video streaming**   | LOW    | Amazon Prime 1080p+ supported by any modern chip            |
| **Local development** | NONE   | Not a developer; no git, no CLI work                        |
| **Native apps**       | LOW    | Notes, Calendar, Reminders -- lightweight                   |
| **Backup strategy**   | MEDIUM | NAS Time Machine; restore from 3-week-old backup sufficient |

---

## Machine Options Matrix

### Option 1: wolf-air (2015 MacBook Air, Intel Core i5 1.8 GHz, 8GB RAM)

| Dimension                       | Rating          | Assessment                                                                                                        |
|---------------------------------|-----------------|-------------------------------------------------------------------------------------------------------------------|
| **Safari tab handling**         | ⚠️ TIGHT        | 8GB RAM for 50+ tabs: possible but requires discipline. Significant swap/slowdown when tabbing furiously.         |
| **Cloud service compatibility** | ✅ ACCEPTABLE    | Monterey 12.7.6 supports all major web services (Zoom, Sheets, Docs, ChatGPT) through 2026.                       |
| **Zoom performance**            | ✅ ACCEPTABLE    | 1080p video codec + dual-core i5 = fine for 1-on-1 calls; may struggle with large group calls (20+ participants). |
| **macOS updates**               | ❌ UNACCEPTABLE  | Stuck at Monterey; cannot upgrade to Tahoe/Sonoma. EOL mid-2026 (6 months away). Security patches end soon.       |
| **Homebrew warnings**           | ⚠️ ACCEPTABLE   | Intel deprecation nags are cosmetic; not a real problem for SaaS user.                                            |
| **Battery life**                | ✅ ACCEPTABLE    | 11-year-old battery will be degraded (50-70% of original); acceptable for desk-bound SaaS use.                    |
| **Cost**                        | ✅ EXCELLENT     | $0 (repurpose existing hardware).                                                                                 |
| **Future-proofing**             | ❌ UNACCEPTABLE  | EOL 6 months away. Not viable as primary machine beyond interim period (3 months max).                            |
| **Migration friction**          | ✅ EXCELLENT     | Time Machine restore from wendy-pro is standard; no hardware surprises.                                           |
| **Startup/shutdown**            | ⚠️ ACCEPTABLE   | Intel boot is slower than M-series (~30-45 seconds); manageable for occasional restarts.                          |
| **Thermals**                    | ✅ GOOD          | Fan will spin under load; not concerning. Passive cooling would be impossible (old chipset).                      |
| **Overall verdict**             | ⚠️ INTERIM ONLY | **Acceptable as temporary (3-6 month) stopgap. NOT viable as long-term primary.**                                 |

**Use case:** Wendy adopts wolf-air immediately post-water-damage to stay productive while hunting for permanent machine.

**Success probability:** ~95% (standard Time Machine restore to working hardware).

---

### Option 2: M2 MacBook Air or Pro (2022, 8GB RAM)

| Dimension                       | Rating       | Assessment                                                                                                                                   |
|---------------------------------|--------------|----------------------------------------------------------------------------------------------------------------------------------------------|
| **Safari tab handling**         | ⚠️ TIGHT     | 8GB RAM with M2 is tighter than M3/M4 due to efficiency cores not being as smart about memory pressure. Will swap; acceptable but not ideal. |
| **Cloud service compatibility** | ✅ EXCELLENT  | Sonoma/Tahoe (current macOS) fully supported; security patches for ~5 years.                                                                 |
| **Zoom performance**            | ✅ EXCELLENT  | M2 GPU + Neural Engine = flawless 1080p; handles group calls with ease.                                                                      |
| **macOS updates**               | ✅ EXCELLENT  | Tahoe current; future Sonoma+1 supported through ~2029.                                                                                      |
| **Homebrew warnings**           | ✅ EXCELLENT  | Apple Silicon; no Intel nags.                                                                                                                |
| **Battery life**                | ✅ EXCELLENT  | M2 efficiency = 14-18 hours typical.                                                                                                         |
| **Cost**                        | ⚠️ MODERATE  | Used 2022 M2 Air: $400-$600. Pro: $500-$700.                                                                                                 |
| **Future-proofing**             | ✅ GOOD       | Solid through 2028+; not cutting-edge by 2026, but capable.                                                                                  |
| **Migration friction**          | ✅ EXCELLENT  | Time Machine restore is seamless.                                                                                                            |
| **Startup/shutdown**            | ✅ EXCELLENT  | M2 boot <10 seconds.                                                                                                                         |
| **Thermals**                    | ✅ EXCELLENT  | M2 runs cool; minimal fan noise.                                                                                                             |
| **Overall verdict**             | ✅ ACCEPTABLE | **Works. 8GB RAM is tight for tab addiction; would recommend 16GB upgrade if budget allows.**                                                |

**Trade-off:** Saves $200-$300 vs. M3/M4, but RAM constraint is annoying.

**Success probability:** ~95% (proven chip; 2-year-old hardware is reliable).

---

### Option 3: M3 MacBook Air (2023, 16GB RAM) ← RECOMMENDED

| Dimension                       | Rating      | Assessment                                                                                        |
|---------------------------------|-------------|---------------------------------------------------------------------------------------------------|
| **Safari tab handling**         | ✅ EXCELLENT | 16GB RAM handles 50+ tabs smoothly; M3 efficiency cores smart about memory pressure. No swap lag. |
| **Cloud service compatibility** | ✅ EXCELLENT | Sonoma/Tahoe current; security patches through ~2030.                                             |
| **Zoom performance**            | ✅ EXCELLENT | M3 GPU outperforms M2; handles any call size trivially.                                           |
| **macOS updates**               | ✅ EXCELLENT | Tahoe current; future Sonoma+2/3 supported. Best-in-class longevity.                              |
| **Homebrew warnings**           | ✅ EXCELLENT | Apple Silicon; zero nags.                                                                         |
| **Battery life**                | ✅ EXCELLENT | 15-18 hours typical; M3 efficiency is solid.                                                      |
| **Cost**                        | ✅ GOOD      | Used 2023 M3 Air 16GB: $500-$700. Sweet spot for value.                                           |
| **Future-proofing**             | ✅ EXCELLENT | Viable primary through 2027+; can adopt as long-term without regret.                              |
| **Migration friction**          | ✅ EXCELLENT | Time Machine restore flawless.                                                                    |
| **Startup/shutdown**            | ✅ EXCELLENT | M3 boot <10 seconds.                                                                              |
| **Thermals**                    | ✅ EXCELLENT | M3 thermals better than M2; silent under light load.                                              |
| **Overall verdict**             | ✅ EXCELLENT | **RECOMMENDED. Best balance of performance, cost, longevity, and RAM for Wendy's needs.**         |

**Why M3 over M4:** Cost savings ($200-$300) don't justify M4's incremental gains for Wendy. M3 is already overkill for her workload.

**Success probability:** ~95% (proven chip; ~1 year of field history).

---

### Option 4: M4 MacBook Air (2024, 16GB RAM)

| Dimension                       | Rating      | Assessment                                                                                       |
|---------------------------------|-------------|--------------------------------------------------------------------------------------------------|
| **Safari tab handling**         | ✅ EXCELLENT | 16GB RAM easily handles 50+ tabs; M4 efficiency is best-in-class. Zero lag.                      |
| **Cloud service compatibility** | ✅ EXCELLENT | Sonoma/Tahoe current; patches through ~2031.                                                     |
| **Zoom performance**            | ✅ EXCELLENT | M4 GPU is overkill; perfect video quality.                                                       |
| **macOS updates**               | ✅ EXCELLENT | Cutting-edge; longest support window (5-6 years).                                                |
| **Homebrew warnings**           | ✅ EXCELLENT | Apple Silicon, latest generation.                                                                |
| **Battery life**                | ✅ EXCELLENT | 16-20 hours typical; M4 efficiency is peak.                                                      |
| **Cost**                        | ⚠️ HIGHER   | Used 2024 M4 Air 16GB: $700-$900.                                                                |
| **Future-proofing**             | ✅ EXCELLENT | Viable through 2029+; future-proofed.                                                            |
| **Migration friction**          | ✅ EXCELLENT | Time Machine restore seamless.                                                                   |
| **Startup/shutdown**            | ✅ EXCELLENT | M4 boot <10 seconds.                                                                             |
| **Thermals**                    | ✅ EXCELLENT | M4 thermals best-in-class; whisper-quiet.                                                        |
| **Overall verdict**             | ⚠️ OVERKILL | **OVERKILL for Wendy's workload. Performance gains not justified by $200-$300 premium over M3.** |

**When to buy M4:** If future budget allows upgrade and Michael's machine is settled first.

**Success probability:** ~95% (newest chip; proven in field).

---

### Option 5: M5 MacBook Air (2025, 16GB RAM)

| Dimension                       | Rating                 | Assessment                                                                           |
|---------------------------------|------------------------|--------------------------------------------------------------------------------------|
| **Safari tab handling**         | ✅ EXCELLENT            | 16GB RAM + M5 efficiency = overkill for tab handling.                                |
| **Cloud service compatibility** | ✅ EXCELLENT            | Latest macOS; patches through ~2032.                                                 |
| **Zoom performance**            | ✅ EXCELLENT            | M5 performance is unnecessary for 1080p video.                                       |
| **macOS updates**               | ✅ EXCELLENT            | Longest possible support window.                                                     |
| **Homebrew warnings**           | ✅ EXCELLENT            | Latest Apple Silicon; zero issues.                                                   |
| **Battery life**                | ✅ EXCELLENT            | 17-21 hours typical; M5 efficiency peak.                                             |
| **Cost**                        | ❌ EXPENSIVE            | New 2025 M5 Air: $1,200-$1,400. Used not yet available (Oct 2025 release).           |
| **Future-proofing**             | ✅ EXCELLENT            | Overkill; viable through 2030+.                                                      |
| **Migration friction**          | ✅ EXCELLENT            | Time Machine restore seamless.                                                       |
| **Startup/shutdown**            | ✅ EXCELLENT            | M5 boot <10 seconds.                                                                 |
| **Thermals**                    | ✅ EXCELLENT            | M5 thermals best-in-class.                                                           |
| **Overall verdict**             | ❌ OVERKILL & EXPENSIVE | **NOT RECOMMENDED. M5 is overkill for Wendy's workload and costs 50% more than M3.** |

**When to buy M5:** Only if Wendy upgrades willingly in 2-3 years and cash flow allows.

---

## Wendy's Recommendation Matrix

| Machine                | Cost      | Viability                        | Recommendation                    | Timeline |
|------------------------|-----------|----------------------------------|-----------------------------------|----------|
| **wolf-air (interim)** | $0        | Interim only (3-6 months)        | Use immediately post-water-damage | Now      |
| **M2 Air 8GB**         | $400-$600 | Acceptable (RAM tight)           | Skip if M3 16GB available         | N/A      |
| **M3 Air 16GB**        | $500-$700 | Excellent (primary)              | ✅ RECOMMENDED                     | ASAP     |
| **M4 Air 16GB**        | $700-$900 | Excellent (overkill)             | Optional upgrade path 2027+       | N/A      |
| **M5 Air 16GB**        | $1,200+   | Excellent (overkill + expensive) | Not recommended now               | N/A      |

---

## Wendy's Decision Path

### Recommended: Interim wolf-air + M3 Air Upgrade

**Phase 1 (Immediate, 1-2 days):** Adopt wolf-air

- Time Machine restore from wendy-pro backup (2026-06-27)
- Viability: Interim (3-6 months max; Monterey EOL mid-2026)
- Cost: $0

**Phase 2 (This week, 3-7 days):** Hunt used M3 Air 16GB

- Search: eBay, Facebook Marketplace, Swappa
- Target: M3, 16GB RAM, 256GB+ SSD
- Cost: $500-$700
- Viability: Primary through 2027+
- Restore from NAS backup (1-2 days)

**Phase 3 (2027+, optional):** Upgrade to M4/M5 if desired

- Not urgent; M3 viable through 2027+

### Timeline

- **Week of 2026-08-05:** Migrate to wolf-air; begin M3 hunt
- **Week of 2026-08-12:** Purchase M3 Air
- **2026-08-13 to 2026-08-15:** Time Machine restore to M3
- **2026-08-16 onwards:** Operational on M3 as primary

---

## Summary: What Wendy Actually Needs

- **RAM:** 16GB minimum (Safari tab addiction)
- **CPU:** M3 sufficient; M4/M5 overkill
- **OS:** Tahoe+ (modern security patches)
- **Storage:** 256GB minimum (cloud-first user; minimal local data)
- **Cost ceiling:** $700 for used M3 Air

**Verdict:** M3 MacBook Air 16GB is the Goldilocks option. Not underpowered, not overkill, and cost-effective.

---

## Sources

- [Claude Code System Requirements](https://houtini.com/articles/claude-code-system-requirements/)
- [macOS Monterey EOL Timeline](https://support.apple.com/en-us/HT211238)
- [M-series Performance Comparison](https://www.anandtech.com/show/21486/the-apple-macbook-pro-m4-pro-review)
