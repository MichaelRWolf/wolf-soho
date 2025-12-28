# Beryl_is_fucked_do_factory_reset_2025-12-27

## Context

GL.iNet Beryl router exhibited periodic (~45s) Wi‑Fi outages despite appearing operational.
User goal: restore *appliance‑like*, out‑of‑box behavior with minimum cognitive load.

This document records observations, tests, conclusions, and the chosen recovery plan.

---

## Symptoms Observed

- Wi‑Fi SSID visible and connectable, but unstable
- Connectivity drops every ~45 seconds
- During drop:
  - NSS collapses to 1
  - TX drops to 0
  - Ping interrupted
- Cycle repeats predictably

---

## Key Log Evidence

Repeated kernel/firmware logs:

```text
ExtEventBeaconLostHandler::FW LOG, Beacon lost (...)
Beacon lost - AP disabled!!!
[DfsCacNormalStart] Normal start. Enable MAC TX
```

Observations:

- “Beacon lost” always precedes DFS CAC restart
- Happens on non‑DFS channels (36, 44)
- Bandwidth reduction (80 → 40 MHz) did not help
- Channel 149 refused to associate

---

## Critical Low‑Level Findings

### mac80211 / PHY State

Commands and results:

- `/sys/class/ieee80211` → **exists but empty**
- `iw phy` → **no output**
- `iw dev` → **no output**
- `ip link | grep wlan` → **no interfaces**

Conclusion:
> Linux kernel has **no registered Wi‑Fi PHY**, even while Wi‑Fi intermittently works.

### Kernel Modules

Loaded:

- cfg80211
- mac80211
- compat

Not observed:

- A visible PHY or interface bound to mac80211

Interpretation:

- Wi‑Fi radio is being managed by **vendor firmware / offload stack**
- Linux tools (`iw`, sysfs) cannot see or control the radio
- Firmware is stuck in a self‑recovery loop

---

## Regulatory Domain

- `iw reg get` shows: `country 00: DFS-UNSET`
- Attempts to set `US` did not persist
- DFS behavior observed even on non‑DFS channels

This is a **symptom**, not the root cause.

---

## Network Mode Confirmation

- GL.iNet UI shows **Internet = Cable**
- WAN via Ethernet (not Repeater / WISP)
- Therefore:
  - “Beacon lost” refers to **local AP radio**
  - Not loss of upstream Wi‑Fi

---

## Root Cause (Best Fit)
>
> Vendor Wi‑Fi firmware entered a crash/recovery loop and never cleanly re‑attached to the kernel.

Effects:

- AP disables itself
- DFS/MAC TX restart logged
- Clients drop
- Firmware retries on watchdog timer (~45s)

This can happen due to:

- firmware crash
- power or RF glitch
- old firmware/kernel mismatch
- incomplete recovery after an internal reset

User did **not** intentionally modify firmware.

---

## Why Reset Is Justified

- Problem is **below configuration level**
- Tuning channels, bandwidth, DFS, region ineffective
- Runtime state is unrecoverable in place
- Factory reset reloads:
  - Wi‑Fi firmware blobs
  - driver/firmware handshake
  - clean hardware state

Reset is **not** giving up; it is restoring the appliance contract.

---

## Factory Reset Semantics (Important)

- GL.iNet devices have **one true factory reset**
- Holding RESET ~10–15 seconds during power‑on:
  - wipes configuration
  - restores vendor firmware defaults
- No “tiers” of reset (15s vs 45s is folklore)
- No data‑dependent magic timing

This yields:
> “Opened the box, powered on for the first time” state

---

## OpenWrt Version Note

- Device reports OpenWrt 19.07.8
- GL.iNet firmware *is* OpenWrt, but customized
- Old version increases likelihood of Wi‑Fi instability

**Recommendation:**

- First: factory reset
- If instability persists:
  - flash latest official GL.iNet firmware for exact model
- Do *not* attempt upstream OpenWrt unless deliberately opting into that maintenance model

---

## Data Preserved Before Reset

Only items worth saving:

- Wi‑Fi SSIDs
- Wi‑Fi PSKs
- (Optional) LAN IP if changed

One‑liner used:

```bash
ssh root@192.168.8.1 'echo "### SSIDs"; uci show wireless | grep "\.ssid="; echo; echo "### WiFi Keys"; uci show wireless | grep "\.key="'
```

---

## Reset Plan (Minimal Risk)

1. Save SSID + PSK
2. Ensure Ethernet access to one machine remains
3. Hardware factory reset (RESET pin 10–15s)
4. Initial UI setup only (SSID + password)
5. No advanced tuning
6. Verify stability
7. If still unstable → flash latest GL.iNet firmware
8. If still unstable → treat as hardware fault and replace

---

## Key Takeaways for Future You

- Intermittent Wi‑Fi + empty `/sys/class/ieee80211` = firmware‑managed radio
- DFS logs on non‑DFS channels often indicate radio reset, not radar
- Periodic timing → watchdog, not RF noise
- Reset is a *tool*, not a failure

---

## Status

Proceeding with **scorched‑earth factory reset** to restore appliance behavior.

---

## Factory Defaults (After Reset)

- **Default SSID:** Printed on the sticker on the bottom of the Beryl  
  (typically `GL-MT1300-XXX` or similar)
- **Default Wi-Fi Password:** Printed on the same sticker
- **Admin UI:** <http://192.168.8.1>
- **Admin Password:** none (you will be prompted to set one on first login)

There is no universal default SSID/password baked into firmware.  
They are **per-device**, generated at the factory, and physically labeled.

---

## Static LAN / DHCP Reservations

If you assigned a **static IP to the NAS via the router (DHCP reservation)**,
that lives in the DHCP config and should be captured before reset.

---

## One‑Liner: Full Pre‑Reset Cheat Sheet

Run this *from another machine via SSH*:

```sh
ssh root@192.168.8.1 '
echo "### LAN IP";
uci get network.lan.ipaddr 2>/dev/null;

echo;
echo "### SSIDs";
uci show wireless | grep "\.ssid=";

echo;
echo "### WiFi Keys";
uci show wireless | grep "\.key=";

echo;
echo "### DHCP Static Leases";
uci show dhcp | grep -E "host\[|\.ip=|\.mac=|\.name=";
'
```

What this captures:

- LAN IP of the router (e.g. `192.168.8.1`)
- All configured SSIDs
- All Wi‑Fi PSKs
- All DHCP reservations (static IPs for NAS, etc.)

Save the output somewhere safe. Re‑enter only what you need after reset.

---

## Definitions (Plain English)

- **LAN IP:**  
  The router’s own address on your internal network  
  (default: `192.168.8.1`)

- **Static IP (via DHCP reservation):**  
  Router promises a specific device (NAS) always gets the same IP

- **Factory Reset Impact:**  
  - DHCP reservations are erased
  - LAN IP resets to default
  - Wi‑Fi SSID/password reset to sticker values

---

## Post‑Reset Reminder

After reset:

1. Re‑enter SSID + password (or keep defaults)
2. Re‑add NAS DHCP reservation (if desired)
3. Do **nothing else** unless something is broken
