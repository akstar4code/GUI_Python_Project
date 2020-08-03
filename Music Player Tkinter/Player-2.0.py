from tkinter import*
from tkinter import messagebox
from tkinter import filedialog  # to open file directory
import pygame
from time import strftime,gmtime,sleep
from mutagen.mp3 import MP3
import tkinter.ttk as ttk
from webbrowser import open_new_tab

## Bulid app
root = Tk()
root.title('MP3 Player')  # add title
root.geometry('500x450')  # dimension

# Initialize Pygame
pygame.mixer.init()


# create a function to deal with time
def play_time():
    global song_dir
    # check to see if song is stopped
    if stopped:
        return

    # get the current time of song play
    current_time = pygame.mixer.music.get_pos() / 1000
    # convert the time format
    converted_current_time = strftime('%M:%S', gmtime(current_time))

    # find the current song length

    song = playlist_box.get(ACTIVE)
    song_name = song
    song = f'{song_dir}/{song}'

    song_mut = MP3(song)
    global song_length
    song_length = song_mut.info.length
    # converted time format
    converted_song_length = strftime('%M:%S', gmtime(song_length))
    # my_label.config(text=song_length)

    # song length in slider
    # song_slider.config(to=song_length)
    # my_label.config(text=song_slider.get())

    # Check to see if song is over
    if int(song_slider.get()) == int(song_length):
        # do something
        stop()
    # paused function
    elif paused:
        # Check to see if paused and pass
        # song_slider.config(value=current_time)
        pass
    else:
        # move slider along 1 second at a time
        next_time = int(song_slider.get()) + 1
        # Output new time value to slider and the length
        song_slider.config(to=song_length, value=next_time)

        # convert the slider position to time format
        converted_current_time = strftime('%M:%S', gmtime(int(song_slider.get())))
        # output slider
        status_bar.config(text=f'Time Elapsed : {converted_current_time} / {converted_song_length}  ')

    # add current time to status bar
    if current_time >= 1:
        status_bar.config(text=f'Time Elapsed : {converted_current_time} / {converted_song_length}  ')
        # my_label.after(1000, play_time) # call after every 1000 ms (1sec)
    # create a loop to check time every secs
    status_bar.after(1000, play_time)

# creating the global varibale for directory
global song_dir


# add song to playlist
def add_song():
    global song_dir
    song = filedialog.askopenfilename(title='Choose A Song', filetypes=(('mp3 file', '*.mp3'),))
    # strip out directory structure and .mp3 from file name
    song_dir,song_name = song.rsplit('/',1)
    #print(song_dir)
    #print(song_name)
    # my_label.config(text=song)
    playlist_box.insert(END, song_name)


def add_many_songs():
    global song_dir
    songs = filedialog.askopenfilenames(initialdir='audio/', title='Choose A Song', filetypes=(('mp3 file', '*.mp3'),))
    # strip out directory structure and .mp3 from file name
    # loop through song list and we have many songs
    for song in songs:
        song_dir,song_name = song.rsplit('/',1)
        # add the end of the playlist
        playlist_box.insert(END, song_name)


# create a function to delete the songs
def delete_songs():
    playlist_box.delete(ANCHOR)  # anchor that click get highlight


def delete_all_songs():
    playlist_box.delete(0, END)  # like the range


# create the play function
def play():
    global song_dir
    # set stopped to false
    global stopped
    stopped = False

    # Reconstruct the song with directory
    try:
        song = playlist_box.get(ACTIVE)
        song_name = song
        song = f'{song_dir}/{song}'
        my_label.config(text=song_name)
        # loop song to play the song
        pygame.mixer.music.load(song)
        # play the songs
        pygame.mixer.music.play(loops=0)  # Play the song once

        # get song time
        play_time()
    except :
        pass

# create the stopped variable
global stopped
stopped = False


# stop function to stop song
def stop():
    # stop the song
    pygame.mixer.music.stop()
    # clear playlist bar
    playlist_box.select_clear(ACTIVE)
    # cofigure the stauts bar for stop of sog
    status_bar.config(text='')
    text = "'Welcome to Mp3 Player2.0'\n'Created by Ashok'"
    my_label.config(text=text)
    # set our slider to zero
    song_slider.config(value=0)
    # set stop variable to true
    global stopped
    stopped = True


# create the paused function
global paused
paused = False


# Pause function
def pause(is_paused):
    global paused
    paused = is_paused
    if paused:
        # unpause
        pygame.mixer.music.unpause()
        paused = False
    else:
        # pause
        pygame.mixer.music.pause()
        paused = True


# create the function of next button
def next_song():
    global song_dir
    # Reset the slider position to play the next song
    status_bar.config(text='')
    song_slider.config(value=0)

    # get the current song number
    next_one = playlist_box.curselection()  # return the tuple of number
    try:
        # my_label.config(text=next_one)
        # Add one to the current song number from tuple
        next_one = next_one[0] + 1
        # grab the song the title from the playlist
        song = playlist_box.get(next_one)
        # song of the directory
        my_label.config(text=song)
        song = f'{song_dir}/{song}'
        # load the songs
        pygame.mixer.music.load(song)
        # play the songs
        pygame.mixer.music.play(loops=0)

        # clear active bar in playlist
        playlist_box.select_clear(0, END)
        # mov active bar to next song
        playlist_box.activate(next_one)
        playlist_box.selection_set(next_one, last=None)
    except:
        messagebox.showwarning(title='Information',message='You are at End or No song Selected')
        stop()
        #playlist_box.activate(0)
        #playlist_box.selection_set(0, last=None)

def prev_songs():
    global song_dir
    # Reset the slider position to play the next song
    status_bar.config(text='')
    song_slider.config(value=0)
    # get the current song number
    next_one = playlist_box.curselection()  # return the tuple of number
    try:
        # my_label.config(text=next_one)
        # Add one to the current song number from tuple
        next_one = next_one[0] - 1
        # grab the song the title from the playlist
        song = playlist_box.get(next_one)
        # song of the directory
        my_label.config(text=song)
        song = f'{song_dir}/{song}'
        # load the songs
        pygame.mixer.music.load(song)
        # play the songs
        pygame.mixer.music.play(loops=0)

        # clear active bar in playlist
        playlist_box.select_clear(0, END)
        # mov active bar to next song
        playlist_box.activate(next_one)
        playlist_box.selection_set(next_one, last=None)
    except:
        messagebox.showwarning(title='Information',message='You are at Begining or No song Selected')
        stop()
# creating the volumne function
def volume(x):
    # my_label.config(text=volume_slider.get())
    pygame.mixer.music.set_volume(volume_slider.get())


# create the scale function
def slide(x):
    global song_dir
    try:
        # Reconstruct the song with directory
        song = playlist_box.get(ACTIVE)
        song_name = song
        song = f'{song_dir}/{song}'
        my_label.config(text=song_name)
        # loop song to play the song
        pygame.mixer.music.load(song)
        # play the songs
        pygame.mixer.music.play(loops=0, start=song_slider.get())  # pygame doesn't know the song length
    except :
        pass

# Exiting from the application by using any quit or destroy
def end_program():
    #root.quit()
    if messagebox.askyesno(title='Are you sure ?',message='This will close all playlist and application Window',):
        root.destroy()
    else:
        return
# Help section of program
def quick_guide_message():
    text = "'This the basic version of Mp3 Music Player '\n'" \
           "FILE OPTION: You can add songs to playlist and exit the application if you wish'\n'" \
           "EDIT OPTION: You can edit your playlist by delete the songs you don't want' \n'" \
           "HELP OPTION: for all queries and updates'"
    messagebox.showinfo(title='Quick Guide',message=text)
def about_us():
    text = " 'Welcome to MP3 Music Player 2.0'\n'This application was developed by Ashok Kumar under Supervisor of John Elder '"
    messagebox.showinfo('About Us',text)
def check_update():
    messagebox.showinfo('Updates','You are using the latest version !')

# Contact Us
def mail_link():
    open_new_tab('https://mail.google.com/mail/u/0/#inbox?compose=CllgCJNxPFlgrhZfqzPzQTpdMWJbkrrJqkCqFGwxmmBhkBxJHrKDpRKdhtdhMGblNxthpFHcBJq')
def telegram_link():
    open_new_tab("https://telegram.me/ashok_telegram")
def github_link():
    open_new_tab('https://github.com/akstar4code/GUITinker')


# Create the main frame
# adding the volumne slider
main_frame = Frame(root)
main_frame.pack(pady=20)


# create playlist by listbox
# select to change the color of background
playlist_box = Listbox(main_frame, bg='black', fg='green',width=60, selectbackground='green', selectforeground='black')
playlist_box.grid(row=0, column=0)  # to give above dist

# adding the scrollbar in playlist box
scrollbar = Scrollbar(main_frame, orient = VERTICAL, command= playlist_box.yview)
#scrollbar.config(troughcolor='Red')
playlist_box.config(yscrollcommand = scrollbar.set)
scrollbar.grid(row=0,column=0, sticky=(NS,E))

# create the volume slider frame
volume_frame = LabelFrame(main_frame, text='Volume')
volume_frame.grid(row=0, column=1, padx=15)

# Create the volumne slider
volume_slider = ttk.Scale(volume_frame, from_=1, to=0, orient=VERTICAL, length=125, value=1, command=volume)
volume_slider.pack(pady=10)

# create the song slider
song_slider = ttk.Scale(main_frame, from_=0, to=100, orient=HORIZONTAL, length=360, value=0, command=slide)
song_slider.grid(row=2, column=0, pady=10)

# define button images for controls
back_btn_img = PhotoImage(file='images/back50.png')
forward_btn_img = PhotoImage(file='images/forward50.png')
play_btn_img = PhotoImage(file='images/play50.png')
pause_btn_img = PhotoImage(file='images/pause50.png')
stop_btn_img = PhotoImage(file='images/stop50.png')
# instead of text we use the images


# create the button frame
control_frame = Frame(main_frame)
control_frame.grid(row=1, column=0, pady=20)

# Play play/stop button
back_button = Button(control_frame, image=back_btn_img, borderwidth=0, command=prev_songs)
forward_button = Button(control_frame, image=forward_btn_img, borderwidth=0, command=next_song)
play_button = Button(control_frame, image=play_btn_img, borderwidth=0, command=play)
pause_button = Button(control_frame, image=pause_btn_img, borderwidth=0, command=lambda: pause(paused))
stop_button = Button(control_frame, image=stop_btn_img, borderwidth=0, command=stop)

# place them as grid on window
back_button.grid(row=0, column=0, padx=10)
forward_button.grid(row=0, column=1, padx=10)
play_button.grid(row=0, column=2, padx=10)
pause_button.grid(row=0, column=3, padx=10)
stop_button.grid(row=0, column=4, padx=10)

# Create the Menu

my_menu = Menu(root)
root.config(menu=my_menu)

# File menu creation contains basic operation
file = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label = 'File',menu=file)
file.add_command(label = 'Add a song to Playlist..', command=add_song)
file.add_command(label = 'Add multiple song to Playlist..', command=add_many_songs)
file.add_separator()
# Adding the other options as close
file.add_command(label = 'Exit', command=end_program)

# Edit menu creation contains deleting options
edit = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label = 'Edit',menu=edit)
edit.add_command(label = 'Delete a song from Playlist..', command=delete_songs)
edit.add_command(label = 'Delete multiple songs from Playlist..', command=delete_all_songs)

# Help section
help = Menu(my_menu,tearoff = 0)
my_menu.add_cascade(label='Help',menu=help)
help.add_command(label='Quick Guide', command=quick_guide_message)
help.add_command(label='About Us', command=about_us)
help.add_command(label='Check for Updates...',command=check_update)

# Contact Us section
contact = Menu(my_menu,tearoff = 0)
my_menu.add_cascade(label='Contact Us',menu=contact)
contact.add_command(label='Write a Mail to us ...', command=mail_link)
contact.add_command(label='Connect via Telegram...', command=telegram_link)
contact.add_separator()
contact.add_command(label='Contribute to App...', command=github_link)

# create status bar
status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)  # fill the x axis

# Temporary Label
text = "'Welcome to Mp3 Player2.0'\n'Created by Ashok'"
my_label = Label(root, text=text)
my_label.pack(pady=20)

root.mainloop()

# Play songs by library by Pygame
