def char_check(text):
    object_names = ['Sirrah', 'Caph', 'Algenib', 'Schedar', 'Mirach', 'Achernar', 'Almach', 'Hamal', 'Polaris', 'Menkar',
                  'Algol', 'Electra', 'Taygeta', 'Maia', 'Merope', 'Alcyone', 'Atlas', 'Zaurak', 'Aldebaran', 'Rigel',
                  'Capella', 'Bellatrix', 'Elnath', 'Nihal', 'Mintaka', 'Arneb', 'Alnilam', 'Alnitak', 'Saiph',
                  'Betelgeuse', 'Menkalinan', 'Mirzam', 'Canopus', 'Alhena', 'Sirius', 'Adara', 'Wezen', 'Castor',
                  'Procyon', 'Pollux', 'Naos', 'Alphard', 'Regulus', 'Algieba', 'Merak', 'Dubhe', 'Denebola', 'Phecda',
                  'Minkar', 'Megrez', 'Gienah Corvi', 'Mimosa', 'Alioth', 'Vindemiatrix', 'Mizar', 'Spica', 'Alcor',
                  'Alcaid', 'Agena', 'Thuban', 'Arcturus', 'Izar', 'Kochab', 'Alphecca', 'Unukalhai', 'Antares',
                  'Rasalgethi', 'Shaula', 'Rasalhague', 'Cebalrai', 'Etamin', 'Kaus Australis', 'Vega', 'Sheliak',
                  'Nunki', 'Sulafat', 'Arkab Prior', 'Arkab Posterior', 'Rukbat', 'Albereo', 'Tarazed', 'Altair',
                  'Alshain', 'Sadr', 'Peacock', 'Deneb', 'Alderamin', 'Alfirk', 'Enif', 'Sadalmelik', 'Alnair',
                  'Fomalhaut', 'Scheat', 'Markab', 'Acamar', 'Acrux', 'Adhara', 'Alkaid', 'Alpheratz', 'Ankaa', 'Atria',
                  'Avior', 'Diphda', 'Gacrux', 'Gienah', 'Menkent', 'Miaplacidus',
                  'Mirfak', 'Sabik', 'Suhail', 'Zubenelgenubi', 'Mercury', 'Venus', 'Mars', 'Jupiter',
                  'Saturn', 'Uranus', 'Neptune', 'Pluto', 'Sun', 'Moon', 'Phobos', 'Deimos', 'Io', 'Europa', 'Ganymede',
                  'Callisto', 'Mimas', 'Enceladus', 'Tethys', 'Dione', 'Rhea', 'Titan', 'Hyperion', 'Iapetus', 'Ariel',
                  'Umbriel', 'Titania', 'Oberon', 'Miranda']
    with open('objects.txt', 'r') as f:
        line = f.readlines()
        custom_objs = [l.split(',') for l in line]
        for i in custom_objs: object_names.append(i[0])
        # print custom_objs

    object_list = [obj for obj in object_names if obj.lower().startswith(text.lower())]
    object_list.sort()
    if text == '':
        del object_list[:]
    for i in range(4):
        if len(object_list) < 4:
            object_list.append('--None--')
        i+=1
    return object_list
