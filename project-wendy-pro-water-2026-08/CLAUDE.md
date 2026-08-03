# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**project-wendy-pro-water-2026-08** is a hardware recovery project tracking the repair of `wendy-pro` (MacBook Pro) after water damage from a broken water bottle (incident date 2026-08-03).

This is NOT a software development repository. There are no builds, tests, or CI/CD workflows. The directory contains operational documentation and recovery checklists.

## Key Files

- **notes.md** -- Single source of truth for the recovery process. Contains incident summary, drying strategy (Phase 1 & 2), recovery checklist, and comparison to michael-pro's prior water damage recovery (2026-06-18).
- **2026-08-03_wendy-pro_water-damage.md** -- Archive version of initial incident log (redundant with notes.md; kept for historical reference).

## Recovery Strategy

The recovery process follows two phases spanning 48-72 hours:

1. **Phase 1 (24-48h):** Bulk moisture removal via sun + fan drying
2. **Phase 2 (~48h onward):** Mineral deposit prevention using 90% isopropyl alcohol followed by power-on testing

The process is documented in detail in notes.md. For reference to a prior similar recovery, see `2026-06-18_michael-pro_water-damage.md` in the parent directory.

## Common Tasks

- **Check drying progress:** Feel air vent exhaust; should be completely dry after 48h
- **Apply IPA treatment:** After case dries, apply 90% isopropyl alcohol to affected areas (around fan, air port, keyboard edges)
- **Test power:** After IPA evaporates, attempt boot and run diagnostics (Disk Utility, Activity Monitor)
- **Battery disconnection (if needed):** If machine won't power on, refer to michael-pro incident log for battery disconnect procedure

## Notes

- Do NOT use 70% IPA (carries water); use 91% drugstore or 99% lab grade
- Target drying temperature: 100-120°F (prevents adhesive damage above ~140°F)
- Thermal cycling (sun ↔ shade) helps expel trapped moisture more effectively than static heat/fan alone
