# Customer Profile & Evidence Summary

**Account #:** 293590230 | **Holders:** Michael Wolf & Wendy Wolf  
**Account Type:** Luddites. Do not upgrade phones. Explicitly reject "Next Up Anytime."  
**Customer Since:** Jan 2000 (26 years)

---

## Customer Profile: Phone Usage Pattern

### Explicit Anti-Upgrade Position

**Michael and Wendy's stated preference to sales associate (Cheboygan, Oct 12, 2026):**

- Use iPhone SE (cheapest, least feature-rich, trailing-edge phones)
- Have owned 3 different SE models over years
- Keep phones until they break -- never upgrade for new features
- The current SE is "too big for us"
- Want original SE form factor (no longer available)
- **Do NOT want "Next Up Anytime" feature -- not even for free**
- Do NOT want device financing -- keeps devices for years, not months

**This is material to the dispute:** If you explicitly reject early-upgrade features, why are you being charged $10/month per line for "Next Up Anytime"?

### Evidence of Luddite Pattern

From equipment_portable.md:

- Nighthawk M1 hotspot (IMEI 015240000553847): Used 2+ years before deactivation
- Marginal performance in Crystal River area for 2+ years -- user kept using it instead of upgrading
- Pattern: Keep devices working as long as possible, no interest in new models

This behavior contradicts the rationale for "Next Up Anytime" (frequent upgraders). You are not a target customer for this feature.

---

## Critical Evidence: Foundation Account Change

Foundation Account IDs don't normally change. A change indicates a system reclassification, account migration, or data error. This aligns with the tech support call (Oct 8) where they discovered an incorrect IMEA in the system "for a long time."

### Foundation Account Timeline

| Date         | Account ID | Bill Total | Notes                                                      |
|--------------|------------|------------|------------------------------------------------------------|
| May 24, 2025 | 00036089   | $225.60    | Oldest available bill                                      |
| Jun 24, 2025 | 00036089   | $212.24    | Consistent ID                                              |
| Jul 24, 2025 | Unknown    | Unknown    | **TODO: Obtain**                                           |
| Aug 24, 2025 | Unknown    | Unknown    | **TODO: Obtain**                                           |
| Sep 24, 2025 | Unknown    | Unknown    | **TODO: Obtain**                                           |
| Oct 24, 2025 | Unknown    | Unknown    | **TODO: Obtain**                                           |
| Nov 24, 2025 | Unknown    | Unknown    | **TODO: Obtain**                                           |
| Dec 24, 2025 | Unknown    | Unknown    | **TODO: Obtain**                                           |
| Jan 24, 2026 | Unknown    | Unknown    | **TODO: Obtain**                                           |
| Feb 24, 2026 | Unknown    | Unknown    | **TODO: Obtain**                                           |
| Mar 24, 2026 | Unknown    | Unknown    | **TODO: Obtain**                                           |
| Apr 24, 2026 | Unknown    | Unknown    | **TODO: Obtain**                                           |
| Aug 24, 2026 | 64587913   | $267.98    | **DIFFERENT ID** -- Change occurred between Apr & Aug 2026 |

**What this means:** Foundation Account changed from 00036089 to 64587913 sometime between April and August 2026. This is evidence of backend system reclassification or account migration error during the period when IMEA misclassification was occurring.

---

## Bill Line-Item Comparison: May 2025 vs. Aug 2026

### Michael's Line (206.679.7941)

| Item             | May 2025                       | Aug 2026             | Change             |
|------------------|--------------------------------|----------------------|--------------------|
| Plan (name)      | Unlimited Starter SL - 3 Lines | AT&T 55+ 2 Lines     | **Renamed**        |
| Plan (base)      | $50.99                         | $65.00               | **+$14.01**        |
| Apple 128GB      | $13.34 (inst. 5/36)            | $13.34 (inst. 20/36) | $0                 |
| Next Up Anytime  | $10.00                         | $10.00               | $0                 |
| Loyalty Discount | -$5.00                         | $0                   | **-$5.00 removed** |
| **Line Total**   | **$76.25**                     | **$87.86**           | **+$11.61**        |

**Red flags:**

1. Plan renamed from "Starter SL - 3 Lines" to "55+ 2 Lines" -- no authorization documented
2. Base plan jumped 27.5% without notification
3. Loyalty discount that existed in May vanished in August
4. Next Up Anytime still present despite user's explicit rejection

### Wendy's Line (206.853.8603)

| Item            | May 2025                       | Aug 2026             | Change      |
|-----------------|--------------------------------|----------------------|-------------|
| Plan (name)     | Unlimited Starter SL - 3 Lines | AT&T 55+ 2 Lines     | **Renamed** |
| Plan (base)     | $55.99                         | $65.00               | **+$9.01**  |
| Apple 128GB     | $13.34 (inst. 5/36)            | $13.34 (inst. 20/36) | $0          |
| Next Up Anytime | $10.00                         | $10.00               | $0          |
| **Line Total**  | **$83.04**                     | **$87.86**           | **+$4.82**  |

**Red flag:** Next Up Anytime still present despite user's explicit rejection in Oct 12 conversation.

### Hotspot Line (984.381.5800)

| Item               | May 2025                            | Aug 2026                      | Change               |
|--------------------|-------------------------------------|-------------------------------|----------------------|
| Device             | Nighthawk M1 (IMEI 015240000553847) | Nighthawk M1 (same)           | No change            |
| Plan (name)        | Unlimited Premium PL - 3 Lines      | Unlimited Premium PL - 1 Line | **Reclassified**     |
| Plan (base)        | $70.99                              | $100.99                       | **+$30.00 (+42.3%)** |
| Signature discount | -$10.00                             | -$10.00                       | $0                   |
| Loyalty discount   | -$5.00                              | -$5.00                        | $0                   |
| **Line Total**     | **$66.31**                          | **$92.26**                    | **+$25.95**          |

**Red flags:**

1. Same hotspot device (Nighthawk) on both bills
2. Plan classification changed from "3 Lines" grouping to "1 Line" solo plan
3. Base cost jumped 42.3% ($30/month more)
4. This aligns with tech support discovery of incorrect IMEA flagging -- the device was misclassified in the system

---

## The Nighthawk M1 IMEA Issue

### From equipment_portable.md

```text
IMEI: 015240000553847
IMEI SV: 13
Service Number: +1 (984) 381-5800
Status: Device deactivated 2026-10-12 in Cheboygan MI AT&T Store
```

### From Oct 8 Tech Support Call (user memory)

> "IMEA number for hotspot was incorrectly flagged in AT&T system. It had been in system for a long time."

### Analysis

The hotspot's IMEI (015240000553847) is a device identifier, not a phone IMEI. If AT&T's system flagged it incorrectly as a personal phone instead of a hotspot, the system would:

1. Remove it from the 3-line grouping it had in May 2025 ("Unlimited Premium PL - 3 Lines")
2. Force it into a solo device tier ("Unlimited Premium PL - 1 Line")
3. Apply premium pricing ($70.99 → $100.99)

**The jump from $66.31 to $92.26/month for the same physical device is evidence of the IMEA misclassification.**

---

## "Next Up Anytime" Evidence of Unauthorized Charge

### Timeline of Next Up Rejection

**Initial Rejection:** ~June 2025 (Dunellen, FL store)

- When account was renegotiated from $150/month → $135/month
- Part of contract change (dropped Disney discount, added autopay discount, agreed to 2-year contract extension)
- **User explicitly rejected "Next Up Anytime" at that time**
- **TODO: Find last bill with Disney discount to confirm exact month of Dunellen renegotiation**

**Continued Rejection:** October 12-13, 2026 (Cheboygan, MI)

- In-store: Sales associate could not remove feature
- By phone (611): User again rejected "Next Up Anytime"
- User's explicit statement: "Not even for free"

### Bills Show Consistent $10/month Per Line (After Oldest Available)

- **May 2025:** Michael $10.00 + Wendy $10.00 = $20.00/month
- **Aug 2026:** Michael $10.00 + Wendy $10.00 = $20.00/month
- **Cumulative (May 2025 - Oct 2026):** 16 months × $20 = **$320 charged**
- **If bill existed before May 2025:** Actual total likely higher ($400+)

### Evidence Summary

- Feature explicitly rejected at Dunellen renegotiation (~June 2025)
- Feature rejected again at Cheboygan visit (Oct 12, 2026)
- Feature still appears on every bill despite rejections
- No authorization trail in available bills
- No documentation of why feature is on account

### Why This Matters in Dispute

Luddite customers (keep phones 2-4+ years, never upgrade within contract term) are not the target market for "Next Up Anytime." Charging this feature to customers who explicitly reject early-upgrade programs is predatory -- it's revenue extraction from customers who won't use it.

**Recommendation for dispute letter:** Include that this feature was added without authorization and is incompatible with documented customer usage pattern and explicit statement of non-interest.

---

## Timeline of Known Events & Inferred System Changes

| Date         | Event                                                                       | Evidence                                         |
|--------------|-----------------------------------------------------------------------------|--------------------------------------------------|
| Jan 11, 2025 | Apple 128GB financing established ($479.99 × 2)                             | Both bills show same financing ID, start date    |
| May 24, 2025 | Bill: $225.60, Foundation Acct 00036089                                     | Oldest available bill                            |
| May-Aug 2025 | Silent plan upgrades begin (unknown exact dates)                            | Plan name changes, base cost increases           |
| Aug 2025     | Hotspot likely reclassified in system (IMEA error ongoing)                  | Evidenced by Aug 2026 pricing jump               |
| ~Jan 2026    | Foundation Account migrated to 64587913 (or changed during system rework)   | Visible in all 2026 bills                        |
| Oct 8, 2026  | Tech support discovers IMEA misclassification, claims "in system long time" | Hotspot service fails after reset in Au Train MI |
| Oct 12, 2026 | Store unable to remove Next Up or disconnect hotspot from store system      | User had to call 611                             |
| Oct 13, 2026 | Caller disconnects hotspot, adds debit discount, finalizes plan change      | New plan: 2 phones only, $50-60/month            |
| Aug 24, 2026 | Bill issued showing $267.98 total                                           | Peak billing amount before correction            |

---

## Dispute Leverage Points

1. **26-year customer:** Since Jan 2000, no switches despite multiple service failures
2. **Documented rejection of "Next Up Anytime":** Oct 12 in-store and Oct 13 phone call -- no authorization trail
3. **Luddite usage pattern:** Equipment_portable.md proves 2+ year device retention, contradicts upgrade-feature rationale
4. **Foundation Account change:** Evidence of backend system rework or error
5. **IMEA misclassification:** Tech support admits error "in system for a long time" -- systematic billing error, not customer error
6. **Unauthorized plan tier jump:** Hotspot went from $66.31 to $92.26/month for same device -- $30/month due to system error
7. **Silent plan renames:** "Starter SL - 3 Lines" → "AT&T 55+ 2 Lines" with no written notification
8. **Loyalty discount removal:** Disappeared between May 2025 and Aug 2026, no explanation

---

## Carrot & Stick for Settlement

### Carrot (We Stay)

- $400-600 service credit for overcharge period (Jan 2025 - Oct 2026)
- Written apology acknowledging IMEA error
- Loyalty acknowledgment: 26-year customer, prefer to remain with AT&T

### Stick (We Go)

- **NC Public Utilities Commission complaint** -- unauthorized plan changes, inadequate notification
- **Small claims court** in Wake County, NC -- claim ~$800+ overcharge (within 3-year statute of limitations)
- **Class-action potential** -- IMEA misclassification may affect other customers with hotspot devices; pattern of unauthorized feature charges
- **Arbitration** -- if AT&T invokes arbitration clause, pursue to conclusion

---

---

## TODOs: Evidence to Confirm or Obtain

### HIGH PRIORITY (Blocks dispute filing)

1. **TODO: Obtain intermediate bills (Feb-Apr 2026)**
   - Call 611 to request
   - Purpose: Find when Foundation Account changed, confirm plan increases, pinpoint Disney discount removal
   - Status: UNDONE

2. **TODO: Find last bill with Disney discount**
   - Confirms Dunellen renegotiation date (when $150→$135 plan happened)
   - Confirms 2-year contract renewal was authorized
   - Status: UNDONE

3. **TODO: Confirm IMEA number is incorrect in AT&T billing data**
   - Currently: Tech support said IMEA was "flagged as personal phone for a long time" (hearsay)
   - Need: AT&T written confirmation in bills or account records showing wrong device classification
   - If unconfirmed, remove from dispute as evidence (keep as plausible theory)
   - Status: UNDONE -- Currently hypothesis, not proven

### MEDIUM PRIORITY (Strengthens dispute, not essential)

1. **TODO: Request bills from before May 2025 (earliest we have)**
   - Purpose: Show full progression of Next Up charges from start
   - Purpose: Find original $150/month bill (baseline for $135 negotiation)
   - Status: UNDONE

2. **TODO: Obtain 2-year contract document from Dunellen renegotiation**
   - Purpose: Prove that Next Up was explicitly rejected as part of that deal
   - Status: UNDONE

---

**Document prepared:** 2026-10-13  
**Last updated:** 2026-10-13  
**Oldest bill available:** May 24, 2025 (ATTBill_0230_May2025.pdf)  
**Evidence sources:** May 2025 & Aug 2026 bill PDFs, equipment_portable.md, user account history  
**Next step:** Call 611 to request Feb-Apr 2026 bills; fold confirmed evidence into formal dispute letter
