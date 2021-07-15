from UARTComms import *

import json
import select
import socket
import time
import traceback

from gpiozero import LED


uart = UARTComms()
loopTime = 0
sensorData = {}

addr = "localhost"
port = 50_000

s = socket.socket(family = socket.AF_INET, 
                  type = socket.SOCK_STREAM)

s.bind((addr, port))
s.listen(10)


recoveryAttempts = 0
cameraLEDTimer = 0

picoResetCoupler = LED(26)
cameraLED = LED(27)
alertLED = LED(22)


def SendTimeUpdateResponse():
    """
    Responds to a request for the current time. Sends as a 'Lossy' packet since
    the packet must be received and processed quickly in order to be relevant.
    By the time we identify that it needs to be resent, it is obsolete.

    The time sent is UTC.
    """
    uart.send('Lossy', json.dumps(['Time Response', int(time.time())]))

cntr = 0

try:
    while True:
        try:
            while True:
                # cntr += 1
                # if cntr%8 == 0:
                #     print("starting loop")
                #     print(f'{len(uart.receiveBuffer)}')
                #     cntr = 0

                activity = False

                # if abs(loopTime - time.time()) >= (10):
                #     loopTime = time.time()
                #     activity = True
                #     sent = uart.send('Lossy', json.dumps("TESTING STRING"))
                
                
                # Receive and process any incomming packets from UART
                # if uart.receivePacketsWaiting():
                receiveData = uart.receive()
                # print(f'{len(uart.receiveBuffer)}')
                # print(f'BUFFER:{uart.receiveBuffer}\n')
                # print(f'RD: {receiveData}\n\n')

                for packetData in receiveData:
                        activity = True
                        data = json.loads(packetData)
                        # print(data)
                        if data[0] == 'Time Request':
                            SendTimeUpdateResponse()
                        elif data[0] == 'event':
                            pass
                        elif data[0] == 'state':
                            sensorData = data[1]
                        else:
                            # Log other packets that have not been processed. <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
                            print('Received: {}'.format(packetData))
                

                # Resend any 'Lossless' packets that have not received an 'Ack'
                if uart.losslessPacketsWaiting():
                    bytesOut = uart.resendLosslessPackets()
                    if bytesOut > 0:
                        activity = True
                

                # Check for socket requests from the PHP server
                clientList, _, _ = select.select([s],[],[], (1/1000))
                for i in clientList:
                    activity = True
                    c, cAddr = i.accept()
                    data = c.recv(1024)
                    data = data.decode()
                    if data == "request":
                        c.send(json.dumps(sensorData).encode())
                    elif data == "cameraLEDOn":
                        cameraLEDTimer = time.time() + 30
                    elif data == "cameraLEDOff": 
                        cameraLEDTimer = time.time() - 1
                    elif data == "cameraLEDToggle":
                        if cameraLED.is_lit:
                            cameraLEDTimer = time.time() - 1
                        else:
                            cameraLEDTimer = time.time() + 30
                    elif data == "chickenDoorOpen":
                        uart.send('Lossless', json.dumps(['chickenDoorOpen','']))
                    elif data == "chickenDoorAuto": 
                        uart.send('Lossless', json.dumps(['chickenDoorAuto','']))
                    else:
                        print(type(data))
                        print(str(data))
                    c.close()


                # Actuate Camera LED light
                if cameraLEDTimer > time.time():
                    if not cameraLED.is_lit:
                        cameraLED.on()
                else:
                    cameraLED.off()



                # Monitor communications from Pi Pico and perform recovery actions
                if abs(uart.lastRXTime() - time.time()) >= 10:
                    recoveryAttempts += 1
                    alertLED.on()
                    uart.sendBreak()
                    uart.send('Connection Test', '')
                elif abs(uart.lastRXTime() - time.time()) >= 500:
                    print("ERROR: UARTCommsWatchdog recovery attempts: " +
                          str(recoveryAttempts) )
                    recoveryAttempts += 1
                    if recoveryAttempts%40 == 0:
                        picoResetCoupler.on()
                        time.sleep(100/1000)
                        picoResetCoupler.off()
                else:
                    recoveryAttempts = 0
                    alertLED.off()


                # Sleep for an appropriate amount of time
                if activity:
                    time.sleep(5/1000)
                else:
                    time.sleep(250/1000)

        except Exception as e:
            border = "=================================================================\n"
            with open('PiZeroBusinessLogicExceptions.txt',  mode='a', encoding='utf-8') as f:
                f.write(border)
                f.write(f"Date: {time.localtime()}\n")
                traceback.print_exc(file=f)
                f.write('\n')
                f.write(border)
                f.flush()
            

except:
    raise

finally:
    alertLED.on()
    cameraLED.off()
    s.shutdown(socket.SHUT_RDWR)
    s.close()

