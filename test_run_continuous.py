# -*- coding: utf-8 -*-
import serial, time

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

buffer_size = 27
five_ms = 0.005
max_tries = 5
close_req = False


def sendQsbInstruction(qsbCommand):
    ioResult = ra.write(qsbCommand+"\r\n")
    if ioResult < 0:
        print "Error writing to QSB device"

def readQsbResponse():
    i = 0
    ioResult = ''
    while True:
        ioResult += ra.read(27)
        time.sleep(five_ms)
        i += 1
        if len(ioResult) > 0 and i < max_tries:
            break
        if i == max_tries:
            print "Error reading from QSB device"
            break

    return ioResult.replace("\r\n", "")


def qsbCommand(command):
    sendQsbInstruction(command)
    return readQsbResponse()



def main():
    # Open the port
    qsb = ra.isOpen()
    if qsb < 0:
        print "Error opening QSB device"

    #command = raw_input("S:\> ")
    #if command == 'exit':
        #close = True
        #ra.close()
        #exit()

    # Print product info
    # qsbCommand("R14")
    print "Current count:", qsbCommand("R0E")

main()