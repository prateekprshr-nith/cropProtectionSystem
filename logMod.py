#!/usr/bin/env python

__author__ = 'Prateek Prasher, CSED NITH'

"""
logMod - This is the module that defines the functions for logging various messages and saving the images
The main functions that will be used directly in the system are:
> saveImg()
> writeLog()
> writeErrLog()

Other functions my be present here but they are solely defined for making the code clear, thus play no role individually
and should not be invoked in the driver program.

v 1.0

#Change Log:

-> Edit 1: Friday 29 June, 2015
   Added the names of the functions
-> Edit 2: Friday 10 July, 2015
   Defined saveImg()
-> Edit 3: Tuesday, 21 July, 2015
   Defined writeLog(), writeErrLog(), writeDebugLog()
"""

import time
import cv2
from configFile import *

"""
Image saving functions
"""

def saveImg(img):
    """
    This is the function that is used to store a motion captured image
    :param img: the image to be stored
    :return: None
    """

    if DEBUG:
        print('In saveImg()')

    # Dict for months
    month = {'January'   : '01',
             'February'  : '02',
             'March'     : '03',
             'April'     : '04',
             'May'       : '05',
             'June'      : '06',
             'July'      : '07',
             'August'    : '08',
             'September' : '09',
             'October'   : '10',
             'November'  : '11',
             'December'  : '12'}

    # Get the current date and time
    currAscTime  = time.asctime()
    currMonth    = currAscTime[4 : 7]
    currDate     = currAscTime[8 : 10]
    currYear     = currAscTime[-2] + currAscTime[-1]
    currTime     = currAscTime[11 : 19]

    for i in list(month):
        if currMonth in i:
            currMonth = month[i]
            break

    # Now make a filename and write the image
    fileName = 'motionPic/' + currDate + '-' + currMonth + '-' + currYear + ' ' + currTime + '.jpg'
    try:
        cv2.imwrite(fileName, img, [int(cv2.IMWRITE_JPEG_QUALITY), 10])
    except IOError:
        writeErrLog('Couldnt save image at %s' %currAscTime)


#------------------------------------------------------------------#
#------------------------------------------------------------------#
"""
Logging functions
"""

def writeLog(msg):
    # TODO Add the documentation
    """
    :param msg:
    :return:
    """
    # Get the current date and time
    currAscTime  = time.asctime()

    # Now make the message that has to be written
    msg = currAscTime + ': ' + msg + '\n'

    # Open the log file and append the message
    try:
        log = open('/logs/general/genlog.log', 'a')
        log.write(msg)
    except IOError:
        log.flush()
        log.close()
    finally:
        log.flush()
        log.close()


#------------------------------------------------------------------#

def writeErrLog(msg):
    # TODO Add the documentation
    """
    :param msg:
    :return:
    """
    # Get the current date and time
    currAscTime  = time.asctime()

    # Now make the message that has to be written
    msg = currAscTime + ': ' + msg + '\n'

    # Open the log file and append the message
    try:
        log = open('/logs/error/errlog.log', 'a')
        log.write(msg)
    except IOError:
        log.flush()
        log.close()
    finally:
        log.flush()
        log.close()


#------------------------------------------------------------------#

def writeDebugLog(msg):
    # TODO Add the documentation
    """
    :param msg:
    :return:
    """
    # Get the current date and time
    currAscTime  = time.asctime()

    # Now make the message that has to be written
    msg = currAscTime + ': ' + msg + '\n'

    # Open the log file and append the message
    try:
        log = open('/logs/debug/debuglog.log', 'a')
        log.write(msg)
    except IOError:
        log.flush()
        log.close()
    finally:
        log.flush()
        log.close()