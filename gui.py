#!/usr/bin/python
# -*- coding: utf-8 -*-

import Tkinter as tk
import datetime, ephem, tkFont
from autocomplete import char_check
from db import save_db
import tkMessageBox
import enc_sim as enc, scope as sc

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
        o.after(10000, lambda : search(obj, type))  # ...repeat the lookup after a second and update HA
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
                return obj
            else:
                log_action('GET User Object', name, 'Read user database failed')


# Track an object, aka update HA every second
def track_o(name):
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


# # Update the scope poition every second
# def track_s():
#     if s_track.get() == 1:  # If tracking is now on...
#         log_action('Track', 'Scope', 'Tracking Started')  # .. log action
#
#         position = scope.where()  # Grab scope position to confirm align
#         st = rho.sidereal_time()  # Grab RHO sidereal time
#         ha = '%s' % ephem.hours(st - ephem.hours(position[0]))  # Calc HA of object from RHO
#         s_ha.set(ha)
#         s_dec.set(str(position[1]))
#         s_tick_ha.set(scope.data['Ticks'][-1][0])
#         s_tick_dec.set(scope.data['Ticks'][-1][1])
#     else:
#         log_action('Track', 'Scope', 'Tracking Stopped')


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


# Align function. Pulls RA and DEC from encoders
def confirm_align(star):
    result = tkMessageBox.askyesno("Align Telescope", "Are you sure?")
    if result is True:
        # Check if encoders are available
        try:
            ra = enc.Enc('RAEncoder')
            dec = enc.Enc('DECEncoder')
        except:
            log_action('ALIGN', 'Scope', 'Encoder(s) not found')
        else:
            # Initialize encoders
            ra = enc.Enc('RAEncoder')
            success = ra.connect()
            if not success:
                log_action('Connect', 'Encoder', 'RAEncoder failed to initialize')
            dec = enc.Enc('DECEncoder')
            success = dec.connect()
            if not success:
                log_action('Connect', 'Encoder', 'DECEncoder failed to initialize')

            # Look up the star
            try:
                ephem.star(star)  # Check if 'name' is a named star
            except KeyError:
                obj = read_db(star)  # If not, read 'name' from the custom objects database (Weird to do but w/e)
            else:
                obj = ephem.star(star)  # But if it was a star...
            obj.compute(rho)
            # Create Scope object
            scope = sc.Scope(obj, ra, dec)
            position = scope.where()  # Grab scope position to confirm align
            st = rho.sidereal_time()  # Grab RHO sidereal time
            ha = '%s' % ephem.hours(st - ephem.hours(position[0]))  # Calc HA of object from RHO
            s_ha.set(ha)
            s_dec.set(str(position[1]))
            s_tick_ha.set(scope.data['Ticks'][-1][0])
            s_tick_dec.set(scope.data['Ticks'][-1][1])
            log_action('Align Success', obj.name, str('HA: '+position[0]+' | DEC: '+position[1]))
            s_ready.set('Telescope Aligned')
            s_scope.config(fg='black')
    else:
        # Do nothing
        return


# Validate is used for multiple text entry boxes to limit the number of numbers entered.
def validate(value, ii):  # The function call includes the max number length, ii
    if len(value) > int(ii):  # if the length is longer then this number ii
        return False  # Don't allow the number to be typed
    return True  # Else, go ahead and let the number be typed


# Code to display fullscreen display of scope coordinates.
def view_large():
    box = tk.Toplevel(root, bg='black')  # Open a new window
    large_font = tkFont.Font(size=80)  # Set large font text size
    medium_font = tkFont.Font(size=50)  # Set not-so-large text size
    box.attributes('-zoomed', True)  # Start window maximized
    box.title('RhoPi Large View')  # Title

    box_f = tk.Frame(box, bg='black')  # Frame within the box window
    box_f.pack(side='top', fill='x', expand=1)  # Placement of frame
    box_f.grid_columnconfigure(0, weight=1)

    tk.Label(box_f, text='INFORMATION', relief='solid', width=27).grid(row=0)  # Section labels/text variables and positions
    tk.Label(box_f, text='Scope DEC: ').grid(row=1, sticky='W')
    tk.Label(box_f, textvariable=s_dec).grid(row=1, sticky='E')
    tk.Label(box_f, text='Scope HA: ').grid(row=2, sticky='W')
    tk.Label(box_f, textvariable=s_ha).grid(row=2, sticky='E')

    box_o = tk.Frame(box, bg='black')  # Second frame in box window
    box_o.pack(side='top', fill='x', expand=1)  # Second frame placement
    box_o.grid_columnconfigure(0, weight=1)

    tk.Label(box_o, text='', width=30).grid(row=0, columnspan=2)  # Section labels/text variables and positions
    tk.Label(box_o, text='Target HA:').grid(row=1, column=0, sticky='W')
    tk.Label(box_o, textvariable=o_ha).grid(row=1, column=1, sticky='E')
    tk.Label(box_o, text='Target DEC:').grid(row=2, column=0, sticky='W')
    tk.Label(box_o, textvariable=o_dec).grid(row=2, column=1, sticky='E')

    tk.Button(box, text='Close Window', command=box.destroy, bg='gray15', fg='red').pack(side='top')

    for child in box_f.winfo_children():  # For each item in the first frame, make the text really large
        child.config(font=large_font, bg='black', fg='red', padx=10)
    for child in box_o.winfo_children():  # For each item in the second frame, make the text kinda large
        child.config(font=medium_font, bg='black', fg='red', padx=10)
    center(box)  # Center the window if for some reason it doesn't open maximized

# Code to display fullscreen display of scope coordinates.
def view_help():
    h = tk.Toplevel(root, pady=10, padx=20)  # Open a new window
    h.title('RhoPi Help')  # Title

    tk.Label(h, text='HOW TO USE THIS PROGRAM', relief='solid', height=2)
    tk.Label(h, text='1) Search for an object to align the telescope to using Quick Search')
    tk.Label(h, text='2) Move the telescope to the chosen object and click ALIGN')
    tk.Label(h, text='3) The telescope position in HA and DEC will now be available')
    tk.Label(h, text='Note: Realigning should only necessary if the program is returning incorrect values')

    tk.Label(h, text='Catalog Section', relief='solid', height=2)
    tk.Label(h, text='This section allows searching of 129 built-in objects, as well as any user-created objects')
    tk.Label(h, text='Type a star, planet, or moon in the text box to search the databases')
    tk.Label(h, text='Click the button with the object name, or press enter to select the first option')
    tk.Label(h, text='You can also enter the coordinates of an object not in the database by clicking "Save New..."')

    tk.Label(h, text='Object Section', relief='solid', height=2)
    tk.Label(h, text='This section shows details about the previously chosen object')
    tk.Label(h, text='The RA, HA, and DEC are for the current date and time. Tracking updates HA every 5 seconds')
    tk.Label(h, text='To align the telescope, point the scope at the object chosen and click ALIGN')
    tk.Label(h, text='This will grab the encoder values and convert them into HA and DEC')
    tk.Label(h, text='Most program actions are also logged, such as searching and tracking')
    tk.Label(h, text='A record of all actions can be found in /logs/{Date}_ObservingLog.txt')

    tk.Label(h, text='Information Section', relief='solid', height=2)
    tk.Label(h, text='This section shows details about the current object and scope positions')
    tk.Label(h, text='"View Large" will open a window with only scope details in red on black font')

    for child in h.winfo_children():  # This is all layout related code for the help window
        if child['height'] is not 2:
            child.pack(side='top', anchor='w', padx=10)
        else:
            child.pack(side='top', expand=1, fill='x', pady=10)

    tk.Button(h, text='Close', fg='red', height=2, command=h.destroy).pack(side='top', anchor='e')

    center(h)  # Center the window if for some reason it doesn't open maximized


def virtual_scope():
    def move_scope(ra, dec):
        scope.ra.move(ra)
        scope.dec.move(dec)

    v = tk.Toplevel(root, pady=5, padx=5)
    v.title('Super Scope 64')
    tk.Label(v, text='Move virtual scope (in minutes/degrees)').pack(side='top', expand=1, fill='x')
    mv = tk.Frame(v)
    mv.pack(side='top', expand=1, fill='x')
    tk.Label(mv, text='RA:').grid(row=0, column=0, sticky='w')
    ra = tk.Entry(mv)
    ra.grid(row=0, column=1, sticky='e')
    tk.Label(mv, text='DEC:').grid(row=1, column=0, sticky='w')
    dec = tk.Entry(mv)
    dec.grid(row=1, column=1, sticky='e')
    tk.Button(v, text='Move', command= lambda event: move_scope(ra.get(), dec.get())).pack(side='top', expand=1, fill='x', anchor='e')



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
    o_log.insert(0, str('  '+details))  # Add an item to the recent log entries box
    o_log.insert(0, str('  '+action+': '+object))
    o_log.insert(0, now)
    with open(today+'_ObservingLog.txt', 'a') as f:  # Append the log entry to the log file from today
        f.write(now+' - '+action+' | '+object+' | '+details+'\n')
    return


# --- Main GUI Code --- #

# Window Options
root = tk.Tk()
root.title("RhoPi Telescope Pointing v0.1.0 (beta)")
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.minsize(width=1023, height=518)
root.grid_columnconfigure(0, weight=1)
default_font = tkFont.nametofont("TkDefaultFont")
default_font.configure(size=11, family='system')

# Observer Setup
rho = ephem.Observer()
rho.lon, rho.lat = '-82.586203', '29.400249'


# --- Section Frames Column Configuration --- #
g = tk.Frame(root)  # Holds columns
g.pack(side='top', fill='both', expand=1)
c = tk.Frame(g)  # c is for catalog section widgets
c.pack(side='left', fill='y', expand=1)
o = tk.Frame(g)  # a is for align section widgets
o.pack(side='left', fill='y', expand=1)
s = tk.Frame(g)  # s is for information section widgets
s.pack(side='left', fill='y', expand=1)


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
c_save = tk.Button(c, text='Save New...', command= lambda: save_db(root, c_name.get(), ra_t, dec_t))  # Open window to save new user object

# Align Section Widgets
o_name = tk.StringVar(c, 'No Object Selected')  # Default values
o_ra = tk.StringVar(c, '---')
o_dec = tk.StringVar(c, '---')
o_ha = tk.StringVar(c, '---')
o_track = tk.IntVar()  # 0 or 1 variable for tracking
o_target = tk.Checkbutton(o, text=' Track Object', var=o_track)  # 0 is no tracking, 1 is tracking
o_target.bind('<ButtonRelease-1>', lambda event: track_o(o_name))  # On click, start tracking function with this object
o_align = tk.Button(o, text='Align on Object', command= lambda : confirm_align(o_name.get()))
o_log = tk.Listbox(o, width=35, bg='dark gray', height=12)  # Recent log entries box

# Information Section Widgets
s_target = tk.StringVar(s, '---')
s_time = tk.StringVar(s, '---')
s_utc = tk.StringVar(s, '---')
s_lst = tk.StringVar(s, '---')
s_ready = tk.StringVar(s, 'Telescope Not Aligned')
s_scope = tk.Label(s, textvariable=s_ready, height=2, fg='red')
s_ha = tk.StringVar(s, '---')
s_dec = tk.StringVar(s, '---')
s_tick_ha = tk.StringVar(s, '---')
s_tick_dec = tk.StringVar(s, '---')
s_large = tk.Button(s, text='View Large Info', height=2, command=view_large)
display_time_now(s_time)  # Start displaying the current times, now that the labels are created


# --- Section Layouts --- #
# This is done through a GRID layout.
# The columns are packed to the left in lines 225-231 (Section Frames Column Configuration)
# So each item only needs ROW options since it belongs to the column on a section frame basis

# Target Section Layout
tk.Label(c, text='CATALOG', relief='solid', width=35, height=2).grid(row=0)  # Section title
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
tk.Label(c_det, text='Name:             ').pack(side='left')  # The extra spaces are due to lazy layout choices
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
tk.Label(o, text='OBJECT', relief='solid', width=35, height=2).grid(row=0)  # Section Title
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
tk.Label(s, text='INFORMATION', relief='solid', width=35, height=2).grid(row=0)  # Section Title
tk.Label(s, text='Time').grid(row=1)
tk.Label(s, text='Local Time (EST):').grid(row=2, sticky='W')
tk.Label(s, textvariable=s_time).grid(row=2, sticky='E')
tk.Label(s, text='Universal Time (UTC):').grid(row=3, sticky='W')
tk.Label(s, textvariable=s_utc).grid(row=3, sticky='E')
tk.Label(s, text='Sidereal Time (LST):').grid(row=4, sticky='W')
tk.Label(s, textvariable=s_lst).grid(row=4, sticky='E')

tk.Frame(s, height=3, width=300, bd=1, relief='ridge').grid(row=5)  # Empty frame used as a visual separator
s_scope.grid(row=6)
tk.Label(s, text='Scope HA: ').grid(row=7, sticky='W')
tk.Label(s, textvariable=s_ha).grid(row=7, sticky='E')
tk.Label(s, text='Scope DEC: ').grid(row=8, sticky='W')
tk.Label(s, textvariable=s_dec).grid(row=8, sticky='E')
tk.Label(s, text='Raw Tick RA:').grid(row=9, sticky='W')
tk.Label(s, textvariable=s_tick_ha).grid(row=9, sticky='E')
tk.Label(s, text='Raw Tick DEC:').grid(row=10, sticky='W')
tk.Label(s, textvariable=s_tick_dec).grid(row=10, sticky='E')
tk.Label(s, text=' ').grid(row=11)  # Spacer
s_large.grid(row=12)  # Large window button

# Close and HELP frame
ch = tk.Frame(root)
ch.pack(side='top', anchor='ne', padx=20, expand=1)
# Close program button
close = tk.Button(ch, fg='red', text='Close', width=10, height=2, command=root.destroy)
close.pack(side='right')
# Open help button
help = tk.Button(ch, fg='black', text='View Help', width=10, height=2, command=view_help)
help.pack(side='right', anchor='ne', padx=20, expand=1)
root.bind('<F1>', lambda event: view_help())
root.bind('<F10>', lambda event: virtual_scope())

# Global Frame settings
for child in c.winfo_children():
    child.grid_configure(padx=10, pady=5)
for child in o.winfo_children():
    child.grid_configure(padx=10, pady=5)
for child in s.winfo_children():
    child.grid_configure(padx=10, pady=5)

root.lift()
root.mainloop()