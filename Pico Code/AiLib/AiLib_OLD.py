# ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡
#
#    Raspberry Pi Pico AI Library
#
# ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡
# Classes that are defined in this library:
#   - GPIO: A generic GPIO pin class for 'gpio-in', 'gpio-out', and 'adc-in'
#   - Sensor: Extends the GPIO class for sensor devices.
#   - Actuator: Extends the GPIO class for actuators.
#   - Agent: A class representing an AI Agent
#   - Environment: 
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
from usys import path
path.append('/RP2040-Pico-RTC')
path.append('/PicoDHT22')
path.append('/AiLib')

from micropython import alloc_emergency_exception_buf
from micropython import schedule
from utime import sleep_ms
from utime import localtime
from utime import mktime
from machine import Pin
from machine import ADC
from _thread import allocate_lock

from types import LambdaType

from DHT22 import DHT22
from SlidingDoorDriver import SlidingDoor
#from RP2040_RTC import rp2RTC

from Events import Event

alloc_emergency_exception_buf(100)


class InoperativeSensorException(Exception):
    pass
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
    __adcPinValues = range(4)
    __adcPinToGPIO = [26,27,28,29]
    __gpioPinValues = range(30)
    __gpioOutInitValues = range(2)
    __stateMachineIdNumbers = range(-1,8)
    __pinModes = ['gpio-in', 'gpio-out', 'adc-in']
    __gpioInTypes = {'up':Pin.PULL_UP, 'down':Pin.PULL_DOWN, 'none':'none'}
    
    __gpioAssignmentLock = allocate_lock()
    __smAssignmentLock = allocate_lock
    
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
        TypeError:  if the supplied parameter type is not an integer
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
        self.__accessLock = allocate_lock
        
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
        TypeError:  if the supplied parameter type is not an integer
        ValueError: if the supplied parameter is outside the legal range
        
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
                ", state machine ID: " + str(self.__getStateMachineNumber) +
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
        
        if self.__getStateMachineNumber is not -1:
            self.__stateMachineIdNumbers.remove(self._stateMachineID)
            self._stateMachineID = -1
        
        self.__smAssignmentLock.acquire()
        
        try:
            availibleStateMachineIdNumbers = (set(self.__stateMachineIdNumbers) -
                                              self.reservedStateMachines - {-1})
            
            if availibleStateMachineIdNumbers < 1:
                raise ResourceUnavailibleException("All state machine ID\'s " +
                                                   "have been assigned.")
            elif newID in availibleStateMachineIdNumbers:
                self.__stateMachineIdNumbers.append(newID)
                result = True
            elif newID == 'auto':
                newID = min(availibleStateMachineIdNumbers)
                self.__stateMachineIdNumbers.append(newID)
                result = True
                
        except:
            raise
        
        finally:
            self.__smAssignmentLock.release()
            
        return result
            

    def __getStateMachineNumber(self):
        """Returns the state machine ID number of this GPIO Object."""
        return self._stateMachineID


# ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡
#
#    Sensor Class
#
# ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡

class Sensor(GPIO):
    """
    A Sensor class for embedded and attached sensor components.

    ≡≡≡ Attributes ≡≡≡
    reservedPins: a list of integers representing all GPIO pins that have been
                  assigned. Part of superclass GPIO.
    
    ≡≡≡ Methods ≡≡≡
    __init__(pinNum, pinMode, name=None, gpioInType='down', irq='none',
             driver='none', convFactorADC=None):
        Initializes a Sensor Object.
        
    __validateSensorInputs(pinMode, irq, driver, convFactorADC):
        Validates the parameter inputs for a Sensor Object.
        
    __str__():
        Returns a brief string representation of a Sensor Object.

    __repr__():
        Returns a complete string representation of a Sensor Object.
    
    getState():
        Reads the current sensor value.
         - For ADC readings, the conversion factor is applied to the average
           of 10 sensor readings to account for noise.
         - For GPIO readings involving a driver, the driver's reading is used.
         - For GPIO readings not involving a driver, the pin's state is retrieved.
    
    enableIRQ():
        Registers an IRQ for a sensor.
    
    disableIRQ():
        Disables an IRQ registered for a sensor.

    
    _ISR(pin):
        Interrupt Service Routine to handle IRQs.
            
    _irqHandler():
        IRQ Handler does necessary processing to account for an IRQ.
        
    getPin():
        Returns the pin number of the GPIO Object. Could be a GPIO Pin (0-29)
        or an ADC Pin (0-3). Part of superclass GPIO.
    
    getGPIOPin():
        Returns the pin number as a GPIO pin number for the GPIO Object. Part of
        superclass GPIO.
    
    getName():
        Returns the name of the GPIO object. Part of superclass GPIO.
    """
    __sensorPinModes = ['gpio-in', 'adc-in']
    __irqTypes = ['none', 'rising', 'falling', 'all']
    __sensorDrivers = ['none', 'dht22', 'slidingdoor']    
    

    def __init__(self, pinNum, pinMode, name=None, gpioInType='down', irq='none', driver='none', convFactorADC=None):
        """
        Initializes a Sensor object.
        
        ≡≡≡ Required Parameters ≡≡≡
        pinNum:  int, representing a valid pin number (0-3 for ADC, 0-29 for GPIO)
        pinMode: str, one of 'gpio-in', 'gpio-out', or 'adc-in'
        
        ≡≡≡ Optional Parameters ≡≡≡
        name:          str, a text name for the Sensor object
        gpioInType:    str, sets a pull-up or pull-down resistor on a GPIO input.
                            Values are either 'up' or 'down', only used for
                            pinMode = 'gpio-in'
        irq:           str, sets the sensor IRQ type to one of 'none',
                            rising', 'falling', or 'all'. Only used for
                            pinMode = 'gpio-in'
        driver:        str, represents a supported sensor driver. Only used for
                            pinMode = 'gpio-in'
        convFactorADC: lambda, representing a conversion factor function for
                               ADC readings. Only used for pinMode = 'adc-in'
         
        ≡≡≡ Raises ≡≡≡
        TypeError: if the supplied parameter type is not an integer
        ValueError: if the supplied parameter is outside the legal range
        ResourceUnavailibleException: if a state machine ID is requred but not availible
        InoperativeSensorException: If the sensor is not returning a reading when
                                    polled.
        """
        try:
            self.__validateSensorInputs(pinMode, irq, driver, convFactorADC)
        except:
            raise
        
        self._irq = 'none'
        self._convFactorADC = None
        self._driver = 'none'
        
        if driver.lower() == 'dht22' and pinMode == 'gpio-in':
            super(Sensor, self).__init__(pinNum=pinNum,
                                         pinMode='gpio-in',
                                         name=name,
                                         gpioInType='up',
                                         stateMachineID = 0)
            self._driver = driver.lower()
            self._driverObj = DHT22(dataPin = self._sensor,
                                    powerPin = None,
                                    dht11 = False,
                                    smID=self.__getStateMachineNumber)
        
        elif driver.lower() == 'slidingdoor' and pinMode == 'gpio-in':
            if pinNum+1 in self.reservedPins:
                raise ValueError ("GPIO_" +
                                  str(pinNum+1) +
                                  " is already assigned.")
            super(Sensor, self,).__init__(pinNum=pinNum,
                                         pinMode='gpio-in',
                                         name=(name+'_s1'),
                                         gpioInType=gpioInType)
            sensor1 = GPIO(pinNum = (pinNum+1), pinMode = 'gpio-in', name = (name+'_s1'), gpioInType = 'down')
            
            self._driver = driver.lower()
            self._driverObj = SlidingDoor(self, sensor1, name)
            
            self._irq = irq.lower()
            self.enableIRQ()
        
        else:
            super(Sensor, self).__init__(pinNum=pinNum,
                                         pinMode=pinMode,
                                         name=name,
                                         gpioInType=gpioInType)
        
        if self._pinMode == 'gpio-in' and self._driver == 'none':
            self._irq = irq.lower()
            self.enableIRQ()
        
        elif self._pinMode == 'adc-in':
            self._convFactorADC = convFactorADC
        
        
    def __validateSensorInputs(self, pinMode, irq, driver, convFactorADC):
        """
        Validates the parameter inputs for a GPIO Object.
        
        ≡≡≡ Required Parameters ≡≡≡
        pinMode:       str, either 'gpio-in' or 'adc-in'
        irq:           str, sets the sensor IRQ type to one of 'none',
                            rising', 'falling', or 'all'
        driver:        str, represents a supported sensor driver
        convFactorADC: lambda, representing a conversion factor function for
                               ADC readings
         
        ≡≡≡ Raises ≡≡≡
        TypeError:  if the supplied parameter type is not an integer
        ValueError: if the supplied parameter is outside the legal range
        
        ≡≡≡ Returns ≡≡≡
        bool: True if successful
        """
        strInputs = {'pinMode':pinMode, 'irq':irq, 'driver':driver}
        lamInputs = {'convFactorADC':convFactorADC}
        
        for key in strInputs:
            if not isinstance(strInputs[key], str):
                raise TypeError("Parameter \'" +
                                key +
                                "\' received parameter of type \'" +
                                str(type(strInputs[key])) +
                                "\' - expected parameter of type \'str\'.")
        for key in lamInputs:
            if not isinstance(lamInputs[key], LambdaType) and lamInputs[key] is not None:
                raise TypeError("Parameter \'" +
                                key +
                                "\' received parameter of type \'" +
                                str(type(intInputs[key])) +
                                "\' - expected parameter of type " +
                                "\'types.LambdaType\'.")
        
        if pinMode.lower() not in self.__sensorPinModes:
            raise ValueError ("\'pinMode\' must be one of " +
                                  str(self.__sensorPinModes) +
                                  ".")
        if pinMode.lower() == 'adc-in' and convFactorADC is None:
            raise ValueError ("\'convFactorADC\' must be a lambda expression " +
                              "for pinMode = \'adc-in\'.")
        if irq.lower() not in self.__irqTypes:
            raise ValueError ("\'irq\' must be one of " +
                                  str(self.__irqTypes) +
                                  ".")
        if driver.lower() not in self.__sensorDrivers:
            raise ValueError ("\'sensorDriver\' must be one of " +
                                  str(self.__sensorDrivers) +
                                  ".")
        return True


    def __str__(self):
        """Returns a brief string representation of a Sensor Object."""
        out = super(Sensor, self).__str__()
        out += ": " + str(self.getState())
        return out


    def __repr__(self):
        """Returns a complete string representation of a Sensor Object."""
        out = super(Sensor, self).__repr__()
        out += (", Sensor Reading: " + str(self.getState()) +
                ", IRQ Type: " + str(self._irq) +
                ", Sensor Driver: " + str(self._driver)
                )
        if self._driver is not 'none':
            out += ", Driver Object: " + str(self._driverObj)
        return out


    def getState(self):
        """
        Reads the current sensor value.
         - For ADC readings, the conversion factor is applied to the average
           of 10 sensor readings to account for noise.
         - For GPIO readings involving a driver, the driver's reading is used.
         - For GPIO readings not involving a driver, the pin's state is retrieved.
        
        ≡≡≡ Raises ≡≡≡
        InoperativeSensorException: If the sensor is not returning a reading.
        
        ≡≡≡ Returns ≡≡≡
        For GPIO inputs:  int or 0 or 1 representing a low/high state
        For ADC sensors:  return type is dependent on the conversion factor lambda
        For DHT22 driver: a dict of {'temp':temp, 'rh':rh} is returned
        """
        if self._driver == 'dht22':
            self.__accessLock.acquire()
            try:
                for i in range(5):
                    temp, rh = self._driverObj.read()
                    if temp is not None and rh is not None:
                        return {'temp':temp, 'rh':rh}
                    # Try again in a bit - the sensor can't cope with a shorter delay
                    sleep_ms(500)
                raise InoperativeSensorException("DHT22 sensor \'" +
                                                 str(self._name) +
                                                 "\' on " +
                                                 str(self._pinMode) + "_" +
                                                 str(self._pin) +
                                                 " is not responding.")
            except:
                raise
            finally:
                self.__accessLock.release()
        
        elif self._driver == 'slidingdoor':
            return self._driverObj.getState()
        
        elif self._pinMode == 'gpio-in':
            return super(Sensor, self).getState()
        
        elif self._pinMode == 'adc-in':
            return self._convFactorADC(super(Sensor, self).getState())
        
        
    def enableIRQ(self):
        """Registers an IRQ for a sensor.""" 
        self._irqCurrentValue = self.getState()
        self._irqNewValue = self._irqCurrentValue
        self._irqTriggered = False
        print(str(self._driver))
        if self._driver == 'slidingdoor':
            self._driverObj.enableIRQ()
        elif self._irq == 'rising':
            self._sensor.irq(trigger = Pin.IRQ_RISING , handler = self._ISR)
        elif self._irq == 'falling':
            self._sensor.irq(trigger = Pin.IRQ_FALLING, handler = self._ISR)
        elif self._irq == 'all':
            self._sensor.irq(trigger = Pin.IRQ_RISING | Pin.IRQ_FALLING,
                             handler = self._ISR)
    
    
    def disableIRQ(self):
        """Disables an IRQ registered for a sensor."""
        if self._driver == 'slidingdoor':
            self._driverObj.disableIRQ()
        else:
            self._sensor.irq(trigger = 0, handler = None)

    
    def _ISR(self, pin): #NEEDS TO BE COMPLETED <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        """Interrupt Service Routine to handle IRQs"""
        try:
            if not self._irqTriggered:
                schedule(Sensor._irqHandler, self)
                self._irqTriggered = True
        
        # A full scheduler throws a runtime error
        except RuntimeError as e:
            print(str(e) + " for " + self.getName())
            #Log an error <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
            
            
    def _irqHandler(self): 
        """IRQ Handler does necessary processing to account for an IRQ"""
        time = mktime(localtime())
        count = 0
        maxCount = 10
        tries = 0
        maxTries = 150 # guarantees the while loop does not become infinite
        
        # Sensor must show stability for 10ms in order to be debounced
        for i in range(10):
            self._irqNewValue = self.getState()
            while count < maxCount and tries < maxTries:
                tries += 1
                if self._irqNewValue == self.getState():
                    count += 1
                else:
                    break
                sleep_ms(1)
            if count >= maxCount:
                break
            else:
                count = 0
  
        if count >= maxCount:
            if self._irqNewValue != self._irqCurrentValue:
                    eventDetail = {'sensorPin': self.getPin(),
                                   'newState': self._irqNewValue,
                                   'oldstate': self._irqCurrentValue}
                    self._irqCurrentValue = self._irqNewValue
                    print(self.__str__())
                    Event('IRQ Triggered', eventDetail, time=time)
        else:
            print("ERROR: _irqHandler count: " + str(count) + "/" + str(maxCount) + "\n" +
                  "tries: " + str(tries) + "/" + str(maxTries) + "\n" +
                  self.__str__())
            #Log an error <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        self._irqTriggered = False
      
    
    
    
# ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡
#
#    Actuator  Class
#
# ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡
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
        except:
            raise
        finally:
            self.__accessLock.release()
        
        if self._reverseStates:
            if stateInt == 0:
                stateInt = 1
            elif stateInt == 1:
                stateInt = 0
        
        if asString:
            return str(self.__gpioOutInitValueTypeNames[stateInt])
        else:
            return stateInt
    
    
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

            
        
        
# ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡
#
#    Agent Class
#
# ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡

class Agent():
    """
    An Agent class for AI decision making.

    ≡≡≡ Attributes ≡≡≡

    ≡≡≡ Methods ≡≡≡

    """

    
    def __init__(self, program, goals):
        """
        Initializes an Agent object.
        
        ≡≡≡ Required Parameters ≡≡≡
        
        ≡≡≡ Optional Parameters ≡≡≡
         
        ≡≡≡ Raises ≡≡≡
        TypeError:  if the supplied parameter type is not an integer
        ValueError: if the supplied parameter is outside the legal range
        """
        try:
            self.__validateAgentInputs(program, goals)
        except:
            raise
        
        self.program = program
        



    def __validateAgentInputs(self, program, goals):
        """
        Validates the parameter inputs for an Agent Object.
        
        ≡≡≡ Required Parameters ≡≡≡
         
        ≡≡≡ Raises ≡≡≡
        TypeError:  if the supplied parameter type is not an integer
        ValueError: if the supplied parameter is outside the legal range
        
        ≡≡≡ Returns ≡≡≡
        bool: True if successful
        """
  
        return True

    
    
    

class Environment():
    
    def __init__(self, agent, sensors=[], actuators=[]):
        self.sensors = sensors
        self.actuators = actuators
        self.agent = agent
    
    def run(self):
        percepts = self.percepts()
        actions = self.agent.program(percepts)
                    
        if actions is not None:
            self.execute_actions(actions)
            
            eventDetail = {'actions': actions,
                           'percepts': percepts}
            Event('Agent Action', eventDetail)
    
    def percepts(self):
        perceptStates = {}
        actuatorStates = {}
        
        for sensor in self.sensors:
            if sensor.getName() not in perceptStates.keys():
                try:
                    perceptStates[sensor.getName()] = sensor.getState()
                except InoperativeSensorException:
                    perceptStates[sensor.getName()] = None
                    # Log Error <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
            else:
                # Log Error <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
                pass
                
        for actuator in self.actuators:
                if actuator.getName() not in actuatorStates.keys():
                    actuatorStates[actuator.getName()] = actuator.getState()
                else:
                    actuatorStates[actuator.getName()+'_DuplicateName'] = actuator.getState()
                    
        return (perceptStates, actuatorStates)
    
    def execute_actions(self, actions):
        for (act, value) in actions:
            act(value)
