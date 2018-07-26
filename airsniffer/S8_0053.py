# S8-0053.py - Python driver for SenseAir S8 Residential Miniature infrared CO2 module
#
# Copyright (C) 2018 by Weidong Zhou <bruce.zhou2002@gmail.com>
#
# This software may be distributed under the terms of the GNU General
# Public License ("GPL") version 2 as published by the Free Software
# Foundation.

import threading, logging, time, copy
import serial

# set log level here for debug purpose
logger = logging.getLogger("S8_0053")
logger.setLevel(logging.INFO)

logger.info("Module S8_0053 Imported!")

# of course we need some "static" variables to "record" sensor status
sensorState = 0
currentUart = 0

currentCO2Data = 0


def co2Data():
    return {'co2Data':currentCO2Data}

def sensorInit(tempDict):
    global sensorState, currentUart

    if tempDict:

        # check if thread alread up
        if sensorState == 1:

            # check if duplicated copy already running
            if tempDict['SensorName'] == sensorInfo['SensorName'] and tempDict['Uart#'] == currentUart :

                # do nothing since sensor already settled down
                logger.info("Sensor: "+ tempDict['SensorName'] +" already up!")
                return
            else:
                sensorState = 0

                # wait a little bit til previous thread quit
                time.sleep(1)

    else :

        # force sensorState to 0 
        sensorState = 0
        logger.info("sensorInit called with empty parameters")
 
        return 
        
    # continue initialization
    sensorState = 1
    currentUart = tempDict['Uart#']

    mthread = threading.Thread(target = pmThread, name = sensorInfo['SensorName'], args=(currentUart,)) 
    mthread.start()     

sensorInfo = {'SensorName':'S8_0053', 'Description':'SenseAir S8 Residential Miniature Infrared CO2 Sensor'}
uart = {'Uart#':[1,2,4,6,7,8]}
revInfo = {'Rev.':"v1.0"}

# function reference for sensor manager module 
# currently we use this dict list to register functions to manager layer
# not know what else feasible to do same thing.
sensorFuncs = { 'co2Data':co2Data, 'sensorInit':sensorInit}

# this return info string could be used by sensor manager layer
def info():
    return dict(sensorInfo.items() + uart.items() + revInfo.items() + sensorFuncs.items())




def pmThread(uart):
    global sensorState
    
    logger.info("Thread " + threading.current_thread().name + " Start!")

    try :

        # open serial port to receive data
        ser = serial.Serial("/dev/ttymxc" + str(uart-1), baudrate = 9600)    

    except :
        logger.info("No connection to the device could be established")
        print e
        sensorState = 0
        return
    
    while sensorState == 1:
    	
        # wait enough time to ensure at least one valid frame data arrived
        ser.write('\xFE\x04\x00\x03\x00\x01\xD5\xC5')

        # frame length = 1 + 1 + 1 + 2 + 2
        # the shortest frame length is 7, as per S8-0053 user manual
        # so we will drop off if partial data
        getData(ser.read(7))            
        ser.flushInput()     

    logger.info("Thread " + threading.current_thread().name + " exit!")

    ser.close()

       
# retrive valid content inside packet
def getData(recv) :

    global  currentCO2Data
    
    recv_bytes_arr = bytearray(recv)      #

    logger.debug("bytes length: " + str(len(recv_bytes_arr)) + ''.join(format(x, '02x') for x in recv_bytes_arr))

    byte_flag_1 = False
    byte_flag_2 = False

    for i, byte in enumerate(recv_bytes_arr):

        """
        """

        if byte_flag_1 is False:

            # 
            # 
            if hex(byte) == '0xfe':    # 
                byte_flag_1 = True
                continue
            else:
                continue

        if byte_flag_2 is False:        #

            if hex(byte) == '0x4':
                byte_flag_2 = True
                continue
            else:
                byte_flag_1 = False     # 
                continue

        if byte_flag_2 is True:         #  

            # frame length = 1 + 1 + 1 + 2 + 2
            # assume a valid packet arrived, we will continue to check content of current packet
            if  byte == 2:

                currentCO2Data = recv_bytes_arr[i+1]*256 + recv_bytes_arr[i+2]
                logger.debug("Valid data in coming! %d", currentCO2Data)
                	
                # return nevertheless valid content updated or not
                break

            # continue in all other cases
            byte_flag_1 = False     # 
            byte_flag_2 = False     # 
            continue               
            	

