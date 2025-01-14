---
title: Solving connection issues on the W-Ergo Split Keyboard (Ergodox dupe)
slug: solving-connection-issues-on-the-w-ergo
date: 2024-12-06T20:29:00.000Z
type: "post"
---

# Solving connection issues on the W-Ergo Split Keyboard (Ergodox dupe) UPDATED: 2025

> TLDR with my solution at the bottom!

I recently purchased the W-Ergo Wireless Split Keyboard from keyclicks.ca. 

First impressions are great, it’s my first split keyboard and so far has stopped the RSI I was feeling in my wrists.

Very much enjoying the process of getting comfortable with the split. The hardest thing for me has been relearning how to type. The split isn’t so bad, but I took the opportunity to also teach myself to TouchType, properly. 

For the past 20 odd years I’ve been using a keyboard with my index and middle fingers and the occasional pinkie and thumb for those shortcuts. 

My typing speed is only around 40 WPM but I’m hoping with the additional use of my digits, I can surpass this and hope to get ~80WPM. That’s my North Star anyway.

## Issues

Now for the part you’re probably here for. I use an M2 Mac for work with a ThunderBolt Dock to power:
- 2 x 1080p monitors
- External usb microphone 
- External DAC
- External Keyboard
- Elgato 4k Webcam

Before having the W-Ergo, I was using a Durgod mechanical keyboard wired into the dock without any issues.

The W-Ergo comes with a 2.4ghz receiver which plugs in via USB. So naturally I swapped my keyboards and plugged it into the dock.

Boom, working! 

Mostly..

As I was typing, some keys  on the right half of the keyboard would ‘stick’ or not register. Okay, no problem. Might be some interference on the 2.4ghz waves, I am sat right next to an access point. I disconnect the Access Point but still no luck.

Maybe the receiver needed a line of sight to the keyboard, even though I read online that it can work up to 50 feet away. Still no luck.

Unplugged and plugged back in, and that worked, for a little bit. I turned the keyboard off and back on and that seemed to connect and then after 5 minutes it would start ‘lagging’ again.

After some Googling I came to the conclusion that it might be some USB interference from the dock. Maybe I was overloading it (which I probably am, given the amount of peripherals hanging off a single thunderbolt port).

I went through the process of elimination by removing one of the peripherals and using the keyboard. I concluded that my webcam was the issue, so I moved the webcam to the other thunderbolt port on my Mac.

This worked for a little while, I figured I had cracked it. 24 hours later the keyboard started having issues again.

I looked online and updated the firmware on the receiver and the left and right halves of the keyboard using the recommended iPhone app following their documentation on the keyclicks website.

Still no joy, but good to have the latest firmware regardless.

Some more googling suggested some software solutions. I found a tutorial which suggested turning off an energy saving setting on the Mac to not turn off USB when the computer goes to sleep (which now that I think of it, I only had keyboard issues on the afternoon, or more specifically, after I’d had my hour lunch break away from the computer)

I changed the option and things started working again.

Until the next day…

Once again, problems with the keyboard. I was considering reaching out to support, but I’ve heard their credibility isn’t great. I was determined to exhaust every possible option before putting it down to a hardware fault.

When I opened my Finder I saw that my dock had a drive attached. I wondered whether the Mac was somehow powering off the dock as a USB device.

Lo and behold, Mac has a setting for this [Insert location here]. I turned the setting from ‘auto’ to ‘never’.

Fingers crossed this has solved the problem. I found it yesterday, haven’t had any problems today and now it’s the weekend, so the real test will be on Monday when I wake up the Mac for work.

It may not be the solution, but figured I’d document my journey for those also looking for solutions!

## TLDR;

EDIT 14/01/2025: I've done some more debugging and had determined that 2.4ghz interference is the issue I am facing.

I changed my Mac to use hardwired ethernet and swiched my Logitech mouse from using Bluetooth to using the Unifying Reciever.

I then disabled WiFi and Bluetooth on my Mac in the settings. This seems to have helped the issues I was having.

The keyboard wireless receiver is sat in between my keyboard halves and under my deskmat.

I sometimes find that having my iPhone nearby also causes some issues. I'll keep an eye on this as that's pretty ridiculous.

I'll keep my steps below for archival purposes, I'm not sure if they contributed to the solution or if I was just chasing my tail.

---

Here’s what I tried: (SEE EDIT ABOVE)
- Rebooted
- Changed USB ports
- Switched the Keyboard to its on thunderbolt port with a USB to USB-C converter 
- Unplugged my other devices one by one to see if it worked
- Removed WiFi interference by unplugging my access point
- Moved the receiver around (it now lives taped under my desk)
- Updated firmware of the receiver and left/right halves (twice)
- Disabled Mac powering off USB devices

What worked: (SEE EDIT ABOVE)
- Turning off unmounting USB drives automatically 

What worked 2025:
- Wifi interference. Hardwired ethernet, turned off Bluetooth, possible USB3.0 interference.
- Moved receiver in between the keyboard halfs. 10cm away from each half.

Well, this may have worked in combination with any of the above steps, but I’m too exhausted to determine the magic combination of settings to get the keyboard working. 

Hope this helps someone and saves them a week of debugging
