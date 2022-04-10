from PyQt6 import QtGui, QtCore
from PyQt6.QtWidgets import QMainWindow, QApplication
import design, sys, os, pygame, subprocess

pygame.mixer.init()
#Converts seconds to min-sec style
def convert(seconds):
    seconds = seconds % (24 * 3600)
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)
#Deletes the .DS_Store file
def minusCash(list):
    Cash = '.DS_Store'
    i = 0
    for item in list:
        if item == Cash:
            del list[i]
        i += 1
    return list
#Add first song and initialize playlist
playlist = os.listdir('music')
playlist = minusCash(playlist)
pygame.mixer.music.load('music/'+playlist[0])
first = pygame.mixer.Sound('music/'+playlist[0])
#Class for GUI and functions for controlling music
class ExampleApp(QMainWindow):
    def __init__(self):
        super().__init__()
        #Setting the new application
        self.ui = design.Ui_MainWindow()
        self.ui.setupUi(self)
        #Variables for functions
        self.check = False
        self.checkVolume = True
        self.checkSettings = False
        self.i = 0
        self.igrek = 535
        self.angle = 0
        self.prevVolume = 0.88
        self.pic = QtGui.QIcon()
        self.pr = QtGui.QIcon()
        #Play and set first music
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(0.88)
        #Settings of GUI elements and calling current methods
        self.ui.pauseButton.clicked.connect(self.pause_resume)
        self.ui.prevButton.clicked.connect(self.prev)
        self.ui.nextButton.clicked.connect(self.next)
        self.ui.volumeButton.clicked.connect(self.volumeOff)#
        self.ui.addSongButton.clicked.connect(self.openFolder)#
        self.ui.settingsButton.clicked.connect(self.moveButton)#
        self.ui.volumeSlider.valueChanged.connect(self.volume)
        self.mus = pygame.mixer.Sound('music/'+playlist[self.i])
        self.labels(playlist[self.i], int(pygame.mixer.Sound.get_length(first)))
        #Timer for update-function
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.setInterval(500)
        self.timer.start()

    # Function to set text to the labels(song name, current time and total time)
    def labels(self, song, long):
        self.ui.songName.setText(song.replace('.mp3',''))
        self.ui.curTime.setText(convert(int(pygame.mixer.music.get_pos()/1000)))
        self.ui.label_4.setText(convert(long))
    #Fuction to update information every 0.5 sec
    def update(self):
        self.ui.curTime.setText(convert(int(pygame.mixer.music.get_pos()/1000)))
        now = int(pygame.mixer.music.get_pos()/1000)
        total = int(pygame.mixer.Sound.get_length(self.mus))
        self.progress(now, total)
        self.isNext(now, total)
        self.labels(playlist[self.i], int(pygame.mixer.Sound.get_length(self.mus)))
        self.addToPlaylist()#

    """Functions to control music"""
    #Checks the signal and pauses or resumes music
    def pause_resume(self):
        self.check = not self.check
        if not self.check:
            self.pause()
            pygame.mixer.music.unpause()
        elif self.check:
            self.resume()
            pygame.mixer.music.pause()
    def pause(self):
        self.pr.addPixmap(QtGui.QPixmap("src/pause.png"), QtGui.QIcon.Mode.Active, QtGui.QIcon.State.Off)
        self.ui.pauseButton.setIcon(self.pr)
    def resume(self):
        self.pr.addPixmap(QtGui.QPixmap("src/resume.png"), QtGui.QIcon.Mode.Active, QtGui.QIcon.State.Off)
        self.ui.pauseButton.setIcon(self.pr)
    #Playing previous and next music
    def prev(self):
        now = int(pygame.mixer.music.get_pos()/1000)
        if now < 5:
            pygame.mixer.music.stop()
            self.i -= 1
            #Condition is needed to loop playlist
            if self.i >= 0:
                self.mus = pygame.mixer.Sound('music/'+playlist[self.i])
                pygame.mixer.music.load('music/'+playlist[self.i])
                pygame.mixer.music.play()
                self.pause()
                return [self.i, self.mus]
            else:
                self.i = len(playlist)-1
                self.mus = pygame.mixer.Sound('music/'+playlist[self.i])
                pygame.mixer.music.load('music/'+playlist[self.i])
                pygame.mixer.music.play()
                self.pause()
                return self.i
        elif now >=5:
            pygame.mixer.music.play()
    def next(self):
        pygame.mixer.music.stop()
        self.i += 1
        #Condition is needed to loop playlist
        if self.i < len(playlist):
            self.mus = pygame.mixer.Sound('music/'+playlist[self.i])
            pygame.mixer.music.load('music/'+playlist[self.i])
            pygame.mixer.music.play()
            self.pause()
            return [self.i, self.mus]
        else:
            self.i = 0
            self.mus = pygame.mixer.Sound('music/'+playlist[self.i])
            pygame.mixer.music.load('music/'+playlist[self.i])
            pygame.mixer.music.play()
            self.pause()
            return self.i
    #Function plays the next song, when current is over(don't delete it)
    def isNext(self, now, total):
        if total - now <= 1:
            self.next()
    #Function for progress bar
    def progress(self, now, total):
        perc = int((now/total)*100)
        self.ui.progressBar.setValue(perc)
    #Function to change volume
    def volume(self):
        volume_value = self.ui.volumeSlider.value()/100
        pygame.mixer.music.set_volume(volume_value)
        if volume_value == 0:
            self.pic.addPixmap(QtGui.QPixmap("src/soundoff.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            self.ui.volumeButton.setIcon(self.pic)
        else:
            self.pic.addPixmap(QtGui.QPixmap("src/sound.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            self.ui.volumeButton.setIcon(self.pic)
    def volumeOff(self):
        self.checkVolume = not self.checkVolume
        if self.checkVolume:
            self.ui.volumeSlider.setValue(self.prevVolume*100)
            pygame.mixer.music.set_volume(self.prevVolume)
            self.pic.addPixmap(QtGui.QPixmap("src/sound.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            self.ui.volumeButton.setIcon(self.pic)
        elif not self.checkVolume:
            self.prevVolume = self.ui.volumeSlider.value()/100
            self.ui.volumeSlider.setValue(0)
            pygame.mixer.music.set_volume(0)
            self.pic.addPixmap(QtGui.QPixmap("src/soundoff.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            self.ui.volumeButton.setIcon(self.pic)
            return self.prevVolume
    def moveButton(self):
        self.checkSettings = not self.checkSettings
        if self.checkSettings:
            self.ui.addSongButton.show()
            self.settingsTimer1 = QtCore.QTimer()
            self.settingsTimer1.setInterval(30)
            self.settingsTimer1.timeout.connect(self.moveUp)
            self.settingsTimer1.start()
        elif not self.checkSettings:
            self.settingsTimer2 = QtCore.QTimer()
            self.settingsTimer2.setInterval(30)
            self.settingsTimer2.timeout.connect(self.moveDown)
            self.settingsTimer2.start()
    def openFolder(self):
        if sys.platform == "win32":
            os.startfile(filename)
        else:
            opener ="open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, 'music'])
    def moveUp(self):
        if self.igrek > 490:
            self.igrek -= 5
            self.ui.addSongButton.move(720, self.igrek)
            return self.igrek
        elif self.igrek <= 490:
            self.settingsTimer1.stop()
    def moveDown(self):
        if self.igrek < 535:
            self.igrek += 5
            self.ui.addSongButton.move(720, self.igrek)
        elif self.igrek >= 535:
            self.ui.addSongButton.hide()
            self.settingsTimer2.stop()
    def addToPlaylist(self):
        playlist = os.listdir('music')
        playlist = minusCash(playlist)
        return playlist


def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('src/icon.png'))
    window = ExampleApp()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()