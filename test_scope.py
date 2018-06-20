# coding: utf-8
"""
Class file for simulated encoder objects {equivalent actual code is in curly braces}
Input: Enc(name_of_encoder)
States:  Enc.enc, the serial port details
         Enc.offset, the tick read at initialization
         Enc.tick, the last tick read
Methods: Enc.__init__, creates serial port object with correct settings
         Enc.read(), reads encoder and returns tick value
         Enc.move(), moves scope by amount in degrees (Virtual encoders only)
"""
import random as rn, time


class Enc:
    def __new__(cls):
        check = 0  # Check if the port is working  {check = cls.enc.isOpen()}
        if check < 0:
            return False  # Bork if not
        # Init the encoder with the correct settings
        # {cls.enc.write("W0343\r\n")}
        time.sleep(0.05)  # Pause for reply
        raw = rn.randint(0, 4294967295)  # Str to read reply {raw = ''}
        # {while cls.enc.inWaiting() > 0:}
        # {    raw += cls.enc.read(1)}  # Append reply from encoder (one char at a time)
        if raw != '':  # if we successfully read from the encoder
            # {raw = raw.split(' ')}
            # This fixes the ticks when they roll over
            if raw > 4000000000:  # Encoders don't return negative ticks  {if raw > int(raw[2], 16) > 4000000000:}
                tick = raw - 4294967295  # Now they do. (Hex 'ffffffff')  {tick = int(raw[2], 16) - 4294967295}
            else:
                tick = raw  # {tick = int(raw[2], 16)}
            cls.tick = tick
        else:
            return False  # Bork if no read from encoder
        return True  # Successful initialization

    def __init__(self, name):
        # self.enc = ser.Serial(port='/dev/'+str(name), baudrate=230400, parity=ser.PARITY_NONE, stopbits=ser.STOPBITS_ONE, bytesize=ser.EIGHTBITS, xonxoff=ser.XOFF, dsrdtr=False, rtscts=False, timeout=None)
        self.name = '/dev/'+str(name)
        if name == 'RAEncoder':
            self.rate = 103
        else: self.rate = 206

    def read(self):  # Read an initialized encoder with encoder_name.read()
        # {self.enc.write("R0E00\r\n")}
        time.sleep(0.05)
        raw = self.tick  # {raw = ''}
        # {while self.enc.inWaiting() > 0:}
        #     {raw += self.enc.read(1)}
        # {self.enc.close()}
        if raw != '':  # if we successfully read from the encoder
            # {raw = raw.split(' ')}
            # This fixes the ticks when they roll over
            if raw > 4000000000:  # Encoders don't return negative ticks  {if raw > int(raw[2], 16) > 4000000000:}
                tick = raw - 4294967295  # Now they do. (Hex 'ffffffff')  {tick = int(raw[2], 16) - 4294967295}
            else:
                tick = raw  # {tick = int(raw[2], 16)}
            self.tick = tick
        else:
            return False  # Bork if no read from encoder
        return True  # Successful initialization

    # Virtual encoder method for moving scope
    def move(self, amt):  # amt is in degrees
        self.tick += self.rate*(1 + 0.1*(rn.random() - rn.random()))  # 10% Gaussian noise
        return int(self.tick)