# wendy-air Setup: Migration Issues & Resolutions

**Timeline:** TBD (awaiting machine purchase)  
**Source:** Intel MacBook Pro (wendy-pro), water damaged  
**Method:** Time Machine restore via Setup Assistant from NAS backup

**For detailed template:** See [project-michael-air/TEMPLATE-macbook-air-setup.md](../project-michael-air/TEMPLATE-macbook-air-setup.md)  
**For lessons learned:** See [project-michael-air/setup.md](../project-michael-air/setup.md)

---

## ⚠️ BLOCKING CONSTRAINT: Migration Sequence

**Wendy's migration cannot start until Michael completes his migration.**

**Correct order:**

1. **Michael:** Migrate from michael-air (M3, current, 256GB) → michael-air2 (M3, new, 512GB)
   - Fresh Time Machine backup created on michael-air (clean M3 source)
   - Restore to michael-air2 via Migration Assistant
   - Status: [project-michael-air](../project-michael-air/) tracks this

2. **Wendy:** Migrate from wendy-pro (M2, water damaged) → michael-air (M3, 256GB, renamed to wendy-air)
   - Michael's current machine becomes Wendy's machine
   - Wendy restores from her wendy-pro Time Machine backup (NAS)
   - Rename to `wendy-air` per [CONTEXT.md](../CONTEXT.md)

**Why this order matters:** Michael's migration must complete first so Wendy can adopt michael-air (clean M3 baseline) instead of waiting for a new machine. This avoids Intel artifact contamination and gives both users modern M3 hardware.

**Status:** Awaiting michael-air2 acquisition and Michael's migration start.

---

## TODO: Network & NAS Configuration

**Before setup, document/confirm the following naming:**

- [ ] **CONTEXT.md reference** -- Verify device name will be `wendy-air` (canonical registry)
- [ ] **NAS service account** -- Plan account name (e.g., `tm-wendy-air`; store in 1Password)
- [ ] **NAS share** -- Plan backup share name (e.g., `Backups-TM-Wendy-Air`)
- [ ] **NAS IP & hostname** -- Confirm `wolfden-nas` (192.168.8.129) reachable from Wendy's locations
- [ ] **Local machine name** -- Confirm system hostname will be `wendy-air`
- [ ] **SSH key identity** -- SSH key comment format: `wendy@wendy-air`

**Reference:** See [project-michael-air/PLAN-names-networks-backups.md](../project-michael-air/PLAN-names-networks-backups.md) for completed example.

---

## Migration Issues & Fixes

(To be populated as issues are discovered during setup)

---

## Completed Tasks Summary

(To be populated as tasks are completed)

---

## See Also

- [machine_purchase.md](machine_purchase.md) -- Specs & purchasing guidance
- [CONTEXT.md](../CONTEXT.md) -- Canonical device registry
