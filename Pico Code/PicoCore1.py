# ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡
#
#    Raspberry Pi Pico Core 1 Driver
#
# ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡
#
# This driver program managees the Pi Pico's communications. The following
# functions are undertaken:
#   - Data is sent and recieved over UART.
#   - The system's RTC is periodically checked for accuracy.
#   - A watchdog process monitors for regular UART traffic and either confirms
#     that the connections is still up or initiates a recovery routine.
#
# The driver is run by calling the 'PicoCore1()' function.
# 
# ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡
# REVISION HISTORY:
#   - 
#
# ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡

from UARTComms import *
from UARTCommsWatchdog import *

from usys import path
if '/RP2040-Pico-RTC' not in path:
    path.append('/RP2040-Pico-RTC')

from micropython import alloc_emergency_exception_buf
alloc_emergency_exception_buf(100)

import gc
if not gc.isenabled():
    gc.enable()
    
import machine
import json
import utime


from RP2040_RTC import rp2RTC
import Event


uart = UARTComms()
loopTime = 0
lastTimeUpdate = 0
lastTimeUpdateRequest = 0



def TimeUpdate(timeResponse):
    """Updates the pico RTC if it is not accurate."""
    global lastTimeUpdate
    if not isinstance(timeResponse, int):
        SendTimeUpdateRequest()
        # LOG AN ISSUE WITH THE TIME UPDATE PROCEDURE < < < < < < < < < < < < < < < < < < < < < < < < < < < <
                    
    elif round(abs(timeResponse - utime.time())) > 1:
        (year, month, day, hour, minute, second, _, _) = utime.localtime(timeResponse)
        rp2RTC.setRTC(year, month, day, hour, minute, second)
        lastTimeUpdate = timeResponse
        # update timestamps for any pending messages, logs, etc. <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        # load pending messages into UARTmsgs.outboundQueue <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    else:
        lastTimeUpdate = timeResponse

def SendTimeUpdateRequest():
    """
    Requests the current time in order to check that the RTC is accurate. Does
    not repeat the request if one had already been sent out in the last second.
    
    The expected time received is UTC.
    """
    global lastTimeUpdateRequest
    now = utime.ticks_ms()
    if abs(utime.ticks_diff(now, lastTimeUpdateRequest)) >= 1000:
        uart.send('Lossless', json.dumps(['Time Request', '']))
        lastTimeUpdateRequest = now



# ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡
# Main program loop
# ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡

def PicoCore1(sensorDict, actuatorDict):
    global loopTime
    global lastTimeUpdate
    global lastTimeUpdateRequest
    global uart
    
    uartWatchdog = UARTCommsWatchdog(uart, actuatorDict['Alert LED'])

    try:
        while True:
            gc.collect()
            activity = False
            
            # Check that Pico RTC is on-time once per day
            if abs(lastTimeUpdate - utime.time()) > 86_400:
                SendTimeUpdateRequest()
            
            
            # Check for events to send out over UART
            if len(Event.Event.eventQueue) > 0:
                activity = True
                for i in range(len(Event.Event.eventQueue)):
                    e = Event.Event.eventQueue.popleft()
                    uart.send('Lossless', json.dumps(['event',
                                                      e.getDict()]
                                                     )
                              )
                    print('Event: {}; {}; {}'.format(e.getEventType(),
                                                     e.getEventDetails(),
                                                     e.getEventTime()
                                                     )
                          )
            
                        
            
            # Periodically send sensor and acutator states out over UART
            if abs(loopTime - utime.time()) > 1:
                loopTime = utime.time()
                activity = True
                msg = {}
                
                for s in sensorDict.keys():
                    if isinstance(sensorDict[s].getState(), dict):
                        name = str(sensorDict[s].getName())
                        state = sensorDict[s].getState()
                        for subState in state:
                            msg[name + ' ' + subState] = state[subState]
                    else:
                        msg[str(sensorDict[s].getName())] = sensorDict[s].getState()
                
                for a in actuatorDict.keys():
                    if actuatorDict[a].getGPIOPin() in [6,7,16,17]:
                        msg[str(actuatorDict[a].getName())] = actuatorDict[a].getState(asString=True)

                uart.send('Lossy', json.dumps(['state', msg]))

            
            
            # Receive and process any incomming packets from UART
            if uart.receivePacketsWaiting():
                activity = True
                receiveData = uart.receive()
                for packetData in receiveData:
                    data = json.loads(packetData)
                    
                    if data[0] == 'Time Response':
                        TimeUpdate(data[1])
                    elif data[0] == 'chickenDoorOpen':
                        actuatorDict['Doorkeeper Override'].setState('on')
                    elif data[0] == 'chickenDoorAuto':
                        actuatorDict['Doorkeeper Override'].setState('off')
                    else:
                        # Other data types can be handled here. <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
                        print('Received: {}'.format(packetData))
            
            
            # Resend any 'Lossless' packets that have not received an 'Ack'
            if uart.losslessPacketsWaiting():
                bytesOut = uart.resendLosslessPackets()
                if bytesOut > 0:
                    activity = True
            
            
            # Sleep for an appropriate amount of time
            if activity:
                utime.sleep(5/1000)
            else:
                utime.sleep(250/1000)

    except Exception as e:
        file = open("ErrorLogCore1.txt", "a")
        file.write(str(e) + "\n\n")
        file.flush()
        file.close()
        raise

    finally:
        from time import sleep
        from machine import Pin
        from machine import PWM

        # An LED frequency of 637hz is well above what chickens can percieve
        # and so will not appear as a flickering light to them.
        led = PWM(Pin(25))
        led.freq(637)
        while True:
            led.duty_u16(2**15)
            sleep(1)
            led.duty_u16(2**13)
            sleep(1)
