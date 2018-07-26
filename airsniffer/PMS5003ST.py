# PMS5003ST.py - Python driver for PMS5003ST module
#
# Copyright (C) 2018 by Weidong Zhou <bruce.zhou2002@gmail.com>
#
# This software may be distributed under the terms of the GNU General
# Public License ("GPL") version 2 as published by the Free Software
# Foundation.

import threading, logging, time, copy
import serial
import innostickGPIO

# set log level here for debug purpose
logger = logging.getLogger("PMS5003ST")
logger.setLevel(logging.INFO)

logger.info("Module PMS5003ST Imported!")

# of course we need some "static" variables to "record" sensor status
sensorState = 0
currentUart = 0
currentResetPin = ''
currentSetPin = ''

currentPMData = []
currentHCHOData = 0
currentTEMPData = 0
currentHUMIData = 0

def pmData():
    if currentPMData:
        return {'pm1Data':currentPMData[0], 'pm25Data':currentPMData[1], 'pm10Data':currentPMData[2]}
    else :
        return {}

def hchoData():
    return {'hchoData':currentHCHOData}

def tempData():
    return {'tempData':currentTEMPData}

def humiData():
    return {'humiData':currentHUMIData}

def sensorInit(tempDict):
    global sensorState, currentUart, currentResetPin, currentSetPin

    if tempDict:

        # check if thread alread up
        if sensorState == 1:

            # check if duplicated copy already running
            if tempDict['SensorName'] == sensorInfo['SensorName'] and tempDict['Uart#'] == currentUart and tempDict['ResetPin#'] == currentResetPin and tempDict['SetPin#'] == currentSetPin :

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
    currentResetPin = tempDict['ResetPin#']
    currentSetPin = tempDict['SetPin#']

    mthread = threading.Thread(target = pmThread, name = sensorInfo['SensorName'], args=(currentUart, currentResetPin, currentSetPin)) 
    mthread.start()     

sensorInfo = {'SensorName':'PMS5003ST', 'Description':'Laser pm2.5 + formaldehyde + temperature + humidity 4in1 PMS5003ST sensor'}
resetPins = {'ResetPin#':innostickGPIO.pinMap.keys()}
setPins = {'SetPin#':innostickGPIO.pinMap.keys()}
uart = {'Uart#':[1,2,4,6,7,8]}
revInfo = {'Rev.':"v1.0"}

# function reference for sensor manager module 
# currently we use this dict list to register functions to manager layer
# not know what else feasible to do same thing.
sensorFuncs = {'pmData':pmData, 'hchoData':hchoData, 'tempData':tempData, 'humiData':humiData, 'sensorInit':sensorInit}

# this return info string could be used by sensor manager layer
def info():
    return dict(sensorInfo.items() + resetPins.items() + setPins.items() + uart.items() + revInfo.items() + sensorFuncs.items())




def pmThread(uart, reset, _set):
    global sensorState
    
    logger.info("Thread " + threading.current_thread().name + " Start!")

    # output reset logic to the sensor
    innostickGPIO.setup(_set, innostickGPIO.OUT)
    innostickGPIO.setup(reset, innostickGPIO.OUT)

    innostickGPIO.output(_set, innostickGPIO.HIGH) 
    innostickGPIO.output(reset, innostickGPIO.LOW) 

    time.sleep(1)

    innostickGPIO.output(reset, innostickGPIO.HIGH) 

    try :

        # open serial port to receive data
        ser = serial.Serial("/dev/ttymxc" + str(uart-1), baudrate = 9600)    

    except :
        logger.info("No connection to the device could be established")
        print e
        sensorState = 0
        innostickGPIO.cleanup()
        return
    
    while sensorState == 1:
    	
        # wait enough time to ensure at least one valid frame data arrived
        time.sleep(1)
        
        # poll inWaiting byte number
        count = ser.inWaiting()

        # frame length = 2 + 2 + 2x13 + 2
        # the shortest frame length is 32, as per PMS5003 user manual
        # so we will drop off if partial data
        if count >= 32 :
            getData(ser.read(count))
            
        ser.flushInput()     

    logger.info("Thread " + threading.current_thread().name + " exit!")

    ser.close()

    # ?? we need recover innostick6GPIO
    innostickGPIO.cleanup()
       
# retrive valid content inside packet
def getData(recv) :

    global currentPMData, currentHCHOData, currentTEMPData, currentHUMIData
    
    recv_bytes_arr = bytearray(recv)      #

    logger.debug("bytes length: " + str(len(recv_bytes_arr)) + ''.join(format(x, '02x') for x in recv_bytes_arr))

    byte_flag_1 = False
    byte_flag_2 = False
    byte_flag_3 = False

    for i, byte in enumerate(recv_bytes_arr):

        """
        """

        if byte_flag_1 is False:

            # 
            # 
            if hex(byte) == '0x42':    # 
                byte_flag_1 = True
                continue
            else:
                continue

        if byte_flag_2 is False:        #

            if hex(byte) == '0x4d':
                byte_flag_2 = True
                continue
            else:
                byte_flag_1 = False     # 
                continue

        if byte_flag_3 is False:         # 

            if hex(byte) == '0x0':
                byte_flag_3 = True
                continue
            else:
                byte_flag_1 = False     # 
                byte_flag_2 = False     # 
                continue

        if byte_flag_3 is True:         #  

            # in case of PMS5003 with PM data only
            # frame length = 2 + 2 + 2x13 + 2
            # assume a valid packet arrived, we will continue to check content of current packet
            if  byte == 28:
                if len(recv_bytes_arr) >= i+29:

                    check_code = recv_bytes_arr[i+27]*256 + recv_bytes_arr[i+28] 
                    bytes_sum = sum(k for k in recv_bytes_arr[i-3:i+27])     #

                    if check_code == bytes_sum:

                        currentPMData = []
                        currentPMData.append(recv_bytes_arr[i+7]*256 + recv_bytes_arr[i+8])
                        currentPMData.append(recv_bytes_arr[i+9]*256 + recv_bytes_arr[i+10])
                        currentPMData.append(recv_bytes_arr[i+11]*256 + recv_bytes_arr[i+12])

                        logger.debug("Valid data in coming! len= %d", byte)

                    else :
                        logger.debug("Checksum error detected!")
                else :
                    logger.debug("not enough data in packet!")
                	
                # return nevertheless valid content updated or not
                break


            # in case of PMS5003ST with PM data + formaldehyde + temperature + humidity
            # frame length = 2 + 2 + 2x17 + 2
            # assume a valid packet arrived, we will continue to check content of current packet
            elif byte == 36:
                if len(recv_bytes_arr) >= i+37:

                    check_code = recv_bytes_arr[i+35]*256 + recv_bytes_arr[i+36] 
                    bytes_sum = sum(k for k in recv_bytes_arr[i-3:i+35])     #

                    if check_code == bytes_sum:

                        currentPMData = []
                        currentPMData.append(recv_bytes_arr[i+7]*256 + recv_bytes_arr[i+8])
                        currentPMData.append(recv_bytes_arr[i+9]*256 + recv_bytes_arr[i+10])
                        currentPMData.append(recv_bytes_arr[i+11]*256 + recv_bytes_arr[i+12])

                        currentHCHOData =  recv_bytes_arr[i+25]*256 + recv_bytes_arr[i+26]
                        currentTEMPData =  recv_bytes_arr[i+27]*256 + recv_bytes_arr[i+28]
                        currentHUMIData =  recv_bytes_arr[i+29]*256 + recv_bytes_arr[i+30]

                        logger.debug("Valid data in coming! currentHCHOData=%d, currentTEMPData=%d, currentHUMIData=%d, currentPMData[0]=%d, currentPMData[1]=%d, currentPMData[2]=%d", currentHCHOData, currentTEMPData, currentHUMIData, currentPMData[0], currentPMData[1], currentPMData[2])

                    else :
                        logger.debug("Checksum error detected!")
                else :
                    logger.debug("not enough data in packet!")
                        
                # return nevertheless valid content updated or not
                break

            # continue in all other cases
            byte_flag_1 = False     # 
            byte_flag_2 = False     # 
            byte_flag_3 = False     # 
            continue               
            	

