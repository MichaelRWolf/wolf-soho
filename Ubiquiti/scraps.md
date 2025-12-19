# Ubiquiti Network Notes

Wow.  Thanks.

We CURRENTLY ARE in Site 1 (for the past 3 weeks).  We can't get any better alignment with the AP at registration.

We WERE in Site 6 (July-Sep this year and all of last year).  We had direct line of sight, right down middle of road to AP at registration.  If we ducked down hill even a little bit, we lost it.  If I walked across the road to Site 7, I could start picking up the barn if I pushed into the woods between site and orchard trail.  At one point, I considered mounting our AP there on a battery, but even though the speed was better, the latency and jitter were not.

We saw marginal improvement moving from Site 6 to Site 1, mostly in signal strength.  We can grab SSID directly instead of using our powered repeater.

Let's bump up out of config level to strategy level.  What geometry would you suggest trying to optimize distance/sight-line to

- Front Registration AP
- Site 3 AP
- Pole Barn AP

It's a loaded question... walking around with my macBook, I don't see much difference.

So... download/upload is fine all around, but it's the latency that's different from

michael@michael-pro: ~/repos/wolf-soho
[0] $ echo Site 1; date; networkQuality; echo
Site 1
Mon Sep 29 17:13:44 EDT 2025
==== SUMMARY ====
Uplink capacity: 3.728 Mbps
Downlink capacity: 7.529 Mbps
Responsiveness: Low (5.144 seconds | 11 RPM)
Idle Latency: 69.189 milliseconds | 867 RPM

michael@michael-pro: ~/repos/wolf-soho
[0] $ echo Barn; date; networkQuality; echo
Barn
Mon Sep 29 17:16:04 EDT 2025
==== SUMMARY ====
Uplink capacity: 4.207 Mbps
Downlink capacity: 5.752 Mbps
Responsiveness: Low (3.388 seconds | 17 RPM)
Idle Latency: 60.783 milliseconds | 987 RPM

michael@michael-pro: ~/repos/wolf-soho
[0] $ uplink-describe
Uplink: SpaceX Services, Inc. — public IP — IP 2605:59ca:13ad:c910:7420:bdf4:439a:ca86

[ Deleted -- a lot of today's technical command line output.  I'll forego the technical analysis for a while and just observe the end user experience. ]

I tried briefly with my macBook to walk around, loosing line of sight to front and gaining line of sight to barn.  I didn't notice a difference.  15 Mbps download, 5 Mbps upload.  All fine.   Better than fine - Zoom wants 2-4 Mbps for HD.  We don't need HD, so around 1 Mbps is typically fine.  Zoom’s support docs recommend latency ≤ 150 ms and jitter ≤ 40 ms for good quality, but I've seen 300 be OK, so maybe here's the issue...

- Your graph shows latency in the neighborhood of 25-50 ms.
- I am typically seeing 500 - 2,000 ms latency.

I will sit on this for a few days.  No need to dig into the technical guts if the end experience is OK.  Which it was today.

I'll let you know how it goes.

Regarding Jeff -- Yup.  That was my read.... that he's very interested in woodwork.  Thanks for being a first-line goto.  It helps diagnose the issue.  I've had AI's suggest how to set QoS (Quality of Service) and related parameters from the admin console (right down to step-by-step keystrokes).  

We are have been in Site 1 for about 3 weeks.  

Earlier this year and all of last year, we were in Site 6 with mobile router in direct line of site down the center of the road to AP at registration.

From Site 6, we had flakey (but tolerable) connection for most of this summer and all of last summer.  We were parked at edge of road and got direct line of sight to the one at registration board.
3 weeks ago, we move to Site 1.  We can't get much closer to antenna up front.

Regarding barn...

- When we sit outside the barn,

Quick subjective gut check....

- My 10:00-1:00 zoom call went better than average.
- speedtest

I have a hand-crafted tool to describe the uplink...

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

... that just a few seconds later flipped from Pasty to SpaceX

=== 2025-09-29 16:21:14 ===
Uplink: SpaceX Services, Inc. — public IP — IP 2605:59ca:13ad:c910:10f8:d06a:d185:dbf5

traceroute to 1.1.1.1 (1.1.1.1), 6 hops max, 40 byte packets
 1  192.168.1.1  14.712 ms  6.019 ms  4.557 ms
 2  192.168.9.1  6.886 ms  3.818 ms  3.552 ms
 3  199.38.31.1  28.235 ms  29.971 ms  19.617 ms
 4  74.221.48.45  28.042 ms  27.202 ms  23.860 ms
 5  ** 62.115.43.192  113.008 ms
 6  195.12.255.181  111.140 ms  107.623 ms
    62.115.63.53  96.949 ms

I don't know how to interpret the traceroute output.  AI's helped me in the past...

On Sep 28, 2025, at 5:43 PM, Adam Millsap <adam@urbanrootsfarm.com> wrote:

Howdy Michael,

I've adopted your Access Point (AP) and adjusted the radio channels in the area, which should lead to some improvements. The previous auto-settings were configured in a counterproductive way. Your radio is now meshing with the AP on the roof of the pole barn. Any steps you can take to improve the line of sight between your device and that AP will help strengthen your downlink signal, as it's currently quite weak.

Could you let me know which site you are currently camped at? There's a wired AP located between Site 3 and the lake. For some reason, I wasn't able to mesh your radio to it directly, but if the signal is good, this would be a better option because no other radios use it for their downlink.

Please keep me updated on how things perform with this new arrangement.

Regarding further improvements to the network infrastructure and software configurations, I'm not entirely sure about Jeff's specific skill set in this area. He is capable, but I'm uncertain how motivated he is to undertake the necessary learning and the trial-and-error efforts that will likely be required. It's important to note that the more devices, especially radios, that are added, the more challenging it becomes to manage the network to prevent interference. You can easily achieve a great signal with many radios, but still experience very poor throughput if they are interfering with each other.

Lastly, the Starlink service was removed from the network in the spring, and the ISP switched back to Pasty Net. Here's a screenshot of the most recent automated tests, which run daily at 5 AM.  I've also included a latency report, as this is likely contributing to the problems you've described. This represents about the best performance typically reported. This bandwidth is split among all network activities. Given that, I'm actually surprised you've had much success with video calls at all.

Interesting.  After passing many traceroute(1) outputs to AI's, they inferred that the barn was "dual hosted" and created an `uplink-describe` script that has confirmed this.  I've seen it flip for 30 seconds or 20 minutes.  Is the script's logic in error as it digs though output, or might there be new dual hosting?

michael@michael-pro: ~/repos/wolf-soho
[0] $ uplink-describe
Uplink: SpaceX Services, Inc. — public IP — IP 2605:59ca:13ad:c910:7420:bdf4:439a:ca86

Here are outputs from about an hour ago.  The first infers

michael@michael-pro: ~/repos/wolf-soho
[0] $ uplink-describe -v
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
michael@michael-pro: ~/repos/wolf-soho
[0] $ uplink-describe -v
=== 2025-09-29 16:21:14 ===
Uplink: SpaceX Services, Inc. — public IP — IP 2605:59ca:13ad:c910:10f8:d06a:d185:dbf5

traceroute to 1.1.1.1 (1.1.1.1), 6 hops max, 40 byte packets
 1  192.168.1.1  14.712 ms  6.019 ms  4.557 ms
 2  192.168.9.1  6.886 ms  3.818 ms  3.552 ms
 3  199.38.31.1  28.235 ms  29.971 ms  19.617 ms
 4  74.221.48.45  28.042 ms  27.202 ms  23.860 ms
 5  ** 62.115.43.192  113.008 ms
 6  195.12.255.181  111.140 ms  107.623 ms
    62.115.63.53  96.949 ms

michael@michael-pro: ~/repos/wolf-soho
[0] $ echo Site 1; date; networkQuality; echo
Site 1
Mon Sep 29 17:13:44 EDT 2025
==== SUMMARY ====
Uplink capacity: 3.728 Mbps
Downlink capacity: 7.529 Mbps
Responsiveness: Low (5.144 seconds | 11 RPM)
Idle Latency: 69.189 milliseconds | 867 RPM

michael@michael-pro: ~/repos/wolf-soho
[0] $ uplink-
uplink-describe  uplink-lib.sh    uplink-lib.sh~   uplink-monitor   uplink-org

michael@michael-pro: ~/repos/wolf-soho
[0] $ uplink-describe
Uplink: SpaceX Services, Inc. — public IP — IP 2605:59ca:13ad:c910:7420:bdf4:439a:ca86

michael@michael-pro: ~/repos/wolf-soho
[0] $ uplink-describe
Uplink: SpaceX Services, Inc. — public IP — IP 2605:59ca:13ad:c910:7420:bdf4:439a:ca86

michael@michael-pro: ~/repos/wolf-soho
[0] $ echo Barn; date; networkQuality; echo
Barn
Mon Sep 29 17:16:04 EDT 2025
==== SUMMARY ====
Uplink capacity: 4.207 Mbps
Downlink capacity: 5.752 Mbps
Responsiveness: Low (3.388 seconds | 17 RPM)
Idle Latency: 60.783 milliseconds | 987 RPM

—Adam

<Screenshot 2025-09-28 at 4.29.40 PM.png>
<Screenshot 2025-09-28 at 4.43.06 PM.png>

Adam  Millsap
Farmer & Consultant

417-848-8877

<Adam@UrbanRootsFarm.com>

<www.Turnbuckle-farm.com>

          -- Know your Farmer. Know your food. --

On Sun, Sep 28, 2025 at 11:41 AM Michael R. Wolf <MichaelRWolf@att.net> wrote:
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

On Sep 24, 2025, at 5:03 PM, Adam Millsap <adam@UrbanRootsFarm.com> wrote:

Howdy Micheal,

Good to hear from you. Sorry I'm just getting back to you, things have been quite busy here, and I've fallen behind in emails.

First off; disclosures. 😉 I'm no longer running the network up there. I handed that off to Jeff in the spring at Aarons request.

That being said, I do still have full admin access, and could probably help you get your uap mesh adopted. In fact, most likely if you give it a factory reset, and power it up, It will show up in my dashboard for adoption. Shoot me a text when it's fired up.

Also, I appreciate the offer of systems checking the bus. I think Béla left it in good order, but I certainly wouldn't complain if you dropped by and had a look. I think the keys are in the door.

--Adam

--
Michael R. Wolf
    <MichaelRWolf@att.net>  | +1-206-679-7941  |  LinkedIn.com/in/MRWolf
        "All mammals learn by playing"

--
Michael R. Wolf
    <MichaelRWolf@att.net>  | +1-206-679-7941  |  LinkedIn.com/in/MRWolf
        "All mammals learn by playing"
