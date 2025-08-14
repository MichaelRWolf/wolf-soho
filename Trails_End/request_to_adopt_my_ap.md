# Campground Network Request – Scripts & Tech Appendix

Below are two short, owner-friendly request scripts you can send, plus a technical appendix with the exact settings. Each request is framed as a one‑time setup with ongoing benefits and minimal maintenance.

---

## Script A — “Adopt My AP Into Your Mesh”

**Subject:** Simple way to extend Wi‑Fi coverage and make my work connection stable

Hi Adam,

Quick idea that can help both of us. I can contribute one of my access points to your Wi‑Fi so it becomes part of your mesh and extends coverage on our end of the property. You would manage it just like your other APs — same controller, firmware, and settings — and there’s no extra work day‑to‑day.

For me, it means a more stable work connection that doesn’t have to hop through client Wi‑Fi. For you and other guests, it should improve coverage and reduce retries in this area. I’ll supply the AP and mount/power it where you prefer. All I’d need is for you to “adopt” it in your controller. It’s a one‑time, 5‑minute step.

If that sounds good, I can drop it by at your convenience.

Thanks!

— Michael

---

## Script B — “Private SSID With Priority”

**Subject:** Small Wi‑Fi tweak for stable calls (low maintenance)

Hi Adam,

Would you be open to adding a private/staff SSID for one laptop (mine) with a little priority? It’s a one‑time change in your Wi‑Fi controller: create a hidden SSID that rides your existing network, and add my device MAC. I’d keep it to low bandwidth — just stable video calls and development work.

This won’t affect public Wi‑Fi settings, and it can actually reduce congestion on the main SSIDs. If you’re up for it, I can send my device MAC and any details you need. I’m aiming for “set it and forget it” on your side.

Appreciate it!

— Michael

---

Technical Appendix (Concise)

> Use whichever section matches the request you choose. Values are suggested defaults; keep everything simple and low‑touch.

## A. Adopt My AP Into Your Mesh

| Item              | Where (Controller/UI)    | Suggested Value                 | Reason                                     | Benefit to Everyone                   | Benefit to Me                         | Maintenance                |
| ----------------- | ------------------------ | ------------------------------- | ------------------------------------------ | ------------------------------------- | ------------------------------------- | -------------------------- |
| Adopt external AP | Devices → Adopt          | Approve + default group         | Adds coverage using your standard policies | Better coverage & capacity in my area | Stable backhaul (no client‑Wi‑Fi hop) | None (managed with others) |
| AP name           | Devices → Details        | `AP-Site2-GuestExt`             | Clear location labeling                    | Easier ops                            | —                                     | None                       |
| Uplink/backhaul   | Devices → Radios/Uplinks | Prefer wired (if PoE) else mesh | Mesh or wired backhaul avoids client mode  | Stronger signal for nearby guests     | Fewer retransmits/jitter              | None                       |
| Power level       | RF/Radio                 | Medium                          | Avoids overlaps/hidden nodes               | Cleaner RF, fewer retries             | Balanced SNR                          | Rare                       |
| Band steering     | WLAN/SSID                | Off (or gentle)                 | Prevent flapping between 2.4/5 GHz         | Fewer drops for guests                | Client stability                      | None                       |
| Minimum RSSI      | WLAN/SSID                | Disable or conservative         | Prevents disconnections on edge            | Less churn                            | Avoids drops                          | Rare                       |
| Firmware track    | System/Settings          | Stable/LTS                      | Avoid regressions                          | Fewer surprises                       | Predictable behavior                  | Normal                     |

**Optional (if you can offer PoE):** Provide a PoE injector and single CAT5e run to AP; controller does the rest.

## B. Private SSID With Priority

| Item                 | Where (Controller/UI) | Suggested Value              | Reason                               | Benefit to Everyone      | Benefit to Me           | Maintenance |
| -------------------- | --------------------- | ---------------------------- | ------------------------------------ | ------------------------ | ----------------------- | ----------- |
| New SSID             | WLAN/SSID             | `Staff-Work` (hidden)        | Keeps public SSIDs unchanged         | Reduces public SSID load | Clean, predictable join | None        |
| VLAN (optional)      | Network/VLANs         | Reuse default or VLAN `30`   | Separation if desired                | Clear traffic boundaries | Easier QoS              | Low         |
| QoS/Smart Queue      | Traffic Mgmt          | Enable; cap to 85–90% uplink | Kills bufferbloat                    | Smoother for all calls   | Lower jitter            | One‑time    |
| Device MAC allowlist | WLAN/Access Control   | Add my laptop MAC            | Keeps SSID private/limited           | No freeloading           | Guaranteed access       | Low         |
| DFS channels         | RF/Radio              | Use stable 5 GHz non‑DFS     | Avoids radar-induced channel changes | Fewer mass disconnects   | Sticky connection       | None        |
| 2.4/5 split          | SSID/Advanced         | Separate SSIDs or band‑lock  | Prevents steer‑flap                  | Clients stay put         | Fewer drops             | None        |
| DHCP lease time      | Network               | 12–24h                       | Fewer reauths/renews                 | More stable sessions     | Fewer surprises         | None        |

## C. ISP/Uplink Consistency (If They Control It)

| Item             | Where (Gateway/Multi‑WAN) | Suggested Value                                     | Reason                         | Benefit to Everyone    | Benefit to Me         | Maintenance |
| ---------------- | ------------------------- | --------------------------------------------------- | ------------------------------ | ---------------------- | --------------------- | ----------- |
| Preferred uplink | Multi‑WAN                 | Pin to best path (PastyNet *or* Starlink), not auto | Avoid path‑flip IP changes     | Fewer global stalls    | Fewer `ECONNRESET`s   | Low         |
| Smart Queue Mgmt | QoS/Traffic Shaping       | Enable CAKE/FQ‑CoDel; set to 85–90% of measured     | Prevents queue bloat           | Low latency under load | Steady calls          | One‑time    |
| DNS resiliency   | DNS                       | At least 2 providers (e.g., 1.1.1.1 & 9.9.9.9)      | Avoids single point of failure | Faster lookups         | Fewer “can’t resolve” | None        |

---

## One‑Pager Summary (copy/paste)

* **Option A:** Adopt my AP into your controller. *One-time step, extends your coverage; I supply hardware and PoE.*
* **Option B:** Add a hidden “work” SSID limited to my laptop, optionally with basic QoS. *One-time policy, lowers load on public SSIDs.*
* **Bonus (if easy):** Pin the uplink to the most stable ISP path and enable smart queue on the gateway. *Everyone’s Zooms get better.*

> I’m happy to provide the AP and a PoE injector, label everything, and keep it tidy so it’s truly “set it and forget it.”
