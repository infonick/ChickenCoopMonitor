# ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡
#
#    Raspberry Pi Pico AI Library - Actuator Class Tests
#
# ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡
#
# 
#
# ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡

import unittest
import AiLib

class Test_Actuator_Functions(unittest.TestCase):

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

    def testActuator_initGPIO(self):
        a = AiLib.Actuator(self.tLED['pinNum'],  
                            name = self.tLED['name'],
                            gpioOutInitValue = self.tLED['gpioOutInitValue'],
                            reverseStates = self.tLED['reverseStates'])
        self.assertTrue(isinstance(a, AiLib.Actuator))


    def testActuator_str(self):
        a = AiLib.Actuator(self.tLED['pinNum'],  
                            name = self.tLED['name'],
                            gpioOutInitValue = self.tLED['gpioOutInitValue'],
                            reverseStates = self.tLED['reverseStates'])
        self.assertTrue(isinstance(a.__str__(), str))

    def testActuator_repr(self):
        a = AiLib.Actuator(self.tLED['pinNum'],  
                            name = self.tLED['name'],
                            gpioOutInitValue = self.tLED['gpioOutInitValue'],
                            reverseStates = self.tLED['reverseStates'])
        self.assertTrue(isinstance(a.__repr__(), str))

    def testActuator_getState(self):
        a = AiLib.Actuator(self.tLED['pinNum'],  
                            name = self.tLED['name'],
                            gpioOutInitValue = self.tLED['gpioOutInitValue'],
                            reverseStates = self.tLED['reverseStates'])
        self.assertTrue(a.getState() in [0,1])

    def testActuator_setState(self):
        adcRange = range(2,65536) 
        a = AiLib.Actuator(self.tLED['pinNum'],  
                            name = self.tLED['name'],
                            gpioOutInitValue = self.tLED['gpioOutInitValue'],
                            reverseStates = self.tLED['reverseStates'])
        a.setState(1)
        self.assertEqual(a.getState(), 1)
        a.setState(0)
        self.assertEqual(a.getState(), 0)
        a.setState('on')
        self.assertEqual(a.getState(), 1)
        a.setState('off')
        self.assertEqual(a.getState(), 0)

    def testActuator_toggleState(self):
        a = AiLib.Actuator(self.tLED['pinNum'],  
                            name = self.tLED['name'],
                            gpioOutInitValue = self.tLED['gpioOutInitValue'],
                            reverseStates = self.tLED['reverseStates'])
        s = a.getState()
        t = (s+1) % 2
        a.toggleState()
        self.assertEqual(a.getState(), t)
        s = a.getState()
        t = (s+1) % 2
        a.toggleState()
        self.assertEqual(a.getState(), t)