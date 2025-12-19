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


## Email from Adam 2025-09-28
```
Howdy Michael,

I've adopted your Access Point (AP) and adjusted the radio channels in the area, which should lead to some improvements. The previous auto-settings were configured in a counterproductive way. Your radio is now meshing with the AP on the roof of the pole barn. Any steps you can take to improve the line of sight between your device and that AP will help strengthen your downlink signal, as it's currently quite weak.

Could you let me know which site you are currently camped at? There's a wired AP located between Site 3 and the lake. For some reason, I wasn't able to mesh your radio to it directly, but if the signal is good, this would be a better option because no other radios use it for their downlink.

Please keep me updated on how things perform with this new arrangement.

Regarding further improvements to the network infrastructure and software configurations, I'm not entirely sure about Jeff's specific skill set in this area. He is capable, but I'm uncertain how motivated he is to undertake the necessary learning and the trial-and-error efforts that will likely be required. It's important to note that the more devices, especially radios, that are added, the more challenging it becomes to manage the network to prevent interference. You can easily achieve a great signal with many radios, but still experience very poor throughput if they are interfering with each other.

Lastly, the Starlink service was removed from the network in the spring, and the ISP switched back to Pasty Net. Here's a screenshot of the most recent automated tests, which run daily at 5 AM.  I've also included a latency report, as this is likely contributing to the problems you've described. This represents about the best performance typically reported. This bandwidth is split among all network activities. Given that, I'm actually surprised you've had much success with video calls at all.

—Adam

Screenshot 2025-09-28 at 4.29.40 PM.png
Screenshot 2025-09-28 at 4.43.06 PM.png
```

![Screenshot 2025-09-28 at 4.43.06 PM](/Users/michael/repos/wolf-soho/Ubiquiti/Screenshot 2025-09-28 at 4.29.40 PM.png)

![Screenshot 2025-09-28 at 4.43.06 PM](/Users/michael/repos/wolf-soho/Ubiquiti/Screenshot 2025-09-28 at 4.43.06 PM.png)



## Email to Adam 2025-09-29
```
Howdy Adam,

I didn't see this message until later in the day after you sent it.  I had spent most of the day on a zoom call that was unusually stable!   Yeah!


> I've adopted your Access Point (AP) and adjusted the radio channels in the area, which should lead to some improvements. The previous auto-settings were configured in a counterproductive way. Your radio is now meshing with the AP on the roof of the pole barn. Any steps you can take to improve the line of sight between your device and that AP will help strengthen your downlink signal, as it's currently quite weak.


> Could you let me know which site you are currently camped at? There's a wired AP located between Site 3 and the lake. For some reason, I wasn't able to mesh your radio to it directly, but if the signal is good, this would be a better option because no other radios use it for their downlink.

We ARE CURRENTLY in Site 1 (for the past 3 weeks).  We can't get any better alignment with the Registration AP!

We WERE in Site 6 (July-Sep this year and all of last year).  We had direct line of sight, right down middle of road to AP at registration.  If we ducked down hill even a little bit, we lost it.  If I walked across the road to Site 7, I could start picking up the barn if I pushed into the woods between site and orchard trail.  At one point, I considered mounting our AP there on a battery, but even though the speed was better, the latency and jitter were not.

We saw marginal improvement moving from Site 6 to Site 1, mostly in signal strength.  From Site 1, we can connect to WiFi directly from macBooks.  In Site 6, we used the mobile router's better antenna then repeated on our own SSID.

Strategy question:  Should we be optomizing the 'Wolf AP' proximity and line of sight to
- Registration AP
- Site 3 AP
- Pole Barn AP

Side note:  Walking around with macBook, I have gotten to within 50 feet of each.  I don't see a differerence that should make a difference.


Site 1
Mon Sep 29 17:13:44 EDT 2025
==== SUMMARY ====
Uplink capacity: 3.728 Mbps
Downlink capacity: 7.529 Mbps
Responsiveness: Low (5.144 seconds | 11 RPM)
Idle Latency: 69.189 milliseconds | 867 RPM

Site 3
Mon Sep 29 17:12:12 EDT 2025
==== SUMMARY ====
Uplink capacity: 3.136 Mbps
Downlink capacity: 23.080 Mbps
Responsiveness: Low (2.531 seconds | 23 RPM)
Idle Latency: 66.848 milliseconds | 897 RPM

Barn
Mon Sep 29 17:16:04 EDT 2025
==== SUMMARY ====
Uplink capacity: 4.207 Mbps
Downlink capacity: 5.752 Mbps
Responsiveness: Low (3.388 seconds | 17 RPM)
Idle Latency: 60.783 milliseconds | 987 RPM



> Please keep me updated on how things perform with this new arrangement.

> Regarding further improvements to the network infrastructure and software configurations, I'm not entirely sure about Jeff's specific skill set in this area. He is capable, but I'm uncertain how motivated he is to undertake the necessary learning and the trial-and-error efforts that will likely be required. 


Yeah.  That was my read..
- this is NEITHER interesting nor important to Jeff
- it is BOTH interesting and important to me

I appreciate it being interesting to you.

The recommendations from AI's are not trivial, but
1. **Signal Strength Optimization** - 30-60 minutes
2. **AP Mesh Configuration** - 45-90 minutes  
3. **Channel Optimization** - 30-45 minutes
4. **QoS Traffic Prioritization** - 60-120 minutes
5. **Network Path Optimization** - 90-180 minutes
**Total: 4-8 hours** for complete optimization

Again, I appreciate your interest, but I am not going to ask you to invest this much.

Do you think that (next year) it would be possible to create "Wolf Enterprises" (like Lake Effect Farm) and set me up with admin access for only that network?  That could be minimal user admin burden on Jeff (or you?) with the network config burden where it's important - me.  It would be something I'd be willing to pay for.


> Lastly, the Starlink service was removed from the network in the spring, and the ISP switched back to Pasty Net. Here's a screenshot of the most recent automated tests, which run daily at 5 AM.  I've also included a latency report, as this is likely contributing to the problems you've described. This represents about the best performance typically reported. This bandwidth is split among all network activities. Given that, I'm actually surprised you've had much success with video calls at all.

That's interesting.  The AI's created a script that analyzes info from https://ifconfig.me to determine uplink info.  I see it flip from Pasty to Starlin in a matter of seconds.  Are you sure it's not dual hosted?  If so, the script is probably showing that Pasty Net is a wrapper and reseller for StarLink.  Pasty does the billing, but Starlink handles the traffic.  And, it's likely that Pasty is multi-headed, with separate traffic on copper, fiber, or satellite.


Uplink: PASTY.NET, INC. — public IP — IP 199.38.31.136

=== 2025-09-29 16:20:45 ===
Uplink: PASTY.NET, INC. — public IP — IP 199.38.31.136

traceroute to 1.1.1.1 (1.1.1.1), 6 hops max, 40 byte packets
 1  192.168.1.1  41.708 ms  10.715 ms  10.844 ms
 2  192.168.9.1  6.266 ms  6.563 ms  5.273 ms
 3  199.38.31.1  22.767 ms  26.278 ms  51.199 ms
 4  74.221.48.45  80.861 ms  51.204 ms  38.769 ms
 5  * 62.115.43.192  70.019 ms  39.447 ms
 6  62.115.63.53  58.522 ms  75.431 ms
    195.12.255.181  48.099 ms


=== 2025-09-29 16:21:14 ===
Uplink: SpaceX Services, Inc. — public IP — IP 2605:59ca:13ad:c910:10f8:d06a:d185:dbf5

traceroute to 1.1.1.1 (1.1.1.1), 6 hops max, 40 byte packets
 1  192.168.1.1  14.712 ms  6.019 ms  4.557 ms
 2  192.168.9.1  6.886 ms  3.818 ms  3.552 ms
 3  199.38.31.1  28.235 ms  29.971 ms  19.617 ms
 4  74.221.48.45  28.042 ms  27.202 ms  23.860 ms
 5  * * 62.115.43.192  113.008 ms
 6  195.12.255.181  111.140 ms  107.623 ms
    62.115.63.53  96.949 ms

> It's important to note that the more devices, especially radios, that are added, the more challenging it becomes to manage the network to prevent interference. You can easily achieve a great signal with many radios, but still experience very poor throughput if they are interfering with each other.

Thanks for knowing (lots) more about this than I do!  I feel that I'm in a cave watching shadows on the wall, while you know what's actually walking about outside!


-- Michael

P.S. If "Wolf Enterprises" is a viable idea, here's a basic plan

## **Adam/Jeff's Load to Create "Wolf Enterprises" Network:**

### **Network Creation (30-60 minutes):**
- **Create new SSID:** "Wolf Enterprises" 
- **Set up VLAN:** Isolated network segment
- **Configure DHCP:** Assign IP range for your network
- **Security settings:** WPA3, password, access controls

### **Access Control Setup (15-30 minutes):**
- **Admin access:** Grant you limited admin rights to "Wolf Enterprises" only
- **Network isolation:** Prevent access to other campground networks
- **Bandwidth limits:** Set reasonable limits for your network segment

### **Your Configuration Access (Ongoing):**
- **QoS settings:** Prioritize Zoom/real-time traffic
- **Traffic shaping:** Manage bandwidth allocation
- **Device management:** Control your AP and connected devices
- **Monitoring:** View performance metrics for your network

### **Total Initial Setup: 45-90 minutes**
### **Ongoing Management: Minimal** (you handle your own config)

## **Benefits for Adam/Jeff:**
- **Reduced support load:** You manage your own network issues
- **Isolated troubleshooting:** Problems don't affect other users
- **Clear boundaries:** You can't break the main campground network

## **Benefits for You:**
- **Full control:** Configure QoS, traffic shaping, device management
- **Real-time optimization:** Adjust settings during Zoom calls
- **Network monitoring:** See actual performance metrics
- **Learning opportunity:** Understand network optimization firsthand

**This is actually a great solution** - gives you the control you need while keeping Adam/Jeff's overall network stable and manageable.

```

![Screenshot 2025-09-28 at 4.43.06 PM](/Users/michael/repos/wolf-soho/Ubiquiti/Screenshot 2025-09-28 at 4.29.40 PM.png)

![Screenshot 2025-09-28 at 4.43.06 PM](/Users/michael/repos/wolf-soho/Ubiquiti/Screenshot 2025-09-28 at 4.43.06 PM.png)



