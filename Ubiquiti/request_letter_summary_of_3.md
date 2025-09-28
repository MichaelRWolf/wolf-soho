# ???

## Email to Adam - 2025-09-02

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

## Email from Adam 2025-09-24

``` markdown

Howdy Micheal, 

Good to hear from you. Sorry I'm just getting back to you, things have been quite busy here, and I've fallen behind in emails. 

First off; disclosures. 😉 I'm no longer running the network up there. I handed that off to Jeff in the spring at Aarons request. 

That being said, I do still have full admin access, and could probably help you get your uap mesh adopted. In fact, most likely if you give it a factory reset, and power it up, It will show up in my dashboard for adoption. Shoot me a text when it's fired up.

Also, I appreciate the offer of systems checking the bus. I think Béla left it in good order, but I certainly wouldn't complain if you dropped by and had a look. I think the keys are in the door. 

--Adam

```

## Email to Adam - Adopting Ubiquiti and addressing jitter - 2025-09-28

Howdy Adam,

Good to hear from you! No worries about timing—I know harvest season is crazy.

My UAP is ready for adoption [Note 1]. I'll keep it powered up while our solar panels can support it.

When I offered to help with the solar panel re-installation, Aaron mentioned you might be on site too. I'd love to work together and catch up on what you've been up to. (And you're welcome to join us for dinner while you're here.)

My network monitoring has revealed something interesting [Note 2]: plenty of bandwidth, but Zoom still drops due to connection instability. Let's start with adopting the UAP and see how that goes.

I'm curious about your take on whether the network configuring we started a couple years ago might still be possible.  This both a computer network topology question, and also wondering if Jeff is up to it. What's your read?

I'll check the bus on my next walk to the compost windrow. (Can you imagine a more beautiful walk for a kitchen chore?)

Thanks,
Michael

---

**Technical Notes:**
My AI assistants are great at technical analysis and also technical writing...

**Note 1 - Device Status:** UAP-AC-M-US (MAC: D8:B3:70:CC:AA:7C), factory reset complete (60- and 30-second versions), powered up at site 1, ready for adoption.

**Note 2 - Network Analysis:** Bandwidth adequate (10-20× Zoom requirements), dual hosting Pasty/Starlink. Issue: connection instability/jitter causing drops for Zoom (and other streaming tools).  There is sufficient speed. Client-side fixes insufficient for real-time application stability.

**Potential Solutions:**
- **Network-side (inside the barn):** QoS prioritization, handoff optimization, channel selection
- **Client-side (inside the RV):** TCP keepalive tuning, DNS optimization (1.1.1.1), macOS network stack adjustments

**Benefit Analysis:** Network improvements provide broader gains for all users; client-side tweaks offer targeted improvements for specific setups.

