from PyQt6 import QtGui, QtCore
from PyQt6.QtWidgets import QMainWindow, QApplication, QDialog
import design
import sys
import os
import pygame
import subprocess

pygame.mixer.init()


"""Block of functions out of class"""
def is_music(playlist: list) -> list:
    # Removes non-music files from playlist
    for item in playlist:
        if item[-4:-1]+item[-1] != '.mp3' and item[-4:-1]+item[-1] != '.wav':
            playlist.remove(item)
    return playlist


def normal_name(text: str) -> str:
    # Returns song name without file extension
    text = text.replace('.mp3', '')
    text = text.replace('.wav', '')
    return text


def convert(seconds: int):
    # Converts seconds to min-sec style
    seconds = seconds % (24 * 3600)
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)


def open_folder():
    # Opens music folder depending of system
        if sys.platform == "win32":
            os.startfile('music')
        else:
            opener ="open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, 'music'])


def add_to_playlist() -> list:
        # Adds music from music folder to playlist
        playlist = is_music(os.listdir('music'))
        return playlist


#Add first song and initialize playlist
playlist = add_to_playlist()
if len(playlist) > 0:
    pygame.mixer.music.load('music/'+playlist[0])


class ExampleApp(QMainWindow):
    # Class for GUI and functions to control music
    def __init__(self):
        super().__init__()

        # Setting the new application
        self.ui = design.Ui_MainWindow()
        self.ui.setupUi(self)

        """Important variables for functions"""
        # Bool variables
        self.check_volume = True
        self.check_settings = False
        self.slider_changed = False
        self.looping = False
        # Digit variables
        self.i = 0
        self.folder_button_y = 535
        self.music_time_now = 0
        self.prev_volume = 0.88
        # Icon variables
        self.volune_button_icon = QtGui.QIcon()
        self.pause_icon = QtGui.QIcon()
        self.loop_icon = QtGui.QIcon()

        if len(playlist) == 0:
        # Condition opens music folder if it's clear
            open_folder()

        elif len(playlist) > 0:
        # If not - player works
            # Play and set first music
            pygame.mixer.music.play()
            pygame.mixer.music.set_volume(0.88)
            self.pause_resume()

            # Settings of GUI elements and calling current methods
            self.ui.pause_button.clicked.connect(self.pause_resume)
            self.ui.prev_button.clicked.connect(self.prev)
            self.ui.next_button.clicked.connect(self.next)
            self.ui.volume_button.clicked.connect(self.volume_off)
            self.ui.add_song_button.clicked.connect(open_folder)
            self.ui.settings_button.clicked.connect(self.move_button)
            self.ui.loop_button.clicked.connect(self.loop)
            self.ui.volume_slider.valueChanged.connect(self.volume)
            self.ui.progress_slider_controlled.valueChanged.connect(self.follow_progress)
            self.ui.progress_slider_controlled.sliderReleased.connect(self.progress_changed)
            self.mus = pygame.mixer.Sound('music/'+playlist[self.i])
            self.labels(playlist[self.i], int(pygame.mixer.Sound.get_length(self.mus)))

            # Timer for update-function and music timer
            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(self.activate_every_half_second)
            self.timer.setInterval(500)
            self.timer.start()


            self.now = int(pygame.mixer.music.get_pos()/1000)
            self.total = int(pygame.mixer.Sound.get_length(self.mus))


    """Block of functions 1. Labels settings, update-function and music timer"""
    def labels(self, song: str, duration: int):
    # Sets text to the labels(song name, current time and total time)
        self.ui.song_name.setText(normal_name(song))
        self.ui.total_time.setText(convert(duration))


    def activate_every_half_second(self):
        self.update()
        self.music_timer_update()


    def update(self):
        # Update information every 0.5 sec
        if not self.slider_changed:
            self.now = int(pygame.mixer.music.get_pos()/1000)
            self.total = int(pygame.mixer.Sound.get_length(self.mus))
            self.ui.cur_time.setText(convert(self.music_time_now))
            self.progress()
            self.is_next()
        self.labels(playlist[self.i], int(pygame.mixer.Sound.get_length(self.mus)))
        add_to_playlist()


    def is_next(self):
    # Plays the next song, when current is over(don't delete it)
        if self.total < self.music_time_now:
            if not self.looping:
                self.next()
            elif self.looping:
                pygame.mixer.music.play()
                self.music_time_now = 0
                return self.music_time_now


    def music_timer_update(self):
        if not self.slider_changed and pygame.mixer.music.get_busy():
            self.music_time_now += 0.5
        return self.music_time_now


    """Block of functions 2. Pause and Resume"""
    def pause_resume(self):
    #Checks the signal and pauses or resumes music
        if not pygame.mixer.music.get_busy():
            self.pause()
            pygame.mixer.music.unpause()
        elif pygame.mixer.music.get_busy():
            self.resume()
            pygame.mixer.music.pause()


    def pause(self):
        self.pause_icon.addPixmap(QtGui.QPixmap("src/pause.png"), QtGui.QIcon.Mode.Active, QtGui.QIcon.State.Off)
        self.ui.pause_button.setIcon(self.pause_icon)


    def resume(self):
        self.pause_icon.addPixmap(QtGui.QPixmap("src/resume.png"), QtGui.QIcon.Mode.Active, QtGui.QIcon.State.Off)
        self.ui.pause_button.setIcon(self.pause_icon)


    """Block of functions 3. Play previous or next music"""
    def prev(self):
    # Plays previous song, when prev_button is clicked
        now = self.music_time_now
        self.music_time_now = 0
        if now < 5:
            pygame.mixer.music.stop()
            self.i -= 1
            #Condition is needed to loop playlist
            if self.i >= 0:
                self.mus = pygame.mixer.Sound('music/'+playlist[self.i])
                pygame.mixer.music.load('music/'+playlist[self.i])
                pygame.mixer.music.play()
                self.pause()
                return [self.i, self.mus, self.music_time_now]
            else:
                self.i = len(playlist)-1
                self.mus = pygame.mixer.Sound('music/'+playlist[self.i])
                pygame.mixer.music.load('music/'+playlist[self.i])
                pygame.mixer.music.play()
                self.pause()
                return [self.i, self.music_time_now]
        elif now >=5:
            pygame.mixer.music.play()
            return self.music_time_now


    def next(self):
    # Plays next song, when next_button is clicked
        pygame.mixer.music.stop()
        self.i += 1
        self.music_time_now = 0
        #Condition is needed to loop playlist
        if self.i < len(playlist):
            self.mus = pygame.mixer.Sound('music/'+playlist[self.i])
            pygame.mixer.music.load('music/'+playlist[self.i])
            pygame.mixer.music.play()
            self.pause()
            return [self.i, self.mus, self.music_time_now]
        else:
            self.i = 0
            self.mus = pygame.mixer.Sound('music/'+playlist[self.i])
            pygame.mixer.music.load('music/'+playlist[self.i])
            pygame.mixer.music.play()
            self.pause()
            return [self.i, self.music_time_now]


    """Block of functions 4. Progress Bar"""
    def progress(self):
    # Move Progress Bar depending on current music time (calls in update-function)
        value = int((self.music_time_now/self.total)*100)
        self.ui.progress_slider.setValue(value)


    def progress_changed(self):
    # Plays music at the time, depending on Controlled Progress Bar's value
        value = self.ui.progress_slider_controlled.value()
        time_value = (value*self.total)/100
        pygame.mixer.music.set_pos(time_value)
        pygame.mixer.music.unpause()
        self.pause()
        self.now = time_value
        if time_value > self.music_time_now:
            self.music_time_now += (time_value - self.music_time_now)
        elif time_value < self.music_time_now:
            self.music_time_now -= self.music_time_now - time_value
        self.progress()
        self.ui.cur_time.setText(convert(self.now))
        self.slider_changed = False
        return [self.now, self.slider_changed, self.music_time_now]


    def follow_progress(self):
    # Moves Progress Bar and changes label's text depending on Controlled Progress Bar's value.
    # Calls, when Controlled Progress Bar is used
        pygame.mixer.music.pause()
        value = self.ui.progress_slider_controlled.value()
        time_value = (value*self.total)/100
        value = self.ui.progress_slider_controlled.value()
        self.ui.progress_slider.setValue(value)
        self.ui.cur_time.setText(convert(int(time_value)))
        self.slider_changed = True
        return self.slider_changed


    """Block of functions 5. Volume"""
    def volume(self):
    # Changes volume
        volume_value = self.ui.volume_slider.value()/100
        pygame.mixer.music.set_volume(volume_value)
        if volume_value == 0:
            self.volune_button_icon.addPixmap(QtGui.QPixmap("src/soundoff.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            self.ui.volume_button.setIcon(self.volune_button_icon)
        else:
            self.volune_button_icon.addPixmap(QtGui.QPixmap("src/sound.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            self.ui.volume_button.setIcon(self.volune_button_icon)


    def volume_off(self):
    # Funtion to configure volume button
        self.check_volume = not self.check_volume
        if self.check_volume:
            self.ui.volume_slider.setValue(self.prev_volume*100)
            pygame.mixer.music.set_volume(self.prev_volume)
            self.volune_button_icon.addPixmap(QtGui.QPixmap("src/sound.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            self.ui.volume_button.setIcon(self.volune_button_icon)
        elif not self.check_volume:
            self.prev_volume = self.ui.volume_slider.value()/100
            self.ui.volume_slider.setValue(0)
            pygame.mixer.music.set_volume(0)
            self.volune_button_icon.addPixmap(QtGui.QPixmap("src/soundoff.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            self.ui.volume_button.setIcon(self.volune_button_icon)
            return self.prev_volume


    """Block of functions 7. Loop button"""
    def loop(self):
        self.looping = not self.looping
        if not self.looping:
            self.loop_icon.addPixmap(QtGui.QPixmap("src/loop.png"), QtGui.QIcon.Mode.Active, QtGui.QIcon.State.Off)
            self.ui.loop_button.setIcon(self.loop_icon)
        elif self.looping:
            self.loop_icon.addPixmap(QtGui.QPixmap("src/loop_true.png"), QtGui.QIcon.Mode.Active, QtGui.QIcon.State.Off)
            self.ui.loop_button.setIcon(self.loop_icon)
        return self.looping


    """Block of functions 6. Settings button"""
    def move_button(self):
    # Animates, shows/hides folder button
        self.check_settings = not self.check_settings
        if self.check_settings:
            self.ui.add_song_button.show()
            self.settingsTimer1 = QtCore.QTimer()
            self.settingsTimer1.setInterval(30)
            self.settingsTimer1.timeout.connect(self.move_up)
            self.settingsTimer1.start()
        elif not self.check_settings:
            self.settingsTimer2 = QtCore.QTimer()
            self.settingsTimer2.setInterval(30)
            self.settingsTimer2.timeout.connect(self.move_down)
            self.settingsTimer2.start()


    def move_up(self):
    # Moves button up and shows it
        if self.folder_button_y > 490:
            self.folder_button_y -= 5
            self.ui.add_song_button.move(720, self.folder_button_y)
            return self.folder_button_y
        elif self.folder_button_y <= 490:
            self.settingsTimer1.stop()


    def move_down(self):
    # Moves button dows and hides it
        if self.folder_button_y < 535:
            self.folder_button_y += 5
            self.ui.add_song_button.move(720, self.folder_button_y)
        elif self.folder_button_y >= 535:
            self.ui.add_song_button.hide()
            self.settingsTimer2.stop()

class WarningExample(QDialog):
    def __init__(self):
        super().__init__()

        # Setting the new application
        self.warning = design.Ui_Dialog()
        self.warning.setupUi(self)

        self.warning.okey_button.clicked.connect(self.close_function)

    def close_function(self):
        self.warning.done()


def main():
    # Main function. Initializes window, shows it and opens
    app = QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('src/icon.png'))
    if len(playlist) > 0:
        window = ExampleApp()
        window.show()
    elif len(playlist) == 0:
        open_folder()
        warning_dialog = WarningExample()
        warning_dialog.show()
    app.exec()


if __name__ == '__main__':
    main()