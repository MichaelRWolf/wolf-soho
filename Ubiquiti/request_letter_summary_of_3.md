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

Good to hear from you too, and no worries about the timing—I know it's harvest season.

My UAP is ready for adoption [See Note 1].  I'll keep it powered-up during daylight hours.   Unfortunately, subsequent monitoring and research leads me to believe this may not improve things [See Note 2].

When I offered to help out with solar panel re-installation, Aaron said you may be on site to assist, too. I'd enjoy that, and to learn what you've been up to. (Aside, while you're here, feel welcome to join us for dinner.)

I will do a quick check at the bus.

I am now unsure if adopting the Ubiquiti device will be sufficient. Subsequent learning and monitoring has had me realize that signal strength and download/upload speed is sufficient for normal email and browsing, but the problem with Zoom (and other HTTPS/streaming tools) is the connection stability and network jitter. The bandwidth is more than adequate—it's the intermittent connection drops and latency spikes that disrupt video calls. We're probably OK for this year, but it would be good to know if you think this is addressable for next year.

Thanks,
Michael

---

Notes

1 - I have powered up my Ubiquiti UAP-AC-M-US device. I attempted a 60-second factory reset that seemed to hang, then a 30-second reset that seemed to complete. Since we are now in site 1, it should be easy to adopt. The device model is UAP-AC-M-US with MAC address D8:B3:70:CC:AA:7C, and it's factory reset and ready for adoption.

2 - My AI assistants summarized the problem thusly:

The network analysis shows adequate bandwidth (10-20× Zoom requirements) with dual hosting between Pasty and Starlink, but Zoom and Cursor crash due to connection instability and network jitter rather than insufficient speed. The intermittent latency spikes and connection drops disrupt real-time applications that require consistent, low-latency connections, making it difficult to prevent these crashes through client-side configuration alone.

Hosting tweaks (Pasty/Starlink optimization) or Ubiquiti mesh parameters could improve user experience by reducing handoff delays, implementing QoS prioritization for real-time traffic, and optimizing channel selection to minimize interference—all without consuming additional bandwidth. Michael could implement TCP keepalive adjustments, DNS optimization to 1.1.1.1, and macOS network stack tuning to improve connection resilience.

The benefits are asymmetric: network-side improvements (hosting optimization, mesh configuration) provide broader, more reliable gains affecting all users, while client-side tweaks (MacBook networking, equipment positioning) offer targeted improvements primarily benefiting Michael's specific setup and usage patterns.

