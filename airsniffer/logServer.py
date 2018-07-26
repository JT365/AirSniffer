# logServer.py - Python extension for airSniffer sensor manager
#
# Copyright (C) 2018 by Weidong Zhou <bruce.zhou2002@gmail.com>
#
# This software may be distributed under the terms of the GNU General
# Public License ("GPL") version 2 as published by the Free Software
# Foundation.
import threading, time, sqlite3, json, math

# set log level here for debug purpose


db="/usr/local/share/winfolder/airsniffer/airsniffer.db"

#
# There are several tables in db
# 1. DBParameter
#    General setting for logServer
# 2. SensorParameter
#    Parameters for various sensors supported by sensorManager
# 3. History
#    Historical data from sensor manager
#
defPMParameter = {'SensorName':'PMS5003ST' , 'Uart#':4 , 'ResetPin#':'GPIO2_IO00' , 'SetPin#':'GPIO2_IO01'}
defHCHOParameter = {'SensorName':'PMS5003ST' , 'Uart#':4 , 'ResetPin#':'GPIO2_IO00' , 'SetPin#':'GPIO2_IO01'}
defTEMPParameter = {'SensorName':'PMS5003ST' , 'Uart#':4 , 'ResetPin#':'GPIO2_IO00' , 'SetPin#':'GPIO2_IO01'}
defHUMIParameter = {'SensorName':'PMS5003ST' , 'Uart#':4 , 'ResetPin#':'GPIO2_IO00' , 'SetPin#':'GPIO2_IO01'}
defCO2Parameter = {'SensorName':'S8_0053' , 'Uart#':2 }
defDBParameter = {'Interval':1}

lock =threading.Lock()
conn = sqlite3.connect(db, check_same_thread = False)


def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value) for idx, value in enumerate(row))



conn.row_factory = sqlite3.Row
cursor = conn.cursor()    
conn.execute('create table if not exists DBParameter (Interval integer)')
conn.execute('create table if not exists SensorParameter (CO2Parameter text, HCHOParameter text, PMParameter text, TEMPParameter text, HUMIParameter text)')
conn.execute('create table if not exists History (id integer PRIMARY KEY AUTOINCREMENT, timestamp integer, pm1Data integer, pm25Data integer, pm10Data integer, hchoData integer, co2Data integer, tempData integer, humiData integer)')

conn.commit()

conn_read = sqlite3.connect(db, check_same_thread = False)
conn_read.row_factory = sqlite3.Row
cursor_read = conn_read.cursor()    

def getDBInterval():
    with lock:
        cursor.execute('select Interval from DBParameter where Interval is not null')
        result = cursor.fetchone()
    if not result :
        return defDBParameter['Interval']
    else :
        return result['Interval']

# todo - we need a more flexible method to write db through input para
def setDBInterval(para):
    with lock:
        cursor.execute('select * from DBParameter')
        result = cursor.fetchone()
        if not result :
            cursor.execute('insert into DBParameter (Interval) values (?)', para)
        else :
            cursor.execute('update DBParameter set Interval = ?', para)
        conn.commit()
    
def getDBCO2Cfg():
    with lock:
        cursor.execute('select CO2Parameter from SensorParameter where CO2Parameter is not null')
        result = cursor.fetchone()
 
    if not result :
        return defCO2Parameter
    else :
        return json.loads(result['CO2Parameter'])

# todo - we need a more flexible method to write db through input para
def setDBCO2Cfg(para):
    with lock:
        cursor.execute('select * from SensorParameter')
        result = cursor.fetchone()
        if not result :
            cursor.execute('insert into SensorParameter (CO2Parameter) values (?)', (json.dumps(para),))
        else :
            cursor.execute('update SensorParameter set CO2Parameter = ?', (json.dumps(para),))
        conn.commit()    

def getDBPMCfg():
    with lock:
        cursor.execute('select PMParameter from SensorParameter where PMParameter is not null')
        result = cursor.fetchone()
    if not result :
        return defPMParameter
    else :
        return json.loads(result['PMParameter'])

# todo - we need a more flexible method to write db through input para
def setDBPMCfg(para):
    with lock:
        cursor.execute('select * from SensorParameter')
        result = cursor.fetchone()
        if not result :
            cursor.execute('insert into SensorParameter (PMParameter) values (?)', (json.dumps(para),))
        else :
            cursor.execute('update SensorParameter set PMParameter = ?', (json.dumps(para),))
        conn.commit()    

def getDBHCHOCfg():
    with lock:
        cursor.execute('select HCHOParameter from SensorParameter where HCHOParameter is not null')
        result = cursor.fetchone()
    if not result :
        return defHCHOParameter
    else :
        return json.loads(result['HCHOParameter'])

# todo - we need a more flexible method to write db through input para
def setDBHCHOCfg(para):
    with lock:
        cursor.execute('select * from SensorParameter')
        result = cursor.fetchone()
        if not result :
            cursor.execute('insert into SensorParameter (HCHOParameter) values (?)', (json.dumps(para),))
        else :
            cursor.execute('update SensorParameter set HCHOParameter = ?', (json.dumps(para),))
        conn.commit()    
    
    
def getDBTEMPCfg():
    with lock:
        cursor.execute('select TEMPParameter from SensorParameter where TEMPParameter is not null')
        result = cursor.fetchone()
    if not result :
        return defTEMPParameter
    else :
        return json.loads(result['TEMPParameter'])

# todo - we need a more flexible method to write db through input para
def setDBTEMPCfg(para):
    with lock:
        cursor.execute('select * from SensorParameter')
        result = cursor.fetchone()
        if not result :
            cursor.execute('insert into SensorParameter (TEMPParameter) values (?)', (json.dumps(para),))
        else :
            cursor.execute('update SensorParameter set TEMPParameter = ?', (json.dumps(para),))
        conn.commit()    
    

def getDBHUMICfg():
    with lock:
        cursor.execute('select HUMIParameter from SensorParameter where HUMIParameter is not null')
        result = cursor.fetchone()
    if not result :
        return defHUMIParameter
    else :
        return json.loads(result['HUMIParameter'])

# todo - we need a more flexible method to write db through input para
def setDBHUMICfg(para):
    with lock:
        cursor.execute('select * from SensorParameter')
        result = cursor.fetchone()
        if not result :
            cursor.execute('insert into SensorParameter (HUMIParameter) values (?)', (json.dumps(para),))
        else :
            cursor.execute('update SensorParameter set HUMIParameter = ?', (json.dumps(para),))
        conn.commit()    
    
    
def getHistory() :
    with lock:
        # check how many records in the table
        # we need reduce data items due to performance restrict

        cursor_read.execute('select * from History ')
        data = cursor_read.fetchall()
    if len(data) > 500 :
        gap = len(data)/500 + 1
    else :
        gap = 1
    
    timestamp = [x['timestamp'] for x in data[::gap]]
    pm1Data = [x['pm1Data'] for x in data[::gap]]
    pm25Data = [x['pm25Data'] for x in data[::gap]]
    pm10Data = [x['pm10Data'] for x in data[::gap]]
    hchoData = [x['hchoData'] for x in data[::gap]]
    co2Data = [x['co2Data'] for x in data[::gap]]
    tempData = [x['tempData'] for x in data[::gap]]
    humiData = [x['humiData'] for x in data[::gap]]

    return (timestamp, pm1Data, pm25Data, pm10Data, hchoData, co2Data, tempData, humiData)
    
def setHistory(para) :

    # save record into db in formal convention
    # we dont want a partial record in DB, so we add some dummy data for value non-exist
    if 'pm1Data' in para :
    	  pm1Data = para['pm1Data']
    else :
        pm1Data = 0

    if 'pm25Data' in para :
    	  pm25Data = para['pm25Data']
    else :
        pm25Data = 0

    if 'pm10Data' in para :
    	  pm10Data = para['pm10Data']
    else :
        pm10Data = 0

    if 'hchoData' in para :
    	  hchoData = round(para['hchoData']/1000.0)
    else :
        hchoData = 0

    if 'co2Data' in para :
    	  co2Data = para['co2Data']
    else :
        co2Data = 0

    if 'tempData' in para :
    	  tempData = round(para['tempData']/10.0)
    else :
        tempData = 0

    if 'humiData' in para :
    	  humiData = round(para['humiData']/10.0)
    else :
        humiData = 0

    with lock:        
        cursor.execute('insert into History (timestamp, pm1Data, pm25Data, pm10Data, hchoData, co2Data, tempData, humiData) values (?, ?, ?, ?, ?, ?, ?, ?)', (int(round(time.time()*1000)), pm1Data, pm25Data, pm10Data, hchoData, co2Data, tempData, humiData)) 
        conn.commit()   