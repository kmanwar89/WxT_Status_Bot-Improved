# Webex-Teams-Status-Bot - Improved!
**IoT status light using a Raspberry Pi Zero W, Python 3, *webexteamssdk* and Adafruit's NeoPixel Stick 8-RGB LED to display your real-time presence status in Webex Teams**

This code was adopted from the great work done by @matthewf01, however that project hasn't been updated for 3 years. Some improvements over the existing code:

- Service file fixes:
  - [X] updated to no longer wait for a graphical interface (this was causing it to never run, as most Pi's are headless)
  - [X] hard-coded references of "Pi" removed from executable location - this should be customized to the user's setup
  - [X] waits for network before running, as this service is useless without network connectivity
  - [x] executable changed to Python 3
- Code updated for Python 3, as Python 2 is deprecated
- NeoPixel is used instead of a single LED - this allows for more granular (16,777,216, to be exact!) colors without pseudo-PWM that the Pi is trying to push to the LED
- More colors included to incorporate new "busy" status
  - NOTE: I've confirmed with WebEx developers that the backend API has not been fully updated to incorporate new features in WxT - namely, "Quiet hours" and "Busy" status. The backend API still shows "unknown" as the status, so the colors are duplicated until those backend changes are made:

      > Yes, this DnD status has been already implemented now in the Production correctly and that's why the DnD status looks to be fine.

      > However, the "Busy" status is still not implemented in the system and it shows as "Unknown". It needs to be handled from backend so that it's available in API.
      
      > Even the "Quiet" status also needs to be implemented from the backend since currently the "Quiet" status shows as "DnD" in the API.

      > We already have a JIRA raised internally from the Product Management team and work is in progress. But don't have a fixed ETA at this moment.
      

<br>

**Finished project mounted on my office door jamb:**
<img src="https://github.com/kmanwar89/WxT_Status_Bot-Improved/raw/master/photos/mounted_final.jpg" height="1024" width="512">

### This project uses the Webex Teams SDK Python library: ###

* [Documentation](https://webexteamssdk.readthedocs.io/en/latest/index.html)

* [Github - webexteamssdk](https://github.com/CiscoDevNet/webexteamssdk)


## Hardware Setup Instructions

### Parts you will need:
* A Raspberry Pi with network connectivity 
  * I used a Pi Zero WH for this build, but other Pi's could be used (though may not mount as cleanly)
* MicroSD card formatted with Raspberry Pi OS (the new name for Raspbian)
  * The Raspberry Pi Foundation's [official imager tool](https://www.raspberrypi.com/software/) is cross-platform and works on Windows, Mac and Linux.
  * It is advised to configure the network SSID, region, language and any other settings. I also set SSH with a static password at first, and then copy over my SSH keys on first boot.
* 1x [Adafruit NeoPixel Stick](https://www.adafruit.com/product/1426)
  * I originally tried the single-LED approach, but realized I bought common Cathode instead of common Annode, and couldn't figure out how all the wires can fit in such a small case. So instead, I re-purposed a NeoPixel stick I had lying around and am much happier with the result!
* A solderless breadboard with jumpers (Female to Male, Male to Male) for testing
* A soldering iron and wire (or jumpers) for final installation
* 3M Command Strip or generic velcro strip for mounting
* [Raspberry Pi Zero official case](https://www.raspberrypi.com/products/raspberry-pi-zero-case/), or any case that allows for GPIO breakout
  * I originally used the camera hole faceplate, but could not figure out how the wiring was finalized, so I switched to using the GPIO cutout faceplate instead. A "final" version may involve a 3D-printed case for a more polished look.
* Hot glue, or equivalent electronics-safe adhesive for semi-permanent mounting

### Wiring Guide

I found the previous instructions rather confusing, and relying on external links is never a great idea since those links might break. Plus, I'm *not* an electronics engineer, so I had to do a cursory dive into PWM, GPIO pinouts, etc. So, for those in the same boat, here's my TL;DR to get up and running *quickly*:

0) Choose a consistent color pattern that makes things easy to remember - I like the following:
  - White - DIN (Digital Input)
  - Green - 5VDC (5 Volts DC)
  - Black - GND (Ground)
1) Using a Female-to-Male jumper cable, solder the male end (square peg, not square hole) directly to the NeoPixel - be sure to solder the DIN side, not the DOUT side - these are meant to be daisy-chained, but we won't be doing that in this project, and the Pi can't power that many anyways!
2) Connect the Female end of the jumper to the following pins on the Pi - [refer to the GPIO pinout](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html)
    * Note - we are NOT counting pins on the board, but rather the GPIO pins. If you look at the pinout, you'll see a pattern - 2 or 3 GPIO pins, followed by a GND, with a smattering of 5V pins throughout. The pins we care about are referenced relating to the GPIO number, so GPIO 18 is not the same as counting 18 pins from either side of the board
    * Note - you can type "pinout" from within the CLI of the Pi for a "graphical" interface that shows this same information. Neat!
    
<img src="https://www.raspberrypi.com/documentation/computers/images/gpiozero-pinout.png" height="512" width="300">

  - White - DIN ---> GPIO 18 (pin 12 in the above image)
  - Green - 5VDC ---> 5V (doesn't matter which one) (pin 2 in the above image)
  - Black - GND ---> Ground (doesn't matter which one) (pin 6 in the above image)

1) Assuming the Pi is powered up, on the network and logged in via SSH, install git and clone this repository directly to the Pi
2) Run the install script, substituting tokens where necessary

## Software Setup Instructions
### You will need 2 pieces of information to complete software setup: ###

1. **Your bot's access token from Webex:**
  * TEMPORARY: you can get a temp access token here, but it will expire in 12 hours. FOR TESTING ONLY.
    * https://developer.webex.com/docs/api/getting-started
  * PERMANENT: create a bot at the site below. Give it a unique name and you'll get an access token good for life
    * https://developer.webex.com/my-apps/new/bot

2. **Your user's personId from Webex:**
  * https://developer.webex.com/docs/api/v1/people/get-my-own-details
    1. Sign into your Webex account, then under the "Try It" section, click "Run"
    2. Copy the value `id` from the response shown


### Run these command from your Raspberry Pi's terminal: ###

* `wget https://raw.githubusercontent.com/matthewf01/Webex-Teams-Status-Box/master/setup.sh`
* `sh setup.sh`

The _setup.sh_ shell script I created is awesome and performs the following for you:
* Prompts you for the access token and your personId
* Stores these credentials in a local file called _mycredentials.txt_ just in case you need them later.
* Downloads the Python script (_webexteams.py_) and a service installation file
* Injects your credentials into the service's unit file
* Installs the script as a service which starts at boot
* Installs the webexteamssdk module via pip
* Reboots on completion

### Testing ###

To test, from Terminal run: `python /Home/pi/Documents/webexteams.py`
After a moment, you should see the status codes being returned from the Webex Teams API. `CTRL+C` to break and stop the test run.

Verify your LED is lighting up properly at this time. Double-check that the GPIO pins you've connected match the `webexteams.py` script.

## Running the thing! ##
The Python script has been set via systemd service to run at startup. 

Restart the Raspberry Pi and confirm the script has started automatically. 

Enjoy your new Webex Teams Status light, and teach your family what the color-codes mean! 

- Red = do not disturb me
- Green = I'm working but you can come into the room
- Blue means inactive (so I'm not working)