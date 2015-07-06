__author__ = 'Prateek Prasher, CSED NITH'

"""
driver - This is the driver program that contains the main functionality of this system.
Its work is to capture the frames and feed them to the underlying modules that are responsible
for animal detection and sounding of buzzers.

v 1.0

Edit 1: Monday 29 June, 2015
Edit 2: Monday 6 July, 2015
"""

from detectMod  import *
from flagMod    import *
from alertMod   import *
from logMod     import *
#import errorMod

# Turn the status led on (1 as argument)
statusLedPid = statusLed(1)

# Firstly create a video capture object
cap = cv2.VideoCapture(0)

# Capture an old frame
try:
    ret, oldFrm = cap.read()
    if not ret :
        raise
except:
    statusLed(0, statusLedPid)  # Turn the status led solid
    cameraErrLed()              # Blink the camera error led
    # TODO Add error handling for camera read error

# Now start the capture loop
while True:
    # Read a new frame
    try:
        ret, newFrm = cap.read()
        if not ret:
            raise
    except:
        statusLed(0, statusLedPid)  # Turn the status led solid
        cameraErrLed()              # Blink the camera error led
        # TODO Add error handling for camera read error

    # Now check for any motion
    motion, motionImg = isMotion(newFrm, oldFrm)

    if motion:
        # Turn on the motion led
        motionLed(1)

        # Save the current image and write the log entry
        saveImg(newFrm)
        writeLog()

        # Motion is found, now check for any animal in image
        animal, animalImg = isAnimal(newFrm)

        # Now if animal is found
        if animal:
            ringAlarm()
    else:
        # Turn off the motion led
        motionLed(0)

    oldFrm = newFrm