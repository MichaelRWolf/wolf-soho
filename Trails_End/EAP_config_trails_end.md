# Network Profile & Optimization Guide: Trails End Campsite

**Device:** TP-Link Omada EAP225-Outdoor
**Deployment Context:** 300-ft clear line-of-sight backhaul to Campground AP; 30-ft local campsite radius.

---

## 1. Hardware Specifications

* **Wireless Standards:** IEEE 802.11ac/n/g/b/a (Dual-Band Concurrent)
* **Maximum Theoretical Speeds:** 2.4 GHz up to 450 Mbps; 5 GHz up to 867 Mbps
* **Antennas:** 2 External Detachable Omni (2.4 GHz: 3 dBi; 5 GHz: 4 dBi)
* **Interface:** 1 Gigabit Ethernet Port (Supports 802.3af PoE and Passive PoE)
* **Weatherproofing:** IP65 durability rating against dust and moisture ingress

---

## 2. Tunable Parameters & Optimization

### Backhaul Link (Long-Range 300-ft Segment)

* **Uplink Frequency: 2.4 GHz Only**
  * *Reason:* Long physical waveforms handle the 300-ft outdoor atmospheric attenuation reliably. Avoids the high drop rates 5 GHz suffers at this range.
* **2.4 GHz Tx Power: High (Custom: 22–24 dBm)**
  * *Reason:* Ensures the hardware has enough output energy to push a clean return packet all the way back to the distant campground antenna.
* **2.4 GHz Channel Width: 20 MHz**
  * *Reason:* Compresses the signal into a narrow, durable lane. Maximizes range and shields the connection from the noisy cluster of campers located near the main AP.

### Local Access Segment (Short-Range 30-ft Campsite)

* **Local Broadcast Frequency: 5 GHz (Dual-Band Optional)**
  * *Reason:* Provides high-speed, interference-free lanes for work devices sitting within 30 feet of the RV. Completely separates local data from the congested 2.4 GHz space down the road.
* **5 GHz Tx Power: Low (Custom: 10–12 dBm)**
  * *Reason:* Generates a tightly confined, quiet wireless bubble for your immediate campsite. Prevents the radio from yelling unnecessarily into the campground and creating local packet feedback.
* **Extended Network SSID: Distinct Name (e.g., `trails_end_local`)**
  * *Reason:* Prevents your work laptops from experience "flip-flop" alerts or trying to roam over to the distant, degraded campground network.

### System Maintenance Automation

* **Automated Reboot Schedule: Daily at 3:00 AM**
  * *Reason:* Erases system cache, flushes unneeded logs, and automatically resets the wireless handshake while you sleep. Eliminates manual maintenance or device intervention during work hours.
