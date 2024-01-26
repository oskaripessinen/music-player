from pytube import *
import os
import customtkinter as ctk
import vlc
import time
import datetime
import threading


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

if not os.path.exists("musics"):
    os.makedirs("musics")

def song_download(link):
    current_lib = os.path.dirname(__file__)
    library = os.path.join(current_lib, "musics")

    yt = YouTube(link)
    vid = yt.streams.filter(only_audio=True).first() 
    vid.download(library)

def playlist_download(link): #download playlist
    
    current_lib = os.path.dirname(__file__)
    library = os.path.join(current_lib, "musics")

    linkit = []
    sl = Playlist(link)
    for url in sl.video_urls:
        linkit.append(url)
        root.update()
    for i in linkit:
        yt = YouTube(i)
        vid = yt.streams.filter(only_audio=True).first()
        vid.download(library)
        root.update()



def clear_window(): 
    for obj in root.winfo_children():
       obj.destroy()

def delete_the_playlist():
    current_lib = os.path.dirname(__file__)
    library = os.path.join(current_lib, "musics")

    for fil in os.listdir(library):
        file_path = os.path.join(library, fil)
        os.remove(file_path)

def play_music(): #plays the music

    current_lib = os.path.dirname(__file__)
    library = os.path.join(current_lib, "musics")

    global media_list
    global media_player
    global player2

    player = vlc.Instance()
    media_list = player.media_list_new()
    media_player = vlc.MediaListPlayer()
    player2 = media_player.get_media_player()

    for fil in os.listdir(library):
        song = os.path.join(library, fil)
        media = player.media_new(song)
        media_list.add_media(media)
        media_player.set_media_list(media_list)
        


def pause_resume():
    
    if media_player.is_playing():
        media_player.pause()
        play.grid(row=2, column=1,pady=5)
        pause.grid_forget()

    else:
        media_player.play()
        pause.grid(row=2, column=1,pady=5)
        play.grid_forget()
        time.sleep(0.1)
        update_slider()
    
    now_playing()
    
    
    

def now_playing():

    song_path = media_player.get_media_player().get_media().get_mrl()

    song_name = os.path.basename(song_path)
    song_name = song_name.replace(".mp4", "")
    song_name = song_name.replace("%20", " ")
    song_name = song_name.replace("%5", " ")
    song_name = song_name.replace("%", " ")
    song_name = song_name.split(" ")
    if len(song_name) > 8:
        del song_name[9::]
        song_name = " ".join(song_name)
    
    now_playing_label.configure(text=song_name)
    

    
def update_slider():
    
    lenght = player2.get_length()/1000
    slider.configure(to=lenght)
    
    
        
    current_time = player2.get_time()/1000
    slider.set(current_time)

    if current_time >= lenght-1000:
        now_playing()

    min_current_time = str(datetime.timedelta(seconds=int(current_time)))
    min_current_time = min_current_time[2::]

    min_song_lenght = str(datetime.timedelta(seconds=int(lenght)))
    min_song_lenght = min_song_lenght[2::]

    time_progress.configure(text=min_current_time+"/"+min_song_lenght)
    
    root.after(100, update_slider)
    


def move_slider(value):
    player2.set_time(int(value * 1000))
        
        



def download_button(): 
    m = link_entry.get()
    link_entry.delete(0,ctk.END)
    downloading_label.grid(row=2, column=0, columnspan=2,pady=5)
    root.update()
    try:
        try:
            song_download(m)
        except:
            playlist_download(m)
    except:
        downloading_label.grid_forget()
        error.grid(row=2, column=0, columnspan=2,pady=5)
        root.update()
        time.sleep(1)
        error.grid_forget()
        root.update()

    downloading_label.grid_forget()
    
    
def clear_media_list(): #clear the media list

    media_list.lock()
    for i in range(media_list.count()):
        media_list.remove_index(0)
    media_list.unlock()


def next_song(): 
    if media_player.is_playing():
        media_player.next()
    else:
        pause.grid(row=2, column=1,pady=5)
        play.grid_forget()
        media_player.next()
    time.sleep(0.1)
    now_playing()
    
    
def prev(): 
    if media_player.is_playing():
        media_player.previous()
    else:
        pause.grid(row=2, column=1,pady=5)
        play.grid_forget()
        media_player.previous()
    time.sleep(0.1)
    now_playing()


def avaa_2(): #open ui2
    
    play_music()
    clear_window()
    clear_media_list()
    ui2()

    
def avaa_1():  #open ui1
    if media_player.is_playing():
        media_player.pause()
        play.grid(row=1, column=1,pady=5)
        pause.grid_forget()
        media_player.stop()
    clear_media_list()
    clear_window()
    ui1()  

def download_thread():
    my_thread = threading.Thread(target=download_button)

    my_thread.start()

    

def ui1(): #download page ui

    global sl_linkki
    global link_entry
    global downloading_label
    global error


    

    frame = ctk.CTkFrame(master=root)
    frame.pack(pady=0, padx=30, fill="both", expand=True)

    link_entry = ctk.CTkEntry(frame, placeholder_text="Song or playlist Link",font=font2, width=200,corner_radius=1)
    link_entry.grid(row=1, column=0, padx=15, pady=30)



    download_button = ctk.CTkButton(frame, text="Download", command=download_thread, font=font2, width=80,corner_radius=1)
    download_button.grid(row=1, column=1)

    downloading_label = ctk.CTkLabel(frame, text="Dowloading...", font=font2)
    downloading_label.grid(row=2, column=0, columnspan=2, pady=5)
    downloading_label.grid_forget()

    error = ctk.CTkLabel(frame, text="Error!", font=font2, text_color="red")
    error.grid(row=2, column=0, columnspan=2, pady=5)
    error.grid_forget()

    text = ctk.CTkLabel(frame, text="Enter the youtube link of the public playlist or song.", font=font2)
    text.grid(row=3, column=0, pady=15, padx=0, columnspan=2)

    open_player = ctk.CTkButton(frame, text="Open the player", width=300, height=35, command=avaa_2,corner_radius=1)
    open_player.grid(row=4, column=0, columnspan=2, pady=5,padx=15)

    delete_playlist = ctk.CTkButton(frame, text="Delete playlist", width=300, height=35, command=delete_the_playlist, corner_radius=1, fg_color="red", hover_color="red4")
    delete_playlist.grid(row=5, column=0, columnspan=2, pady=10,padx=15)
    


def ui2(): #player ui
    global play
    global pause
    global frame
    global now_playing_label
    global slider
    global time_progress

    clear_media_list()
    play_music()
    
    frame = ctk.CTkFrame(master=root)
    frame.pack(pady=0, padx=30, fill="both", expand=True)

    download_button = ctk.CTkButton(frame,text="Download more", command=avaa_1, corner_radius=1,width=340, height=30)
    download_button.grid(row=0, column=0,columnspan=3,pady=3)

    now_playing_label = ctk.CTkLabel(frame, text="", font=font2)
    now_playing_label.grid(row=1, column=0,columnspan=3, pady=100, rowspan=2)

    back = ctk.CTkButton(frame, text="◁◁", corner_radius=1, height=33, width=35, font=("arial",26), command=prev)
    back.grid(row=2, column=1,pady=0, sticky="w")

    play = ctk.CTkButton(frame, text="▶", corner_radius=1, height=35,width=50, font=("arial",28), command=pause_resume)
    play.grid(row=2, column=1,pady=0)

    pause = ctk.CTkButton(frame, text="▐ ▌", corner_radius=1, height=35,width=50, font=("arial",12), command=pause_resume)
    pause.grid(row=2, column=1,pady=0)
    pause.grid_forget()
    
    next = ctk.CTkButton(frame, text="▷▷", corner_radius=1, height=33, width=35, font=("arial",26), command=next_song)
    next.grid(row=2, column=1,pady=0, sticky="e")

    time_progress = ctk.CTkLabel(frame, font=font2, text="")
    time_progress.grid(row=2, column=0, pady=0, columnspan=3, sticky="s")

    slider = ctk.CTkSlider(frame, from_ = 0, to = 1, border_width=1, height=10, command=move_slider)
    slider.set(0)
    slider.grid(row=3, column=0, columnspan=3)
    
    
    
root = ctk.CTk()
font1 = ctk.CTkFont("Bahnschrift SemiBold",34)
font2 = ctk.CTkFont("Bahnschrift",12)


root.geometry("400x300")
root.resizable(0, 0)
root.title("")

ui1()

root.mainloop()