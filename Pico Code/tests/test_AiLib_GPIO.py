# ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡
#
#    Raspberry Pi Pico AI Library - GPIO Class Tests
#
# ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡
#
# 
#
# ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡

import unittest
import AiLib
from utime import sleep_ms

class Test_GPIO_TypeAndValueErrors(unittest.TestCase):

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
                    'convFactorADC':lambda x:x*39,
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


    def testGPIO_initFail_TypeError_pinNum(self):
        with self.assertRaises(TypeError):
            AiLib.GPIO('cant be a string', # Should give a TypeError
                 self.tLED['pinMode'], 
                 name = self.tLED['name'],
                 gpioInType = self.tLED['gpioInType'], 
                 gpioOutInitValue = self.tLED['gpioOutInitValue'], 
                 stateMachineID = self.tLED['stateMachineID'])

    def testGPIO_initFail_TypeError_pinMode(self):
        with self.assertRaises(TypeError):
            AiLib.GPIO(self.tLED['pinNum'], 
                 0, # Should give a TypeError since its not a string
                 name = self.tLED['name'],
                 gpioInType = self.tLED['gpioInType'], 
                 gpioOutInitValue = self.tLED['gpioOutInitValue'], 
                 stateMachineID = self.tLED['stateMachineID'])

    def testGPIO_initFail_TypeError_gpioInType(self):
        with self.assertRaises(TypeError):
            AiLib.GPIO(self.tVBUS['pinNum'], 
                 self.tVBUS['pinMode'], 
                 name = self.tVBUS['name'],
                 gpioInType = 0, # Should give a TypeError since its not a string
                 gpioOutInitValue = self.tVBUS['gpioOutInitValue'], 
                 stateMachineID = self.tVBUS['stateMachineID'])

    def testGPIO_initFail_TypeError_gpioOutInitValue(self):
        with self.assertRaises(TypeError):
            AiLib.GPIO(self.tLED['pinNum'], 
                 self.tLED['pinMode'], 
                 name = self.tLED['name'], 
                 gpioInType = self.tLED['gpioInType'],  
                 gpioOutInitValue = 'cant be a string',  # Should give a TypeError
                 stateMachineID = self.tLED['stateMachineID'])

    def testGPIO_initFail_TypeError_stateMachineID(self):
        with self.assertRaises(TypeError):
            AiLib.GPIO(self.tLED['pinNum'], 
                 self.tLED['pinMode'], 
                 name = self.tLED['name'],
                 gpioInType = self.tLED['gpioInType'], 
                 gpioOutInitValue = self.tLED['gpioOutInitValue'], 
                 stateMachineID = 'cant be a string') # Should give a TypeError


    def testGPIO_initFail_ValueError_pinNumGPIO(self):
        tooLow = range(-10,0,1)
        tooHigh = range(30,50,1)
        invalidRange = list(tooLow) + list(tooHigh)
        
        for i in invalidRange:
            with self.assertRaises(ValueError):
                AiLib.GPIO(i, 
                    self.tLED['pinMode'], 
                    name = self.tLED['name'],
                    gpioInType = self.tLED['gpioInType'], 
                    gpioOutInitValue = self.tLED['gpioOutInitValue'], 
                    stateMachineID = self.tLED['stateMachineID'])

    def testGPIO_initFail_ValueError_pinNumADC(self):
        tooLow = range(-10,0,1)
        tooHigh = range(5,50,1)
        invalidRange = list(tooLow) + list(tooHigh)
        
        for i in invalidRange:
            with self.assertRaises(ValueError):
                AiLib.GPIO(i, 
                    self.tTEMP['pinMode'], 
                    name = self.tTEMP['name'],
                    gpioInType = self.tTEMP['gpioInType'], 
                    gpioOutInitValue = self.tTEMP['gpioOutInitValue'], 
                    stateMachineID = self.tTEMP['stateMachineID'])


    def testGPIO_initFail_ValueError_pinMode(self):
        with self.assertRaises(ValueError):
            AiLib.GPIO(self.tLED['pinNum'], 
                 'pinMode', # Should fail as a non-valid pinMode code string. 
                 name = self.tLED['name'],
                 gpioInType = self.tLED['gpioInType'], 
                 gpioOutInitValue = self.tLED['gpioOutInitValue'], 
                 stateMachineID = self.tLED['stateMachineID'])       

    def testGPIO_initFail_ValueError_(self):
        with self.assertRaises(ValueError):
            AiLib.GPIO(self.tVBUS['pinNum'], 
                 self.tVBUS['pinMode'], 
                 name = self.tVBUS['name'],
                 gpioInType = 'gpioInType', # Should fail as a non-valid gpioInType code string.
                 gpioOutInitValue = self.tVBUS['gpioOutInitValue'], 
                 stateMachineID = self.tVBUS['stateMachineID'])   

    def testGPIO_initFail_ValueError_gpioOutInitValue(self):
        tooLow = range(-10,0,1)
        tooHigh = range(2,40,1)
        invalidRange = list(tooLow) + list(tooHigh)
        
        for i in invalidRange:
            with self.assertRaises(ValueError):
                AiLib.GPIO(self.tLED['pinNum'], 
                    self.tLED['pinMode'], 
                    name = self.tLED['name'],
                    gpioInType = self.tLED['gpioInType'], 
                    gpioOutInitValue = i, 
                    stateMachineID = self.tLED['stateMachineID'])   

    def testGPIO_initFail_ValueError_stateMachineID(self):
        tooLow = range(-10,-1,1)
        tooHigh = range(8,40,1)
        invalidRange = list(tooLow) + list(tooHigh)
        
        for i in invalidRange:
            with self.assertRaises(ValueError):
                AiLib.GPIO(self.tLED['pinNum'], 
                    self.tLED['pinMode'], 
                    name = self.tLED['name'],
                    gpioInType = self.tLED['gpioInType'], 
                    gpioOutInitValue = self.tLED['gpioOutInitValue'], 
                    stateMachineID = i)  





class Test_GPIO_Functions(unittest.TestCase):

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
                    'convFactorADC':lambda x:x*39,
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


    def testGPIO_init_nameGiven(self):
        a = AiLib.GPIO(self.tLED['pinNum'], 
                self.tLED['pinMode'], 
                name = self.tLED['name'],
                gpioInType = self.tLED['gpioInType'], 
                gpioOutInitValue = self.tLED['gpioOutInitValue'], 
                stateMachineID = self.tLED['stateMachineID'])
        self.assertEqual(a.getName(), self.tLED['name'])
        
    def testGPIO_init_nameNotGiven(self):
        a = AiLib.GPIO(self.tLED['pinNum'], 
                self.tLED['pinMode'], 
                name = None,
                gpioInType = self.tLED['gpioInType'], 
                gpioOutInitValue = self.tLED['gpioOutInitValue'], 
                stateMachineID = self.tLED['stateMachineID'])
        self.assertEqual(a.getName(), 'GPIO-OUT_25')

    def testGPIO_init_gpioOutInitValue(self):
        for i in [0,1,0]:
            a = AiLib.GPIO(self.tLED['pinNum'], 
                    self.tLED['pinMode'], 
                    name = self.tLED['name'],
                    gpioInType = self.tLED['gpioInType'], 
                    gpioOutInitValue = i, 
                    stateMachineID = self.tLED['stateMachineID'])
            self.assertEqual(a.getState(), i)
            self.tearDown()

    def testGPIO_init___getStateMachineNumber(self):
        a = AiLib.GPIO(self.tLED['pinNum'], 
                self.tLED['pinMode'], 
                name = self.tLED['name'],
                gpioInType = self.tLED['gpioInType'], 
                gpioOutInitValue = self.tLED['gpioOutInitValue'], 
                stateMachineID = 2)
        self.assertEqual(a.__getStateMachineNumber(), 2)

    def testGPIO_init_reservedStateMachines(self):
        a = AiLib.GPIO(self.tLED['pinNum'], 
                self.tLED['pinMode'], 
                name = self.tLED['name'],
                gpioInType = self.tLED['gpioInType'], 
                gpioOutInitValue = self.tLED['gpioOutInitValue'], 
                stateMachineID = 3)
        self.assertTrue(a.reservedStateMachines.issuperset(set([3])))
        self.assertTrue(a.reservedStateMachines.issubset(set([3])))

    def testGPIO_init_getPin(self):
        a = AiLib.GPIO(self.tLED['pinNum'], 
                self.tLED['pinMode'], 
                name = self.tLED['name'],
                gpioInType = self.tLED['gpioInType'], 
                gpioOutInitValue = self.tLED['gpioOutInitValue'], 
                stateMachineID = self.tLED['stateMachineID'])
        self.assertEqual(a.getPin(), self.tLED['pinNum'])

    def testGPIO_init_reservedPins(self):
        a = AiLib.GPIO(self.tLED['pinNum'], 
                self.tLED['pinMode'], 
                name = self.tLED['name'],
                gpioInType = self.tLED['gpioInType'], 
                gpioOutInitValue = self.tLED['gpioOutInitValue'], 
                stateMachineID = self.tLED['stateMachineID'])
        self.assertTrue(a.reservedPins.issuperset(set([self.tLED['pinNum']])))
        self.assertTrue(a.reservedPins.issubset(set([self.tLED['pinNum']])))

    def testGPIO_init_getPinADC(self):
        a = AiLib.GPIO(self.tVSYS['pinNum'], 
                self.tVSYS['pinMode'], 
                name = self.tVSYS['name'],
                gpioInType = self.tVSYS['gpioInType'], 
                gpioOutInitValue = self.tVSYS['gpioOutInitValue'], 
                stateMachineID = self.tVSYS['stateMachineID'])
        self.assertEqual(a._pin, self.tVSYS['pinNum'])
        self.assertEqual(a.getPin(), 3)
        self.assertEqual(a.getGPIOPin(), 29)
    
    def testGPIO_getState_GPIO(self):
        a = AiLib.GPIO(self.tVBUS['pinNum'], 
                self.tVBUS['pinMode'], 
                name = self.tVBUS['name'],
                gpioInType = self.tVBUS['gpioInType'], 
                gpioOutInitValue = self.tVBUS['gpioOutInitValue'], 
                stateMachineID = self.tVBUS['stateMachineID'])
        self.assertEqual(a.getState(), 1)

    def testGPIO_getState_ADC(self):
        adcRangeMin = 2/65535 #VSYS must have some kind of voltage if the device is running this test.
        adcRangeMax = 1 #VSYS must have some kind of voltage if the device is running this test.
        a = AiLib.GPIO(self.tVSYS['pinNum'], 
                self.tVSYS['pinMode'], 
                name = self.tVSYS['name'],
                gpioInType = self.tVSYS['gpioInType'], 
                gpioOutInitValue = self.tVSYS['gpioOutInitValue'], 
                stateMachineID = self.tVSYS['stateMachineID'])
        self.assertTrue(a.getState() > adcRangeMin)
        self.assertTrue(a.getState() < adcRangeMax)

    def testGPIO_str(self):
        a = AiLib.GPIO(self.tLED['pinNum'], 
                self.tLED['pinMode'], 
                name = self.tLED['name'],
                gpioInType = self.tLED['gpioInType'], 
                gpioOutInitValue = self.tLED['gpioOutInitValue'], 
                stateMachineID = self.tLED['stateMachineID'])
        self.assertTrue(isinstance(a.__str__(), str))

    def testGPIO_repr(self):
        a = AiLib.GPIO(self.tLED['pinNum'], 
                self.tLED['pinMode'], 
                name = self.tLED['name'],
                gpioInType = self.tLED['gpioInType'], 
                gpioOutInitValue = self.tLED['gpioOutInitValue'], 
                stateMachineID = self.tLED['stateMachineID'])
        self.assertTrue(isinstance(a.__repr__(), str))
