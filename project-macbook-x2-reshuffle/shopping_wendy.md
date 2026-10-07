# Wendy's MacBook Air Shopping Guide

**Goal:** Find M3 MacBook Air 16GB 512GB with free returns, 1-year warranty.

**Status:** Hunting (as of 2026-10-07). #44 (ideal option) sold out in early Oct 2026.

---

## Wendy's Requirements

**Primary workload:** Safari browser with 10-50+ concurrent tabs + SaaS web services (ChatGPT, Sheets, Docs, MailChimp, webmail).

| Requirement         | Must-have | Details                                                              |
|---------------------|-----------|----------------------------------------------------------------------|
| **CPU**             | M3+       | **M3 minimum** (M2 no longer available; M4+ acceptable but overkill) |
| **RAM**             | 16GB      | **CRITICAL.** Safari tab management requires 16GB minimum            |
| **Storage**         | 256GB+    | SaaS data lives in cloud; local storage is minimal need              |
| **macOS**           | Tahoe+    | Monterey acceptable short-term (EOL mid-2026); prefer Tahoe/Sonoma   |
| **Display quality** | 1080p+    | For streaming video (Amazon Prime) and web browsing clarity          |
| **Video codec**     | 1080p+    | Streaming playback support (H.264, VP9)                              |
| **Battery health**  | >80%      | For used/refurbished; confirm cycle count                            |
| **Activation Lock** | Clean     | Must be free of MDM enrollment                                       |
| **Warranty**        | Preferred | 1-year+ coverage; return policy valuable for peace of mind           |

**Why these matter:** RAM is the limiter for 50+ Safari tabs. CPU is irrelevant (cloud-first user). Display quality for video streaming and web comfort. Battery health ensures machine doesn't fail mid-day.

**Zoom calls specific:** Built-in mic/camera sufficient (1080p+ video). Thermal management (quiet fan or fanless). Stable WiFi. Audio codec support (Opus, H.264 video).

**Not needed:** High CPU, discrete GPU (integrated is sufficient), compilers, development tools, large local storage, gaming/3D capabilities.

---

## Wendy Air Candidates (Updated Oct 2026)

### Status: #44 SOLD OUT

~~#44 was ideal (gadgetpickup M3 Open Box 512GB, 30-day returns, $850) but sold by 2026-10-07.~~ **HUNTING NEW M3 16GB 512GB OPTIONS.**

---

### Current Spec Requirements

**Machine:** M3 MacBook Air, 16GB RAM, **512GB required** (video production workload), Open Box or Very Good Refurb, **30-day returns required**.

**Rationale for 512GB:** wendy-pro had 256GB baseline (2022 M2). Video production scratch files + local project data need headroom. 512GB is non-negotiable.

**Price target:** $800-$900.

---

### Available Candidates

#### #49 -- Jarts Auto Parts M3 Used 512GB ⚠️ (No Returns)

**Link:** [eBay #257772522540](https://www.ebay.com/itm/257772522540) -- Found 2026-10-07

| Factor         | Value                         |
|----------------|-------------------------------|
| Price          | $764.99                       |
| Specs          | M3 16GB 512GB ✅               |
| Condition      | Used (71 cycles, barely used) |
| Returns        | ❌ **NO** (Risk)               |
| Recommendation | ⚠️ **RISKY; SKIP**            |

**Why:** Specs match (512GB required), but no-return policy is disqualifying. "Don't cheap out on Wendy" means protection, not just storage.

**Mitigation rejected:** Allstate warranty ($74.99) doesn't replace free returns. If defect arrives, Wendy is stuck without recourse.

---

#### #43 -- gadgetpickup M3 Open Box 256GB (Below Spec -- Don't Use)

**Link:** [eBay #307108920696](https://www.ebay.com/itm/307108920696) -- Purchased 2026-08-10 (Michael's machine, out of stock)

| Factor         | Value                  |
|----------------|------------------------|
| Price          | $749.99                |
| Specs          | M3 16GB **256GB** ❌    |
| Condition      | Open Box (new)         |
| Returns        | ✅ **Free 30-day**      |
| Warranty       | 1-year included        |
| Recommendation | ❌ **Below spec; skip** |

**Why:** 256GB is below the 512GB requirement for video production. Same trusted seller (gadgetpickup), but storage shortfall is disqualifying. Do not use as fallback.

---

## Hunt Strategy

### Search Terms

**eBay:** `M3 MacBook Air 16GB 512GB -M2 -M1`

### Target Sellers

- **gadgetpickup** (proven, 99.9% feedback) -- if #44 restocks
- **reviveit.io** (Very Good refurb, 99.8%, 119.5K ratings)
- **itsworthmore** (refurb tested, 99.6%, 170.1K ratings)
- **eBay Refurbished** (official refurbs with return policy)

### Verification Checklist

Before purchasing, confirm:

- ✅ Return policy: 30+ days free returns (non-negotiable)
- ✅ Battery cycle count: <200 for refurb, <50 for Open Box
- ✅ Warranty: 1-year included preferred
- ✅ Activation Lock: Clean (free of MDM enrollment)
- ✅ Specs: M3 16GB 512GB exactly (or 256GB fallback)

### Add New Listings Here

When you find M3 16GB 512GB options, add them with date and link:

```markdown
#### #50 -- [Seller Name] M3 [Condition] [Storage]

**Link:** [eBay #XXXXXXXXX](https://www.ebay.com/itm/XXXXXXXXX) -- Found [DATE]
```

---

## Decision Rules

| Condition                        | Action                                 |
|----------------------------------|----------------------------------------|
| **M3 16GB 512GB + free returns** | 🟢 **BUY** (exact match)               |
| **M3 16GB 256GB + free returns** | 🔴 **SKIP** (below 512GB requirement)  |
| **M3 16GB 512GB, no returns**    | 🔴 **SKIP** (return risk too high)     |
| **M2 anything**                  | 🔴 **SKIP** (outdated chip)            |
| **M3 8GB anything**              | 🔴 **SKIP** (insufficient RAM)         |
| **M4+ 16GB 512GB**               | 🟡 **ACCEPTABLE** (overkill but works) |

---

## Reference

**Parent document:** [shopping.md](shopping.md) -- Full tracker with Michael's options and all historical listings.

**Related files in project:**

- [michael-options.md](michael-options.md) -- Michael's hardware analysis
- [wendy-options.md](wendy-options.md) -- Detailed workload comparison
- [notes.md](notes.md) -- Strategy and timeline
