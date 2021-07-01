# ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡
#
#    Raspberry Pi Pico AI Library - Agent and Environment Class Tests
#
# ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡
#
# 
#
# ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡

import unittest
from usys import path
path.append('/RP2040-Pico-RTC')
path.append('/PicoDHT22')

from micropython import alloc_emergency_exception_buf
alloc_emergency_exception_buf(100)

import AiLib
from RP2040_RTC import rp2RTC

import GPIOConfig

sensorDict = {}
actuatorDict = {}

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




class Test_GPIOConfig(unittest.TestCase):

    yesAnswers = ['y', 'yes']
    actuatorStates = ['off','on']
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass

    def test_GPIOConfig_Sensors(self):      
        for s in sensorDict:
            print("SENSOR {}:\n------------------------------------".format(s))
            print(sensorDict[s].__str__())
            print()
            answer = input("Do the above values for {} appear to be correct? (y/n) ".format(s))
            self.assertTrue(answer.lower() in self.yesAnswers)
            print("\n\n")

    def test_GPIOConfig_Actuators(self):
        for a in actuatorDict:
            print("ACTUATOR {}:\n----------------------------------".format(a))
            print(actuatorDict[a].__str__())
            print()
            answer = input("Do the above values for {} appear to be correct? (y/n) ".format(a))
            self.assertTrue(answer.lower() in self.yesAnswers)
            for i in range(2):
                newState = (actuatorDict[a].getState() + 1) % 2
                actuatorDict[a].setState(newState)
                answer = input("Is {} now {}? (y/n) ".format(a, self.actuatorStates[newState]))
                self.assertTrue(answer.lower() in self.yesAnswers)
            print("\n\n")
