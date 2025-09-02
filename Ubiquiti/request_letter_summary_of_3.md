# Letter to Adam

Hi Adam,

I hope this finds you well as summer shifts into late summer, back-to-school season, and Béla’s return.

First, thank you for all the infrastructure work you did at Trails End and Lake Effect. We're back for a fourth summer largely because of those efforts. I love how both the water pipes and data pipes became “farm systems” in your hands.

As technomads, we especially appreciate the WiFi. It far exceeds expectations—allowing us to meet with clients across the country (and world) from an off‑grid campsite that’s still on the internet!

That said, Zoom calls sometimes drop. Infrequent as they are, they’re disruptive. Remote work depends on a stable connection.

I’ve done quite a bit of monitoring, debugging, configuring, and research. ChatGPT and Claude have been invaluable, but I’ve reached the limit of what I can solve alone.

Here’s what I’ve tried so far:

**Done:**

1. Repositioned my mobile router while tracking signal strength, noise, and errors. For a device designed for airports and hotels, it’s doing a yeoman’s job, but there’s little room for improvement.

**Attempted (but unsuccessful):**

1. Tried running a Ubiquiti device in stand‑alone mode. I bought the same model Katya uses, hoping it could connect to *Trails End WiFi* instead of my mobile router. I couldn’t get it working.

**Possible next steps:**

1. **Adopt my Ubiquiti device into the existing mesh.** I believe this is how Katya’s setup works. The device is factory‑reset and ready. Once adopted, it would be powered by our house battery, available to anyone nearby, and managed alongside existing APs. Likely just a quick setup.
2. **Join a different network.** The public SSID may optimize for speed, but what I need is predictability and stability. Even when Zoom is flaky, available bandwidth is 10–20× what’s required—it’s the dropped connections that matter.

Could you point me in the right direction?

Thanks,
Michael

---

**Technical Appendix (courtesy of ChatGPT):**

*Adopting Ubiquiti Device:*

* Model: Ubiquiti UAP‑AC‑M‑US (same as Katya’s)
* MAC Address: D8\:B3:70\:CC\:AA:7C
* Status: Factory reset, ready for adoption
* Power: PoE injector and mounting hardware available
* Preference: Integration into existing mesh (not standalone)
* Compliance: Happy to follow network policies and naming conventions
* Documentation: Will provide setup notes for future reference

*Alternative approaches (if adoption isn’t feasible):*

* Private SSID with device MAC allow‑list
* QoS prioritization for work traffic
* Band steering adjustments
* Channel selection guidance
