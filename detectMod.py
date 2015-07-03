__author__ = 'Prateek Prasher, CSED NITH'

"""
detectMOd - This is the module that defines the functions for motion detection and object recognition. The main
functions that will be used directly in the system are:
> isMotion()
> isAnimal()

Other functions my be present here but they are solely defined for making the code clear, thus play no role individually
and should not be invoked in the driver program.

Friday 19 June, 2015
v 1.0
"""

from flagMod import *
import cv2
import time
import numpy as np



"""
Motion detection functions
"""

def blurAndSub(imgNew, imgOld):
    """
    This is a helper function that takes two images and does following:
    > resize (IF ON RASPI)
    > blur
    > threshold
    > dialate
    :rtype : tuple
    :param imgNew: The new image
    :param imgOld: The older image
    :return: Returns the processed image
    """

    if DEBUG:
        print('In blurAndSub()')

    # Resize the image if on a RasPi
    # New image is quarter of the original one
    if RASPI:
        imgNew = cv2.resize(imgNew, (0, 0), fx=0.5, fy=0.5)
        imgOld = cv2.resize(imgOld, (0, 0), fx=0.5, fy=0.5)

    # Now apply some gaussian blur on the image to reduce noise
    imgNew = cv2.GaussianBlur(imgNew, (5, 5), 0)
    imgOld = cv2.GaussianBlur(imgOld, (5, 5), 0)

    # Now find the difference between 2 images, threshold and dialate
    imgDif      = cv2.absdiff(imgNew, imgOld)

    imgThresh   = cv2.threshold(imgDif, 35, 255, cv2.THRESH_BINARY)[1]

    imgDilated  = cv2.dilate(imgThresh, None, iterations=3)

    if DEBUG:
        print('Successfully executed blurAndSub()')

    return imgDilated

#------------------------------------------------------------------#

def isMotion(imgNew, imgOld):
    """
    This is the fucntion that is used to find any motion in hte image. If there is any motion
    it returns true and false otherwise, along with the motion image

    :param imgNew: The new image
    :param imgOld: The old image
    :return: true is motion found, false otherwise, along with the motion image
    """

    if DEBUG:
        print('In isMotion()')

    # Find the difference in the frames
    if DEBUG:
        t1 = time.time()

    # Convert to grayscale
    imgNew = cv2.cvtColor(imgNew, cv2.COLOR_BGR2GRAY)
    imgOld = cv2.cvtColor(imgOld, cv2.COLOR_BGR2GRAY)

    imgDiff = blurAndSub(imgNew, imgOld)

    if DEBUG:
        print('Took %fms to detect motion' %(time.time() - t1))

    # Now find the changed pixels in image
    change = np.sum(imgDiff)

    if DEBUG:
        print('Change %f' %change)
        print('Successfully executed isMotion()')

    if change > 1000:
        return True, imgDiff
    else:
        return False, imgDiff

#------------------------------------------------------------------#
#------------------------------------------------------------------#

"""
Animal detection functions
"""

def isAnimal(img):
    pass