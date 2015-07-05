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
# TODO : in the fucntion statusLed, blinkLed script has to be made

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
    GPIO.cleanup()

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

    :return: nothing
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

def statusLed(status, pid):
    """
    This is the function that is used to blink status led or turn it solid.
    It blinks if system is working fine and turns solid on some error.
    -> if arg is 1, the process blinkLed is created.
    -> if arg is 0, the process (pid) is killed and the led is turned solid.

    :arg:status: 1 for blinking, 0 for solid light
    :arg:pid: the pid of process to be killed
    :return: pid
    """
    if DEBUG:
        print("In statusLed()")

    if status == 1:
        pid = os.fork()
        if pid == 0:
            os.execl("/helper/blinkLed.py", "/helper/blinkLed.py")
        else:
            return pid
    else:
        os.kill(pid, SIGKILL)
        GPIO.output(pins["STATUS_PIN"], 1)  # Turn status led solid
        return None