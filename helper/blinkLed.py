#!/usr/bin/env python

"""
This script is used to blink an led, as specified by argv[1].
It keeps on blinking the led with an interval of PAUSE seconds, as defined below.

- Prateek Prasher, CSED NITH

v 1.0
Monday, 6th July, 2015
"""

import RPi.GPIO as GPIO
import os
import sys
import signal
import time

SIGKILL = 6     # The signal for exitng the process
PAUSE = 0.001   # Pause for led in seconds

"""
The signal handler function, it turns off the blinking led
"""
def turnOffBlink(pid, frame=None):
    GPIO.output(PIN_NO, 0)      # Turn off the led
    exit()

# Associate singal with handler
signal.signal(SIGKILL, turnOffBlink)

# Error if led no. is not provided
if len(sys.argv) == 1:
    print("Usage: blinkLed [pin number]")
    exit()
else:
    PIN_NO = int(sys.argv[1])

# Set up the gpio
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_NO, GPIO.OUT)

# Now set the led to blink
val = 1                         # Keep on toggling this var btw 0 and 1

while True:
    GPIO.output(PIN_NO, val)
    time.sleep(PAUSE)
    if val == 1:
        val = 0
    else:
        val = 1