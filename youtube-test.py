import os  
URLdict = {'oN2Xs-MvxLw': 'Zack Hemsey - "The Way (Instrumental)"',
'CrTmHil72ls': "Laid-Back Camp - Ending | Fuyu Biyori"}

for directory_Element in os.listdir(r"./"):

    # Store the possible location / index of the possible id
    idLocation1 = directory_Element.rfind("[")

    # Check if the possible id exists
    if idLocation1 > 0 :

        # Store the ending location / index of the possible id
        idLocation2 = directory_Element.rfind("]")

        # Store the possible id
        id = directory_Element[idLocation1 + 1 : idLocation2]

        # Check if the id exists in the URL dictonary
        exists = id in URLdict.keys()

        # Rename is exists
        if exists:

            # Name to replace by removing the brackets
            newName = directory_Element[ : idLocation1].strip()

            # Extension of the media
            extension = directory_Element[directory_Element.rfind("."): ]
            
            os.rename(directory_Element, newName + extension)
