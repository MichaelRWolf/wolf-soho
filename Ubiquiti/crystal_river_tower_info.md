# Crystal River Tower Info

## Going on a signal hunt

### 1. Your place: Rascally Raccoon Refuge

* **USPS address**
  **8459 W Oak St, Crystal River, FL 34428** ([Cause IQ][1])
* **Approximate coordinates**

  * **Lat:** ~28.9235° N ([ae.maptons.com][2])
  * **Lon:** ~82.59° W (Crystal River west side; approximate from mapping sites)

---

### 2. Likely AT&T tower(s) within ~5 miles

From public tower databases, the only clearly AT&T-flagged macro site within a few miles of you is this one:

#### Downtown Crystal River AT&T site

* **License / callsign:** KNKN738 (AT&T Mobility Services LLC)
* **USPS address (structure):**
  **142 Northeast 11th Street, Crystal River, FL 34428** ([FindTower][3])
* **Coordinates from FCC-style data (your screenshot):**

  * Lat: **28.9047° N**
  * Lon: **82.5917° W**
* **Other database entries** list several AT&T sectors at almost the same spot, around

  * ~**28.8985° N, 82.5967° W** (FindTower “AT&T-Network” records) ([FindTower][3])
    These are effectively the same **tower cluster** for our purposes.

#### Distance & direction from the Refuge

Using the refuge at ~28.9235 N, 82.59 W as the reference:

* **FCC tower point (28.9047, -82.5917)**

  * Roughly **1.3 miles** away
  * Bearing ≈ **185°** (almost due **south**, just a hair west)
* **Cluster point (28.8985, -82.5967)**

  * Roughly **1.8 miles** away
  * Bearing ≈ **193°** (**south-south-west**)

So: from your driveway, the “fat rabbit” AT&T tower is basically **down toward town, a bit to the right of due south**, around the NE 11th St / US-19 area.

---

### 3. What your Nighthawk is reporting

From the diagnostics screen you shared:

* **Network:** AT&T (MCC 310, MNC 410)
* **Radio:** **LTE Band 66 (B66)**
* **Cell ID:** **179944649**
* **Signal metrics:**

  * RSRP: **-114 dBm** (weak-ish but usable)
  * RSRQ: **-12 dB**
  * SINR (RS-SINR): **5 dB**

Those numbers line up with being on a **moderate / marginal LTE link** to that downtown tower cluster, not something much farther away.

---

### 4. How to use this for your “hunt”

* When you walk around with the Nighthawk, orient roughly **south to SSW** from the refuge to get “in line” with that tower cluster.
* As you move, watch **RSRP** and **SINR** on the diagnostics page: higher (less negative) RSRP and higher SINR mean you’re getting closer to a clean line-of-sight path to the tower.
* Once you find a sweet spot (maybe at the edge of the clearing or near the driveway), you can decide if it’s close enough to run power out there, or if you want a longer extension cord / different mounting point.

If you’d like, next step I can help you turn this into a tiny one-page “tower map” note you can print and tape near the router so Future-Michael remembers where the invisible big stick in the sky actually is. 📡🦝

[1]: https://www.causeiq.com/organizations/rascally-raccoon-refuge%2C923486676/?utm_source=chatgpt.com "The Rascally Raccoon | Crystal River, FL"
[2]: https://ae.maptons.com/p/14895988280?utm_source=chatgpt.com "The Rascally Raccoon Refuge Inc., 8459 W Oak St, خريطة الموقع"
[3]: https://findtowerapp.com/coverage/Florida/Crystal-River/ATT?utm_source=chatgpt.com "Crystal River AT&T Cell Towers, Florida - FindTower App"
