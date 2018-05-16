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
    timeout=0.005
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
    timeout=0.005
)


def sendQsbInstruction(qsbCommand):
    ioResult = ra.write(qsbCommand+"\r\n")
    if ioResult < 1:
        print "Error writing to QSB device"

def readQsbResponse():
    i = 0
    ioResult = ''
    while ra.inWaiting() > 0:
        ioResult += ra.read(16)
        time.sleep(0.005)
        i += 1
        if len(ioResult) > 0 and i < 5:
            print i
            break
        if i == 5:
            print "Error reading from QSB device"
            break
    return ioResult


def qsbCommand(command):
    sendQsbInstruction(command)
    return readQsbResponse()


def main():
    close_req = False
    while not close_req:
        # Open the port
        qsb = ra.isOpen()
        if qsb < 0:
            print "Error opening QSB device"

        command = raw_input("S:\> ")
        if command == 'exit':
            close_req = True
            ra.close()
            exit()
        else:
            print qsbCommand(command)

        # Print product info
        # qsbCommand("R14")
        #print "Current count:", qsbCommand("R0E")

main()