from machine import Pin
from machine import PWM
import _thread
from utime import sleep


# An LED frequency of 637hz is well above what chickens can percieve
# and so will not appear as a flickering light to them.
led = PWM(Pin(25))
led.freq(637)
led.duty_u16(2**12)


# from PicoCore0 import *
# from PicoCore1 import *
import PicoCore0
import PicoCore1

sleep(5) #just in case we need to halt the program before it gets on with the main loops.

_thread.start_new_thread(PicoCore1.PicoCore1, (PicoCore0.sensorDict, PicoCore0.actuatorDict))

PicoCore0.PicoCore0()