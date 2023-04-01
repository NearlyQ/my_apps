from PyQt6 import QtCore, QtGui, QtWidgets

progress_bar_style = """
QSlider::groove:horizontal {
background: rgba(0, 0, 0, 0);
height: 10px;
border-radius: 5px;
}

QSlider::sub-page:horizontal {
background: qlineargradient(spread:pad, x1:0.463054, y1:0.0965909, x2:0.487685, y2:0.813, stop:0 rgba(40, 113, 250, 150), stop:1 rgba(103, 23, 205, 150));
height: 10px;
border-radius: 5px;
}

QSlider::add-page:horizontal {
background: qlineargradient(spread:pad, x1:0.463054, y1:0.0965909, x2:0.487685, y2:0.813, stop:0 rgba(56, 56, 56, 150), stop:1 rgba(40, 40, 40, 150));
height: 10px;
}

QSlider::sub-page:horizontal:disabled {
background: rgba(0, 0, 0, 0);
border-color: #999;
border-radius: 5px;
}

QSlider::add-page:horizontal:disabled {
background: rgba(0, 0, 0, 0);
border-color: #999;
border-radius: 5px;
}

QSlider::handle:horizontal:disabled {
background: rgba(0, 0, 0, 0);
border: 1px solid #aaa;
border-radius: 5px;
}
"""
controlled_progress_bar_style = """
QSlider::groove:horizontal {
background: rgba(0, 0, 0, 0);
height: 10px;
border-radius: 5px;
}

QSlider::sub-page:horizontal {
background: qlineargradient(spread:pad, x1:0.463054, y1:0.0965909, x2:0.487685, y2:0.813, stop:0 rgba(210, 90, 70, 0), stop:1 rgba(5, 240, 25, 0));
height: 10px;
border-radius: 5px;
}

QSlider::add-page:horizontal {
background: qlineargradient(spread:pad, x1:0.463054, y1:0.0965909, x2:0.487685, y2:0.813, stop:0 rgba(56, 56, 56, 0), stop:1 rgba(40, 40, 40, 0));
height: 10px;
}

QSlider::sub-page:horizontal:disabled {
background: rgba(0, 0, 0, 0);
border-color: #999;
border-radius: 5px;
}

QSlider::add-page:horizontal:disabled {
background: rgba(0, 0, 0, 0);
border-color: #999;
border-radius: 5px;
}

QSlider::handle:horizontal:disabled {
background: rgba(0, 0, 0, 0);
border: 1px solid #aaa;
border-radius: 5px;
}
"""
volume_slider_style = """
QSlider::groove:horizontal {
background: rgba(0, 0, 0, 0);
height: 10px;
border-radius: 5px;
}

QSlider::sub-page:horizontal {
background: qlineargradient(spread:pad, x1:0.463054, y1:0.0965909, x2:0.487685, y2:0.813, stop:0 rgba(40, 113, 250, 150), stop:1 rgba(103, 23, 205, 150));
height: 10px;
border-radius: 5px;
}

QSlider::add-page:horizontal {
background: qlineargradient(spread:pad, x1:0.463054, y1:0.0965909, x2:0.487685, y2:0.813, stop:0 rgba(56, 56, 56, 150), stop:1 rgba(40, 40, 40, 150));
height: 10px;
}

QSlider::handle:horizontal {
background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
    stop:0 #eee, stop:1 #ccc);
border: 1px solid #777;
width: 13px;
margin-top: -2px;
margin-bottom: -2px;
border-radius: 6px;
}
QSlider::handle:horizontal:hover {
background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
    stop:0 #fff, stop:1 #ddd);
border: 1px solid #444;
border-radius: 6px;
}
QSlider::sub-page:horizontal:disabled {
background: rgba(0, 0, 0, 0);
border-color: #999;
border-radius: 5px;
}

QSlider::add-page:horizontal:disabled {
background: rgba(0, 0, 0, 0);
border-color: #999;
border-radius: 5px;
}

QSlider::handle:horizontal:disabled {
background: rgba(0, 0, 0, 0);
border: 1px solid #aaa;
border-radius: 5px;
}"""
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.background = QtWidgets.QLabel(self.centralwidget)
        self.background.setGeometry(QtCore.QRect(0, 0, 801, 601))
        self.background.setText("")
        self.background.setPixmap(QtGui.QPixmap("music-player/src/BackGround-v5.png"))
        self.background.setScaledContents(True)
        self.cur_time = QtWidgets.QLabel(self.centralwidget)
        self.cur_time.setGeometry(QtCore.QRect(400, 180, 60, 20))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.cur_time.setFont(font)
        self.cur_time.setObjectName("cur_time")
        self.song_name = QtWidgets.QLabel(self.centralwidget)
        self.song_name.setGeometry(QtCore.QRect(400, 110, 380, 32))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.song_name.setFont(font)
        self.song_name.setObjectName("song_name")
        self.total_time = QtWidgets.QLabel(self.centralwidget)
        self.total_time.setGeometry(QtCore.QRect(710, 180, 60, 20))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.total_time.setFont(font)
        self.total_time.setObjectName("total_time")
        self.volume_slider = QtWidgets.QSlider(self.centralwidget)
        self.volume_slider.setGeometry(QtCore.QRect(320, 550, 160, 25))
        self.volume_slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.volume_slider.setValue(88)
        self.volume_slider.setStyleSheet(volume_slider_style)
        self.volume_slider.setObjectName("volume_slider")
        self.progress_slider = QtWidgets.QSlider(self.centralwidget)
        self.progress_slider.setGeometry(QtCore.QRect(453, 185, 250, 10))
        self.progress_slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.progress_slider.setStyleSheet(progress_bar_style)
        self.progress_slider.setRange(0, 99)
        self.progress_slider.setValue(0)
        self.progress_slider.setTracking(False)
        self.progress_slider_controlled = QtWidgets.QSlider(self.centralwidget)
        self.progress_slider_controlled.setGeometry(QtCore.QRect(453, 185, 250, 10))
        self.progress_slider_controlled.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.progress_slider_controlled.setStyleSheet(controlled_progress_bar_style)
        self.progress_slider.setRange(0, 99)
        self.progress_slider_controlled.setValue(0)
        self.volume_button = QtWidgets.QPushButton(self.centralwidget)
        self.volume_button.setGeometry(QtCore.QRect(270, 540, 42, 42))
        self.volume_button.setAutoFillBackground(False)
        self.volume_button.setText("")
        iconV = QtGui.QIcon()
        iconV.addPixmap(QtGui.QPixmap("music-player/src/sound.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.volume_button.setIcon(iconV)
        self.volume_button.setIconSize(QtCore.QSize(42, 42))
        self.volume_button.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n"
"border: none;")
        self.loop_button = QtWidgets.QPushButton(self.centralwidget)
        self.loop_button.setGeometry(QtCore.QRect(200, 540, 42, 42))
        self.loop_button.setAutoFillBackground(False)
        self.loop_button.setText("")
        iconR = QtGui.QIcon()
        iconR.addPixmap(QtGui.QPixmap("music-player/src/loop.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.loop_button.setIcon(iconR)
        self.loop_button.setIconSize(QtCore.QSize(42, 42))
        self.loop_button.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n"
"border: none;")
        self.pause_button = QtWidgets.QPushButton(self.centralwidget)
        self.pause_button.setGeometry(QtCore.QRect(20, 540, 42, 42))
        self.pause_button.setAutoFillBackground(False)
        self.pause_button.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("music-player/src/pause.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pause_button.setIcon(icon)
        self.pause_button.setIconSize(QtCore.QSize(32, 32))
        self.pause_button.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n"
"border: none;")
        self.pause_button.setObjectName("pause")
        self.hidenButton = QtWidgets.QPushButton(self.centralwidget)
        self.hidenButton.setGeometry(QtCore.QRect(20, 540, 42, 42))
        self.hidenButton.setAutoFillBackground(False)
        self.hidenButton.setText("")
        iconk = QtGui.QIcon()
        iconk.addPixmap(QtGui.QPixmap("music-player/src/pause.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.hidenButton.setIcon(iconk)
        self.hidenButton.setIconSize(QtCore.QSize(32, 32))
        self.hidenButton.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n"
"border: none;")
        self.hidenButton.hide()
        self.prev_button = QtWidgets.QPushButton(self.centralwidget)
        self.prev_button.setGeometry(QtCore.QRect(80, 540, 42, 42))
        self.prev_button.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n"
"border: none;")
        self.prev_button.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("music-player/src/prev.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.prev_button.setIcon(icon1)
        self.prev_button.setIconSize(QtCore.QSize(32, 32))
        self.prev_button.setCheckable(False)
        self.prev_button.setObjectName("prev")
        self.next_button = QtWidgets.QPushButton(self.centralwidget)
        self.next_button.setGeometry(QtCore.QRect(130, 540, 42, 42))
        self.next_button.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n"
"border: none;")
        self.next_button.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("music-player/src/next.png"), QtGui.QIcon.Mode.Active, QtGui.QIcon.State.Off)
        self.next_button.setIcon(icon2)
        self.next_button.setIconSize(QtCore.QSize(32, 32))
        self.next_button.setObjectName("next")
        self.settings_button = QtWidgets.QPushButton(self.centralwidget)
        self.settings_button.setGeometry(QtCore.QRect(718, 535, 45, 45))
        self.settings_button.setAutoFillBackground(False)
        self.settings_button.setText("")
        self.icon3 = QtGui.QIcon()
        self.icon3.addPixmap(QtGui.QPixmap("music-player/src/settings.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.settings_button.setIcon(self.icon3)
        self.settings_button.setIconSize(QtCore.QSize(42, 42))
        self.settings_button.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n"
"border: none;")
        self.add_song_button = QtWidgets.QPushButton(self.centralwidget)
        self.add_song_button.setGeometry(QtCore.QRect(720, 535, 42, 42))
        self.add_song_button.setAutoFillBackground(False)
        self.add_song_button.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("music-player/src/folder.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.add_song_button.setIcon(icon4)
        self.add_song_button.setIconSize(QtCore.QSize(32, 32))
        self.add_song_button.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n"
"border: none;")
        self.add_song_button.hide()
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", ""))
        self.cur_time.setText(_translate("MainWindow", "00:00"))
        self.song_name.setText(_translate("MainWindow", "Add music to folder"))
        self.total_time.setText(_translate("MainWindow", "03:00"))


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setFixedSize(320, 240)
        self.warning_background = QtWidgets.QLabel(Dialog)
        self.warning_background.setGeometry(QtCore.QRect(0, 0, 321, 241))
        self.warning_background.setText("")
        self.warning_background.setScaledContents(True)
        self.warning_background.setObjectName("warning_background")
        self.warning_background.setPixmap(QtGui.QPixmap("music-player/src/WarningBackGround.png"))
        self.warning_background.setScaledContents(True)
        self.info_label = QtWidgets.QLabel(Dialog)
        self.info_label.setGeometry(QtCore.QRect(70, 50, 180, 90))
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(False)
        font.setWeight(50)
        self.info_label.setFont(font)
        self.info_label.setScaledContents(False)
        self.info_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.info_label.setWordWrap(True)
        self.info_label.setObjectName("label")
        self.okey_button = QtWidgets.QPushButton(Dialog)
        self.okey_button.setGeometry(QtCore.QRect(105, 160, 110, 32))
        self.okey_button.setObjectName("pushButton")
        

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", ""))
        self.info_label.setText(_translate("Dialog", "Добавьте музыку в папку"))
        self.okey_button.setText(_translate("Dialog", "Окей"))

    