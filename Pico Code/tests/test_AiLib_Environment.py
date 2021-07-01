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
import AiLib
import Event

from ucollections import deque


class Test_Environment_TypeAndValueErrors(unittest.TestCase):
    tAgent = None
    tLED = None
    tVBUS = None

    def agentFunction():
        return None

    def setUp(self):
        self.tAgent = AiLib.Agent(self.agentFunction, 
                                {'goal1':1}
                                )

        self.tLED = AiLib.Actuator(25,
                          name='boardLED', 
                          gpioOutInitValue = 0, 
                          reverseStates= False)

        self.tVBUS = AiLib.Sensor(24, 
                         'gpio-in', 
                         name='VBUS', 
                         gpioInType='down', 
                         irq='none', 
                         driver='none', 
                         convFactorADC= None)
    
    def tearDown(self):
        AiLib.GPIO.reservedPins = set()
        AiLib.GPIO.reservedStateMachines = set()

    def testEnvironment_init_NoErrorRaised(self):
        a = AiLib.Environment(self.tAgent, 
                              actuators = [self.tLED], 
                              sensors = [self.tVBUS])
        self.assertIsInstance(a, AiLib.Environment)

    def testEnvironment_initFail_TypeError_agent(self):
        with self.assertRaises(TypeError):
            AiLib.Environment(self.tLED,  # not of type AiLib.Agent
                              sensors = [self.tVBUS], 
                              actuators = [self.tLED])
    
    def testEnvironment_initFail_TypeError_sensorList(self):
        with self.assertRaises(TypeError):
            AiLib.Environment(self.tAgent, 
                              sensors = self.tVBUS,  # not in a list
                              actuators = [self.tLED])
    
    def testEnvironment_initFail_TypeError_actuatorList(self):
        with self.assertRaises(TypeError):
            AiLib.Environment(self.tAgent, 
                              sensors = [self.tVBUS],
                              actuators = self.tLED)   # not in a list

    def testEnvironment_initFail_TypeError_actuators(self):
        with self.assertRaises(TypeError):
            AiLib.Environment(self.tAgent, 
                              sensors = [self.tVBUS], 
                              actuators = [self.tVBUS]) # sensor as actuator should throw error
    
    def testEnvironment_initFail_TypeError_sensors(self):
        with self.assertRaises(TypeError):
            AiLib.Environment(self.tAgent, 
                              sensors = [self.tLED],  # actuator as sensor should throw error
                              actuators = [self.tLED])                     

    def testEnvironment_initFail_ValueError_actuators(self):
        with self.assertRaises(ValueError):
            AiLib.Environment(self.tAgent,
                              sensors = [self.tVBUS],
                              actuators = [self.tLED, self.tLED] # duplicate actuator name should throw error
                             )
    
    def testEnvironment_initFail_ValueError_sensors(self):
        with self.assertRaises(ValueError):
            AiLib.Environment(self.tAgent, 
                              sensors = [self.tVBUS, self.tVBUS], # duplicate sensor name should throw error
                              actuators = [self.tLED]
                             )



class Test_Environment_Functions(unittest.TestCase):
    tLED = None
    tVBUS = None
    tVSYS = None
    tTEMP = None
    agentGoal = {'VBUS_LED': 1,
                 'LED_OFF': 0}

    def agentProgramChangeState(self, percepts, goals):
            (perceptStates, actuatorStates) = percepts
            actuatorState = actuatorStates['boardLED']
            turnActuatorOn = 0

            if actuatorStates['boardLED'] != goals['LED_OFF']:
                turnActuatorOn = 0
            elif perceptStates['VBUS'] == goals['VBUS_LED']:
                turnActuatorOn = 1
            
            if actuatorState == turnActuatorOn:
                return None
            elif turnActuatorOn:
                return [('boardLED', 1)]
            else:
                return [('boardLED', 0)]

    def agentProgramKeepState(self, percepts, goals):
            (perceptStates, actuatorStates) = percepts
            actuatorState = actuatorStates['boardLED']
            turnActuatorOn = actuatorStates['boardLED']

            if actuatorState == turnActuatorOn:
                return None
            elif turnActuatorOn:
                return [('boardLED', 1)]
            else:
                return [('boardLED', 0)]


    def agentProgramCheckSensors(self, percepts, goals):
            (perceptStates, actuatorStates) = percepts
            VBUS_State = tVBUS.getState()
            VSYS_State = tVSYS.getState()
            TEMP_State = tTEMP.getState()
            

            return None


    def setUp(self):
        self.tLED = AiLib.Actuator(25,
                            name = 'boardLED', 
                            gpioOutInitValue = 0, 
                            reverseStates = False)

        self.tVBUS = AiLib.Sensor(24, 
                            'gpio-in', 
                            name='VBUS', 
                            gpioInType='down', 
                            irq='none', 
                            driver='none', 
                            convFactorADC= None)

        self.tVSYS = AiLib.Sensor(3, 
                            'adc-in', 
                            name = 'VSYS', 
                            gpioInType ='down', 
                            irq = 'none', 
                            driver = 'none', 
                            convFactorADC = lambda x:x*39
                            )

        self.tTEMP = AiLib.Sensor(4, 
                            'adc-in', 
                            name = 'sTemp', 
                            gpioInType = 'down', 
                            irq = 'none', 
                            driver = 'none', 
                            convFactorADC = lambda x: 27 - ((x*3.3) - 0.706) / 0.001721
                            )

        self.tLED.setState(0)

    
    def tearDown(self):
        AiLib.GPIO.reservedPins = set()
        AiLib.GPIO.reservedStateMachines = set()
        Event.Event.eventQueue = deque((), 100, 1)

    def testEnvironment_AgentKeepsState(self):
        originalState = self.tLED.getState()
        agent = AiLib.Agent(self.agentProgramKeepState, 
                            self.agentGoal)

        env = AiLib.Environment(agent, 
                                sensors = [self.tVBUS, self.tVSYS, self.tTEMP], 
                                actuators = [self.tLED]
                               )
        env.run()
        self.assertEqual(self.tLED.getState(), originalState)

    def testEnvironment_AgentChangesState1(self):
        originalState = self.tLED.getState()
        agent = AiLib.Agent(self.agentProgramChangeState, 
                            self.agentGoal)

        env = AiLib.Environment(agent, 
                                sensors = [self.tVBUS, self.tVSYS, self.tTEMP], 
                                actuators = [self.tLED]
                               )
        env.run()
        self.assertNotEqual(self.tLED.getState(), originalState)

    def testEnvironment_AgentChangesState2(self):
        self.tLED.setState(1)
        originalState = self.tLED.getState()
        agent = AiLib.Agent(self.agentProgramChangeState, 
                            self.agentGoal)

        env = AiLib.Environment(agent, 
                                sensors = [self.tVBUS, self.tVSYS, self.tTEMP], 
                                actuators = [self.tLED]
                               )
        env.run()
        self.assertNotEqual(self.tLED.getState(), originalState)


    def testEnvironment_AgentEventKeepsState(self):
        originalState = self.tLED.getState()
        agent = AiLib.Agent(self.agentProgramKeepState, 
                            self.agentGoal)

        env = AiLib.Environment(agent, 
                                sensors = [self.tVBUS, self.tVSYS, self.tTEMP], 
                                actuators = [self.tLED]
                               )
        env.run()
        # There should be no event recorded.
        with self.assertRaises(IndexError):
            e = Event.Event.eventQueue.popleft()


    def testEnvironment_AgentEventChangesState1(self):
        agent = AiLib.Agent(self.agentProgramChangeState, 
                            self.agentGoal)

        env = AiLib.Environment(agent, 
                                sensors = [self.tVBUS, self.tVSYS, self.tTEMP], 
                                actuators = [self.tLED]
                               )
        env.run()
        e = Event.Event.eventQueue.popleft()
        self.assertIsInstance(e, Event.Event)

    def testEnvironment_AgentEventChangesState2(self):
        self.tLED.setState(1)
        agent = AiLib.Agent(self.agentProgramChangeState, 
                            self.agentGoal)

        env = AiLib.Environment(agent, 
                                sensors = [self.tVBUS, self.tVSYS, self.tTEMP], 
                                actuators = [self.tLED]
                               )
        env.run()
        e = Event.Event.eventQueue.popleft()
        self.assertIsInstance(e, Event.Event)


    def testEnvironment_percepts(self):
        agent = AiLib.Agent(self.agentProgramCheckSensors, 
                            self.agentGoal)
        env = AiLib.Environment(agent, 
                                sensors = [self.tVBUS, self.tVSYS, self.tTEMP], 
                                actuators = [self.tLED]
                               )
        VBUS_State = self.tVBUS.getState()
        VSYS_State = self.tVSYS.getState()
        TEMP_State = self.tTEMP.getState()
        (perceptStates, actuatorStates) = env.percepts()

        self.assertEqual(perceptStates['VBUS'], VBUS_State)
        self.assertAlmostEqual(perceptStates['VSYS'], VSYS_State, delta=0.2)
        self.assertAlmostEqual(perceptStates['sTemp'], TEMP_State, delta=0.2)


# TEST FOR EVENT UPON RUN AND AGENT ACTION!