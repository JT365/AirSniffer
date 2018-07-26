# innostickGPIO.py - Python driver for innostick 6 GPIO module
#
# Copyright (C) 2018 by Weidong Zhou <bruce.zhou2002@gmail.com>
#
# This software may be distributed under the terms of the GNU General
# Public License ("GPL") version 2 as published by the Free Software
# Foundation.
import logging
import gpio

# set log level here for debug purpose
logger = logging.getLogger("innostckGPIO")
logger.setLevel(logging.INFO)

logger.info("Module innostckGPIO Imported!")

IN, OUT = 'in', 'out'
LOW, HIGH = 'low', 'high'

pinMap = {'GPIO1_IO00':0, 'GPIO1_IO01':1, 'GPIO1_IO02':2, 'GPIO1_IO03':3, 'GPIO1_IO04':4, 'GPIO1_IO05':5, 'GPIO1_IO06':6, 'GPIO1_IO07':7, \
    'GPIO1_IO08':8, 'GPIO1_IO09':9, 'GPIO1_IO10':10, 'GPIO1_IO11':11, 'GPIO1_IO12':12, 'GPIO1_IO13':13, 'GPIO1_IO14':14, 'GPIO1_IO15':15, \
    'GPIO1_IO16':16, 'GPIO1_IO17':17, 'GPIO1_IO18':18, 'GPIO1_IO19':19, 'GPIO1_IO20':20, 'GPIO1_IO21':21, 'GPIO1_IO22':22, 'GPIO1_IO23':23, \
    'GPIO1_IO24':24, 'GPIO1_IO25':25, 'GPIO1_IO26':26, 'GPIO1_IO27':27, 'GPIO1_IO28':28, 'GPIO1_IO29':29, \
    'GPIO2_IO00':32, 'GPIO2_IO01':33, 'GPIO2_IO02':34, 'GPIO2_IO03':35, 'GPIO2_IO04':36, 'GPIO2_IO05':37, 'GPIO2_IO06':38, 'GPIO2_IO07':39, \
    'GPIO2_IO08':40, 'GPIO2_IO09':41, 'GPIO2_IO10':42, 'GPIO2_IO11':43, 'GPIO2_IO12':44, 'GPIO2_IO13':45, 'GPIO2_IO14':46, 'GPIO2_IO15':47, \
    'GPIO4_IO11':107, 'GPIO4_IO12':108, 'GPIO4_IO13':109, 'GPIO4_IO14':110, 'GPIO4_IO15':111, 'GPIO4_IO16':112 }

def setup(pin, mode):
    if pin in pinMap :
        gpio.setup(pinMap[pin], mode)        
    else :
        logger.info("pinname " + pin + "is not supported!")
    
def output(pin, value):
    if pin in pinMap :
        gpio.output(pinMap[pin], value)        
    else :
        logger.info("pinname " + pin + "is not supported!")
    
def input(pin):
    if pin in pinMap :
        return gpio.input(pinMap[pin])        
    else :
        logger.info("pinname " + pin + "is not supported!")
    
def mode(pin):
    if pin in pinMap :
        return gpio.mode(pinMap[pin])        
    else :
        logger.info("pinname " + pin + "is not supported!")

def cleanup(pin, assert_exists):
    if pin in pinMap :
        return gpio.cleanup(pinMap[pin], assert_exists)        
    else :
        logger.info("pinname " + pin + "is not supported!")


