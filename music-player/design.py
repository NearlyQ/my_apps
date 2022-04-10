from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.background = QtWidgets.QLabel(self.centralwidget)
        self.background.setGeometry(QtCore.QRect(0, 0, 801, 601))
        self.background.setText("")
        self.background.setPixmap(QtGui.QPixmap("src/BackGround-v5.png"))
        self.background.setScaledContents(True)
        self.curTime = QtWidgets.QLabel(self.centralwidget)
        self.curTime.setGeometry(QtCore.QRect(400, 180, 60, 20))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.curTime.setFont(font)
        self.curTime.setObjectName("curTime")
        self.songName = QtWidgets.QLabel(self.centralwidget)
        self.songName.setGeometry(QtCore.QRect(400, 110, 380, 32))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.songName.setFont(font)
        self.songName.setObjectName("songName")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(710, 180, 60, 20))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(453, 185, 250, 10))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setStyleSheet("QProgressBar{"
                                        "border-radius: 4px;"
                                        "background-color: qlineargradient(spread:pad, x1:0.463054, y1:0.0965909, x2:0.487685, y2:0.813, stop:0 rgba(56, 56, 56, 150), stop:1 rgba(40, 40, 40, 150));}"
                                        "QProgressBar::chunk{"
                                        "border-radius: 4px;"
                                        "background-color: qlineargradient(spread:pad, x1:0.463054, y1:0.0965909, x2:0.487685, y2:0.813, stop:0 rgba(40, 113, 250, 150), stop:1 rgba(103, 23, 205, 150));}")
        self.progressBar.setFormat('')
        self.progressBar.setObjectName("progressBar")
        self.volumeSlider = QtWidgets.QSlider(self.centralwidget)
        self.volumeSlider.setGeometry(QtCore.QRect(260, 553, 160, 25))
        self.volumeSlider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.volumeSlider.setValue(88)
        self.volumeSlider.setObjectName("volumeSlider")
        self.volumeButton = QtWidgets.QPushButton(self.centralwidget)
        self.volumeButton.setGeometry(QtCore.QRect(200, 540, 42, 42))
        self.volumeButton.setAutoFillBackground(False)
        self.volumeButton.setText("")
        iconV = QtGui.QIcon()
        iconV.addPixmap(QtGui.QPixmap("src/sound.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.volumeButton.setIcon(iconV)
        self.volumeButton.setIconSize(QtCore.QSize(42, 42))
        self.volumeButton.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n"
"border: none;")
        self.pauseButton = QtWidgets.QPushButton(self.centralwidget)
        self.pauseButton.setGeometry(QtCore.QRect(20, 540, 42, 42))
        self.pauseButton.setAutoFillBackground(False)
        self.pauseButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("src/pause.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pauseButton.setIcon(icon)
        self.pauseButton.setIconSize(QtCore.QSize(32, 32))
        self.pauseButton.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n"
"border: none;")
        self.pauseButton.setObjectName("pause")
        self.hidenButton = QtWidgets.QPushButton(self.centralwidget)
        self.hidenButton.setGeometry(QtCore.QRect(20, 540, 42, 42))
        self.hidenButton.setAutoFillBackground(False)
        self.hidenButton.setText("")
        iconk = QtGui.QIcon()
        iconk.addPixmap(QtGui.QPixmap("src/pause.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.hidenButton.setIcon(iconk)
        self.hidenButton.setIconSize(QtCore.QSize(32, 32))
        self.hidenButton.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n"
"border: none;")
        self.hidenButton.hide()
        self.prevButton = QtWidgets.QPushButton(self.centralwidget)
        self.prevButton.setGeometry(QtCore.QRect(80, 540, 42, 42))
        self.prevButton.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n"
"border: none;")
        self.prevButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("src/prev.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.prevButton.setIcon(icon1)
        self.prevButton.setIconSize(QtCore.QSize(32, 32))
        self.prevButton.setCheckable(False)
        self.prevButton.setObjectName("prev")
        self.nextButton = QtWidgets.QPushButton(self.centralwidget)
        self.nextButton.setGeometry(QtCore.QRect(130, 540, 42, 42))
        self.nextButton.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n"
"border: none;")
        self.nextButton.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("src/next.png"), QtGui.QIcon.Mode.Active, QtGui.QIcon.State.Off)
        self.nextButton.setIcon(icon2)
        self.nextButton.setIconSize(QtCore.QSize(32, 32))
        self.nextButton.setObjectName("next")
        self.settingsButton = QtWidgets.QPushButton(self.centralwidget)
        self.settingsButton.setGeometry(QtCore.QRect(718, 535, 45, 45))
        self.settingsButton.setAutoFillBackground(False)
        self.settingsButton.setText("")
        self.icon3 = QtGui.QIcon()
        self.icon3.addPixmap(QtGui.QPixmap("src/settings.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.settingsButton.setIcon(self.icon3)
        self.settingsButton.setIconSize(QtCore.QSize(42, 42))
        self.settingsButton.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n"
"border: none;")
        self.addSongButton = QtWidgets.QPushButton(self.centralwidget)
        self.addSongButton.setGeometry(QtCore.QRect(720, 535, 42, 42))
        self.addSongButton.setAutoFillBackground(False)
        self.addSongButton.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("src/folder.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.addSongButton.setIcon(icon4)
        self.addSongButton.setIconSize(QtCore.QSize(32, 32))
        self.addSongButton.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n"
"border: none;")
        self.addSongButton.hide()
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", ""))
        self.curTime.setText(_translate("MainWindow", "00:00"))
        self.songName.setText(_translate("MainWindow", "Add music to folder"))
        self.label_4.setText(_translate("MainWindow", "03:00"))