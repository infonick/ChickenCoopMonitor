from time import time
from UARTComms import UARTComms
from os import uname


__UNAME_PICO = 'Raspberry Pi Pico with RP2040'
__UNAME_ZERO = 'armv6l'

if uname()[4] == __UNAME_ZERO:
    pass

if uname()[4] == __UNAME_PICO:
    from micropython import alloc_emergency_exception_buf
    alloc_emergency_exception_buf(100)

    import gc
    if not gc.isenabled():
        gc.enable()
        
    from machine import Timer
    from micropython import schedule



class UARTCommsWatchdog():
    """
    A class that works in concert with the UARTcomms class to ensure that
    regular successful communications are being received.

    ≡≡≡ Attributes ≡≡≡
    TIMER_PERIOD_MS:       The time in milliseconds between followups.
    MAX_RECOVERY_ATTEMPTS: The maximum number of times the watchdog will
                           attempt to communicate before taking recovery
                           actions.
    
    ≡≡≡ Methods ≡≡≡
    __init__(UARTCommsObj):
        Validates the parameter inputs for, and instantiates, a
        UARTCommsWatchdog Object.
    
    enable():
        Enables the UARTCommsWatchdog object.
        
    disable():
        Disables the UARTCommsWatchdog object.
        
    _ISR():
        Interupt Service Routine used as a callback function when the watchdog
        timer expires.

    _irqHandler(): 
        does the necessary processing for a triggered watchdog object.

    """
    
    TIMER_PERIOD_MS = 5_000
    MAX_RECOVERY_ATTEMPTS = 3
    
    
    def __init__(self, UARTCommsObj):
        """
        Validates the parameter inputs for, and instantiates, a UARTComms Object.
        
        ≡≡≡ Required Parameters ≡≡≡
        UARTCommsObj: an instantiated UARTComms object that can be used for
                      sending and receiving packets over UART.
              
        ≡≡≡ Raises ≡≡≡
        TypeError: if the supplied parameter type is not correct
        
        ≡≡≡ Returns ≡≡≡
        UARTCommsWatchdog Object
        """
        if not isinstance(UARTCommsObj, UARTComms):
            raise TypeError('The supplied parameter was not a UARTComms object.')
        
        self.uart = UARTCommsObj
        self.recoveryAttempts = 0
        self.timer = Timer()
        self.enable()
        
        
    def enable(self):
        """Enables the UARTCommsWatchdog object."""
        self.timer.init(mode = Timer.PERIODIC,
                        period = self.TIMER_PERIOD_MS,
                        callback = self._ISR)
    
    
    def disable(self):
        """Disables the UARTCommsWatchdog object."""
        self.timer.deinit()
        
        

    def _ISR(self, t):
        """
        Interupt Service Routine used as a callback function when the watchdog
        timer expires. Schedules the _irqHandler function to run at a safe
        time if the watchdog is being triggered.
        
        A full scheduler throws a runtime error. This is not a problem since
        the ISR will run again during the next timer iteration if it still
        needs to be triggered.
        """
        try:
            if abs(self.uart.lastRXTime() - time()) >= (self.TIMER_PERIOD_MS/1_000):
                schedule(UARTCommsWatchdog._irqHandler, self)
            else:
                self.recoveryAttempts = 0
                
        except RuntimeError:
            pass
    
    
    def _irqHandler(self): 
        """
        _irqHandler does the necessary processing for a triggered watchdog
        object. If less than the maximum number of recovery attempts have been
        attempted, a connection test will be sent as a heartbeat packet (the
        other side will reply with an 'Ack' which counts as TX/RX activity).
        If less than the maximum number of recovery attempts have been
        attempted, then a recovery procedure will be undertaken.
        """
        self.recoveryAttempts += 1
        if self.recoveryAttempts <= self.MAX_RECOVERY_ATTEMPTS:
            try:
                self.uart.send('Connection Test', '')
            except:
                raise
            
        else:
            # Implement Recovery Procedure here
            print("ERROR: UARTCommsWatchdog recovery attempts: " +
                  str(self.recoveryAttempts) )
            # Process recovery actions <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
            # Process user alert actions
            # Log the use of recovery actions