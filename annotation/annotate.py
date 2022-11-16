"""
    Bare Bones Media Player Demo with Playlist.  Adapeted from media player located at https://github.com/israel-dryer/Media-Player
    Original Author :   Israel Dryer
    Modified to be a PySimpleGUI Demo Program
    A very simple media player ready for you to customize.  Uses the VLC player to playback local files and YouTube streams.  You will need to install the Python bindings for VLC as well as the VLC player itself.
    You will need to pip install:
        pip install python-vlc
        pip install youtube-dl
"""
import os

import PySimpleGUI as sg
import vlc
from sys import platform as PLATFORM


#------- GUI definition & setup --------#
sg.theme('DarkBlue')


def btn(name):  # a PySimpleGUI "User Defined Element" (see docs)
    return sg.Button(name, size=(8, 1), pad=(1, 1))


layout = [[btn('Music'), btn('SFX'), btn('Voice')],
          [sg.Image('', size=(300, 170), key='-VID_OUT-')],
          [btn('load'), btn('play'), btn('next'), btn('pause'), btn('stop')],
          [sg.Text('Load media to start', key='-MESSAGE_AREA-')]]

window = sg.Window('Mini Player', layout, element_justification='center', finalize=True, resizable=True)

window['-VID_OUT-'].expand(True, True)                # type: sg.Element

"""------------ Media Player Setup ---------"""

inst = vlc.Instance()
list_player = inst.media_list_player_new()
media_list = inst.media_list_new([])

annotations = []
current_file = ""
list_player.set_media_list(media_list)
player = list_player.get_media_player()
player.set_rate(2)
if PLATFORM.startswith('linux'):
    player.set_xwindow(window['-VID_OUT-'].Widget.winfo_id())
else:
    player.set_hwnd(window['-VID_OUT-'].Widget.winfo_id())


"""------------ The Event Loop ------------"""

# player.vlm_set_loop("death_note", True)

while True:
    event, values = window.read()       # run with a timeout so that current location can be updated
    if event == sg.WIN_CLOSED:
        break

    if event == 'play' or event == 'next':
        list_player.stop()
        if len(annotations) == 0:
            continue

        for item in annotations:
            list_player.set_media_list([item])
            current_file = item
            break
        annotations = annotations[1:]
        list_player.play()
    if event == 'pause':
        list_player.pause()
    if event == 'stop':
        list_player.stop()
    # if event == 'previous':
    #     list_player.previous()      # first call causes current video to start over
    #     list_player.previous()      # second call moves back 1 video from current
    #     list_player.play()
    if event == 'load':
        # if values['-VIDEO_LOCATION-'] and not 'Video URL' in values['-VIDEO_LOCATION-']:
        #     media_list.add_media(values['-VIDEO_LOCATION-'])
        #     list_player.set_media_list(media_list)
        #     window['-VIDEO_LOCATION-'].update('Video URL or Local Path:') # only add a legit submit
        folder = sg.popup_get_folder("Chọn thư mục")
        for video in os.listdir(folder):
            split_tup = os.path.splitext(video)
            # extract the file name and extension
            file_name = split_tup[0]
            file_extension = split_tup[1]
            if file_extension in [".mp4", ".mkv"]:
                annotations.append(f"{folder}/{video}")
            # list_player.set_media_list(media_list)
        sg.popup_ok("Tải xong")
    elif event == "Music" or event == "SFX" or event == "Voice":
        file_dir, file_path = os.path.split(current_file)
        os.makedirs(f"{file_dir}/{event}", exist_ok=True)
        os.rename(current_file, f"{file_dir}/{event}/{file_path}")

    # update elapsed time if there is a video loaded and the player is playing
    if player.is_playing():
        title = player.get_title()
        window['-MESSAGE_AREA-'].update("{} {:02d}:{:02d} / {:02d}:{:02d}".format(title, *divmod(player.get_time()//1000, 60), *divmod(player.get_length()//1000, 60)))
        # if player.get_time() // 1000 >= player.get_length() // 1000 - 4:
            # stop before 3s
            # list_player.pause()
            # sg.popup_ok("Vui lòng chọn thể loại")
    else:
        window['-MESSAGE_AREA-'].update('Load media to start' if media_list.count() == 0 else 'Ready to play media' )

window.close()
