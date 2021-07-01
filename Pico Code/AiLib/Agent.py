# ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡
#
#    Raspberry Pi Pico AI Library - Agent Class
#
# ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡
# Classes that are defined in this library:
#   - GPIO: A generic GPIO pin class for 'gpio-in', 'gpio-out', and 'adc-in'
#   - Sensor: Extends the GPIO class for sensor devices.
#   - Actuator: Extends the GPIO class for actuators.
#   - Agent: A class representing an AI Agent
#   - Environment:  A class representing an AI Agent's environment.
#
#
# IMPORTANT NOTES:
#   - 
#
# ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡
# REVISION HISTORY:
#   - 
#
# ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡

from micropython import alloc_emergency_exception_buf
alloc_emergency_exception_buf(100)

from types import FunctionType
from types import MethodType
from types import LambdaType

class Agent():
    """
    An Agent class for AI decision making.

    ≡≡≡ Attributes ≡≡≡

    ≡≡≡ Methods ≡≡≡
    __init__(program, goals)
        Initializes an Agent object.
    
    __validateAgentInputs(program, goals):
        Validates the parameter inputs for an Agent Object.

    """

    
    def __init__(self, program, goals):
        """
        Initializes an Agent object.
        
        ≡≡≡ Required Parameters ≡≡≡
        program: A function for how the agent interacts with sensors and actuators.
        goals:   A dictionary of goals in the format {'goalName':goalValue}

        ≡≡≡ Raises ≡≡≡
        TypeError:  if the supplied parameter type is not correct.
        """
        try:
            self.__validateAgentInputs(program, goals)
        except:
            raise
        
        self.program = program
        self.goals = goals



    def __validateAgentInputs(self, program, goals):
        """
        Validates the parameter inputs for an Agent Object.
        
        ≡≡≡ Required Parameters ≡≡≡
        program: A function for how the agent interacts with sensors and actuators.
        goals:   A dictionary of goals in the format {'goalName':goalValue}

        ≡≡≡ Raises ≡≡≡
        TypeError:  if the supplied parameter type is not an integer
        
        ≡≡≡ Returns ≡≡≡
        bool: True if successful
        """
        if not (isinstance(program, FunctionType) or 
                isinstance(program, MethodType)  or
                isinstance(program, LambdaType) ):
            raise TypeError("Parameter \'program\' received value of type \'" +
                                str(type(program)) +
                                "\' - expected parameter of type \'function\'.")
        
        if not isinstance(goals, dict):
            raise TypeError("Parameter \'goals\' received value of type \'" +
                                str(type(goals)) +
                                "\' - expected parameter of type \'dict\'.")
  
        return True

    