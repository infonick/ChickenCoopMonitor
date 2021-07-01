from machine import Pin
from micropython import alloc_emergency_exception_buf
from micropython import schedule
from utime import sleep_ms
from utime import localtime
from utime import mktime
from Event import Event

# from AiLib import GPIO
# from AiLib import Sensor

alloc_emergency_exception_buf(100)

class SlidingDoor():
    """
    A Sensor class for sliding doors.

    ≡≡≡ Attributes ≡≡≡
    reservedPins: a list of integers representing all GPIO pins that have been
                  assigned. Part of superclass GPIO.
    
    ≡≡≡ Methods ≡≡≡
    __init__(pinNum, pinMode, name=None, gpioInType='down', irq='none',
             driver='none', convFactorADC=None):
        Initializes a Sliding Door Sensor Object.

    
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
        
    """
    __validStates = ['Unknown', 'Closing', 'Closed', 'Opening', 'Open']
    
    def __init__(self, sensor0, sensor1, name):
        # Closed position sensor
        self.sensor0 = sensor0
        # Open position sensor
        self.sensor1 = sensor1
        self.name = name
        self.setState()
    
    
    def setState(self):
        if self.genS0State():
            self.state = 2
        elif self.sensor1.getState():
            self.state = 4
        else:
            self.state = 0
            
    
    def getState(self, asint = False):
        if asint:
            return self.state
        else:
            return SlidingDoor.__validStates[self.state]
    
    
    def genS0State(self):
        return self.sensor0._sensor.value()

    
    def enableIRQ(self):
        """Registers an IRQ for each sensor.""" 
        self._irqTriggered = False

        self.sensor0._sensor.irq(trigger = Pin.IRQ_RISING | Pin.IRQ_FALLING,
                                 handler = self._ISR)
        self.sensor1._sensor.irq(trigger = Pin.IRQ_RISING | Pin.IRQ_FALLING,
                                 handler = self._ISR)
    
    
    def disableIRQ(self):
        """Disables the IRQs registered for the sensors."""
        self.sensor0._sensor.irq(trigger = 0, handler = None)
        self.sensor1._sensor.irq(trigger = 0, handler = None)
    
    
    def _ISR(self, pin): #NEEDS TO BE COMPLETED <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        """Interrupt Service Routine to handle sliding door IRQs"""
        try:
            if not self._irqTriggered:
                schedule(SlidingDoor._irqHandler, self)
                self._irqTriggered = True
                print('sldr ISR: ' + str(pin))
        
        # A full scheduler throws a runtime error
        except RuntimeError as e:
            print(str(e) + " for " + self.name)
            #Log an error <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
            
            
    def _irqHandler(self): 
        """IRQ Handler does necessary processing to account for an IRQ"""
        time = mktime(localtime())
        newState = -1
        count = 0
        maxCount = 10
        tries = 0
        maxTries = 150 # guarantees the while loop does not become infinite
        
        # Sensors must show stability for 10ms in order to be debounced
        for i in range(10):
            irqNewValue0 = self.genS0State()
            irqNewValue1 = self.sensor1.getState()
            while count < maxCount and tries < maxTries:
                tries += 1
                if (irqNewValue0 == self.genS0State() and
                   irqNewValue1 == self.sensor1.getState()):
                    count += 1
                else:
                    break
                sleep_ms(1)
            if count >= maxCount:
                break
            else:
                count = 0
  
        if count >= maxCount:
            if self.getState(asint=True) in [0,1,3]:
                if irqNewValue0:
                    newState = 2
                elif irqNewValue1:
                    newState = 4
                else:
                    newState = 0
            if self.getState(asint=True) in [2,4]:
                if self.getState(asint=True) == 2:
                    newState = 3
                elif self.getState(asint=True) == 4:
                    newState = 1
                else:
                    newState = 0     
                    
            
            if self.getState(asint=True) != newState:
                    eventDetail = {'sensorPin': self.sensor0.getPin(),
                                   'newState': SlidingDoor.__validStates[newState],
                                   'oldstate': SlidingDoor.__validStates[self.getState(asint=True)]}
                    self.state = newState
                    Event('IRQ Triggered', eventDetail, time=time)
        else:
            print("ERROR: _irqHandler count: " + str(count) + "/" + str(maxCount) + "\n" +
                  "tries: " + str(tries) + "/" + str(maxTries) + "\n" +
                  self.__str__())
            self.setState()
            #Log an error <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        self._irqTriggered = False
        
