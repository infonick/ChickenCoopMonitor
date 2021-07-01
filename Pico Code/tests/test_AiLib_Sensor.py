# ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡
#
#    Raspberry Pi Pico AI Library - Sensor Class Tests
#
# ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡
#
# 
#
# ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡

import unittest
import AiLib

class Test_Sensor_Functions(unittest.TestCase):

    tLED = {'pinNum':25, 
            'pinMode':'gpio-out', 
            'name':'testLED', 
            'gpioInType':'down', 
            'irq':'none', 
            'driver':'none', 
            'convFactorADC':None,
            'gpioOutInitValue':0, 
            'stateMachineID': -1,
            'reverseStates': False}

    tVBUS = {'pinNum':24, 
                    'pinMode':'gpio-in', 
                    'name':'VBUS_in_down', 
                    'gpioInType':'down', 
                    'irq':'none', 
                    'driver':'none', 
                    'convFactorADC':None,
                    'gpioOutInitValue':0, 
                    'stateMachineID':-1}

    tVSYS = {'pinNum':3, 
                    'pinMode':'adc-in', 
                    'name':'VSYS_Voltage', 
                    'gpioInType':'down', 
                    'irq':'none', 
                    'driver':'none', 
                    'convFactorADC': lambda x:x*39,
                    'gpioOutInitValue':0, 
                    'stateMachineID':-1}

    tTEMP = {'pinNum':4, 
                    'pinMode':'adc-in', 
                    'name':'system_Temp', 
                    'gpioInType':'down', 
                    'irq':'none', 
                    'driver':'none', 
                    'convFactorADC': lambda x: 27 - ((x*3.3) - 0.706) / 0.001721,
                    'gpioOutInitValue':0, 
                    'stateMachineID':-1}

    def setUp(self):
        pass
    
    def tearDown(self):
        AiLib.GPIO.reservedPins = set()
        AiLib.GPIO.reservedStateMachines = set()

    def testSensor_initGPIO(self):
        a = AiLib.Sensor(self.tVBUS['pinNum'], 
                   self.tVBUS['pinMode'], 
                   name = self.tVBUS['name'],
                   gpioInType = self.tVBUS['gpioInType'], 
                   irq = self.tVBUS['irq'], 
                   driver = self.tVBUS['driver'],
                   convFactorADC = self.tVBUS['convFactorADC'])
        self.assertTrue(isinstance(a, AiLib.Sensor))

    def testSensor_initADC(self):
        a = AiLib.Sensor(self.tVSYS['pinNum'], 
                   self.tVSYS['pinMode'], 
                   name = self.tVSYS['name'],
                   gpioInType = self.tVSYS['gpioInType'], 
                   irq = self.tVSYS['irq'], 
                   driver = self.tVSYS['driver'],
                   convFactorADC = self.tVSYS['convFactorADC'])
        self.assertTrue(isinstance(a, AiLib.Sensor))

    def testSensor_str(self):
        a = AiLib.Sensor(self.tVBUS['pinNum'], 
                   self.tVBUS['pinMode'], 
                   name = self.tVBUS['name'],
                   gpioInType = self.tVBUS['gpioInType'], 
                   irq = self.tVBUS['irq'], 
                   driver = self.tVBUS['driver'],
                   convFactorADC = self.tVBUS['convFactorADC'])
        self.assertTrue(isinstance(a.__str__(), str))

    def testSensor_repr(self):
        a = AiLib.Sensor(self.tVBUS['pinNum'], 
                   self.tVBUS['pinMode'], 
                   name = self.tVBUS['name'],
                   gpioInType = self.tVBUS['gpioInType'], 
                   irq = self.tVBUS['irq'], 
                   driver = self.tVBUS['driver'],
                   convFactorADC = self.tVBUS['convFactorADC'])
        self.assertTrue(isinstance(a.__repr__(), str))

    def testSensor_getState_GPIO(self):
        a = AiLib.Sensor(self.tVBUS['pinNum'], 
                self.tVBUS['pinMode'], 
                name = self.tVBUS['name'],
                gpioInType = self.tVBUS['gpioInType'], 
                irq = self.tVBUS['irq'], 
                driver = self.tVBUS['driver'],
                convFactorADC = self.tVBUS['convFactorADC'])
        self.assertEqual(a.getState(), 1)

    def testSensor_getState_ADC_1(self):
        adcRangeMin = 1.5 #VSYS must have some kind of voltage if the device is running this test.
        adcRangeMax = 6 #VSYS must have some kind of voltage if the device is running this test.
        a = AiLib.Sensor(self.tVSYS['pinNum'], 
                   self.tVSYS['pinMode'], 
                   name = self.tVSYS['name'],
                   gpioInType = self.tVSYS['gpioInType'], 
                   irq = self.tVSYS['irq'], 
                   driver = self.tVSYS['driver'],
                   convFactorADC = self.tVSYS['convFactorADC'])
        self.assertTrue(a.getState() > adcRangeMin)
        self.assertTrue(a.getState() < adcRangeMax)
       

    def testSensor_getState_ADC_2(self):
        tempRangeHigh = 80 #system temperature is likely less than 80'C
        tempRangeLow = 5 #system temperature is likely higher than 5'C
        a = AiLib.Sensor(self.tTEMP['pinNum'], 
                   self.tTEMP['pinMode'], 
                   name = self.tTEMP['name'],
                   gpioInType = self.tTEMP['gpioInType'], 
                   irq = self.tTEMP['irq'], 
                   driver = self.tTEMP['driver'],
                   convFactorADC = self.tTEMP['convFactorADC'])
        self.assertTrue(a.getState() < tempRangeHigh)
        self.assertTrue(a.getState() > tempRangeLow)