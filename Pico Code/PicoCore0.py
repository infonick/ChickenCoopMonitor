# ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡
#
#    Raspberry Pi Pico Core 0 Driver
#
# ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡
#
# This driver program managees the Pi Pico's AI functionality. The following
# functions are undertaken:
#   - AI sensors and actuators are instantiated
#   - AI agents and their environments are instantiated
#   - The main program loop periodically runs the agents.
#
# The driver is run by calling the 'PicoCore0()' function.
# 
# ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡
# REVISION HISTORY:
#   - 
#
# ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡

from usys import path
if '/RP2040-Pico-RTC' not in path:
    path.append('/RP2040-Pico-RTC')
if '/PicoDHT22' not in path:
    path.append('/PicoDHT22')

from micropython import alloc_emergency_exception_buf
alloc_emergency_exception_buf(100)

import gc
if not gc.isenabled():
    gc.enable()

import utime
from machine import WDT

import AiLib
import GPIOConfig
import AgentPrograms
from RP2040_RTC import rp2RTC

agentRuntimeFrequencyInSeconds = 5


# Load sensor dictionary
sensorDict = {}
for sensor in GPIOConfig.sensors:
    if sensor['name'] in list(sensorDict.keys()):
        raise ValueError("Two of the items in list \'sensors\' have " +
                         "the same name. All sensors are required to " + 
                         "have unique names.")
    
    s = AiLib.Sensor(sensor['pinNum'],
                     sensor['pinMode'],
                     name = sensor['name'],
                     gpioInType = sensor['gpioInType'],
                     irq = sensor['irq'],
                     driver = sensor['driver'],
                     convFactorADC = sensor['convFactorADC']
                     )
    sensorDict[s.getName()] = s


# Load actuator dictionary
actuatorDict = {}
for actuator in GPIOConfig.actuators:
    if actuator['name'] in list(actuatorDict.keys()):
        raise ValueError("Two of the items in list \'actuators\' have " +
                         "the same name. All actuators are required to " + 
                         "have unique names.")
    
    a = AiLib.Actuator(actuator['pinNum'],
                       name = actuator['name'],
                       gpioOutInitValue = actuator['gpioOutInitValue'],
                       reverseStates = actuator['reverseStates']
                       )
    actuatorDict[a.getName()] = a


# Load agents and their environments
agentEnvironments = {}
agentEnvironments['Heat Agent'] = AgentPrograms.setupHeatAgent(sensorDict, actuatorDict)



# ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡
# Main program loop
# ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡

def PicoCore0():
    global sensorDict
    global actuatorDict
    global agentEnvironments
    
    aiWatchdog = WDT(0, (5 * agentRuntimeFrequencyInSeconds * 1000))
    
    try:
        while True:
            aiWatchdog.feed()
            gc.collect()
            startTime = utime.ticks_ms()
            
            for agent in agentEnvironments.keys():
                agentEnvironments[agent].run()
            
            stopTime = utime.ticks_ms()
            runTime = abs(utime.ticks_diff(stopTime, startTime))
            if runTime < (agentRuntimeFrequencyInSeconds*1000):
                sleeptime = (agentRuntimeFrequencyInSeconds*1000) - runTime
                utime.sleep_ms(sleeptime)

    except Exception as e:
        file = open("ErrorLogCore0.txt", "a")
        file.write(str(e) + "\n\n")
        file.flush()
        file.close()
        raise

    finally:
        from time import sleep
        from machine import Pin
        from machine import PWM

        # An LED frequency of 637hz is well above what chickens can percieve
        # and so will not appear as a flickering light to them.
        led = PWM(Pin(25))
        led.freq(637)
        while True:
            led.duty_u16(2**15)
            sleep(1)
            led.duty_u16(2**13)
            sleep(1)
            
