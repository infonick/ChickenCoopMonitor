from micropython import alloc_emergency_exception_buf
alloc_emergency_exception_buf(100)

import gc
if not gc.isenabled():
    gc.enable()

from UARTComms import *
from UARTCommsWatchdog import *

u = UARTComms()
w = UARTCommsWatchdog(u)

from time import sleep


while True:
    u.receive()
    u.resendLosslessPackets()
    sleep(100/1000)