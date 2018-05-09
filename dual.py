import serial, time
import talkserialtome as ts


ra = serial.Serial(
    port='/dev/RAencoder',
    baudrate=230400,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    xonxoff=serial.XOFF,
    dsrdtr=False,
    rtscts=False,
    timeout=1
)
dec = serial.Serial(
    port='/dev/DECencoder',
    baudrate=230400,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    xonxoff=serial.XOFF,
    dsrdtr=False,
    rtscts=False,
    timeout=1
)
#ser = serial.Serial('/dev/RAencoder')  # open serial port
print ra.name, dec.name         # check which port was really used

#ser.isOpen()

print 'Enter your commands below.\r\nInsert "exit" to leave the application.'

input=1
while 1 :
    # get keyboard input
    #print "1 cycle is one RA, DEC readout"
    input = raw_input("Enter command: ")
        # Python 3 users
        # input = input(">> ")
    if input == 'exit':
        ra.close()
        dec.close()
        exit()
    else:
        # seconds = int(input)
        # while seconds > 0:

        # send the character to the device
        # (note that I append a \r\n carriage return and line feed to the characters - this is requested by my device)
        ra_val, dec_val = '', ''
        input += '\r\n'
        # let's wait one second before reading output (let's give device time to answer)

        ra.write(input)
        time.sleep(0.2)

        while ra.inWaiting() > 0:
            ra_val += ra.read(1)
        if ra_val != '':
            print "RA:", ra_val, int(ts.clean_str(ra_val), 16)
        else:
            print 'RA encoder input error!'

        dec.write(input)
        time.sleep(0.2)

        while dec.inWaiting() > 0:
            dec_val += dec.read(1)
        if dec_val != '':
            print "DEC:", dec_val, ts.clean_str(dec_val)
        else:
            print 'DEC encoder input error!'
        # seconds -= 1

ra.close()             # close port
dec.close()