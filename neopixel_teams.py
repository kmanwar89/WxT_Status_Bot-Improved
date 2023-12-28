#!/usr/bin/python
'''
2023-10-14 Kadar Anwar
- neopixel_teams.py - Display WebEx Teams status using a Pi Zero and an 8-LED NeoPixel stick from Adafruit (https://www.adafruit.com/product/1426)
- Re-written using the NeoPixel library, along with other improvements
- Code concept adopted from matthewf01's WebEx Teams Status Bot (https://github.com/matthewf01/Webex-Teams-Status-Box)
'''

# Import libraries
import board
import neopixel
from time import sleep
from webexteamssdk import WebexTeamsAPI

# Create a pixel object; assign to GPIO 18 on the Pi with 8 LED's
pixels = neopixel.NeoPixel(board.D18, 8)

# Create a "Connection Object"
api=WebexTeamsAPI(access_token="ACCESS TOKEN HERE")

# Set the "person ID" of the bot
mywebexid="PERSON ID HERE"

# Get the status (this needs to be changed to a loop, with a dictionary rather than multiple if statements)
api.people.get(personId=mywebexid).status

try:
        while True:
                status = api.people.get(personId=mywebexid).status
                if status == "active":
                        pixels.fill((0,255,0))
                        print ("active - GREEN")
                        sleep (10)
                elif status == "call":
                        pixels.fill((255,128,0))
                        print ("On a call - ORANGE")
                        sleep (10)
                elif status == "inactive":
                        pixels.fill((0,0,255))
                        print ("inactive - BLUE")
                        sleep (10)
                elif status == "OutOfOffice":
                        pixels.fill((255,0,255))
                        print ("Out of Office - PURPLE")
                        sleep (10)
                elif status == "DoNotDisturb":
                        pixels.fill((255,0,0))
                        print ("Do Not Disturb - RED")
                        sleep (10)
                elif status == "unknown":
                        pixels.fill((0,255,255))
                        print ("Busy - CYAN")
                        sleep (10)
                elif status == "presenting":
                        pixels.fill((255,0,0))
                        print ("presenting - RED")
                        sleep (10)
                elif status == "meeting":
                        pixels.fill((255,128,0))
                        print ("meeting - ORANGE")
                        sleep (10)
                else:
                        pixels.fill((255,255,0))
                        print ("Couldn't determine status")

except KeyboardInterrupt:
        pixels.fill((0,0,0))

# Status codes include: active,inactive,DoNotDisturb,meeting,presenting,call,unknown (busy), OutOfOffice