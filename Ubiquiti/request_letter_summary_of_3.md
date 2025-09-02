# Letter to Adam

Hi Adam,

I hope this finds you well as "official summer" blends into late summer, back-to-school, and return-of-Béla.

First, thank you for all the "infrastructure" work you did at Trails
End and Lake Effect. We're back for a 4th summer in large part to that
work. I like how water pipes and the data pipes were both "farm
systems" to you.

As technomads, we especially appreciate the WiFi. It far exceeds what
we could expect -- meeting clients around the country (and world) from
a camp site that's off the power grid but on the internet!

But zoom has infrequent, but obtrusive, drops.  Working from home doesn't work when the network drops.

I've done a lot of monitoring, debugging, configuring, and research.
ChatGPT and Claude have been invaluable but I'm at the limits of what
I can accomplish alone.

Here's what my AI collegues recommended.

- **DONE**
  1. Reposition mobile router while monitoring signal strength, noise, and failures.  Given that it was designed for airports and hotels, it's doing a yoeman's job and unlikely to improve.

- **Attempted/Failed**
  1. Ubiquiti device in stand-alone mode.  I purchased the same device that's on Katya's RV.  I could not get it working in stand-alone mode.

- **Suggested**
  1. Adopt my Ubiquiti device into existing mesh.  I suspect this is Katya's setup. It uses the device's default mode: mesh.  It would be powered by our house battery, and accessible by anyone in range.  It's likely a 5-minute adoption step, then would be managed in the pool of exising AP's with no extra work.
  2. Join another network - The public SSID likely optomizes speed, but we need predictabiltiy/stability more than speed.  When zoom is flakey, the available bandwidth is 10x-20x what's required.  It's the dropped connections that are likely the problem.

Could you direct or advise me how to continue?

Thanks,
Michael

P.S. Technical Appendix (courtesy of ChatGPT)

I'd be happy to have ChatGPT generate a step-by-step guide -- it's really good at that.  Here are the parameters it thinks are necessary.

**Adopting Ubiquiti:**
- Device: Ubiquiti UAP-AC-M-US (same model Katya uses)
- MAC Address: D8:B3:70:CC:AA:7C
- Current status: Factory reset, ready for adoption
- I an provide PoE injector and mounting hardware
- Prefer integration over standalone operation
- Willing to follow your network policies and naming conventions
- Can document setup for future reference

**Alternative Approaches:** (if adoption isn't feasible):
- Private SSID with device MAC allowlist
- QoS prioritization for work traffic
- Band steering optimization
- Channel selection guidance
