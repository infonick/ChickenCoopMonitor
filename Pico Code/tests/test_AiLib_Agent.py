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

def agentFunction_1():
    return None

class Test_Agent_TypeErrors(unittest.TestCase):
    agentGoal = {'goal1':1}

    def agentFunction_2():
        return None

    def testAgent_init_NoErrorRaised_1(self):
        a = AiLib.Agent(self.agentFunction_2, 
                        self.agentGoal
                        )
        self.assertIsInstance(a, AiLib.Agent)

    def testAgent_init_NoErrorRaised_2(self):
        a = AiLib.Agent(self.agentFunction_2, 
                        {'goal1':1}
                        )
        self.assertIsInstance(a, AiLib.Agent)

    def testAgent_init_NoErrorRaised_3(self):
        a = AiLib.Agent(agentFunction_1, 
                        self.agentGoal
                        )
        self.assertIsInstance(a, AiLib.Agent)

    def testAgent_init_NoErrorRaised_3(self):
        a = AiLib.Agent(lambda x:x, 
                        self.agentGoal
                        )
        self.assertIsInstance(a, AiLib.Agent)

    def testAgent_initFail_TypeError_program(self):
        with self.assertRaises(TypeError):
            AiLib.Agent('cant be a string', # Should give a TypeError since a program must be a function
                        {'goal1':1}
                        )
    
    def testAgent_initFail_TypeError_goals(self):
        with self.assertRaises(TypeError):
            AiLib.Agent(self.agentFunction_2, 
                        []# Should give a TypeError since a list is not a dict
                        )



class Test_Agent_Functions(unittest.TestCase):

    agentGoal = {'goal1': 1}
    
    def setUp(self):
        self.testAgent = AiLib.Agent(agentFunction_1, 
                                     self.agentGoal)
    
    def tearDown(self):
        pass

    def testAgent_program(self):
        self.assertIs(self.testAgent.program, agentFunction_1)

    def testAgent_goals(self):
        self.assertIs(self.testAgent.goals, self.agentGoal)
