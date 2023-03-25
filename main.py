import PySimpleGUI as sg
import yt_dlp
import os

URLS = []
URL_dict = dict()
song_info = ""

# Determines whether correct song has been inputted
waitingforConfirmation = False
ydl = yt_dlp.YoutubeDL({})
right_click_menu = ['', ['Paste', 'Select All', 'Cut']]

# Define the window's contents
layout = [
            # 1 ==========================================================================================================================================  
            [
                sg.Text("Enter the YouTube URL", text_color="Black", background_color="White")
            ],
            # 2 ==========================================================================================================================================
            [
                sg.Input(key='-INPUT-', text_color="Black", background_color="#cbcee6"),
                sg.Radio("Video", group_id= "Media Type", key="-MEDIA VIDEO-", default=True, text_color="Black", background_color="White"),
                sg.Radio("Audio", group_id= "Media Type", key="-MEDIA AUDIO-", text_color="Black", background_color="White"),
                sg.Button('Add Song', key="-ADD SONG-", button_color=("Black","White"))
            ],
            # 3 ==========================================================================================================================================
            [
                sg.Text(key='-NOTIFICATION-', text_color="Black", background_color="White")
            ],
            # 4 ==========================================================================================================================================
            [
                sg.Push(background_color="White"),
                sg.Button('Yes', key="-CONFIRM SONG-", button_color=("#282930","#a5d6a3"), visible=False),
                sg.Button('No', key="-REJECT SONG-", button_color=("#282930","#f94449"), visible=False),
                sg.Push(background_color="White")
            ],

            # 5 ==========================================================================================================================================
            [
                sg.Push(background_color="White"),
                sg.Multiline(key='-DOWNLOAD LIST-', auto_size_text=True, auto_refresh=True, expand_y=True, size = (60,10)),
                sg.Push(background_color="White")
            ],
            # 6 ==========================================================================================================================================
            [
                sg.Push(background_color="White"),
                sg.Button('Download 0 songs', key='-NUM SONGS-', button_color=("Black","White")),
                sg.Push(background_color="White")
            ]
        ]
          

# Create the window
window = sg.Window('Window Title', layout, background_color="White", resizable=True)

# Display and interact with the Window using an Event Loop
while True:
    event, values = window.read()

    # See if user wants to quit or window was closed
    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break

    # Check if the input is populated
    populated = len(values['-INPUT-']) > 0

    # Error Checking
    if event == '-ADD SONG-' and (not populated):
        window['-NOTIFICATION-'].Update('Invalid Input', text_color="Red")

    #  See if user wants to add a song
    if event == '-ADD SONG-' and not waitingforConfirmation:
        try:
            # Get info of the input URL and display info to the user to confirm the correct song has been chosen
            song_info = ydl.sanitize_info(ydl.extract_info(url = values['-INPUT-'], download=False))
            window['-NOTIFICATION-'].update("You are trying to download the vedio/audio(s):\n" + song_info["title"] + " by Uploader " + song_info["uploader"], text_color="Black")
            window['-ADD SONG-'].update(visible=False)
            window["-CONFIRM SONG-"].update(visible=True)
            window["-REJECT SONG-"].update(visible=True)
            waitingforConfirmation = True
        except Exception as e:
            window['-NOTIFICATION-'].Update("Error. Check the input")
    
    elif event == '-REJECT SONG-' and waitingforConfirmation:
        # Finish Confirmation
        waitingforConfirmation = False

        # Update the window
        window['-INPUT-'].update("")
        window['-NOTIFICATION-'].update("")
        window['-ADD SONG-'].update(visible=True)
        window["-CONFIRM SONG-"].update(visible=False)
        window["-REJECT SONG-"].update(visible=False)


    # Confirm if the correct song has been selected
    elif event == '-CONFIRM SONG-' and waitingforConfirmation:
        # Check if the song has already been added to the download list
        if(song_info["id"] in URL_dict):
            window['-NOTIFICATION-'].update("The song is already added to download.")
        else:
            # Store the song to download
            URL_dict[song_info["id"]] =  song_info["title"]
            URLS.append((values['-INPUT-'], window["-MEDIA AUDIO-"].get()))
            waitingforConfirmation = False
            
            window['-NUM SONGS-'].update("Download " + str(len(URLS)) + " songs")
            window['-NOTIFICATION-'].update('The song has been added to the download list.')
            window['-DOWNLOAD LIST-'].update(str(len(URLS))+ ". " + song_info["title"].upper() + "\n", append=True)
            window['-INPUT-'].update("")
        
        # Update the button
        window['-ADD SONG-'].update(visible=True)
        window["-CONFIRM SONG-"].update(visible=False)
        window["-REJECT SONG-"].update(visible=False)
    
    if event == "-NUM SONGS-":

        window['-NOTIFICATION-'].update('Starting Download')
        window.refresh()

        for songURL in URLS:

            ydl_opts = {}

            if songURL[1]:
                ydl_opts = {
                    'format': 'm4a/bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'm4a',
                    }]
                }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download(songURL[0])
        


# Finish up by removing from the screen
window.close()

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
        exists = id in URL_dict.keys()

        # Rename is exists
        if exists:

            # Name to replace by removing the brackets
            newName = directory_Element[ : idLocation1].strip()

            # Extension of the media
            extension = directory_Element[directory_Element.rfind("."): ]
            
            os.rename(directory_Element, newName + extension)