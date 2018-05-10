#!/usr/bin/python
# -*- coding: utf-8 -*-

import Tkinter as tk
import datetime, ephem, tkFont
from autocomplete import char_check
from db import save_db
import tkMessageBox
import talkserialtome as ts

ra_slope = -102.133333333
dec_slope = -204.671666667


# This function updates the local and sidereal times
def display_time_now(event):
    def time_now():
        rho.date = ephem.now()  # Calculate now at rho
        s_time.set(str(ephem.localtime(ephem.now()).strftime("%H:%M:%S")))
        s_utc.set(str(ephem.date(ephem.now()).datetime().strftime("%H:%M:%S")))
        s_lst.set(str(rho.sidereal_time()))
        s.after(500, time_now)  # Call the function after 500 ms to update the time.
    time_now()


# This function fills the catalog buttons
def auto_fill(entry_box, text_box):
    star_list = char_check(entry_box.get())  # Call the char_check function on the current catalog search string
    # Star list returns a list of up to four matching items from the combination of named stars, planets and moons,
    # and user-submitted object list.
    if star_list[0] == '--None--':  # As long as the text is not '--None--', enable the button
        c_0.config(state='disabled')  # There are four repetitions because the four buttons have unique names.
    else:
        c_0.config(state='normal')  # Possibly could reduce by using dict of { button : label }
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
    text_box[0].set(str(star_list[0]))  # Set the text variables to update button
    text_box[1].set(str(star_list[1]))
    text_box[2].set(str(star_list[2]))
    text_box[3].set(str(star_list[3]))


# Align function. Pulls RA and DEC from encoders
def confirm_align(name, ra, dec):
    result = tkMessageBox.askyesno("Align Telescope", "Are you sure?")
    if result is True:
        # Pull current tick counts
        # print ts.get_ra(), ts.get_dec()
        try:
            ts.get_ra()
            ts.get_dec()
        except:
            log_action('Align', 'Failed', 'Encoder not found')
            tkMessageBox.Message('Align Failed: Encoder(s) not found! Try again dummy :P')
        else:
            log_action('Align Success', name.get(), str('HA: '+o_ha.get()+' | DEC: '+o_dec.get()))
            tick_ra = ts.get_ra()
            tick_dec = ts.get_dec()
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with open('TickData.txt', 'a') as f:  # Append the data
                f.write(now+'\t'+str(tick_ra)+'\t'+o_ha.get()+'\t'+str(tick_dec)+'\t'+o_dec.get()+'\t'+name.get()+'\n')

            # Set the ra_tick offset to the hour angle of object
            if tick_ra > 2000000:
                tick_ra =- 4294967295
            print tick_ra, ra_slope, 'degs:', tick_ra/ra_slope
            ra_deg = ephem.degrees(tick_ra/ra_slope) # [tick]/[ticks/degrees] = [degrees]
            ra_offset = ra_deg - ephem.hours(o_ha.get())
            # ra_offset is applied to all other RA calls to find the correct position
            s_ready.set('Telescope Aligned')
            s_scope.config(fg='black')
            # else -> Save current ticks as angle [rad] = Scale*Tick + Offset
    else:
        # Do nothing
        return


# Use a custom J2000 star entered into the GUI. **Must be a J2000 item.**
def use(name, ra_t, dec_t):
    clear_lock()  # Turn off tracking of previous object
    ra = ra_t[0].get() + ' ' + ra_t[1].get() + ' ' + ra_t[2].get()
    dec = dec_t[0].get() + ' ' + dec_t[1].get() + ' ' + dec_t[2].get()  # Formatting...
    log_action('USE Custom', name, str('RA: '+ra+' | DEC: '+dec))  # Log custom object use
    db = ephem.readdb(name+',f,'+ra+','+dec+',0,2000,0')  # Create temp fixed object in ephem database format
    search(db, 'GET Custom')  # Run search and calculate details


# Search() takes an ephem object and runs calculations on it for RHO at time NOW
def search(obj, type):
    rho.date = ephem.now()  # Calculate rho details at time now
    obj.compute(rho)  # Calculate object details relative to rho
    o_name.set('%s' % obj.name)  # Set labels showing object details
    o_ra.set('%s' % obj.ra)
    o_dec.set('%s' % obj.dec)
    st = rho.sidereal_time()  # Grab RHO sidereal time
    ha = '%s' % ephem.hours(st - obj.ra)  # Calc HA of object from RHO
    o_ha.set(ha)  # Update label
    if o_track.get() == 1:  # If tracking is checked...
        o.after(1000, lambda : search(obj, type))  # ...repeat the lookup after a second and update HA
    else:
        log_action(type, obj.name, 'HA: '+ha)  # If first search, log activity


# Read user objects file database, 'objects.txt'
def read_db(name):
    with open('objects.txt', 'r') as f:  # Open file, do stuff
        lines = f.readlines()
        for line in lines:  # For each line, search for the name given
            if line[0:len(name.get())] == name.get():  # If the string matches
                obj = ephem.readdb(line)  # Read the line into an ephem object
                rho.date = ephem.now()  # Grab RHO at NOW details
                obj.compute(rho)  # Calc object details at RHO at NOW
                search(obj, 'GET User Object')  # Perform object search and send log activity detail
                break  # Stop searching after you find the object


# Track an object, aka update HA every second
def track_s(name):
    if o_track.get() == 1:  # If tracking is now on...
        log_action('Track Object', name.get(), 'Tracking Started')  # .. log action
        quick_s(name, True)  #
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


# Quick search is using the catalog to find stars, planets, moons, or user objects
def quick_s(name, track):
    if not track:  # If variable 'track' is False, clear the tracking because it's a new object being searched.
        clear_lock()
    if hasattr(ephem, name.get()):  # Check if variable 'name' is a named planet/moon
        obj = getattr(ephem, name.get())()  # If so, grab it
        search(obj, 'GET Planet/Moon')  # Object search and log detail
    else:
        try:
            ephem.star(name.get())  # Check if 'name' is a named star
        except KeyError:
            read_db(name)  # If not, read 'name' from the custom objects database
        else:
            obj = ephem.star(name.get())  # But if it was a star...
            search(obj, 'GET Named Star')  # ...Send it along with the correct log detail


def clear_lock():
    o_track.set(0)  # turn off tracking


# Validate is used for multiple text entry boxes to limit the number of numbers entered.
def validate(value, ii):  # The function call includes the max number length, ii
    if len(value) > int(ii):  # if the length is longer then this number ii
        return False  # Don't allow the number to be typed
    return True  # Else, go ahead and let the number be typed


# Code to display fullscreen display of scope coordinates.
def view_large():
    box = tk.Toplevel(root, bg='black')  # Open a new window
    large_font = tkFont.Font(size=80)  # Set large font text size
    medium_font = tkFont.Font(size=42)  # Set not-so-large text size
    box.attributes('-zoomed', True)  # Start window maximized
    box.title('RhoPi Large View')  # Title
    box_f = tk.Frame(box, bg='black')  # Frame within the box window
    box_f.grid(row=0, sticky='WE')  # Placement of frame

    tk.Label(box_f, text='INFORMATION', relief='solid', width=27).grid(row=0)  # Section labels/text variables and positions
    tk.Label(box_f, text='Scope RA: ').grid(row=7, sticky='W')
    tk.Label(box_f, textvariable=s_ra).grid(row=7, sticky='E')
    tk.Label(box_f, text='Scope DEC: ').grid(row=8, sticky='W')
    tk.Label(box_f, textvariable=s_dec).grid(row=8, sticky='E')
    tk.Label(box_f, text='Scope HA:').grid(row=9, sticky='W')
    tk.Label(box_f, textvariable=s_ha).grid(row=9, sticky='E')

    box_o = tk.Frame(box, bg='black')  # Second frame in box window
    box_o.grid(row=1, sticky='WE')  # Second frame placement

    tk.Label(box_o, text='', width=50).grid(row=0, columnspan=2)  # Section labels/text variables and positions
    tk.Label(box_o, text='Target RA:').grid(row=1, column=0, sticky='W')
    tk.Label(box_o, textvariable=o_ra).grid(row=1, column=1, sticky='E')
    tk.Label(box_o, text='Target DEC:').grid(row=2, column=0, sticky='W')
    tk.Label(box_o, textvariable=o_dec).grid(row=2, column=1, sticky='E')
    tk.Button(box_o, text='Close Window', command=box.destroy, activebackground='dark gray', highlightbackground='gray').grid(row=3, columnspan=2)

    for child in box_f.winfo_children():  # For each item in the first frame, make the text really large
        child.config(font=large_font, bg='black', fg='red')
    for child in box_o.winfo_children():  # For each item in the second frame, make the text kinda large
        child.config(font=medium_font, bg='black', fg='red')
    center(box)  # Center the window if for some reason it doesn't open maximized


# Function for repositioning a window after it's been created
def center(win):
    win.update_idletasks()  # Something they said to do on stackexchange
    width = win.winfo_width()  # Grab window width, height
    height = win.winfo_height()
    x = (win.winfo_screenwidth() / 2) - (width / 2)  # Calculate width, height midpoint of the screen...
    y = (win.winfo_screenheight() / 2) - (height / 2)  # ...and subtract off the midpoint of the window
    win.geometry('+{}+{}'.format(x, y))  # Place window in the middle of the screen


# This function writes the log files
def log_action(action, object, details):  # A log entry contains action taken (GET, USE), the object name, and details
    # Actions: Searched, Aligned, Saved, Error
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 'now' is used for log entries
    today = datetime.datetime.now().strftime('%Y-%m-%d')  # 'today' is used for log file names
    o_log.insert(0, str('  '+object+' | '+details))  # Add an item to the recent log entries box
    o_log.insert(0, now+' - '+action)
    with open(today+'_ObservingLog.txt', 'a') as f:  # Append the log entry to the log file from today
        f.write(now+' - '+action+' | '+object+' | '+details+'\n')
    return


# --- Main GUI Code --- #

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

# Catalog Section Widgets
c_fill = [tk.StringVar(c, '--None--'), tk.StringVar(c, '--None--'), tk.StringVar(c, '--None--'), tk.StringVar(c, '--None--')]
# c_fill initializes four button labels with label '--None--'
c_entry = tk.Entry(c, width=30)  # This is the box for catalog/quick search
c_entry.bind('<KeyRelease>', lambda event: auto_fill(c_entry, c_fill))  # On any key release, run auto_fill()
c_entry.bind('<Return>', lambda event: quick_s(c_fill[0], False))  # On a return press, send top button to quick_s()
c_entry.bind('<BackSpace>', lambda event: clear_lock())  # Backspacing or deleting the entry box also clears tracking
c_entry.bind('<Delete>', lambda event: clear_lock())
# Catalog button initializations - start disabled with '--None--' text. On click, run quick_s() without tracking.
c_0 = tk.Button(c, textvariable=c_fill[0], state='disabled', command= lambda: quick_s(c_fill[0], False))
c_1 = tk.Button(c, textvariable=c_fill[1], state='disabled', command= lambda: quick_s(c_fill[1], False))
c_2 = tk.Button(c, textvariable=c_fill[2], state='disabled', command= lambda: quick_s(c_fill[2], False))
c_3 = tk.Button(c, textvariable=c_fill[3], state='disabled', command= lambda: quick_s(c_fill[3], False))
c_det = tk.Frame(c)  # Catalog entry items frame
c_name = tk.Entry(c_det, width=21)  # Entry box for user catalog items
c_ra = tk.Frame(c)  # User RA frame
c_dec = tk.Frame(c)  # User DEC frame

# User object RA and DEC boxes
ra_h = tk.Entry(c_ra, width=3, validate='key')  # Entry box, validate on keypress
ra_h['validatecommand'] = (ra_h.register(validate), '%P', 3)  # Validate function call, length 3 (+/-HH)
ra_m = tk.Entry(c_ra, width=2, validate='key')
ra_m['validatecommand'] = (ra_m.register(validate), '%P', 2)  # Validate length 2 (MM)
ra_s = tk.Entry(c_ra, width=5, validate='key')
ra_s['validatecommand'] = (ra_s.register(validate), '%P', 5)  # Validate length 5 (SS.SS)
dec_h = tk.Entry(c_dec, width=3, validate='key')
dec_h['validatecommand'] = (dec_h.register(validate), '%P', 3)
dec_m = tk.Entry(c_dec, width=2, validate='key')
dec_m['validatecommand'] = (dec_m.register(validate), '%P', 2)
dec_s = tk.Entry(c_dec, width=5, validate='key')
dec_s['validatecommand'] = (dec_s.register(validate), '%P', 5)
ra_t = ra_h, ra_m, ra_s  # pack variables
dec_t = dec_h, dec_m, dec_s  # pack em up for sending
c_use = tk.Button(c, text='Use', command= lambda: use(c_name.get(), ra_t, dec_t))  # Use the entered RA and DEC object
c_save = tk.Button(c, text='Save...', command= lambda: save_db(root, c_name.get(), ra_t, dec_t))  # Open window to save new user object

# Align Section Widgets
o_name = tk.StringVar(c, 'No Object Selected')  # Default values
o_ra = tk.StringVar(c, '---')
o_dec = tk.StringVar(c, '---')
o_ha = tk.StringVar(c, '---')
o_track = tk.IntVar()  # 0 or 1 variable for tracking
o_target = tk.Checkbutton(o, text=' Track Object', var=o_track)  # 0 is no tracking, 1 is tracking
o_target.bind('<ButtonRelease-1>', lambda event: track_s(o_name))  # On click, start tracking function with this object
o_align = tk.Button(o, text='Align on Object', command= lambda : confirm_align(o_name, o_ra, o_dec))
o_log = tk.Listbox(o, width=40, bg='dark gray', height=12)  # Recent log entries box

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
display_time_now(s_time)  # Start displaying the current times, now that the labels are created


# --- Section Layouts --- #
# This is done through a GRID layout.
# The columns are positioned through lines 225-231 (Section Frames Column Configuration)
# So each item only needs ROW options since it belongs to the column on a section frame basis

# Target Section Layout
tk.Label(c, text='CATALOG', relief='solid', width=40, height=2).grid(row=0)  # Section title
tk.Label(c, text='Quick Search').grid(row=1)
c_entry.grid(row=2)  # Catalog search box
c_0.grid(row=3)  # Buttons
c_1.grid(row=4)
c_2.grid(row=5)
c_3.grid(row=6)
tk.Frame(c, height=3, width=300, bd=1, relief='ridge').grid(row=7)  # Empty frame used as a visual separator
tk.Label(c, text='Enter New J2000 Object', height=2).grid(row=8)

# Custom Target Section Layout
c_det.grid(row=9)
tk.Label(c_det, text='Name:             ').pack(side='left')  # The extra spaces are due to lazy layout
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
dec_h.pack(side='right')  # Save and Use buttons
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
tk.Frame(o, height=3, width=300, bd=1, relief='ridge').grid(row=6)  # Empty frame used as a visual separator
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

tk.Frame(s, height=3, width=300, bd=1, relief='ridge').grid(row=5)  # Empty frame used as a visual separator
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
s_large.grid(row=12)  # Large window button

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
