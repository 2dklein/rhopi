import serial, time
import Tkinter as tk


def send_to_enc(full):
    if rae.get():
        ra = serial.Serial(port='/dev/RAencoder', baudrate=230400, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS, xonxoff=serial.XOFF, dsrdtr=False, rtscts=False, timeout=1)
        ra.write(full+'\r\n')
        i = 0
        print full
        while i < 5:
            time.sleep(0.005)
            response = ra.read(27)
            if len(response) == 0:
                i += 1
            else:
                fullcomm.set(response)
                error['fg'] = 'blue'
                break
            if i == 5:
                fullcomm.set('Encoder not responding')
                error['fg'] = 'red'
    if dece.get():
        dec = serial.Serial(port='/dev/DECencoder', baudrate=230400, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS, xonxoff=serial.XOFF, dsrdtr=False, rtscts=False, timeout=1)
        dec.write(full+'\r\n')
        i=0
        print full
        while i < 5:
            time.sleep(0.005)
            response = dec.read(27)
            if len(response) == 0:
                i+=1
            else:
                fullcomm.set('Success')
                error['fg'] = 'blue'
                break
            if i == 5:
                fullcomm.set('Encoder not responding')
                error['fg'] = 'red'
    else:
        fullcomm.set('One encoder needs to be selected')
        error['fg'] = 'red'

def change_dropdown(commands):
    comm.set(commands_list[commands.get()])
    check_comm()


def check_comm():
    comms = comm.get()
    val = value.get()
    if val == '':
        val = 0
    try:
        hex(int(val, 2))
    except:
        print val
        fullcomm.set('Value must be in binary')
        error['fg'] = 'red'
        write['state'] = 'disabled'
    else:
        hexval = hex(int(val, 2))
        fullcomm.set(comms+str(hexval[2:]))
        error['fg'] = 'black'
        write['state'] = 'normal'


def create_comm(rw):
    check_comm()
    # print 'yes'
    if fullcomm.get() != 'Value must be in binary':
        send_to_enc(rw+fullcomm.get())
        # print 'success'


root = tk.Tk()
root.title("Serial Command GUI")
box = tk.Frame(root, width=475, height=30)
bot = tk.Frame(root)
value = tk.Entry(box)
value.bind('<KeyRelease>', lambda event: check_comm())
commands_list = {'00 - Encoder Mode': '00', '03 - Counter Mode R0': '03', '04 - Counter Mode R1': '04',
                 '0E - Read Encoder': '0E'}  # List of commands
commands = tk.StringVar()
commands.set('0E - Read Encoder')
choices = sorted(commands_list.keys())  # Pull the keys from the dictionary, sort, and use as dropdown options
register = tk.OptionMenu(box, commands, *choices)
comm = tk.StringVar()
comm.set('0E')
fullcomm = tk.StringVar()
fullcomm.set('0E')
rae = tk.IntVar()
rae.set(1)
dece = tk.IntVar()
dece.set(1)
write = tk.Button(bot, text='Write', state='disabled', command=lambda: create_comm('W'))
read = tk.Button(bot, text='Read', command=lambda: create_comm('R'))

box.pack(fill='both', side='top')
bot.pack(fill='both', side='top')
tk.Label(box, text='RA').pack(side='left')
tk.Checkbutton(box, variable=rae).pack(side='left')
tk.Label(box, text='DEC').pack(side='left')
tk.Checkbutton(box, variable=dece).pack(side='left')
register.pack(side='left')
value.pack(side='right')
tk.Label(box, text='Value:').pack(side='right')
commands.trace('w', lambda _, __, ___: change_dropdown(commands))

tk.Label(bot, text='Command: ').pack(side='left')
error = tk.Label(bot, textvariable=fullcomm)
error.pack(side='left')
tk.Button(bot, text='Close', command=root.destroy, fg='red').pack(side='right')
read.pack(side='right')
write.pack(side='right')
box.pack_propagate(0)

root.mainloop()
