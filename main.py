import PySimpleGUI as sg
import yt_dlp
from yt_dlp import YoutubeDL
import os

URLS = []
URL_set = set()
song_info = ""

waitingforConfirmation = False
ydl = yt_dlp.YoutubeDL({})

# Define the window's contents
layout = [
            # 1 ==========================================================================================================================================  
            [
                sg.Text("Enter the YouTube URL", text_color="Black", background_color="White")
            ],
            # 2 ==========================================================================================================================================
            [
                sg.Input(key='-INPUT-', text_color="Black", background_color="#cbcee6"),
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
            song_info = ydl.sanitize_info(ydl.extract_info(url = values['-INPUT-'], download=False))
            window['-NOTIFICATION-'].update("Is this the song you are trying to download \n" + song_info["title"] + " by Uploader " + song_info["uploader"], text_color="Black")
            #window['-ADD SONG-'].update("Yes", button_color=("#282930","#a5d6a3"))
            window['-ADD SONG-'].update(visible=False)
            window["-CONFIRM SONG-"].update(visible=True)
            waitingforConfirmation = True
        except:
            window['-NOTIFICATION-'].Update('Something went wrong. \n Check the internet or the URL and try again later.')
            

    # Confirm if the correct song has been selected
    elif event == '-CONFIRM SONG-' and waitingforConfirmation:
        if(song_info["id"] in URL_set):
            window['-NOTIFICATION-'].update("The song is already added to download.")
        else:
            URL_set.add(song_info["id"])
            URLS.append(values['-INPUT-'])
            waitingforConfirmation = False
            
            window['-NUM SONGS-'].update("Download " + str(len(URLS)) + " songs")
            window['-NOTIFICATION-'].update('The song has been added to the download list.')
            window['-DOWNLOAD LIST-'].update(str(len(URLS))+ ". " + song_info["title"].upper() + "\n", append=True)
            window['-INPUT-'].update("")
        
        # Update the button
        window['-ADD SONG-'].update(visible=True)
        window["-CONFIRM SONG-"].update(visible=False)
    
    if event == "-NUM SONGS-":

        window['-NOTIFICATION-'].update('Starting Download')
        window.refresh()
        
        ydl_opts = {
            'format': 'm4a/bestaudio/best',
            # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
            'postprocessors': [{  # Extract audio using ffmpeg
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'm4a',
            }]
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(URLS)
        
        for directory_Element in os.listdir(r"./"):
            if directory_Element.endswith(".m4a"):
                oldName = directory_Element
                newName = directory_Element.split("[")[0].split("(")[0].strip() + ".m4a"
                os.rename(oldName,newName)        

# Finish up by removing from the screen
window.close()
