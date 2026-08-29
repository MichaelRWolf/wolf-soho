# wendy-air: Decision Log & Notes

**Project status:** Machine purchase awaiting; setup phase TBD.

---

## TODO

1. [ ] **Analyze wendy-pro TM backup. Confirm 256GB is sufficient for new wendy-air.** -- Mount `Backups-TM-Wendy-Pro` from NAS (192.168.8.129); run `du -sh` on backup to measure actual disk footprint. Expected: ~143GB usage with 113GB free. Decision point: confirm before committing to 256GB hand-down from michael-air vs. purchasing 512GB alternative.

---

## Decision Log

### Storage Sizing: 256GB vs 512GB (2026-08-29)

**Question:** Will 256GB be sufficient if Wendy adopts michael-air?

**Analysis completed:** See [artifact: Michael vs Wendy Storage Analysis](https://claude.ai/code/artifact/d48b3446-d42e-43ac-907b-20bf03e19a1d)

**Preliminary verdict:** ✅ 256GB sufficient for Wendy's cloud-first workflow (projected 143GB usage). Empirical verification pending (see TODO).

**Related decision:** Michael should upgrade to 512GB to escape 90% disk utilization on current michael-air.

---

## References

- [setup.md](setup.md) -- Migration checklist and NAS configuration
- [machine_purchase.md](machine_purchase.md) -- Hardware specs & purchasing guidance
- [project-macbook-x2-reshuffle/wendy-options.md](../project-macbook-x2-reshuffle/wendy-options.md) -- Workload profile and machine comparison matrix
