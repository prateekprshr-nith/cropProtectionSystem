#!/usr/bin/env python


"""
Author : Prateek Prasher, CSED NITH

config - This is the module that helps to set the various parameters of the system

v1.0

#Change log:

->Edit 1: Tuesday 21, 2015
  Initial commmit

"""

__author__ = 'Prateek Prasher, CSED NITH'

import os
from configFile import *

#--------------------------------------------------------------------------------------#
"""
getInput() - Gets input from the user
"""
def getInput(msg, valRange):
    """
    This function is used to get the input of the parameters from the user.
    It also checks for any wrong input that is entered by the user.
    @:param
    :rtype : int, float
    """
    while True:
        try:
            val = input('Enter new %s: ' %msg)
        except NameError:
            print('Please enter a correct value!!!')
        except KeyboardInterrupt:
            print('\n^C pressed, exiting and restoring previous settings.')
            exit()
        else:
            if isinstance(val, (int, float)) and (val >= valRange[0]) and (val < valRange[1]):
                return val
            else:
                print('Please enter a correct value!!!')

#--------------------------------------------------------------------------------------#
"""
createBackup() - Create a backup of current settings
"""
def createBackup():
    try:
        config = open('configFile.py')
        buff = config.read()
    except IOError:
        print("Unable to open file. Please try again later.")
        exit()
    else:
        config.close()
        return buff

#--------------------------------------------------------------------------------------#
"""
saveSettings() - Saves the current settings
"""
def saveSettings(newSetting, bakData):
    try:
        config = open('configFile.py', 'w')
        for line in newSetting:
            config.write(line[0])
            config.write(line[1])
            config.write('\n')
    except (IOError, KeyboardInterrupt):
        config.seek(0)
        config.write(bakData)
        config.close()
        print('Error witing new settings, restoring previous ones')
    finally:
        config.flush()
        os.fsync(config.fileno())
        config.close()

#--------------------------------------------------------------------------------------#
# Set up the data to be written and the backup
bakData = createBackup()
newSetting = [ ['MOTION_THRESH = ', '500'],
             ['SCALE_FACTOR = ', '0.6'],
             ['THRESH_LEVEL = ', '35'],
             ['MOTION_DILATION_FACTOR = ', '3'],
             ['MIN_DETECTION_AREA = ', '500'],
             ['DETECTION_DILATION_FACTOR = ', '22'],
             ['MIN_ASPECT_RATIO = ', '0.5'],
             ['MAX_CORR_COFF = ', '0.8'],
             ['DEBUG = ', 'True'],
             ['VIDEO = ', 'False'] ]


# Now get the user input
print('###########################################################')
print('SMART CROP PROTECTION SYSTEM(v1.0) CONFIGURATION FILE')
print('**Please make changes to this file only if you know what you are doing.**')
print("**Enter older value again if you don't want to change**")
print("**Enter given default values for default settings**")
print('\n->Please enter the new settings:')

print('1) Motion Threshold\n   (High value means lesser senstivity)\n   Default value = 500\n   Range = [1 - 10000]'
      '\n   Current value: %f' %MOTION_THRESH)
newSetting[0][1] = str(getInput('Motion threshold', (1, 10001)))

print('\n2) Image Scaling Factor\n   (High value means faster operation, lesser accuracy)'
      '\n   Default value = 0.5\n   Range [0.1 - 0.99]\n   Current value: %f' %SCALE_FACTOR)
newSetting[1][1] = str(getInput('Scale factor', (0.1, 1.0)))

print('\n3) Threshold Level\n   (High value means larger threshold)\n   Default value = 35\n   Range =  [1 - 254]'
      '\n   Current value: %f' %THRESH_LEVEL)
newSetting[2][1] = str(getInput('Threshold level', (1, 255)))

print('\n4) Motion Dilation Factor\n   (High value means slower operation)\n   Default value =  3\n   Range=  [1 - 22]'
      '\n   Current value: %f' %MOTION_DILATION_FACTOR)
newSetting[3][1] = str(getInput('Motion Dilation Factor', (1, 23)))

print('\n5) Minimum Detection area\n   (High value means lesser senstivity)\n   Default value  = 500\n   Range  = [100 - 10000]'
      '\n   Current value: %f' %MIN_DETECTION_AREA )
newSetting[4][1] = str(getInput('Minimum Detection area', (100, 10001)))

print('\n6) Detection Dilation Factor\n   (High value means slower operation, higher accuracy)'
      '\n   Default value 22\n   Range [3 - 50]\n   Current value: %f' %DETECTION_DILATION_FACTOR)
newSetting[5][1] = str(getInput('Detection Dilation factor', (3, 51)))

print('\n7) Minimum Aspect Ratio\n   (High value means less error)\n   Default value =  0.6\n   Range =  [0.1 - 10]'
      '\n   Current value: %f' %MIN_ASPECT_RATIO)
newSetting[6][1] = str(getInput('Minimum Aspect Ratio', (0.1, 11)))

print('\n8) Max Correlation Cofficient\n   (High value means more false positives)\n   Default value = 0.8'
      '\n   Range  = [0.1 - 0.99]\n   Current value: %f' %MAX_CORR_COFF)
newSetting[7][1] = str(getInput('Max Correlation Cofficient', (0.1, 1.0)))

debug = raw_input('\n->Do you want to enable debugging messages y/n?')
if debug == 'Y' or debug == 'y':
    newSetting[8][1] = 'True'
else:
    newSetting[8][1] = 'False'

video = raw_input('\n->Do you want to enable video outputs y/n?')
if video == 'Y' or video == 'y':
    newSetting[9][1] = 'True'
else:
    newSetting[9][1] = 'False'

# Now save the settings
saveSettings(newSetting, bakData)

print('\nSettings saved, please restart the system to load new settings.')
choice = raw_input('Do you want to restart now y/n?')
if choice == 'Y' or choice == 'y':
    os.system('halt --reboot')
else:
    exit()