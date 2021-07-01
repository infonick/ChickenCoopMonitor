from binascii import crc32
from math import floor
from time import time
from os import uname


__UNAME_PICO = 'Raspberry Pi Pico with RP2040'
__UNAME_ZERO = 'armv6l'

if uname()[4] == __UNAME_ZERO:
    import serial
    
elif uname()[4] == __UNAME_PICO:
    from machine import Pin
    from machine import UART



class PacketError(Exception):
    pass

class OversizePKTError(Exception):
    pass

class UnsupportedSYSError(Exception):
    pass



class UARTComms():
    """
    A class that establishes a protocol for communicating over UART.
    
    UARTComms allows for data to be transmitted either in 'Lossy' packets
    (without acknowlegement), or as 'Lossless' packets (require acknowledgement
    to guarantee delivery). If data packets become malformed they are discarded.
    A crc32 checksum is used to validate packet integrity. This class does not
    automatically send and receive packets, so the user must provide a driver
    program that periodically performs send and receive functions. The
    UARTComms packet format is diagrammed at the end of this docstring for
    reference.
    
    Any use of this class should utilize all three of the following methods:
      - receive():               To receive packets from the UART hardware
                                 buffer
      - send(pktType, pktData):  To transmit packets over UART
      - resendLosslessPackets(): To re-transmit any 'Lossless' packets that
                                 have not yet been acknowledged by the other
                                 side.
    
    This class works with:
      - Raspberry Pi Pico
      - Raspberry Pi Zero (with the pyserial library and the PL011 UART)
      - May work with other Raspberry Pi SBC's with the pyserial library and
        the PL011 UART. Disabling the Rasberry Pi onboard bluetooth is required
        to make the PL011 UART available. See
        https://www.raspberrypi.org/documentation/configuration/uart.md
    

    ≡≡≡ Attributes ≡≡≡
    MAX_PACKET_SIZE: Maximum packet size in bytes, including the 12-byte
                     header.
    PACKET_TYPES:    A list of valid communication packet types. 'Ack'
                     packets should only be used internally by this class.
    
    UART_BAUDRATE:
    UART_BITS:
    UART_STOPBITS:
    UART_PARITY:
    UART_TIMEOUT:
    UART_TXRXBUFFER:
    UART_PICO_TX_PINS:
    UART_PICO_RX_PINS:

    
    ≡≡≡ Methods ≡≡≡
    __init__(uartPortID = __DEFAULT_SERIAL_PORT_ID):
        Validates the parameter inputs for, and instantiates, a UARTComms Object.
    
    receive():
        Reads and receives UARTComms packets from the UART hardware buffer.
        
    send(pktType, pktData):
        Transmits a UARTComms packet.
    
    resendLosslessPackets():
        Re-transmits any Lossless packets that have been sent and no Ack has
        been received to confirm their successful transmission.
    
    receivePacketsWaiting():
        Returns a boolean True if the UART receive buffer has information
        for processing. False if the UART receive buffer is empty.
    
    losslessPacketsWaiting():
        Returns a boolean True if there are Lossless packets that have been
        sent and no Ack has been received to confirm their successful
        transmission.
        
    lastRXTime():
        Returns the timestamp of the last received transmission. Useful with
        a watchdog process that monitors for regular successful activity.
        
    
    
    __updateRXTime():
        Updates the timestamp of the last received transmission.
    
    __pktDecode(msg):
        Decodes a data packet from a transmission.
    
    __pktEncode(pktType, pktData, seqNum):
        Encodes a data packet as a bytes object for transmission.
    
    __nextSeqNum():
        Returns an int representing the next transmission sequence number to use.
        
    __getIncommingBufferSize():
        Returns an int representing the number of bytes waiting in the UART
        receive buffer.
    
    __pareReceiveBuffer():
        Trims the front of the software receive buffer until a valid packet
        start sequence is identified.

    __pktChecksum(msgBytes):
        Calculates and returns a checksum for a packet. 



    ≡≡≡ UARTComms PACKET FORMAT ≡≡≡
    
      |-1-||-2--||3-||4-||5||-6-|
    b' URT  cksm  lt  sq  t  dta '
    
    1: Start sequence "URT"
    2: 4-byte checksum (little endian)
    3: 2-byte length (little endian)
    4: 2-byte sequence number (little endian)
    5: 1-byte message type ID number (little endian)
    6: packet data (0 to many bytes)
    
    """
    MAX_PACKET_SIZE = 1024
    PACKET_TYPES = ['Ack',
                    'Lossy',
                    'Lossless',
                    'Connection Test'
                   ]
        
        
    __MAX_SEQUENCE_NUMBER = 65_536
    __PACKET_HEADER_SIZE = 12
    __PACKET_START_SEQUENCE = b'URT'
    
    __UNAME_PICO = 'Raspberry Pi Pico with RP2040'
    __UNAME_ZERO = 'armv6l'
    __SERIAL_PORT_ID_PICO = [0, 1]
    __SERIAL_PORT_ID_ZERO = ['/dev/serial0',
                             '/dev/serial1']
    __SYSTEM_ID = ''
    __DEFAULT_SERIAL_PORT_ID = 0
    
    UART_BAUDRATE = 115_200
    UART_BITS = 8
    UART_STOPBITS = 1
    UART_PARITY = 1     # 0, 1, or None
    UART_TIMEOUT = 1
    UART_TXRXBUFFER = min(32_766, max(4096, MAX_PACKET_SIZE*2)) # Maximum ~32766 on Pi Pico
    
    if uname()[4] == __UNAME_ZERO:
        if UART_PARITY == 0:
            UART_PARITY = serial.PARITY_EVEN
        elif UART_PARITY == 1:
            UART_PARITY = serial.PARITY_ODD
        elif UART_PARITY is None:
            UART_PARITY = serial.PARITY_NONE
        __SYSTEM_ID = 'PiZero'
        __DEFAULT_SERIAL_PORT_ID = '/dev/serial0'
    
    elif uname()[4] == __UNAME_PICO:
        UART_PICO_TX_PINS = [Pin(0), Pin(4)]
        UART_PICO_RX_PINS = [Pin(1), Pin(5)]
        __SYSTEM_ID = 'PiPico'
        __DEFAULT_SERIAL_PORT_ID = 0

    
    
    def __init__(self, uartPortID = __DEFAULT_SERIAL_PORT_ID):
        """
        Validates the parameter inputs for, and instantiates, a UARTComms Object.
        
        ≡≡≡ Required Parameters ≡≡≡
        uartPortID:   either 1 or 0 for the Pi Pico or one of '/dev/serial0' or
                      '/dev/serial1' for the Pi Zero
                      Default for Pi Pico: 0
                      Default for Pi Zero: '/dev/serial0'
              
        ≡≡≡ Raises ≡≡≡
        TypeError:           if the supplied parameter type is not correct
        ValueError:          if the supplied parameter value is incorrect
        UnsupportedSYSError: if the detected system is not supported by the
                             protocol
        
        ≡≡≡ Returns ≡≡≡
        UARTComms Object
        """
        if self.__SYSTEM_ID == 'PiZero':
            if uartPortID not in self.__SERIAL_PORT_ID_ZERO:
                raise ValueError('\'uartPortID\' is not valid. Must be one of: '
                                 + str(self.__SERIAL_PORT_ID_ZERO)
                                 + '.')
            
            self.uart = serial.Serial(uartPortID,
                                      baudrate = self.UART_BAUDRATE, 
                                      parity = self.UART_PARITY, 
                                      stopbits = self.UART_STOPBITS, 
                                      bytesize = self.UART_BITS, 
                                      timeout = self.UART_TIMEOUT)
            
        elif self.__SYSTEM_ID == 'PiPico':
            if uartPortID not in self.__SERIAL_PORT_ID_PICO:
                raise ValueError('\'uartPortID\' is not valid.Must be one of: '
                                 + str(self.__SERIAL_PORT_ID_PICO)
                                 + '.')
        
            self.uart = UART(uartPortID,
                             baudrate = self.UART_BAUDRATE,
                             bits = self.UART_BITS,
                             parity = self.UART_PARITY,
                             stop = self.UART_STOPBITS,
                             tx = self.UART_PICO_TX_PINS[uartPortID],
                             rx = self.UART_PICO_RX_PINS[uartPortID],
                             txbuf = self.UART_TXRXBUFFER,
                             rxbuf = self.UART_TXRXBUFFER,
                             timeout = self.UART_TIMEOUT,
                             timeout_char = self.UART_TIMEOUT)
            
        else:
            raise UnsupportedSYSError('\'{}\''.format(uname()[4]) +
                                      ' is not supported by UARTComms.')
    
        self.seqNumber = 0
        self.outboundPackets = {}
        self.receiveBuffer = b''
        self.rxTime = time()
    
    
    def __nextSeqNum(self):
        """
        Returns an int representing the next transmission sequence number to use.
        """
        seqNumber = self.seqNumber
        self.seqNumber = (self.seqNumber + 1) % self.__MAX_SEQUENCE_NUMBER
        return seqNumber
    
    
    def __getIncommingBufferSize(self):
        """
        Returns an int representing the number of bytes waiting in the UART
        receive buffer.
        """
        buffSize = 0
        
        if self.__SYSTEM_ID == 'PiZero':
            buffSize = self.uart.in_waiting
            
        elif self.__SYSTEM_ID == 'PiPico':
            buffSize = self.uart.any()
        
        return buffSize
    

    def __pareReceiveBuffer(self):
        """
        Trims the front of the software receive buffer until a valid packet
        start sequence is identified.
        """
        startSeqLength = len(self.__PACKET_START_SEQUENCE)
        startSeq = self.__PACKET_START_SEQUENCE
            
        while ((len(self.receiveBuffer) > startSeqLength) and
               (self.receiveBuffer[:startSeqLength] != startSeq)):
            self.receiveBuffer = self.receiveBuffer[1:]


    def receivePacketsWaiting(self):
        """
        Returns a boolean True if the UART receive buffer has information
        for processing. False if the UART receive buffer is empty.
        """
        if self.__getIncommingBufferSize() > 0:
            return True
        else:
            return False


    def receive(self):
        """
        Reads and receives UARTComms packets from the UART hardware buffer.
        
        The receive routine will run until it either runs out of packets to
        process or has processed > 1024 bytes, at which time it breaks to
        return control so as not to starve other processes or consume all
        availible memory.
        
        ≡≡≡ Returns ≡≡≡
        receiveData: a list of packet data received. Each list item is the
                     data from one packet.
        """
        buffSize = self.__getIncommingBufferSize()
        self.receiveBuffer += self.uart.read(buffSize)
        
        receiveData = []
        totalBytesReceived = 0
        processingBuffer = True
        
        while processingBuffer:   
            self.__pareReceiveBuffer()
            
            if totalBytesReceived > 1024:
                processingBuffer = False
                break
            
            if len(self.receiveBuffer) < self.__PACKET_HEADER_SIZE:
                processingBuffer = False
                break
            
            nextPacketLength = int.from_bytes(self.receiveBuffer[7:9], 'little')
            
            if len(self.receiveBuffer) < nextPacketLength:
                processingBuffer = False
                break
            else:
                msg = self.receiveBuffer[:nextPacketLength]
                try:
                    pktType, pktData, seqNum = self.__pktDecode(msg)
                except PacketError:
                    self.receiveBuffer = self.receiveBuffer[1:]
                    continue
                
                self.__updateRXTime()
            
                if pktType == 'Ack':
                    try:
                        self.outboundPackets.pop(pktData)
                    except KeyError:
                        pass
                    
                elif pktType in ['Lossless', 'Connection Test']:
                    try:
                        self.send('Ack', str(seqNum))
                    except:
                        raise
                
                if pktType not in ['Ack', 'Connection Test']:
                    receiveData.append(pktData)
                    
                self.receiveBuffer = self.receiveBuffer[nextPacketLength:]
                totalBytesReceived += nextPacketLength
                
        return receiveData


    def send(self, pktType, pktData):
        """
        Transmits a UARTComms packet.
        
        ≡≡≡ Required Parameters ≡≡≡
        pktType: a text string corresponding to one of the UARTComms packet types.
        pktData: a text string containing the data to be transmitted. 
              
        ≡≡≡ Raises ≡≡≡
        TypeError:        if the supplied parameter type is not correct
        ValueError:       if the supplied parameter value is incorrect
        OversizePKTError: if the packet size is larger than the maximum
                          permissible
        
        ≡≡≡ Returns ≡≡≡
        int: representing the nubmer of bytes transmitted.
        """
        seqNum = self.__nextSeqNum()
        try:
            msg = self.__pktEncode(pktType, pktData, seqNum)
        except:
            raise
        
        if pktType in ['Lossless', 'Connection Test']:
            self.outboundPackets[str(seqNum)] = [pktType, pktData, time()] 

        return self.uart.write(msg)
    
    
    def __updateRXTime(self):
        """Updates the timestamp of the last received transmission."""
        self.rxTime = int(time())
    
    
    def lastRXTime(self):
        """
        Returns the timestamp of the last received transmission. Useful with
        a watchdog process that monitors for regular successful activity.
        """
        return self.rxTime
    
    
    def losslessPacketsWaiting(self):
        """
        Returns a boolean True if there are Lossless packets that have been
        sent and no Ack has been received to confirm their successful
        transmission.
        """
        if len(self.outboundPackets) > 0:
            return True
        else:
            return False
    
    
    def resendLosslessPackets(self):
        """
        Re-transmits any Lossless packets that have been sent and no Ack has
        been received to confirm their successful transmission.
        
        Packets are only re-sent if the system has been waiting for at least
        one second for an Ack.
        
        ≡≡≡ Returns ≡≡≡
        bytesOut: int, representing the total number of bytes transmitted
        """
        now = time()
        bytesOut = 0
        for key in list(self.outboundPackets.keys()):
            if floor(abs(self.outboundPackets[key][2] - now)) >= 1:
                try:
                    msg = self.__pktEncode(self.outboundPackets[key][0],
                                           self.outboundPackets[key][1],
                                           int(key))
                except:
                    raise
                bytesOut += self.uart.write(msg)
                self.outboundPackets[key][2] = now
        return bytesOut


    def __pktChecksum(self, msgBytes):
        """
        Calculates and returns a checksum for a packet.
        
        ≡≡≡ Required Parameters ≡≡≡
        msgBytes:  a bytes object. msgBytes is the ordered combination of
                   components 3, 4, 5, and 6 of the UARTComms packet 
              
        ≡≡≡ Raises ≡≡≡
        TypeError: if msgBytes is not a bytes object.
        
        ≡≡≡ Returns ≡≡≡
        cSum: a bytes object of 4-bytes representing the message checksum.
        """
        if not isinstance(msgBytes, bytes):
            raise TypeError("\'msgBytes\' must be of type \'bytes\'.")
        cSum = crc32(msgBytes, 0)
        cSum = cSum.to_bytes(4,'little')
        return cSum


    def __pktEncode(self, pktType, pktData, seqNum):
        """
        Encodes a data packet as a bytes object for transmission.
        
        ≡≡≡ Required Parameters ≡≡≡
        pktType: a text string corresponding to one of the UARTComms packet
                 types.
        pktData: a text string containing the data to be transmitted.
        seqNum:  an integer to use as the trasmission sequence number.
              
        ≡≡≡ Raises ≡≡≡
        TypeError:        if the supplied parameter type is not correct
        ValueError:       if the supplied parameter value is incorrect
        OversizePKTError: if the packet size is larger than the maximum
                          permissible
        
        ≡≡≡ Returns ≡≡≡
        msg: a bytes object representing an entire UARTComms data packet.
        """
        if not isinstance(pktType, str):
            raise TypeError("\'pktType\' must be of type \'str\'.")
        
        if not isinstance(pktData, str):
            raise TypeError("\'pktData\' must be of type \'str\'.")
        
        if not isinstance(seqNum, int):
            raise TypeError("\'seqNum\' must be of type \'int\'.")
        
        if pktType not in self.PACKET_TYPES:
            raise ValueError('Message type not valid.')
        
        pktData = pktData.encode()
        length = self.__PACKET_HEADER_SIZE + len(pktData)
        
        if length > self.MAX_PACKET_SIZE:
            raise OversizePKTError('Packet data is too large at ' +
                                   str(length - self.__PACKET_HEADER_SIZE) +
                                   ' bytes. Max size is ' +
                                   str(self.MAX_PACKET_SIZE -
                                       self.__PACKET_HEADER_SIZE) +
                                   ' bytes.')
        
        msg = (length.to_bytes(2,'little') +
               seqNum.to_bytes(2,'little') +
               self.PACKET_TYPES.index(pktType).to_bytes(1,'little') +
               pktData
              )
        
        msg = (self.__PACKET_START_SEQUENCE +
               self.__pktChecksum(msg) +
               msg
               )
        return msg


    def __pktDecode(self, msg):
        """
        Decodes a data packet from a transmission.
        
        ≡≡≡ Required Parameters ≡≡≡
        msg: a bytes object representing an entire UARTComms data packet.
        
              
        ≡≡≡ Raises ≡≡≡
        TypeError:   if the supplied parameter type is not correct
        PacketError: if the packet is somehow malformed or otherwise fails to
                     validate the transmission checksum.
        
        ≡≡≡ Returns ≡≡≡
        pktType: a text string corresponding to one of the UARTComms packet types.
        pktData: a text string containing the data that was transmitted.
        seqNum:  an integer corresponding to the trasmission sequence number.
        """
        if not isinstance(msg, bytes):
            raise TypeError("\'msgBytes\' must be of type \'bytes\'.")
        
        startSeq = msg[0:3]
        cSum = msg[3:7]
        cSumMsg = msg[7:]
        length = int.from_bytes(msg[7:9], 'little')
        seqNum = int.from_bytes(msg[9:11], 'little')
        pktType = self.PACKET_TYPES[int.from_bytes(msg[11:12], 'little')]
        if len(msg) > self.__PACKET_HEADER_SIZE:
            pktData = msg[12:].decode()
        else:
            pktData = ''
        
        if startSeq != self.__PACKET_START_SEQUENCE:
            raise PacketError('Packet is malformed.')
        if len(msg) != length:
            raise PacketError('Packet is malformed.')
        if cSum != self.__pktChecksum(cSumMsg):
            raise PacketError('Packet is malformed.')

        return pktType, pktData, seqNum
