#!/usr/bin/python
# -*- coding: utf-8 -*-

import Tkinter as tk
import datetime, ephem, tkFont
from autocomplete import char_check
from db import save_db
import tkMessageBox
import talkserialtome as ts


def display_time_now(event):
    def time_now():
        rho.date = ephem.now()
        s_time.set(str(ephem.localtime(ephem.now()).strftime("%H:%M:%S")))
        s_utc.set(str(ephem.date(ephem.now()).datetime().strftime("%H:%M:%S")))
        s_lst.set(str(rho.sidereal_time()))
        s.after(500, time_now)
    time_now()


def auto_fill(entry_box, text_box):
    star_list = char_check(entry_box.get())
    if star_list[0] == '--None--':
        c_0.config(state='disabled')
    else:
        c_0.config(state='normal')
    if star_list[1] == '--None--':
        c_1.config(state='disabled')
    else:
        c_1.config(state='normal')
    if star_list[2] == '--None--':
        c_2.config(state='disabled')
    else:
        c_2.config(state='normal')
    if star_list[3] == '--None--':
        c_3.config(state='disabled')
    else:
        c_3.config(state='normal')
    text_box[0].set(str(star_list[0]))
    text_box[1].set(str(star_list[1]))
    text_box[2].set(str(star_list[2]))
    text_box[3].set(str(star_list[3]))


def confirm_align(name, ra, dec):
    log_action('Aligned', name.get(), str('RA: '+ra.get()+' | DEC: '+dec.get()))
    result = tkMessageBox.askyesno("Align Telescope", "Are you sure?")
    if result is True:
        s_scope.config(fg='black')
        # Pull current tick counts
        print ts.get_ra(), ts.get_dec()
        # if error -> display error and log it
        # else -> Save current ticks as angle [rad] = Scale*Tick + Offset
        return
    else:
        # Do nothing
        return


# use() is the function for a custom J2000 star entered into the GUI. MUST BE J2000
def use(name, ra_t, dec_t):
    ra = ra_t[0].get() + ' ' + ra_t[1].get() + ' ' + ra_t[2].get()
    dec = dec_t[0].get() + ' ' + dec_t[1].get() + ' ' + dec_t[2].get()  # Formatting...
    log_action('USE Custom', name, str('RA: '+ra+' | DEC: '+dec))  # Log custom object use
    db = ephem.readdb(name+',f,'+ra+','+dec+',0,2000,0')  # Create temp fixed object in ephem database format
    clear_lock()
    search(db, 'GET Custom')  # Run search and calculate details


# Search() takes an ephem object and runs calculations on it for RHO at time NOW
def search(obj, type):
    rho.date = ephem.now()
    obj.compute(rho)
    o_name.set('%s' % obj.name)
    o_ra.set('%s' % obj.ra)
    o_dec.set('%s' % obj.dec)
    st = rho.sidereal_time()
    ha = '%s' % ephem.hours(st - obj.ra)
    o_ha.set(ha)
    if o_track.get() == 1:
        o.after(1000, lambda : search(obj, type))
    else:
        log_action(type, obj.name, 'HA: '+ha)


def read_db(name):
    rho.date = ephem.now()
    with open('objects.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line[0:len(name.get())] == name.get():
                obj = ephem.readdb(line)
                rho.date = ephem.now()
                obj.compute(rho)
                search(obj, 'GET User Object')
                break


def track_s(name):
    if o_track.get() == 1:
        log_action('Track Object', name.get(), 'Tracking Started')
        quick_s(name, True)
        c_0['state'] = 'disabled'
        c_1['state'] = 'disabled'
        c_2['state'] = 'disabled'
        c_3['state'] = 'disabled'
    else:
        log_action('Track Object', name.get(), 'Tracking Stopped')
        if c_fill[0].get() != '--None--':
            c_0['state'] = 'normal'
        if c_fill[1].get() != '--None--':
            c_1['state'] = 'normal'
        if c_fill[2].get() != '--None--':
            c_2['state'] = 'normal'
        if c_fill[3].get() != '--None--':
            c_3['state'] = 'normal'


def quick_s(name, track):
    if not track:
        clear_lock()
    if hasattr(ephem, name.get()):  # Check for named planets/moons
        obj = getattr(ephem, name.get())()
        search(obj, 'GET Planet/Moon')
    else:
        try:
            ephem.star(name.get())  # Check if named star
        except KeyError:
            read_db(name)  # If not, read from custom objects database
        else:
            obj = ephem.star(name.get())  # If it's a star
            search(obj, 'GET Named Star')


def clear_lock():
    o_track.set(0)


def validate(value, ii):
    if len(value) > int(ii):
        return False
    return True


def view_large():
    box = tk.Toplevel(root, bg='black')
    box_font = tkFont.Font(size=50)
    box.attributes('-zoomed', True)
    box.title('RhoPi Large View')
    box_f = tk.Frame(box, bg='black')
    box_f.pack()
    tk.Label(box_f, text='INFORMATION', relief='solid', width=42).grid(row=0)  # Section Title
    tk.Label(box_f, text='Local Time (EST):').grid(row=2, sticky='W')
    tk.Label(box_f, textvariable=s_time).grid(row=2, sticky='E')
    tk.Label(box_f, text='Universal Time (UTC):').grid(row=3, sticky='W')
    tk.Label(box_f, textvariable=s_utc).grid(row=3, sticky='E')
    tk.Label(box_f, text='Sidereal Time (LST):').grid(row=4, sticky='W')
    tk.Label(box_f, textvariable=s_lst).grid(row=4, sticky='E')
    tk.Label(box_f, text='Scope RA: ').grid(row=7, sticky='W')
    tk.Label(box_f, textvariable=s_ra).grid(row=7, sticky='E')
    tk.Label(box_f, text='Scope DEC: ').grid(row=8, sticky='W')
    tk.Label(box_f, textvariable=s_dec).grid(row=8, sticky='E')
    tk.Label(box_f, text='Scope HA:').grid(row=9, sticky='W')
    tk.Label(box_f, textvariable=s_ha).grid(row=9, sticky='E')
    tk.Label(box_f, text='Raw Tick RA:').grid(row=10, sticky='W')
    tk.Label(box_f, textvariable=s_tick_ra).grid(row=10, sticky='E')
    tk.Label(box_f, text='Raw Tick DEC:').grid(row=11, sticky='W')
    tk.Label(box_f, textvariable=s_tick_dec).grid(row=11, sticky='E')
    tk.Button(box_f, text='Close Window', command=box.destroy, activebackground='dark gray', highlightbackground='gray').grid(row=12)
    for child in box_f.winfo_children():
        child.config(font=box_font, bg='black', fg='red')
    center(box)


def center(win):
    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    x = (win.winfo_screenwidth() / 2) - (width / 2)
    y = (win.winfo_screenheight() / 2) - (height / 2)
    win.geometry('+{}+{}'.format(x, y))


def log_action(action, event, details):
    # Actions: Searched, Aligned, Saved, Error
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    o_log.insert(0, str('  '+event+' | '+details))
    o_log.insert(0, now+' - '+action)
    with open(today+'_ObservingLog.txt', 'a') as f:
        f.write(now+' - '+action+' | '+event+' | '+details+'\n')
    return


# Window Options
root = tk.Tk()
root.title("RhoPi Telescope Pointing v0.0.5 (alpha)")
default_font = tkFont.nametofont("TkDefaultFont")
default_font.configure(size=11, family='system')
# print tkFont.families()

# Observer Setup
rho = ephem.Observer()
rho.lon, rho.lat = '-82.586203', '29.400249'


# --- Section Frames Column Configuration --- #
c = tk.Frame(root)  # c is for catalog section widgets
c.grid(column=0, row=0, sticky='N')
o = tk.Frame(root)  # a is for align section widgets
o.grid(column=1, row=0, sticky='N')
s = tk.Frame(root)  # s is for information section widgets
s.grid(column=2, row=0, sticky='N')


# --- All widget initializations and names --- #

# Target Section Widgets
c_fill = [tk.StringVar(c, '--None--'), tk.StringVar(c, '--None--'), tk.StringVar(c, '--None--'), tk.StringVar(c, '--None--')]
c_entry = tk.Entry(c, width=30)
c_entry.bind('<KeyRelease>', lambda event: auto_fill(c_entry, c_fill))
c_entry.bind('<Return>', lambda event: quick_s(c_fill[0], False))
c_entry.bind('<BackSpace>', lambda event: clear_lock())
c_entry.bind('<Delete>', lambda event: clear_lock())
c_0 = tk.Button(c, textvariable=c_fill[0], state='disabled', command= lambda: quick_s(c_fill[0], False))
c_1 = tk.Button(c, textvariable=c_fill[1], state='disabled', command= lambda: quick_s(c_fill[1], False))
c_2 = tk.Button(c, textvariable=c_fill[2], state='disabled', command= lambda: quick_s(c_fill[2], False))
c_3 = tk.Button(c, textvariable=c_fill[3], state='disabled', command= lambda: quick_s(c_fill[3], False))
c_det = tk.Frame(c)
c_name = tk.Entry(c_det, width=21)
c_ra = tk.Frame(c)
c_dec = tk.Frame(c)

# Custom RA and DEC boxes
ra_h = tk.Entry(c_ra, width=3, validate='key')
ra_h['validatecommand'] = (ra_h.register(validate), '%P', 3)
ra_m = tk.Entry(c_ra, width=2, validate='key')
ra_m['validatecommand'] = (ra_m.register(validate), '%P', 2)
ra_s = tk.Entry(c_ra, width=5, validate='key')
ra_s['validatecommand'] = (ra_s.register(validate), '%P', 5)
dec_h = tk.Entry(c_dec, width=3, validate='key')
dec_h['validatecommand'] = (dec_h.register(validate), '%P', 3)
dec_m = tk.Entry(c_dec, width=2, validate='key')
dec_m['validatecommand'] = (dec_m.register(validate), '%P', 2)
dec_s = tk.Entry(c_dec, width=5, validate='key')
dec_s['validatecommand'] = (dec_s.register(validate), '%P', 5)
ra_t = ra_h, ra_m, ra_s
dec_t = dec_h, dec_m, dec_s
c_use = tk.Button(c, text='Use', command= lambda: use(c_name.get(), ra_t, dec_t))
c_save = tk.Button(c, text='Save...', command= lambda: save_db(root, c_name.get(), ra_t, dec_t))

# Align Section Widgets
o_name = tk.StringVar(c, 'No Object Selected')
o_ra = tk.StringVar(c, '---')
o_dec = tk.StringVar(c, '---')
o_ha = tk.StringVar(c, '---')
o_track = tk.IntVar()
o_target = tk.Checkbutton(o, text=' Track Object', var=o_track)
o_target.bind('<ButtonRelease-1>', lambda event: track_s(o_name))
o_align = tk.Button(o, text='Align on Object', command= lambda : confirm_align(o_name, o_ra, o_dec))
o_log = tk.Listbox(o, width=40, bg='dark gray', height=12)

# Information Section Widgets
s_target = tk.StringVar(s, '---')
s_time = tk.StringVar(s, '---')
s_utc = tk.StringVar(s, '---')
s_lst = tk.StringVar(s, '---')
s_ready = tk.StringVar(s, 'Telescope Not Aligned')
s_scope = tk.Label(s, textvariable=s_ready, height=2, fg='red')
s_ra = tk.StringVar(s, '---')
s_dec = tk.StringVar(s, '---')
s_ha = tk.StringVar(s, '---')
s_tick_ra = tk.StringVar(s, '---')
s_tick_dec = tk.StringVar(s, '---')
s_large = tk.Button(s, text='View Large Info', height=2, command=view_large)
display_time_now(s_time)


# --- Section Layouts --- #

# Target Section Layout
tk.Label(c, text='CATALOG', relief='solid', width=40, height=2).grid(row=0)  # Section title
tk.Label(c, text='Quick Search').grid(row=1)
c_entry.grid(row=2)
c_0.grid(row=3)
c_1.grid(row=4)
c_2.grid(row=5)
c_3.grid(row=6)
tk.Frame(c, height=3, width=300, bd=1, relief='ridge').grid(row=7)
tk.Label(c, text='Enter New J2000 Object', height=2).grid(row=8)

# Custom Target Section Layout
c_det.grid(row=9)
tk.Label(c_det, text='Name:             ').pack(side='left')
c_name.pack(side='right')
c_ra.grid(row=10)  # Frame holding the RA coords
tk.Label(c_ra, text='RA:                   ').pack(side='left')
ra_s.pack(side='right')
tk.Label(c_ra, text=':').pack(side='right')
ra_m.pack(side='right')
tk.Label(c_ra, text=':').pack(side='right')
ra_h.pack(side='right')
c_dec.grid(row=11)  # Frame with DEC coords
tk.Label(c_dec, text='DEC:                  ').pack(side='left')
dec_s.pack(side='right')
tk.Label(c_dec, text=':').pack(side='right')
dec_m.pack(side='right')
tk.Label(c_dec, text=':').pack(side='right')
dec_h.pack(side='right')
c_save.grid(row=12, sticky='W')
c_use.grid(row=12, sticky='E')

# Align Section Positions
tk.Label(o, text='OBJECT', relief='solid', width=40, height=2).grid(row=0)  # Section Title
tk.Label(o, text='Object Name:').grid(row=1, sticky='W')
tk.Label(o, textvariable=o_name).grid(row=1, sticky='E')
tk.Label(o, text='Right Ascension:').grid(row=2, sticky='W')
tk.Label(o, textvariable=o_ra).grid(row=2, sticky='E')
tk.Label(o, text='Declination:').grid(row=3, sticky='W')
tk.Label(o, textvariable=o_dec).grid(row=3, sticky='E')
tk.Label(o, text='Object Hour Angle: ').grid(row=4, sticky='W')
tk.Label(o, textvariable=o_ha).grid(row=4, sticky='E')
o_align.grid(row=5, sticky='W')
o_target.grid(row=5, sticky='E')
tk.Frame(o, height=3, width=300, bd=1, relief='ridge').grid(row=6)
tk.Label(o, text='Recent Log Entries').grid(row=7)
o_log.grid(row=8)

# Info Section Positions
tk.Label(s, text='INFORMATION', relief='solid', width=40, height=2).grid(row=0)  # Section Title
tk.Label(s, text='Time').grid(row=1)
tk.Label(s, text='Local Time (EST):').grid(row=2, sticky='W')
tk.Label(s, textvariable=s_time).grid(row=2, sticky='E')
tk.Label(s, text='Universal Time (UTC):').grid(row=3, sticky='W')
tk.Label(s, textvariable=s_utc).grid(row=3, sticky='E')
tk.Label(s, text='Sidereal Time (LST):').grid(row=4, sticky='W')
tk.Label(s, textvariable=s_lst).grid(row=4, sticky='E')
tk.Frame(s, height=3, width=300, bd=1, relief='ridge').grid(row=5)
s_scope.grid(row=6)
tk.Label(s, text='Scope RA: ').grid(row=7, sticky='W')
tk.Label(s, textvariable=s_ra).grid(row=7, sticky='E')
tk.Label(s, text='Scope DEC: ').grid(row=8, sticky='W')
tk.Label(s, textvariable=s_dec).grid(row=8, sticky='E')
tk.Label(s, text='Scope HA:').grid(row=9, sticky='W')
tk.Label(s, textvariable=s_ha).grid(row=9, sticky='E')
tk.Label(s, text='Raw Tick RA:').grid(row=10, sticky='W')
tk.Label(s, textvariable=s_tick_ra).grid(row=10, sticky='E')
tk.Label(s, text='Raw Tick DEC:').grid(row=11, sticky='W')
tk.Label(s, textvariable=s_tick_dec).grid(row=11, sticky='E')
s_large.grid(row=12)

# Close GUI
close = tk.Button(root, fg='red', text='Close', width=10, height=2, command=root.destroy)
close.grid(row=1, column=2, sticky='E')

# Global Frame settings
for child in c.winfo_children():
    child.grid_configure(padx=10, pady=5)
for child in o.winfo_children():
    child.grid_configure(padx=10, pady=5)
for child in s.winfo_children():
    child.grid_configure(padx=10, pady=5)
root.lift()
root.mainloop()
