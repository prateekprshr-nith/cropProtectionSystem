__author__ = 'Prateek Prasher, CSED NITH'

"""
driver - This is the driver program that contains the main functionality of this system.
Its work is to capture the frames and feed them to the underlying modules that are responsible
for animal detection and sounding of buzzers.

Monday 29 June, 2015
v 1.0
"""

from detectMod import *
#import errorMod
#import logMod
#import alertMod

# Firstly create a video capture object
cap = cv2.VideoCapture(0)

# Capture an old frame
try:
    ret, oldFrm = cap.read()
    if not ret :
        raise
except:
    # Error handling to be added later
    pass

# Now start the capture loop
while True:
    # Read a new frame
    try:
        ret, newFrm = cap.read()
        if not ret:
            raise
    except:
        # Error handling to be added later
        pass

    # Now check for any motion
    motion, motionImg = isMotion(newFrm, oldFrm)

    if motion:
        # Save the current image and write the log entry
        saveImg(newFrm)
        writeLog()

        # Motion is found, now check for any animal in image
        animal, animalImg = isAnimal(newFrm)

        # Now if animal is found
        if animal:
            ringAlarm()

        # Continue capturing the frames
