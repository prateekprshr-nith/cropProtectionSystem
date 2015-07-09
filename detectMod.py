__author__ = 'Prateek Prasher, CSED NITH'

"""
detectMOd - This is the module that defines the functions for motion detection and object recognition. The main
functions that will be used directly in the system are:
> isMotion()
> isAnimal()

Other functions my be present here but they are solely defined for making the code clear, thus play no role individually
and should not be invoked in the driver program.

v1.0

#Change log:

->Edit 1: Friday 19 June, 2015
  Added the two functions blurAndSub() and isMotion()

->Edit 2: Wednesday 8 July, 2015
  Added the isAnimal() an getRoi()

->Edit 3: Thurusday 9 July, 2015
  Added MOTION_THRESH, changed it to 500
  Added MIN_AREA, changed it to 500
  Finished the isAnimal() function


"""

from flagMod import *
import cv2
import time
import numpy as np



"""
Motion detection functions
"""

MOTION_THRESH = 500

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

    # Convert to grayscale
    imgNew = cv2.cvtColor(imgNew, cv2.COLOR_BGR2GRAY)
    imgOld = cv2.cvtColor(imgOld, cv2.COLOR_BGR2GRAY)

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
    This is the fucntion that is used to find any motion in the image. If there is any motion
    it returns true and false otherwise, along with the motion image

    :param imgNew: The new image
    :param imgOld: The old image
    :return: true is motion found, false otherwise, along with the motion image
    """

    if DEBUG:
        print('In isMotion()')

    if DEBUG:
        t1 = time.time()

    # Find the difference in the frames
    imgDiff = blurAndSub(imgNew, imgOld)

    if DEBUG:
        print('Took %fms to detect motion' %(time.time() - t1))

    # Now find the changed pixels in image
    change = np.sum(imgDiff)

    if DEBUG:
        print('Change %f' %change)
        print('Successfully executed isMotion()')

    if change > MOTION_THRESH:
        return True, imgDiff
    else:
        return False, imgDiff

#------------------------------------------------------------------#
#------------------------------------------------------------------#

"""
Animal detection functions
"""

MIN_AREA = 500

def getRoi(img):
    """
    This is the fucntion that is used to get a list of roi's from the motion captured image

    :param img: The binary diff image
    :return: list of roi in decreasing order of area
    :rtype : list
    """
    if DEBUG:
        print('In getRoi()')

    # Now find the contours and save their dim and area in a list
    roi = []
    _, cnts, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for c in cnts:
        # Get the contour area and the bounding rectangle
        areaNrect = (cv2.contourArea(c), cv2.boundingRect(c))

        # Discard the smaller contours
        if areaNrect[0] < MIN_AREA:
            continue

        roi.append(areaNrect)

    # Sort the contours on the basis of area, and return 4 with max area
    roi.sort()
    return roi

#------------------------------------------------------------------#

def getCorr(imgNew, imgOld):
    """
    This is the fucntion that is used to calculate correlation between roi area and old area

    :param imgNew: the extracted roi
    :param imgOld: the area in reference image
    :return: correlation in two images
    :rtype : float
    """
    h1 = cv2.calcHist([imgNew], [0], None, [256], [0, 255])
    h2 = cv2.calcHist([imgOld], [0], None, [256], [0, 255])

    currCorr = cv2.compareHist(h1, h2, cv2.HISTCMP_CORREL)
    return currCorr

#------------------------------------------------------------------#

def isAnimal(img, imgRef):
    """
    This is the fucntion that is used to detect any animal in the motion captured image.

    :param img: The motion captured image
    :param imgRef: The reference image for background subtraction
    :return: true if motion is found, false otherwise
    :rtype: bool
    """
    if DEBUG:
        print('In isAnimal()')

    # Calculate the difference in the images
    imgDif = blurAndSub(img, imgRef)
    imgDif  = cv2.dilate(imgDif, None, iterations=22)

    # Now get the list of roi
    roiVec = getRoi(imgDif)

    # Now try to identify a human. A false value should be returned if a human is found
    for obj in roiVec:
        aspectRatio = float(obj[1][2]) / float(obj[1][3])           # width/height
        extent      = float(obj[0]) / float(obj[1][2] * obj[1][3])  # contour area / rectangle area

        if DEBUG:
            print('Aspect ratio: %f' %aspectRatio)
            print('Extent: %f' %extent)
        X = obj[1][0]
        W = obj[1][2]
        Y = obj[1][1]
        H = obj[1][3]
        roiOld = imgRef[Y:Y+H, X:X+W]
        roiNew = img[Y:Y+H, X:X+W]
        if aspectRatio > 0.5 and getCorr(roiOld, roiNew) < 0.8:
            return True

    return False