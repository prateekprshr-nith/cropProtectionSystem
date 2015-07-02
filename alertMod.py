__author__ = 'Prateek Prasher, CSED NITH'

"""
alertMod - This is the module that defines the functions for ringing ararms and lighting various indication lights.
The main functions that will be used directly in the system are:
> ringAlarm()
> only this much for now

Other functions my be present here but they are solely defined for making the code clear, thus play no role individually
and should not be invoked in the driver program.

Edit 1: Friday 29 June, 2015
v 1.0

Edit 2: Thursday 2 July, 2015

"""

from flagMod import *
import RPi.GPIO as GPIO
import time


# BCM Numbering has been used to refer to board pins
pins = {"ALARM_PIN"     : 12,
        "MOTION_PIN"    : 8,
        "STATUS_PIN"    : 20,
        "CAMERA_PIN"    : 21}

# Time in seconds for which the alarm will run
ALARM_TIME  = 600


"""
Function to setup GPIO
"""

def gpioSetup():
    """
    This function is used to set up the gpio pins for i/o

    :return: nothing
    """
    GPIO.setmode(GPIO.BCM)
    GPIO.cleanup()

    # Now setup the pins for output
    for pin in list(pins):
        GPIO.setup(pins[pin], GPIO.OUT)

#------------------------------------------------------------------#
#------------------------------------------------------------------#

"""
Alarm ringing functions
"""

def ringAlarm():
    """
    This is the function that is used to ring the alarm in case an animal is found in the image.
    The alarm is buzzed for 10 mins

    :return: nothing
    """
    GPIO.output(pins['ALARM_PIN'], 1)   # Turn on buzzer
    time.sleep(600)                     # Sound it for 600 sec or 10 minutes
    GPIO.output(pins['ALARM_PIN'], 0)   # Turn the buzzer off














