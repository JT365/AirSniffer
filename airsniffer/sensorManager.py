# sensorManager.py - Python extension for airSniffer sensor manager
#
# Copyright (C) 2018 by Weidong Zhou <bruce.zhou2002@gmail.com>
#
# This software may be distributed under the terms of the GNU General
# Public License ("GPL") version 2 as published by the Free Software
# Foundation.
import threading, logging, time, json
import logServer, PMS5003ST, S8_0053

# set log level here for debug purpose
logger = logging.getLogger("sensorManager")
logger.setLevel(logging.INFO)

logger.info("Module sensorManager Imported!")

sensors = []

# separate individual sensors per different sensor type
pmSensors = []
co2Sensors = []
hchoSensors = []
tempSensors = []
humiSensors = []

def pmListInit():
    for i in sensors:
        if 'pmData' in i:
            pmSensors.append(i)

def co2ListInit():
    for i in sensors:
        if 'co2Data' in i:
            co2Sensors.append(i)

def hchoListInit():
    for i in sensors:
        if 'hchoData' in i:
            hchoSensors.append(i)

def tempListInit():
    for i in sensors:
        if 'tempData' in i:
            tempSensors.append(i)

def humiListInit():
    for i in sensors:
        if 'humiData' in i:
            humiSensors.append(i)

def emptyData():
    logger.info("stub function should not get called")
    return
    
currentCO2Sensor = {}
currentHCHOSensor = {}
currentPMSensor = {}
currentTEMPSensor = {}
currentHUMISensor = {}
currentCO2Data=currentHCHOData=currentPMData=currentTEMPData=currentHUMIData=emptyData

# gather all supported sensor info into sensors list
sensors.append(PMS5003ST.info())
sensors.append(S8_0053.info())
           
pmListInit()
co2ListInit()
hchoListInit()
tempListInit()
humiListInit()

# tempDict is a dict string which could be jsonized in between airsniffer front end and sqlite DB
# so this is a generic interface between front end and back end
def pmSensorInit(tempDict):
    global currentPMSensor, currentPMData

    if 'SensorName' in tempDict :

        # we do not want a new init when current setting identical with the previous one
        # 2 sceneries should be take into account: different sensors and same sensor with different configuration
        if cmp(tempDict, currentPMSensor) != 0 :

            # find out the sensor name in support list
            for i in pmSensors:
            	  if i['SensorName'] == tempDict['SensorName']:

                    # we need stop first sensor thread if new sensor configured
                    if 'SensorName' in currentPMSensor :
                        if currentPMSensor['SensorName'] != tempDict['SensorName'] :
  
                            currentPMSensor['sensorInit']('')
                            time.sleep(1)

                    # callback registed in dict 'sensorInit'
                    i['sensorInit'](tempDict)
  
                    currentPMSensor = tempDict
                    currentPMData = i['pmData']

                    # put a record in DB
                    logServer.setDBPMCfg(currentPMSensor)
                    logger.info("Current PM Sensor set to: " + currentPMSensor['SensorName'])

                    break
                    
# tempDict is a dict string which could be jsonized in between airsniffer front end and sqlite DB
# so this is a generic interface bwteen front end and back end
def co2SensorInit(tempDict):
    global currentCO2Sensor, currentCO2Data

    if 'SensorName' in tempDict :

        # we do not want a new init when current setting identical with the previous one
        # 2 sceneries should be take into account: different sensors and same sensor with different configuration
        if cmp(tempDict, currentCO2Sensor) != 0 :

            # find out the sensor name in support list
            for i in co2Sensors:
            	  if i['SensorName'] == tempDict['SensorName']:

                    # we need stop first sensor thread if new sensor configed
                    if 'SensorName' in currentCO2Sensor :
                        if currentCO2Sensor['SensorName'] != tempDict['SensorName'] :
                            currentCO2Sensor['sensorInit']('')
                            time.sleep(1)

                    # callback registed in dict 'sensorInit'
                    i['sensorInit'](tempDict)
  
                    currentCO2Sensor = tempDict
                    currentCO2Data = i['co2Data']

                    logServer.setDBCO2Cfg(currentCO2Sensor)
                    logger.info("Current CO2 Sensor set to: " + currentCO2Sensor['SensorName'])

                    break

# tempDict is a dict string which could be jsonized in between airsniffer front end and sqlite DB
# so this is a generic interface bwteen front end and back end
def hchoSensorInit(tempDict):
    global currentHCHOSensor, currentHCHOData

    if 'SensorName' in tempDict :

        # we do not want a new init when current setting identical with the previous one
        # 2 sceneries should be take into account: different sensors and same sensor with different configuration
        if cmp(tempDict, currentHCHOSensor) != 0 :

            # find out the sensor name in support list
            for i in hchoSensors:
            	  if i['SensorName'] == tempDict['SensorName']:

                    # we need stop first sensor thread if new sensor configed
                    if 'SensorName' in currentHCHOSensor :
                        if currentHCHOSensor['SensorName'] != tempDict['SensorName'] :
                            currentHCHOSensor['sensorInit']('')
                            time.sleep(1)

                    # callback registed in dict 'sensorInit'
                    i['sensorInit'](tempDict)
  
                    currentHCHOSensor = tempDict
                    currentHCHOData = i['hchoData']

                    logServer.setDBHCHOCfg(currentHCHOSensor)
                    logger.info("Current HCHO Sensor set to: " + currentHCHOSensor['SensorName'])

                    break

# tempDict is a dict string which could be jsonized in between airsniffer front end and sqlite DB
# so this is a generic interface bwteen front end and back end
def tempSensorInit(tempDict):
    global currentTEMPSensor, currentTEMPData

    if 'SensorName' in tempDict :

        # we do not want a new init when current setting identical with the previous one
        # 2 sceneries should be take into account: different sensors and same sensor with different configuration
        if cmp(tempDict, currentTEMPSensor) != 0 :

            # find out the sensor name in support list
            for i in tempSensors:
            	  if i['SensorName'] == tempDict['SensorName']:

                    # we need stop first sensor thread if new sensor configed
                    if 'SensorName' in currentTEMPSensor :
                        if currentTEMPSensor['SensorName'] != tempDict['SensorName'] :
                            currentTEMPSensor['sensorInit']('')
                            time.sleep(1)

                    # callback registed in dict 'sensorInit'
                    i['sensorInit'](tempDict)
  
                    currentTEMPSensor = tempDict
                    currentTEMPData = i['tempData']

                    logServer.setDBTEMPCfg(currentTEMPSensor)
                    logger.info("Current TEMP Sensor set to: " + currentTEMPSensor['SensorName'])

                    break

# tempDict is a dict string which could be jsonized in between airsniffer front end and sqlite DB
# so this is a generic interface bwteen front end and back end
def humiSensorInit(tempDict):
    global currentHUMISensor, currentHUMIData

    if 'SensorName' in tempDict :

        # we do not want a new init when current setting identical with the previous one
        # 2 sceneries should be take into account: different sensors and same sensor with different configuration
        if cmp(tempDict, currentHUMISensor) != 0 :

            # find out the sensor name in support list
            for i in humiSensors:
            	  if i['SensorName'] == tempDict['SensorName']:

                    # we need stop first sensor thread if new sensor configed
                    if 'SensorName' in currentHUMISensor :
                        if currentHUMISensor['SensorName'] != tempDict['SensorName'] :
                            currentHUMISensor['sensorInit']('')
                            time.sleep(1)

                    # callback registed in dict 'sensorInit'
                    i['sensorInit'](tempDict)
  
                    currentHUMISensor = tempDict
                    currentHUMIData = i['humiData']

                    logServer.setDBHUMICfg(currentHUMISensor)
                    logger.info("Current HUMI Sensor set to: " + currentHUMISensor['SensorName'])

                    break


                    
# return dict list currentCO2Sensor for front panel configuration purpose
def co2SensorStatus():
    return currentCO2Sensor    

def pmSensorStatus():
    return currentPMSensor    

def hchoSensorStatus():
    return currentHCHOSensor    

def tempSensorStatus():
    return currentTEMPSensor    

def humiSensorStatus():
    return currentHUMISensor    
        
# return final results of all current sensor data
# data returned wll be jsonized and sent to airsniffer front end
def _getAirQuality():
    results={}

    if currentCO2Sensor: 
        results.update(currentCO2Data())
    if currentHCHOSensor: 
        results.update(currentHCHOData())
    if currentPMSensor: 
        results.update(currentPMData())
    if currentTEMPSensor: 
        results.update(currentTEMPData())
    if currentHUMISensor: 
        results.update(currentHUMIData())
 
    return results

def getAirQuality() :
    return json.dumps(_getAirQuality())
    
def getHistory() :
    return json.dumps(logServer.getHistory())
        
# get current sensor setting from DB
# and start them for front end data query
co2SensorInit(logServer.getDBCO2Cfg())
hchoSensorInit(logServer.getDBHCHOCfg())
pmSensorInit(logServer.getDBPMCfg())
tempSensorInit(logServer.getDBTEMPCfg())
humiSensorInit(logServer.getDBHUMICfg()) 

def dbThread(interval):
    global dbState
    
    time.sleep(3)
    logger.info("Thread " + threading.current_thread().name + " Start!")
    
    dbState = 1
    while dbState == 1:
    	
        # set interval here for db recording
        time.sleep(interval)
        
        logServer.setHistory(_getAirQuality())  

    logger.info("Thread " + threading.current_thread().name + " exit!")

mthread = threading.Thread(target = dbThread, name = 'AirsnifferLogger', args=(logServer.getDBInterval(),)) 
mthread.start()     