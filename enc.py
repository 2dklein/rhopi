# coding: utf-8
"""
Class file for encoder objects.
Input: Enc(name_of_encoder)
States:  Enc.enc, the serial port details
         Enc.offset, the tick read at initialization
         Enc.tick, the last tick read
Methods: Enc.__init__, creates serial port object with correct settings
         Enc.read(), reads encoder and returns tick value
"""
import serial as ser, time


class Enc:
    def __new__(cls):
        check = cls.enc.isOpen()  # Check if the port is working
        if check < 0:
            return False  # Bork if not
        cls.enc.write("W0343\r\n")  # Init the encoder with the correct settings
        time.sleep(0.05)  # Pause for reply
        raw = ''  # Str to read reply
        while cls.enc.inWaiting() > 0:
            raw += cls.enc.read(1)  # Append reply from encoder (one char at a time)

        '''
        Need code:
         Verify initialization return string
        '''

        cls.enc.write("R0E00\r\n")
        time.sleep(0.05)
        read = ''
        if read != '':  # if we successfully read from the encoder
            read = read.split(' ')
            # This fixes the ticks when they roll over
            if int(read[2], 16) > 4000000000:  # Encoders don't return negative ticks
                tick = int(read[2], 16) - 4294967295  # Now they do. (Hex 'ffffffff')
            else:
                tick = int(read[2], 16)
            cls.tick = tick
        else:
            return False  # Bork if no read from encoder
        return True  # Successful initialization

    def __init__(self, name):
        self.enc = ser.Serial(port='/dev/'+str(name), baudrate=230400, parity=ser.PARITY_NONE, stopbits=ser.STOPBITS_ONE, bytesize=ser.EIGHTBITS, xonxoff=ser.XOFF, dsrdtr=False, rtscts=False, timeout=None)

    def read(self):  # Read an initialized encoder with encoder_name.read()
        check = self.enc.isOpen()  # Check if the port is working
        if check < 0:
            return False  # Bork if not
        self.enc.write("R0E00\r\n")
        time.sleep(0.05)
        read = ''
        while self.enc.inWaiting() > 0:
            read += self.enc.read(1)  # To do: figure out exact byte size returned from enc
        self.enc.close()
        if read != '':
            read = read.split(' ')  # Break up text returned from encoder
            # This fixes the ticks when they roll over
            if int(read[2], 16) > 4000000000:
                tick = int(read[2], 16) - 4294967295
            else:
                tick = int(read[2], 16)
            return self.tick  # Successful read
        else:
            return False  # boo
