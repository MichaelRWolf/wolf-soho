# wendy-pro Water Damage -- Recovery Notes

**Incident Date:** 2026-08-03 (Trails End)

## What Happened

Water bottle broke in briefcase → liquid contacted laptop → opened back panel → found water intrusion around fan, likely through air port → already dried with canned air → now sitting in sun with fan.

## Answers to Your Questions

### How long to sit in sun?

**48-72 hours minimum.**

- First 24-48h: bulk moisture removal (sun + fan combo is ideal)
- After 48h: inspect case -- should feel completely dry to touch
- Continue to 72h if still cool/damp inside vents

Thermal cycling (moving between sun and shade) helps push moisture from pockets trapped near components.

### Will 90% isopropyl alcohol help (like michael-pro)?

**Yes, absolutely.** Same process that saved michael-pro's logic board.

**Timeline:**

- Let machine dry 48h first (bulk water gone, mineral deposits forming now)
- Apply 90% IPA to water-affected areas (around fan, air port, keyboard edges)
- Brush gently; let IPA drain and evaporate (~5 min)
- Run fan after to accelerate evaporation
- IPA displaces water and prevents corrosion deposits on solder joints

**Key point:** michael-pro was treated at ~36h into drying with the same 90%+ IPA and it worked. Don't wait too long -- mineral corrosion deposits start forming immediately.

**90% is fine** (drugstore isopropyl works; 99% lab grade also works). Avoid 70% IPA (too much water).

## Quick Action Plan

1. **Now through 2026-08-05 (48h):** Sun + fan, no intervention
2. **2026-08-05 evening:** Check case feels dry; if still damp, continue another 12-24h
3. **2026-08-05 to 2026-08-06:** Apply 90% IPA to affected areas
4. **After IPA:** Run fan 10-15 min, wait 5 min, attempt power-on
5. **If boots:** Run Disk Utility / Activity Monitor to confirm no hardware errors
6. **If no boot:** Refer to michael-pro procedure for battery disconnect and motherboard inspection

## Files

- [2026-08-03_wendy-pro_water-damage.md](../2026-08-03_wendy-pro_water-damage.md) -- Main incident log with full recovery procedure
- [2026-06-18_michael-pro_water-damage.md](../2026-06-18_michael-pro_water-damage.md) -- Reference: battery disconnect, disassembly, IPA treatment, corrosion cleaning

---

**Started:** 2026-08-03 ~afternoon (exact time TBD)
**Next check:** 2026-08-05 evening (48h mark)
