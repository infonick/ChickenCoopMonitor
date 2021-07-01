# ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡
#
#    Raspberry Pi Pico AI Library - Sensor Class
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
from usys import path
# path.append('/RP2040-Pico-RTC')
path.append('/PicoDHT22')
# path.append('/AiLib')

from micropython import alloc_emergency_exception_buf
from micropython import schedule
from utime import sleep_ms
from utime import localtime
from utime import mktime
from machine import Pin
from machine import ADC
# from _thread import allocate_lock

from types import LambdaType

from DHT22 import DHT22
from SlidingDoorDriver import SlidingDoor
from AiLib import GPIO
from Event import Event

alloc_emergency_exception_buf(100)


class InoperativeSensorException(Exception):
    pass
class ResourceUnavailibleException(Exception):
    pass



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
                                    smID=self.__getStateMachineNumber())
        
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
      
    
