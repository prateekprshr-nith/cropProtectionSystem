#!/usr/bin/env python


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

Edit 3: Monday 6 July, 2015

"""

from flagMod import *
import RPi.GPIO as GPIO
import time
import os


# BCM Numbering has been used to refer to board pins
pins = {"ALARM_PIN"     : 12,
        "MOTION_PIN"    : 8,
        "STATUS_PIN"    : 20,
        "CAMERA_PIN"    : 21}

SIGKILL = 6 # Signal to be sent to blinkLed process

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
    if DEBUG:
        print("In gpioSetup()")

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    # Now setup the pins for output
    for pin in list(pins):
        GPIO.setup(pins[str(pin)], GPIO.OUT)

#------------------------------------------------------------------#
#------------------------------------------------------------------#

"""
ringAlarm() : Alarm ringing function
"""

def ringAlarm():
    """
    This is the function that is used to ring the alarm in case an animal is found in the image.
    The alarm is buzzed for 10 mins

    :return: None
    """
    if DEBUG:
        print("In ringAlarm()")

    GPIO.output(pins["ALARM_PIN"], 1)   # Turn on buzzer
    time.sleep(600)                     # Sound it for 600 sec or 10 minutes
    GPIO.output(pins["ALARM_PIN"], 0)   # Turn the buzzer off


#------------------------------------------------------------------#
#------------------------------------------------------------------#

"""
statusLed() : Toggle status led
"""

def statusLed(status, pid=None):
    """
    This is the function that is used to blink status led or turn it solid.
    It blinks if system is working fine and turns solid on some error.
    -> if arg is 1, the process blinkLed is created.
    -> if arg is 0, the process (pid) is killed and the led is turned solid.

    :param status: 1 for blinking, 0 for solid light
    :param pid: the pid of process to be killed
    :return: pid of the blinkLed process
    """
    if DEBUG:
        print("In statusLed()")

    if status == 1:                # Blink the led
        pid = os.fork()
        if pid == 0:
            os.execl("./helper/blinkLed.py", "./helper/blinkLed.py", str(pins["STATUS_PIN"]))
        else:
            return pid
    else:                          # Turn status led solid
        os.kill(pid, SIGKILL)
        GPIO.output(pins["STATUS_PIN"], 1)
        return None

#------------------------------------------------------------------#
#------------------------------------------------------------------#

"""
cameraErrLed() : Blink camera error led
"""

def cameraErrLed():
    """
    This is the function that is used to blink camera err led
    It blinks if the frame couldn't be read from the camera

    :return: None
    """
    if DEBUG:
        print("In cameraErrLed()")

    try:
        pid = os.fork()                 # Blink the led
        if pid < 0:
            raise OSError
    except OSError:
        # TODO add error handling function here
        pass

    if pid == 0:
        os.execl("./helper/blinkLed.py", "./helper/blinkLed.py", str(pins["CAMERA_PIN"]))

#------------------------------------------------------------------#
#------------------------------------------------------------------#

"""
motionLed() : Light up the motion led on motion
"""

def motionLed(val):
    """
    This is the function that is used to light up the led in case of motion, or turn it off if there is no motion
    :param val: 1 for lighting the led, 0 for turning it off
    :return: None
    """
    if val == 1:
        GPIO.output(pins["MOTION_PIN"], 1)
    else:
        GPIO.output(pins["MOTION_PIN"], 0)