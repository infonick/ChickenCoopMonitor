# ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡
#
#    Raspberry Pi Pico AI Library - Actuator  Class
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
# from usys import path
# path.append('/RP2040-Pico-RTC')
# path.append('/PicoDHT22')
# path.append('/AiLib')

from micropython import alloc_emergency_exception_buf
# from micropython import schedule
# from utime import sleep_ms
# from utime import localtime
# from utime import mktime
from machine import Pin
from machine import ADC
# from _thread import allocate_lock

# from types import LambdaType

# from DHT22 import DHT22
# from SlidingDoorDriver import SlidingDoor
#from RP2040_RTC import rp2RTC
from AiLib import GPIO

# from Events import Event

alloc_emergency_exception_buf(100)


# class InoperativeSensorException(Exception):
#     pass
# class ResourceUnavailibleException(Exception):
#     pass

 

class Actuator(GPIO):
    """
    An Actuator class for embedded and attached actuating components.

    ≡≡≡ Attributes ≡≡≡
    reservedPins: a list of integers representing all GPIO pins that have been
                  assigned. Part of superclass GPIO.
    
    ≡≡≡ Methods ≡≡≡
    __init__(pinNum, name=None, gpioOutInitValue=0):
        Initializes an Actuator Object.
        
    __validateActuatorInputs(pinMode, irq, driver, convFactorADC):
        Validates the parameter inputs for an Actuator Object.
        
    __str__():
        Returns a brief string representation of an Actuator Object.

    __repr__():
        Returns a complete string representation of an Actuator Object.
    
    getState(asString=False):
        Returns the current actuator state.
    
    setState(newState):
        Sets the actuator to a new state. 
    
    toggleState(self):
        Toggles the actuator state.
        
    getPin():
        Returns the pin number of the GPIO Object. Could be a GPIO Pin (0-29)
        or an ADC Pin (0-3). Part of superclass GPIO.
    
    getGPIOPin():
        Returns the pin number as a GPIO pin number for the GPIO Object. Part of
        superclass GPIO.

    getName():
        Returns the name of the GPIO object. Part of superclass GPIO.
    """
    __gpioOutInitValueTypes = range(2)
    __gpioOutInitValueTypeNames = ['Off', 'On']
    
    def __init__(self, pinNum, name=None, gpioOutInitValue=0, reverseStates = False):
        """
        Initializes an Actuator object.
        
        ≡≡≡ Required Parameters ≡≡≡
        pinNum:  int, representing a valid pin number (0-3 for ADC, 0-29 for GPIO)
        
        ≡≡≡ Optional Parameters ≡≡≡
        name:             str, a text name for the Actuator object
        gpioOutInitValue: int, an initial setting for the actuator when 
                               instantiated. 0 = initially off, 1 = initially
                               on.
        reverseStates:    bool, if True will set the GPIO high as the 'Off'
                                and low as the 'On' state.
         
        ≡≡≡ Raises ≡≡≡
        TypeError:  if the supplied parameter type is not an integer
        ValueError: if the supplied parameter is outside the legal range
        """
        try:
            self.__validateActuatorInputs(gpioOutInitValue, reverseStates)
        except:
            raise
        
        if reverseStates:
            if gpioOutInitValue == 0:
                gpioOutInitValue = 1
            elif gpioOutInitValue == 1:
                gpioOutInitValue = 0
        
        super(Actuator, self).__init__(pinNum=pinNum, pinMode='gpio-out', name=name,
                                       gpioOutInitValue=gpioOutInitValue)
        self._reverseStates = reverseStates


    def __validateActuatorInputs(self, gpioOutInitValue, reverseStates):
        """
        Validates the parameter inputs for a GPIO Object.
        
        ≡≡≡ Required Parameters ≡≡≡
        gpioOutInitValue:  int, an initial setting for the actuator when instantiated
                            0 = initially off, 1 = initially on.
         
        ≡≡≡ Raises ≡≡≡
        TypeError:  if the supplied parameter type is not an integer
        ValueError: if the supplied parameter is outside the legal range
        
        ≡≡≡ Returns ≡≡≡
        bool: True if successful
        """
        intInputs = {'gpioOutInitValue':gpioOutInitValue}
        boolInputs = {'reverseStates':reverseStates}
        
        for key in intInputs:
            if not isinstance(intInputs[key], int):
                raise TypeError("Parameter \'" +
                                key +
                                "\' received parameter of type \'" +
                                str(type(intInputs[key])) +
                                "\' - expected parameter of type \'int\'.")
        
        for key in boolInputs:
            if not isinstance(boolInputs[key], bool):
                raise TypeError("Parameter \'" +
                                key +
                                "\' received parameter of type \'" +
                                str(type(boolInputs[key])) +
                                "\' - expected parameter of type \'bool\'.")
        
        if gpioOutInitValue not in self.__gpioOutInitValueTypes:
            raise ValueError ("\'gpioOutInitValue\' must be an integer in the range " +
                                  str(min(self.__gpioOutInitValueTypes)) +
                                  " to " + 
                                  str(max(self.__gpioOutInitValueTypes)) +
                                  ".")
        return True


    def __str__(self):
        """Returns a brief string representation of an Actuator Object."""
        out = super(Actuator, self).__str__()
        out += " State: " + str(self.getState(asString=True))
        return out


    def __repr__(self):
        """Returns a complete string representation of an Actuator Object."""
        out = super(Actuator, self).__repr__()
        out += (", Actuator State: " + str(self.getState(asString=True))
                )
        return out
    
    
    def getState(self, asString=False):
        """
        Returns the current actuator state.
        
        ≡≡≡ Optional Parameters ≡≡≡
        asString:  bool, True = return state as a string ('Off' / 'On')
                         False = return state as an integer (0 or 1)
        
        ≡≡≡ Returns ≡≡≡
        bool: True if successful, False if no change made.
        """
        self.__accessLock.acquire()
        try:
            stateInt = super(Actuator, self).getState()

            
            if self._reverseStates:
                if stateInt == 0:
                    stateInt = 1
                elif stateInt == 1:
                    stateInt = 0
            
            if asString:
                return str(self.__gpioOutInitValueTypeNames[stateInt])
            else:
                return stateInt
        except:
            raise
        finally:
            self.__accessLock.release()
    
    
    def setState(self, newState):
        """
        Sets the actuator to a new state.
        
        ≡≡≡ Required Parameters ≡≡≡
        newState:  int or str, 0 or 'Off' = off, 1 or 'On' = on.
        
        ≡≡≡ Returns ≡≡≡
        bool: True if successful, False if unsuccessful
        """

        if isinstance(newState, str):
            if newState.lower() == 'on':
                newState = 1
            elif newState.lower() == 'off':
                newState = 0
        
        if self._reverseStates and isinstance(newState, int):
            if newState == 1:
                newState = 0
            elif newState == 0:
                newState = 1
        
        self.__accessLock.acquire()
        try:
            if isinstance(newState, int):
                if newState == 1:
                    self._sensor.value(1)
                    return True
                elif newState == 0:
                    self._sensor.value(0)
                    return True
        except:
            raise
        finally:
            self.__accessLock.release()
            
        return False
    
    
    def toggleState(self):
        """
        Toggles the actuator state.
        
        ≡≡≡ Returns ≡≡≡
        bool: True if successful, False if unsuccessful
        """
        if self.getState(asString=False):
            return self.setState(0)
        else:
            return self.setState(1)

