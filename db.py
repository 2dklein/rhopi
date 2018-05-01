import ephem, datetime, time, tkMessageBox
import Tkinter as tk


# Save to database file function
def save_db(root, name_t, ra_t, dec_t):  # root is base window that it belongs to.. weird tkinter thing

    def change_dropdown(subtype, spec):  # Object type dropdown selection
        subtype_val.set(subtype[obj_type.get()])
        chars = set('TBDSV')  # If the dropdown displays one of these star types...
        if any((c in chars) for c in subtype_val.get()):
            spec.config(state='normal')  # ... spectral class is enabled
        else:
            spec.delete(0, 'end')  # ... otherwise, clear out spectral class box
            spec['state'] = 'disabled'  # Spectral class is disabled

    def validate(value, ii):  # Same validate function as before
        if len(value) > int(ii):
            return False
        return True

    def save(name, ra_t, dec_t, mag, spec):
        # Reset fill boxes if error occurred previously
        name['bg'] = 'white'
        mag['bg'] = 'white'
        spec['bg'] = 'white'
        [dec.config(bg='white') for dec in dec_t]
        [ra.config(bg='white') for ra in ra_t]

        # Create string variables to add to error message box if errors
        name_err, ra_err, dec_err, mag_err, spec_err = tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()

        # Verify all entries and set errors messages if there's a problem
        errors = [name_err, ra_err, dec_err, mag_err, spec_err]
        try:
            if not bool(name.get().strip()):  # Check if name has usable text (aka not blank)
                raise Exception
            with open('objects.txt', 'r') as f:
                line = f.readlines()  # Read each line of objects.txt
                user_objs = [l.split(',') for l in line]  # Create list of objects
                # Check user objects for object with the same name
                for object in user_objs:
                    if name.get().lower() == object[0].lower():  # Object[0] is the name
                        raise Exception  # If you are trying to add a duplicate object, flag as error
        except:
            name_err.set('Name cannot be blank or match an existing user object!')  # Here's the error
            name['bg'] = 'pink'  # Mark box with error in pink
        for ra in ra_t:
            try:
                float(ra.get())
            except ValueError:
                ra_err.set('Right Ascension error! Format: -00:00:00.00 or 00:00:00')
                [ra.config(bg='pink') for ra in ra_t]
        for dec in dec_t:
            try:
                float(dec.get())
            except ValueError:
                dec_err.set('Declination error! Format: -00:00:00.00 or 00:00:00')
                [dec.config(bg='pink') for dec in dec_t]
        try:
            float(mag.get())
        except:
            mag_err.set('Magnitude error! Format: -00.00 or 00.00')
            mag['bg'] = 'pink'

        if spec['state'] == 'normal':
            try:
                spec_test = str(spec.get())
                chars = 'OBAFGKMobafgkm'  # One of these characters should be first
                if not any((c in chars) for c in spec_test[0]):
                    spec_err.set('Spectral class error! Format: F0 or A')
                if len(spec_test) > 1:  # If there's more than just the spectral class, check if the second digit is int
                    int(spec_test[1])
            except:
                spec_err.set('Spectral class error! Format: F0 or A')
                spec['bg'] = 'pink'
        elif spec['state'] == 'disabled':
            spec_err.set('')

        if all(error.get() == '' for error in errors):  # Check if all error messages are blank
            if tkMessageBox.askyesno("Confirm Save", "Are you sure?"):  # Final confirmation for adding user object
                # Write to custom object database
                ra = ' '.join([r.get() for r in ra_t])
                dec = ' '.join([de.get() for de in dec_t])
                with open('objects.txt', 'a') as f:
                    print name.get()+',f|'+subtype[obj_type.get()]+'|'+spec.get()+','+ra+','+dec+','+mag.get()+',2000,0\n'
                    f.write(name.get()+',f|'+subtype[obj_type.get()]+'|'+spec.get()+','+ra+','+dec+','+mag.get()+',2000,0\n')
                log_action('SAVE Custom', name.get(), str('RA: '+ra+' | DEC: '+dec))  # Log action
                time.sleep(1)  # Pause for a second to prevent double saves
            d.destroy()  # Close save dialog window
        else:  # If there are errors, display them in a popup windown telling them what they did wrong
            error_popup = tk.Toplevel(d)
            error_popup.title('Error Message')
            for err in errors:
                if err is not '':
                    tk.Label(error_popup, text=err.get(), fg='red').pack()
            center(error_popup)

    def center(win):  # Center the popup windows
        win.update_idletasks()
        width = win.winfo_width()
        height = win.winfo_height()
        x = (win.winfo_screenwidth() / 2) - (width / 2)
        y = (win.winfo_screenheight() / 2) - (height / 2)
        win.geometry('+{}+{}'.format(x, y))

    def log_action(action, event, details):  # Log actions taken into logfile for today
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        with open(today+'_ObservingLog.txt', 'a') as f:
            f.write(now+' - '+action+' | '+event+' | '+details+'\n')
        return


    # --- Create Frames --- #
    d = tk.Toplevel(root)
    d.title('Save to Database')
    ra = tk.Frame(d)
    dec = tk.Frame(d)

    # --- Initialize Widgets --- #
    subtype = {'Quasar': 'Q', 'Nebula, Bright': 'N', 'Star': 'S', 'Cluster, Open': 'O', 'Galaxy, Spherical': 'H',
               'Supernova': 'Y', 'Star, Vis. Double': 'D', 'Nebula, Dark': 'K', 'Star, Multiple': 'M',
               'Supernova Remnant': 'R', 'Galaxy, Spiral': 'G', 'Star, Variable': 'V', 'Radio': 'J',
               'Cluster, Globular': 'C', 'Pulsar': 'L', 'Nebula, Planetary': 'P',
               'Stellar Object': 'T', 'Nebula, Diffuse': 'F', 'Star, Binary': 'B'}  # Subclass options
    subtype_val = tk.StringVar()
    obj_type = tk.StringVar(d)
    obj_type.set('Star')  # set the default option for dropdown
    choices = sorted(subtype.keys())  # Pull the keys from the dictionary, sort, and use as dropdown options
    subclass = tk.OptionMenu(d, obj_type, *choices)
    empty = tk.StringVar()
    name = tk.Entry(d, width=42)
    name.insert(0, name_t)

    ra_h = tk.Entry(ra, width=3, validate='key')
    ra_h['validatecommand'] = (ra_h.register(validate), '%P', 3)  # Length check for entry boxes
    ra_h.insert(0, ra_t[0].get())
    ra_m = tk.Entry(ra, width=2, validate='key')
    ra_m['validatecommand'] = (ra_m.register(validate), '%P', 2)
    ra_m.insert(0, ra_t[1].get())
    ra_s = tk.Entry(ra, width=5, validate='key')
    ra_s['validatecommand'] = (ra_s.register(validate), '%P', 5)
    ra_s.insert(0, ra_t[2].get())

    dec_h = tk.Entry(dec, width=3, validate='key')
    dec_h['validatecommand'] = (dec_h.register(validate), '%P', 3)
    dec_h.insert(0, dec_t[0].get())
    dec_m = tk.Entry(dec, width=2, validate='key')
    dec_m['validatecommand'] = (dec_m.register(validate), '%P', 2)
    dec_m.insert(0, dec_t[1].get())
    dec_s = tk.Entry(dec, width=5, validate='key')
    dec_s['validatecommand'] = (dec_s.register(validate), '%P', 5)
    dec_s.insert(0, dec_t[2].get())

    mag = tk.Entry(d, width=7, validate='key')
    mag['validatecommand'] = (mag.register(validate), '%P', 6)
    spec = tk.Entry(d, width=3, validate='key')
    spec['validatecommand'] = (spec.register(validate), '%P', 2)
    obj_type.trace('w', lambda _, __, ___: change_dropdown(subtype, spec))


    # --- Layout --- #
    # Left side
    tk.Label(d, text='All Fields Required', fg='red', width=42, height=2, relief='solid').grid(row=0, columnspan=2)
    tk.Label(d, text='Name:').grid(row=1, columnspan=2, sticky='W')

    ra.grid(row=2, column=0, sticky='W')  # Frame holding the RA coords
    tk.Label(ra, text='RA:  ').pack(side='left')
    ra_s.pack(side='right')
    center(d)
    tk.Label(ra, text=':').pack(side='right')
    ra_m.pack(side='right')
    tk.Label(ra, text=':').pack(side='right')
    ra_h.pack(side='right')

    dec.grid(row=3, column=0, sticky='W')  # Frame with DEC coords
    tk.Label(dec, text='DEC: ').pack(side='left')
    dec_s.pack(side='right')
    tk.Label(dec, text=':').pack(side='right')
    dec_m.pack(side='right')
    tk.Label(dec, text=':').pack(side='right')
    dec_h.pack(side='right')

    tk.Label(d, text='Object Type: ', height=2).grid(row=4, columnspan=2, sticky='W')
    subclass.grid(row=4, columnspan=2, sticky='E')
    tk.Label(d, textvariable=empty, width=12).grid(row=5, column=0, sticky='W')

    # Right Side
    name.grid(row=1, columnspan=2, sticky='E')
    tk.Label(d, text='Magnitude: ').grid(row=2, column=1, sticky='W')
    mag.grid(row=2, column=1, sticky='E')
    tk.Label(d, text='Spectral Class: ').grid(row=3, column=1, sticky='W')
    spec.grid(row=3, column=1, sticky='E')
    dbs = tk.Frame(d)
    dbs.grid(row=5, column=1)

    ra_t = ra_h, ra_m, ra_s
    dec_t = dec_h, dec_m, dec_s
    tk.Button(dbs, text='Save to DB', command=lambda: save(name, ra_t, dec_t, mag, spec)).pack(side='left')
    tk.Button(dbs, text='Cancel', fg='red', command=d.destroy).pack(side='left')

    for child in d.winfo_children():
        child.grid_configure(padx=10, pady=2)
    center(d)
