import serial, time

def clean_str(string):
    #  r 0E 0000018B !
    info = string.split(' ')
    return info[2]


def get_ra():
    ra = serial.Serial(
        port='/dev/RAencoder',
        baudrate=230400,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        xonxoff=serial.XOFF,
        dsrdtr=False,
        rtscts=False,
        timeout=None
        )

    ra.write("R0E00\r\n")
    time.sleep(0.2)
    ra_raw = ''
    while ra.inWaiting() > 0:
        ra_raw += ra.read(1)
    if ra_raw != '':
        ra_val = ra_raw.split(' ')
        ra_tick = int(ra_val[2], 16)
#        print "raw >>", ra_raw
#        print "val >>", ra_val
#        print "bin >>", bin(int(ra_val, 16))
#        print "int >>", int(ra_val, 16)
    ra.close()
    return ra_tick+1000000

def get_dec():
    dec = serial.Serial(
        port='/dev/DECencoder',
        baudrate=230400,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        xonxoff=serial.XOFF,
        dsrdtr=False,
        rtscts=False,
        timeout=None
        )

    dec.write("R0E00\r\n")
    time.sleep(0.2)
    dec_raw = ''
    while dec.inWaiting() > 0:
        dec_raw += dec.read(1)
    if dec_raw != '':
        dec_val = dec_raw.split(' ')
        dec_tick = int(dec_val[2], 16)
#        print "raw >>", ra_raw
#        print "val >>", ra_val
#        print "bin >>", bin(int(ra_val, 16))
#        print "int >>", int(ra_val, 16)
    dec.close()
    return dec_tick+1000000

#ra = serial.Serial(
#    port='/dev/RAencoder',
#    baudrate=230400,
#    parity=serial.PARITY_NONE,
#    stopbits=serial.STOPBITS_ONE,
#    bytesize=serial.EIGHTBITS,
#    xonxoff=serial.XOFF,
#    dsrdtr=False,
#    rtscts=False,
#    timeout=1
#)
#
#print ra.name
#input=1
#while 1 :
#    # get keyboard input
#    #print "1 cycle is one RA, DEC readout"
#    input = raw_input("S:\>")
#        # Python 3 users
#        # input = input(">> ")
#    if input == 'exit':
#        ra.close()
#        exit()
#
#    else:
#        ra.write(input+'\r\n')
#        time.sleep(0.2)
#        ra_raw = ''
#        while ra.inWaiting() > 0:
#            ra_raw += ra.read(1)
#        if ra_raw != '':
#            ra_val = clean_str(ra_raw)
#            print "raw >>", ra_raw
#            print "val >>", ra_val
#            print "bin >>", bin(int(ra_val, 16))
#            print "int >>", int(ra_val, 16)
#ra.close()