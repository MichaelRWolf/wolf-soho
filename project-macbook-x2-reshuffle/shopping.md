# MacBook Shopping Tracker

---

## Machine Requirements

### Michael's Requirements

**Primary workload:** Claude Code (cloud-based) + light git operations + bash scripting.

| Requirement         | Must-have | Details                                                              |
|---------------------|-----------|----------------------------------------------------------------------|
| **CPU**             | M-series  | M3+ preferred for Homebrew support and modern macOS; M2 acceptable   |
| **RAM**             | 16GB      | 8GB minimum works; 16GB recommended for multi-file Claude sessions   |
| **Storage**         | 256GB+    | Code repos + Claude cache                                            |
| **macOS**           | Tahoe+    | Monterey acceptable but EOL mid-2026; Tahoe/Sonoma preferred         |
| **Battery health**  | >80%      | For used/refurbished; confirm cycle count and original Apple battery |
| **Activation Lock** | Clean     | Must be free of MDM enrollment and Activation Lock                   |
| **Warranty**        | Preferred | 1-year+ coverage valuable for refurbished/used machines              |
| **Homebrew**        | No Intel  | Apple Silicon avoids deprecation warnings (cosmetic but annoying)    |

**Why these matter:** Claude Code is cloud-based (low local load). Git is pure CLI. M-series avoids Homebrew nag. 16GB RAM provides headroom for multi-file analysis.

**AI/Claude Code specific:** Stable WiFi/ethernet, low latency API calls. No GPU needed (cloud inference). Browser memory for large context windows (16GB headroom).

**Not needed:** Native IDEs, compilers, video editing, GPU (integrated is sufficient), high local CPU, native LLM training.

---

### Wendy's Requirements

**Primary workload:** Safari browser with 10-50+ concurrent tabs + SaaS web services (ChatGPT, Sheets, Docs, MailChimp, webmail).

| Requirement         | Must-have | Details                                                             |
|---------------------|-----------|---------------------------------------------------------------------|
| **CPU**             | ANY       | CPU is NOT the bottleneck; M2/M3/M4 all sufficient for web browsing |
| **RAM**             | 16GB      | **CRITICAL.** Safari tab management requires 16GB minimum           |
| **Storage**         | 256GB+    | SaaS data lives in cloud; local storage is minimal need             |
| **macOS**           | Tahoe+    | Monterey acceptable short-term (EOL mid-2026); prefer Tahoe/Sonoma  |
| **Display quality** | 1080p+    | For streaming video (Amazon Prime) and web browsing clarity         |
| **Video codec**     | 1080p+    | Streaming playback support (H.264, VP9)                             |
| **Battery health**  | >80%      | For used/refurbished; confirm cycle count                           |
| **Activation Lock** | Clean     | Must be free of MDM enrollment                                      |
| **Warranty**        | Preferred | 1-year+ coverage; return policy valuable for peace of mind          |

**Why these matter:** RAM is the limiter for 50+ Safari tabs. CPU is irrelevant (cloud-first user). Display quality for video streaming and web comfort. Battery health ensures machine doesn't fail mid-day.

**Zoom calls specific:** Built-in mic/camera sufficient (1080p+ video). Thermal management (quiet fan or fanless). Stable WiFi. Audio codec support (Opus, H.264 video).

**Not needed:** High CPU, discrete GPU (integrated is sufficient), compilers, development tools, large local storage, gaming/3D capabilities.

---

## How to Find Battery Cycle Count (GUI)

When asking sellers for battery health, they can check this way without Terminal:

1. Click **Apple menu** (top-left) → **About This Mac**
2. Click **System Report...** button
3. In the left sidebar, click **Power**
4. Look for **Cycle Count** in the right pane (e.g., "452 cycles")
5. Send you a screenshot or the cycle count number

**Rule of thumb:** Under 300 cycles = excellent (new); 300-700 = good (refurb baseline); 700-1000 = acceptable (used); >1000 = worn (avoid unless heavily discounted).

---

## Active Listings

### Quick Comparison

| # | Offering | CPU | RAM  | Disk  | OS/EOL      | Video  | Batt    | MDM | Cond        | Status            |
|---|----------|-----|------|-------|-------------|--------|---------|-----|-------------|-------------------|
| 1 | Apple    | M2  | 16GB | 512GB | Sonoma/2028 | 1080p+ | TBD     | TBD | eBay Refurb | Awaiting reply    |
| 2 | Bilberry | M2  | 8GB  | 512GB | Sonoma/2028 | 1080p+ | Unknown | N/A | F5 Refurb   | Negotiable; risky |

---

### 1. Apple --- A-Offering (Wisetek Market M2 Refurb)

**Status:** Awaiting seller message return

- **Link:** [eBay Listing #800079144456](https://www.ebay.com/itm/800079144456)
- **Price:** $614.50 (free shipping)
- **Machine:** Apple MacBook Air (M2, 2022), 13.6", 16GB RAM, Space Gray
- **Condition:** eBay Refurbished
- **Warranty:** 1-year included
- **Seller:** Wisetek Market (99.1% positive; 15482 ratings)
- **Specs claimed:** 18 hrs battery life
- **Your question:** Requested battery health %, cycle count, original Apple battery status, Activation Lock / MDM enrollment status
- **Assessment:** Higher-tier refurb rating; awaiting detailed battery/lock response
- **Fit for Michael:** ✅ **YES** --- M2 + 16GB RAM meets all requirements; solid choice if battery > 80%
- **Fit for Wendy:** ✅ **YES** --- 16GB RAM is exactly what Wendy needs for Safari tab management

---

### 2. Bilberry --- B-Offering (ITAD Technologies M2, 8GB)

**Status:** In second place; price negotiable

- **Link:** [eBay Listing #128000806739](https://www.ebay.com/itm/128000806739)
- **Price:** $549.99 or Best Offer (~$49.38/mo financing available)
- **Machine:** Apple MacBook Air 13" (M2), 8GB LPDDR5, 512GB SSD, macOS Sonoma (MLY43LL/A)
- **Condition:** Used; "F5 Refurbished"
- **Returns:** 30-day return policy on 8GB variant
- **Seller:** ITAD Technologies (9578 ratings)
- **Assessment:** Lower price; used condition; only 8GB RAM (tight for multi-file work); no warranty mentioned yet
- **Risk:** 8GB is at lower end of Michael's comfort zone (16GB recommended); battery status unknown
- **Fit for Michael:** ⚠️ **TIGHT** --- 8GB RAM is below recommended 16GB; would work but no headroom for multi-file sessions
- **Fit for Wendy:** ❌ **NO** --- 8GB RAM is inadequate for 50+ Safari tabs; would cause lag and crashes

---

## Summary & Next Steps

**For Michael:** Option 1 (Apple) is preferred if battery health > 80%. Option 2 (Bilberry) is budget alternative but 8GB is tight.

**For Wendy:** Option 1 (Apple) meets 16GB requirement. Option 2 (Bilberry) is insufficient.

**Next steps:**

1. Wait for Wisetek response on Apple (1) battery health and Activation Lock
2. If Apple (1) confirms good battery (>80%) and clean lock status, **proceed with 1**
3. If Wisetek silent or poor battery report, escalate Bilberry (2) with negotiation ("$500 max; 8GB is tight for our use case")
4. If both fail, continue hunting M3 options (better value long-term than M2)
