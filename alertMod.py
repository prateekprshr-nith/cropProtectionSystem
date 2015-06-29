__author__ = 'Prateek Prasher, CSED NITH'

"""
alertMod - This is the module that defines the functions for ringing ararms and lighting various indication lights.
The main functions that will be used directly in the system are:
> ringAlarm()
> only this much for now

Other functions my be present here but they are solely defined for making the code clear, thus play no role individually
and should not be invoked in the driver program.

Friday 29 June, 2015
v 1.0
"""

from flagMod import *
if RASPI:
    import RPi.GPIO


"""
Alarm ringing functions
"""

def ringAlarm():
    """
    This is the fucntion that is used to ring the alarm in case an animal is found in the image

    :return: nothing
    """
    pass
