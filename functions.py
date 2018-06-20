def autocomplete(text):
    """Input: string to search objects list for
    Output: List of matching names"""
    # Object names is all of the default stars, planets, and moons included in ephem
    object_names = ['Sirrah', 'Caph', 'Algenib', 'Schedar', 'Mirach', 'Achernar', 'Almach', 'Hamal', 'Polaris', 'Menkar', 'Algol', 'Electra', 'Taygeta', 'Maia', 'Merope', 'Alcyone', 'Atlas', 'Zaurak', 'Aldebaran', 'Rigel', 'Capella', 'Bellatrix', 'Elnath', 'Nihal', 'Mintaka', 'Arneb', 'Alnilam', 'Alnitak', 'Saiph', 'Betelgeuse', 'Menkalinan', 'Mirzam', 'Canopus', 'Alhena', 'Sirius', 'Adara', 'Wezen', 'Castor', 'Procyon', 'Pollux', 'Naos', 'Alphard', 'Regulus', 'Algieba', 'Merak', 'Dubhe', 'Denebola', 'Phecda', 'Minkar', 'Megrez', 'Gienah Corvi', 'Mimosa', 'Alioth', 'Vindemiatrix', 'Mizar', 'Spica', 'Alcor', 'Alcaid', 'Agena', 'Thuban', 'Arcturus', 'Izar', 'Kochab', 'Alphecca', 'Unukalhai', 'Antares', 'Rasalgethi', 'Shaula', 'Rasalhague', 'Cebalrai', 'Etamin', 'Kaus Australis', 'Vega', 'Sheliak', 'Nunki', 'Sulafat', 'Arkab Prior', 'Arkab Posterior', 'Rukbat', 'Albereo', 'Tarazed', 'Altair', 'Alshain', 'Sadr', 'Peacock', 'Deneb', 'Alderamin', 'Alfirk', 'Enif', 'Sadalmelik', 'Alnair', 'Fomalhaut', 'Scheat', 'Markab', 'Acamar', 'Acrux', 'Adhara', 'Alkaid', 'Alpheratz', 'Ankaa', 'Atria', 'Avior', 'Diphda', 'Gacrux', 'Gienah', 'Menkent', 'Miaplacidus', 'Mirfak', 'Sabik', 'Suhail', 'Zubenelgenubi', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'Sun', 'Moon', 'Phobos', 'Deimos', 'Io', 'Europa', 'Ganymede', 'Callisto', 'Mimas', 'Enceladus', 'Tethys', 'Dione', 'Rhea', 'Titan', 'Hyperion', 'Iapetus', 'Ariel', 'Umbriel', 'Titania', 'Oberon', 'Miranda']
    # 'objects.txt' contains all user-added objects
    with open('objects.txt', 'r') as f:
        line = f.readlines()
        custom_objs = [l.split(',') for l in line]
        # Append all object names from this list to the set of object_names
        for i in custom_objs: object_names.append(i[0])

    # Check if the entry text matches any of the objects collected
    object_list = [obj for obj in object_names if obj.lower().startswith(text.lower())]
    object_list.sort()  # Sort them alphabetically
    if text == '':  # If the sent text was blank
        del object_list[:]  # Make sure the object list is empty
    for i in range(4):
        if len(object_list) < 4:  # Since we always have four buttons that display options, we need to make unfilled...
            object_list.append('--None--')  # ...boxes display the text '--None--'
        i+=1  # Check next list length
    return object_list  # Send collected objects list back to GUI