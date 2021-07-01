# ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡
#
#    Raspberry Pi Pico AI Library - Environment Class
#
# ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡
# Classes that are defined in this library:
#   - GPIO: A generic GPIO pin class for 'gpio-in', 'gpio-out', and 'adc-in'
#   - Sensor: Extends the GPIO class for sensor devices.
#   - Actuator: Extends the GPIO class for actuators.
#   - Agent: A class representing an AI Agent
#   - Environment: A class representing an AI Agent's environment.
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

from Event import Event
from AiLib import Agent
from AiLib import Sensor
from AiLib import Actuator

class InoperativeSensorException(Exception):
    pass
# class ResourceUnavailibleException(Exception):
#     pass

    

class Environment():
    """
    An Environment class for AI Agents to exist within.

    ≡≡≡ Attributes ≡≡≡

    ≡≡≡ Methods ≡≡≡
    __init__(program, goals)
        Initializes an Environment object.
    
    __validateAgentInputs(program, goals):
        Validates the parameter inputs for an Environment Object.

    """
    
    def __init__(self, agent, sensors=[], actuators=[]):
        """
        Initializes an Environment object.
        
        ≡≡≡ Required Parameters ≡≡≡
        agent:   An object of type 'AiLib.Agent'.
        sensors: A list of objects of type 'AiLib.Sensor'.
        sensors: A list of objects of type 'AiLib.Actuator'.

        ≡≡≡ Raises ≡≡≡
        TypeError:  if the supplied parameter type is not correct.
        ValueError: if the supplied parameter is outside the legal range
        """
        try:
            self.__validateEnvironmentInputs(agent, sensors, actuators)
        except:
            raise

        self.sensors = sensors
        self.actuators = actuators
        self.agent = agent


    def __validateEnvironmentInputs(self, agent, sensors, actuators):
        """
        Validates the parameter inputs for an Environment Object.
        
        ≡≡≡ Required Parameters ≡≡≡
        agent:   An object of type 'AiLib.Agent'.
        sensors: A list of objects of type 'AiLib.Sensor'.
        sensors: A list of objects of type 'AiLib.Actuator'.

        ≡≡≡ Raises ≡≡≡
        TypeError:  if the supplied parameter type is not correct.
        ValueError: if the supplied parameter is outside the legal range.
        
        ≡≡≡ Returns ≡≡≡
        bool: True if successful
        """
        listInputs = {'sensors':sensors,
                     'actuators':actuators}
        sensorNames = []
        actuatorNames = []                     
        
        for key in listInputs:
            if not isinstance(listInputs[key], list):
                raise TypeError("Parameter \'" +
                                key +
                                "\' received parameter of type \'" +
                                str(type(listInputs[key])) +
                                "\' - expected parameter of type \'list\'.")

        for item in sensors:
            if not isinstance(item, Sensor):
                raise TypeError("One of the items in list \'sensors\' is of type \'" +
                                str(type(item)) +
                                "\' - expected that the list consist entirely of " + 
                                "items of type \'AiLib.Sensor\'.")    

        for item in actuators:
            if not isinstance(item, Actuator):
                raise TypeError("One of the items in list \'actuators\' is of type \'" +
                                str(type(item)) +
                                "\' - expected that the list consist entirely of " + 
                                "items of type \'AiLib.Actuator\'.")

        if not isinstance(agent, Agent):
            raise TypeError("Parameter \'agent\' received value of type \'" +
                                str(type(agent)) +
                                "\' - expected parameter of type \'AiLib.Agent\'.")
        

        for item in sensors:
            if item.getName() in sensorNames:
                raise ValueError("Two of the items in list \'sensors\' have " +
                                 "the same name. All sensors are required to " + 
                                 "have unique names.") 
            else:
                sensorNames.append(item.getName())

        for item in actuators:
            if item.getName() in actuatorNames:
                raise ValueError("Two of the items in list \'actuators\' " +
                                 "have the same name. All actuators are " + 
                                 "required to have unique names.")   
            else:
                actuatorNames.append(item.getName())

        return True


    def run(self):
        """Runs the environment and agent"""
        percepts = self.percepts()
        actions = self.agent.program(percepts, self.agent.goals)
                    
        if actions is not None:
            self.execute_actions(actions)
            
            eventDetail = {'actions': actions,
                           'percepts': percepts}
            Event('Agent Action', eventDetail)
    

    def percepts(self):
        """Collects all percept values for the environment."""
        perceptStates = {}
        actuatorStates = {}
        
        for sensor in self.sensors:
            try:
                perceptStates[sensor.getName()] = sensor.getState()
            except InoperativeSensorException:
                perceptStates[sensor.getName()] = None
                # Log Error <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
                
        for actuator in self.actuators:
            actuatorStates[actuator.getName()] = actuator.getState()
                    
        return (perceptStates, actuatorStates)
    

    def execute_actions(self, actions):
        """Executes the agent's actions within the environment."""
        for (actuatorName, newState) in actions:
            for i in range(len(self.actuators)):
                if actuatorName == self.actuators[i].getName():
                    self.actuators[i].setState(newState)
