# ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡
#
#    Raspberry Pi Pico AI Library - GPIO Class
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
from _thread import allocate_lock

# from types import LambdaType

# from DHT22 import DHT22
# from SlidingDoorDriver import SlidingDoor
#from RP2040_RTC import rp2RTC

# from Events import Event

alloc_emergency_exception_buf(100)


# class InoperativeSensorException(Exception):
#     pass
class ResourceUnavailibleException(Exception):
    pass


class GPIO():
    """
    A generic GPIO pin class for 'gpio-in', 'gpio-out', and 'adc-in'

    ≡≡≡ Attributes ≡≡≡
    reservedPins: a list of integers representing all GPIO pins that have been
                  assigned.
    
    ≡≡≡ Methods ≡≡≡
    __init__(pinNum, pinMode, name=None, gpioInType='down', gpioOutInitValue=0):
        Initializes a GPIO Object.
        
    __validateInputs(pinNum, pinMode, gpioInType, gpioOutInitValue):
        Validates the parameter inputs for a GPIO Object.
        
    __str__():
        Returns a brief string representation of a GPIO Object.

    __repr__():
        Returns a complete string representation of a GPIO Object.
    
    getPin():
        Returns the pin number of the GPIO Object. Could be a GPIO Pin (0-29)
        or an ADC Pin (0-3).
    
    getGPIOPin():
        Returns the pin number as a GPIO pin number for the GPIO Object.
    
    getName():
        Returns the name of the GPIO object.
    
    getState():
        Reads the current GPIO value.
         - For ADC readings, the value is averaged over 10 sensor readings to
           account for noise.
         - For GPIO readings, the pin's state is retrieved.
    """
    __adcPinValues = range(5)
    __adcPinToGPIO = [26,27,28,29,-1]
    __gpioPinValues = range(30)
    __gpioOutInitValues = range(2)
    __stateMachineIdNumbers = range(-1,8)
    __pinModes = ['gpio-in', 'gpio-out', 'adc-in']
    __gpioInTypes = {'up':Pin.PULL_UP, 'down':Pin.PULL_DOWN, 'none':'none'}
    
    __gpioAssignmentLock = allocate_lock()
    __smAssignmentLock = allocate_lock()
    
    reservedPins=set()
    reservedStateMachines=set()
    
    
    def __init__(self, pinNum, pinMode, name=None, gpioInType='down', gpioOutInitValue=0, stateMachineID=-1):
        """
        Initializes a GPIO Object.
        
        ≡≡≡ Required Parameters ≡≡≡
        pinNum:  int, representing a valid pin number (0-3 for ADC, 0-29 for GPIO)
        pinMode: str, one of 'gpio-in', 'gpio-out', or 'adc-in'
        
        ≡≡≡ Optional Parameters ≡≡≡
        name:         str, a text name for the GPIO object
        gpioInType:   str, sets a pull-up or pull-down resistor on a GPIO input.
                           Values are either 'up' or 'down', only used for
                           pinMode = 'gpio-in'
        gpioOutInitValue: int, sets the initial GPIO value for a GPIO Output. Values
                           may be either 0 (off) or 1 (on), only used for pinMode
                           = 'gpio-out'. 
              
        ≡≡≡ Raises ≡≡≡
        TypeError:  if the supplied parameter type is not correct
        ValueError: if the supplied parameter is outside the legal range
        ResourceUnavailibleException: if a state machine ID is required but not availible
        """
        try:
            self.__validateInputs(pinNum, pinMode, gpioInType, gpioOutInitValue, stateMachineID)
        except:
            raise
        
        self._pin = pinNum
        self._pinMode = pinMode.lower()
        self._gpioInType = 'none'
        self._gpioOutInitValue = 'none'
        self._stateMachineID = -1
        self.__accessLock = allocate_lock()
        
        if (name == None) or name.isspace():
            self._name = self._pinMode.upper() + "_" + str(self._pin)
        else:
            self._name = str(name)
        
        
        self.__gpioAssignmentLock.acquire()
                
        try:
            if self._pinMode == 'adc-in' and self.__adcPinToGPIO[pinNum] in self.reservedPins :
                raise ValueError ("ADC" +
                                  str(pinNum) +
                                  " (aka: GPIO " +
                                  str(self.__adcPinToGPIO[pinNum]) +
                                  ") already assigned.")
            elif pinNum in self.reservedPins:
                raise ValueError ("GPIO_" +
                                  str(pinNum) +
                                  " is already assigned.")
            
            if self._pinMode == 'gpio-in':
                self._gpioInType = gpioInType.lower()
                self._sensor = Pin(self._pin, mode=Pin.IN, pull=self.__gpioInTypes[self._gpioInType])
                self.reservedPins.add(self._pin)
            
            elif self._pinMode == 'gpio-out':
                self._gpioOutInitValue = gpioOutInitValue
                self._sensor = Pin(self._pin, mode=Pin.OUT, value=self._gpioOutInitValue)
                self.reservedPins.add(self._pin)
                
            elif self._pinMode == 'adc-in':                
                self._sensor = ADC(self._pin)
                self.reservedPins.add(self.__adcPinToGPIO[self._pin])
        except:
            raise
        
        finally:
            self.__gpioAssignmentLock.release()
        
        if stateMachineID > -1:
            if self.setStateMachineNumber(stateMachineID) == False:
                self.setStateMachineNumber()


    def __validateInputs(self, pinNum, pinMode, gpioInType, gpioOutInitValue, stateMachineID):
        """
        Validates the parameter inputs for a GPIO Object.
        
        ≡≡≡ Required Parameters ≡≡≡
        pinNum:       int, representing a valid pin number (0-3 for ADC, 0-29
                           for GPIO)
        pinMode:      str, one of 'gpio-in', 'gpio-out', or 'adc-in'
        gpioInType:   str, sets a pull-up or pull-down resistor on a GPIO input.
                           Values are either 'up' or 'down', only used for
                           pinMode = 'gpio-in'
        gpioOutInitValue: int, sets the initial GPIO value for a GPIO Output. Values
                           may be either 0 (off) or 1 (on), only used for pinMode
                           = 'gpio-out'.
        stateMachineID:   int, may be a value from -1 to 7 where -1 means 'none'
              
        ≡≡≡ Raises ≡≡≡
        TypeError:  if the supplied parameter type is not correct.
        ValueError: if the supplied parameter is outside the legal range.
        
        ≡≡≡ Returns ≡≡≡
        bool: True if successful
        """
        strInputs = {'pinMode':pinMode, 'gpioInType':gpioInType}
        intInputs = {'pinNum':pinNum, 'gpioOutInitValue':gpioOutInitValue,
                     'stateMachineID':stateMachineID}
        
        for key in strInputs:
            if not isinstance(strInputs[key], str):
                raise TypeError("Parameter \'" +
                                key +
                                "\' received parameter of type \'" +
                                str(type(strInputs[key])) +
                                "\' - expected parameter of type \'str\'.")
        for key in intInputs:
            if not isinstance(intInputs[key], int):
                raise TypeError("Parameter \'" +
                                key +
                                "\' received parameter of type \'" +
                                str(type(intInputs[key])) +
                                "\' - expected parameter of type \'int\'.")
        
        if pinMode.lower() not in self.__pinModes:
            raise ValueError ("\'pinMode\' must be one of " +
                                  str(self.__pinModes) +
                                  ".")
        
        if pinMode.lower() == 'adc-in':
            if pinNum not in self.__adcPinValues:
                raise ValueError ("ADC pin number must be in range " +
                                  str(min(self.__adcPinValues)) +
                                  " to " + 
                                  str(max(self.__adcPinValues)) +
                                  ".")
            if self.__adcPinToGPIO[pinNum] in self.reservedPins:
                raise ValueError ("ADC" +
                                  str(pinNum) +
                                  " (aka: GPIO " +
                                  str(self.__adcPinToGPIO[pinNum]) +
                                  ") already assigned.")
        
        else:
            if pinNum not in self.__gpioPinValues:
                raise ValueError ("GPIO pin number must be in range " +
                                  str(min(self.__gpioPinValues)) +
                                  " to " + 
                                  str(max(self.__gpioPinValues)) +
                                  ".")
            if pinNum in self.reservedPins:
                raise ValueError ("GPIO_" +
                                  str(pinNum) +
                                  " is already assigned.")
            
            if pinMode.lower() == 'gpio-in':
                if gpioInType.lower() not in self.__gpioInTypes.keys() or gpioInType.lower() is 'none':
                    raise ValueError ("\'gpioInType\' must be one of " +
                                      str([key for key in self.__gpioInTypes.keys() if key is not 'none']) +
                                      ".")
                
            elif pinMode.lower() == 'gpio-out':
                if gpioOutInitValue not in self.__gpioOutInitValues:
                    raise ValueError ("\'gpioOutInitValue\' must be in range " +
                                  str(min(self.__gpioOutInitValues)) +
                                  " to " + 
                                  str(max(self.__gpioOutInitValues)) +
                                  ".")
            if stateMachineID not in self.__stateMachineIdNumbers:
                raise ValueError ("\'stateMachineID\' must be in range " +
                                  str(min(self.__stateMachineIdNumbers)) +
                                  " to " + 
                                  str(max(self.__stateMachineIdNumbers)) +
                                  ".")
        
        return True
    
    def getPin(self):
        """
        Returns the pin number of the GPIO Object. Could be a GPIO Pin (0-29)
        or an ADC Pin (0-3).
        """
        return self._pin
    
    def getName(self):
        """Returns the name of the GPIO object."""
        return self._name
    
    def getGPIOPin(self):
        """Returns the pin number as a GPIO pin number for the GPIO Object."""
        if self._pinMode == 'adc-in':                
            return self.__adcPinToGPIO[self._pin]
        else:
            return self._pin
    
    def getState(self):
        """
        Reads the current GPIO value.
         - For ADC readings, the value is averaged over 10 sensor readings to
           account for noise.
         - For GPIO readings, the pin's state is retrieved.
        
        ≡≡≡ Returns ≡≡≡
        For GPIO:        int, 0 or 1 representing a low/high state
        For ADC inputs:  float, representing a percentage of a full reading -
                         (readingValue/65535)
        """
        if self._pinMode == 'gpio-in' or self._pinMode == 'gpio-out':
            return self._sensor.value()
        elif self._pinMode == 'adc-in':
            rawReading = 0
            for i in range(10):
                rawReading += self._sensor.read_u16()
            return (rawReading/10)/65535

    def __str__(self):
        """Returns a brief string representation of a GPIO Object."""
        return (self._name +
                " (" +
                str(self._pinMode) +
                "_" +
                str(self._pin) +
                ")")

    def __repr__(self):
        """Returns a complete string representation of a GPIO Object."""
        return ("Name: " + str(self._name) +
                ", Pin #: " + str(self._pin) +
                ", PinMode: " + str(self._pinMode) +
                ", gpioInType: " + str(self._gpioInType) +
                ", gpioOutInitValue: " + str(self._gpioOutInitValue) +
                ", state machine ID: " + str(self.__getStateMachineNumber()) +
                ", Sensor Object: " + str(self._sensor)
                )
    
    def setStateMachineNumber(self, newID='auto'):
        """
        Reserves a state machine ID number for the GPIO Object.
         
        ≡≡≡ Optional Parameters ≡≡≡
        newID: may be either 'auto' or an integer in the range 0 to 8
        
        ≡≡≡ Raises ≡≡≡
        ResourceUnavailibleException: if no state machine ID's are availible
        
        ≡≡≡ Returns ≡≡≡
        bool: False if assignment was unsuccessful, True if successful
        """
        result = False
        
        if self.__getStateMachineNumber() is not -1:
            self.reservedStateMachines.remove(self.__getStateMachineNumber())
            self._stateMachineID = -1
        
        self.__smAssignmentLock.acquire()
        
        try:
            availibleStateMachineIdNumbers = (set(self.__stateMachineIdNumbers) -
                                              self.reservedStateMachines - {-1})
            
            if len(availibleStateMachineIdNumbers) < 1:
                raise ResourceUnavailibleException("All state machine ID\'s " +
                                                   "have been assigned.")
            elif newID in availibleStateMachineIdNumbers:
                self.reservedStateMachines.add(newID)
                self._stateMachineID = newID
                result = True
            elif newID == 'auto':
                newID = min(availibleStateMachineIdNumbers)
                self.reservedStateMachines.add(newID)
                self._stateMachineID = newID
                result = True
                
        except:
            raise
        
        finally:
            self.__smAssignmentLock.release()
            
        return result
            

    def __getStateMachineNumber(self):
        """Returns the state machine ID number of this GPIO Object."""
        return self._stateMachineID

