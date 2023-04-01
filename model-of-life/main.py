import sys
import random

from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel, QGraphicsDropShadowEffect, QPushButton
from PyQt6.QtCore import QPropertyAnimation
from PyQt6 import QtCore, QtGui, QtWidgets

import design
import name_dict

window_width = 1600
window_height = 900
label_width = 950

# Class Field - main class, that shows and simulates everything
class Field(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.ui = design.Ui_MainWindow()
        self.setFixedSize(QtCore.QSize(window_width, window_height))
        self.ui.setupUi(self)
        self.frogs = [  Frog(self, random.randint(10, 20), 'Maxim', 'Male', 200, 100), 
                        Frog(self, random.randint(10, 20), 'Liza', 'Female', 170, 100)]
        self.house = Home(self)
        self.chest = Chest(self)
        self.chest.inventory.apples_in_inventory = 3
        self.trees = [AppleTree(self)]
        self.wood = [WoodTree(self)]
        self.chestMenu = ChestInfo(self, self.chest.inventory.apples_in_inventory, 
        self.chest.inventory.wood_in_inventory)
        self.mainMenu = Information(self)
        self.menu_button = QtWidgets.QPushButton(self)
        self.menu_button.setIcon(QtGui.QIcon('model-of-life/src/menu_button.png'))
        self.menu_button.setIconSize(QtCore.QSize(84, 84))
        self.menu_button.setGeometry(1460, 760, 84, 84)
        self.menu_button.setStyleSheet("background-color: none;\nborder: none;")
        self.mainMenu.hide()
        for frog in self.frogs:
            self.mainMenu.verticalLayout.addWidget(FrogInfo(self.mainMenu, frog.name))
        self.chestMenu.hide()
        self.timer = QtCore.QTimer()
        self.ui.button.hide()
        self.chest.clicked.connect(lambda: self.chestMenu.show())
        self.menu_button.clicked.connect(lambda: self.mainMenu.show())
        self.timer.timeout.connect(self.step)
        self.timer.setInterval(10000)
        self.timer.start()

# Creates new frog, when its allowed. New frog has its own sex, name etc    
    def born_frog(self):
        sex = random.choice(['Male', 'Female'])
        names = name_dict.name_dict.get(sex)
        name = names.pop(random.randint(0, len(names)-1))
        self.frogs.append(  Frog(self, random.randint(10, 20), 
                            name, sex, 200, 100))
        self.mainMenu.verticalLayout.addWidget(FrogInfo(self.mainMenu, name))
        if self.mainMenu.verticalLayout.count() > 5:
            self.mainMenu.w.setFixedHeight(self.mainMenu.w.height()+90)
        self.frogs[len(self.frogs)-1].show()


# Every action executes every new step
    def step(self):
        for i in range(0, len(self.frogs)):
            self.make_decision(i)
        self.grow_new()
        QtCore.QTimer().singleShot(6000, lambda: 
        self.chestMenu.wood_info.setText(str(int(self.chest.inventory.wood_in_inventory))))
        QtCore.QTimer().singleShot(6000, lambda: 
        self.chestMenu.apples_info.setText(str(self.chest.inventory.apples_in_inventory)))


# Function grows new apples on the apple tree and new wood tree every step with its own probability
    def grow_new(self):
        if random.randint(0, 100) < 30:
            self.trees[random.randint(0, len(self.trees)-1)].grow_apple()
        if random.randint(0, 100) < 40:
            self.wood[random.randint(0, len(self.wood)-1)].grow_tree()


# Every step every frog makes its own decision what to do:
# Eat apple to get stamina, get apple, cut the tree, upgrade a house,
# get a new frog, bring everything from inventory to chest or just walk around
    def make_decision(self, number):
        self.eat_apple_value = self.frogs[number].calculate_eat_apple_value()
        self.get_apple_value = self.calculate_get_apple_value()
        self.get_wood_value = self.calculate_get_wood_value()
        self.upgrade_house_value = self.calculate_upgrade_house_value()
        self.reproduction_value = self.calculate_reproduction_value()
        self.take_to_chest_value = self.calculate_take_to_chest_value(number)
        self.just_move_value = 5
        self.list_of_value = {  self.eat_apple: self.eat_apple_value,
                                self.get_apple: self.get_apple_value,
                                self.get_wood: self.get_wood_value,
                                self.upgrade_house: self.upgrade_house_value,
                                self.reproduction: self.reproduction_value,
                                self.take_to_chest: self.take_to_chest_value,
                                self.just_move: self.just_move_value
                             }
        for k, v in self.list_of_value.items():
            if v == max(self.list_of_value.values()):
                k(number)
        # print(self.frogs[number].name, end=': ')
        # print(self.list_of_value.values())


# After making a decisions this functions do the decision
    def eat_apple(self, number):
        if self.frogs[number].inventory.apples_in_inventory > 0:
            self.frogs[number].inventory.apples_in_inventory -= 1
            self.frogs[number].energy += 50
        else:
            if self.chest.inventory.apples_in_inventory > 0:
                self.chest.inventory.apples_in_inventory -= 1
                self.frogs[number].energy += 50
            else:
                self.get_apple(number)
    def get_apple(self, number):
        tree_number = random.randint(0, len(self.trees)-1)
        self.frogs[number].move_frog(QtCore.QPoint(random.randint(150, 158),
                                                    random.randint(156, 164)))
        if self.trees[tree_number].inventory.apples_in_inventory > 0 and self.frogs[number].energy >= 20:
            self.frogs[number].energy -= 10
            self.trees[tree_number].pluck_apple()
            self.frogs[number].inventory.apples_in_inventory += 1
        else:
            print('No more apples')
    def get_wood(self, number):
        tree_number = random.randint(0, len(self.wood)-1)
        self.frogs[number].move_frog(QtCore.QPoint(random.randint(175, 185),
                                                   random.randint(745, 755)))
        if self.wood[tree_number].inventory.wood_in_inventory > 0 and self.frogs[number].energy >= 40:
            self.frogs[number].energy -= 30
            self.frogs[number].inventory.wood_in_inventory += 150
            self.wood[tree_number].cut_tree()
        else:
            print('No more wood!')
    def upgrade_house(self, number):
        center = QtCore.QPoint(int(self.house.x()+(self.house.width()/2)), 
                               int(self.house.y()+self.house.height()+5))
        self.frogs[number].move_frog(center)
        print(self.frogs[number].energy)
        if self.chest.inventory.wood_in_inventory > self.house.required_wood and \
           self.frogs[number].energy >= 60:
            self.frogs[number].energy -= 50
            self.chest.inventory.wood_in_inventory -= self.house.required_wood
            self.house.upgrade_house()
        elif self.frogs[number].energy < 60:
            self.eat_apple(number)
        return self.chest.inventory.wood_in_inventory
    def reproduction(self, number):
        home = QtCore.QPoint(self.house.x()+self.house.width()/2,
                             self.house.y()+self.house.height()/2)
        self.frogs[number].move_frog(home)
        print(self.frogs[number].energy)
        if self.frogs[number].energy >= 30 and len(self.frogs) < self.house.max_capacity:
            self.frogs[number].energy -= 20
            self.born_frog()
        elif self.frogs[number].energy < 30:
            self.eat_apple(number)
    def just_move(self, number):
        self.frogs[number].move_frog(QtCore.QPoint(random.randint(15, 1520), 
                                                   random.randint(15, 785)))
    def take_to_chest(self, number):
        self.frogs[number].move_frog(QtCore.QPoint(random.randint(1150, 1154),
                                                   random.randint(218, 222)))
        self.chest.inventory.wood_in_inventory += self.frogs[number].inventory.wood_in_inventory
        if self.frogs[number].inventory.apples_in_inventory > 2:
            diff = self.frogs[number].inventory.apples_in_inventory - 2
            self.frogs[number].inventory.apples_in_inventory = 2
            self.chest.inventory.apples_in_inventory += diff
        self.frogs[number].inventory.wood_in_inventory = 0


# This functions calculate the value of every decision. Frog do that one, that is the most valuable 

# Value of bringing everything to the chest depends on amount of staff in frog's inventory
    def calculate_take_to_chest_value(self, number):
        if self.frogs[number].inventory.apples_in_inventory > 2:
            return 50
        elif self.frogs[number].inventory.wood_in_inventory > 0:
            return 50
        elif self.frogs[number].inventory.wood_in_inventory == 0 or \
            self.frogs[number].inventory.apples_in_inventory <= 2:
            return 0

# Value of reproduction depends on percent of occupancy of vacant places in the house
    def calculate_reproduction_value(self):
        perc = ((len(self.frogs)/self.house.max_capacity)*100)
        if perc == 100:
            return 0
        elif perc <= 60:
            return 90
        elif perc > 60:
            return int((-29/9000)*perc**3+(49/72)*perc**2-(2879/60)*perc+1215)

# Value of upgrading house depends on amount of frogs in the house.
# And returns 0 if frog has not enough wood in the chest
    def calculate_upgrade_house_value(self):
        if self.chest.inventory.wood_in_inventory < self.house.required_wood:
            return 0
        else:
            if 0 <= self.house.max_capacity - len(self.frogs) < 3:
                return ((-10*(self.house.max_capacity - len(self.frogs)))+70)
            else:
                return 0

# Value of cutting wood depends on amount of wood in the chest and amount of wood, 
# needed to upgrade the house. If tree is already cutted, it returns 0
    def calculate_get_wood_value(self):
        all_wood = 0
        for i in range(0, len(self.wood)):
            all_wood += self.wood[i].inventory.wood_in_inventory
        if all_wood == 0:
            return 0
        else:
            x = (self.chest.inventory.wood_in_inventory/self.house.required_wood)*100
            return int((1/2)*(-x)+75)

# Value of picking an apple depends on amount of apples on many things, like:
# House occupancy rate, current and maximum energy of all frogs, and ratio of apples in chest to frogs
    def calculate_get_apple_value(self):
        energy = 0
        max_energy = 0
        all_apples = 0
        for i in range(len(self.frogs)):
            energy += self.frogs[i].energy
            max_energy += self.frogs[i].max_energy
        for i in range(0, len(self.trees)):
            all_apples += self.trees[i].inventory.apples_in_inventory
        if all_apples == 0:
            return 0
        elif self.chest.inventory.apples_in_inventory < len(self.frogs):
            return 100
        else:
            return 0.5*self.number()+self.max_number()+int(self.hunger(energy, max_energy))+int(self.storage())

    def number(self):
        x = int((len(self.frogs)/self.house.max_capacity)*100)
        if x < 25:
            return 100
        elif x < 50:
            return (1/1680)*(x-25)**3 + (-2/35)*(x-25)**2 + (-317/336)*(x-25)+100
        elif x <= 100:
            return -0.8*(x-100)+10
        else:
            return 10

    def max_number(self):
        return (self.house.tier*2)+1

    def hunger(self, energy, max_energy):
        x = ((energy/max_energy)-0.45)*100
        return (-3/8)*(x-65)

    def storage(self):
        x = int((self.chest.inventory.apples_in_inventory/len(self.frogs))*100)
        if x < 25:
            return ((-2/375)*x**3 + (2/25)*x**2 + (-2/3)*x + 100) * 0.2
        elif x < 100:
            return (-1/5)*x
        elif x >= 100:
            return 5


# Class Frog, that has main frog characteristics and functions
class Frog(QLabel):
    def __init__(self, parent, health: int, name: str, sex: str, speed: int, energy):
        super().__init__(parent)
        self.health = health
        self.name = name
        self.speed = speed
        self.sex = sex
        self.max_energy = energy
        self.energy = self.max_energy
        self.age = 0
        self.setGeometry(QtCore.QRect( random.randint(15, 1520), 
                                            random.randint(15, 785), 
                                            64, 64))
        self.setText('')
        self.setPixmap(QtGui.QPixmap('model-of-life/src/front.png'))
        self.setScaledContents(True)
        self.inventory = Inventory()
        self.animation = QPropertyAnimation(self)
        self.animation.setTargetObject(self)
        self.animation.setPropertyName(b'pos')


# Function moves frog's to certain point. According to the angle, frog changes its icon
    def move_frog(self, end_pos: QtCore.QPoint):
        start_pos = self.pos()
        vector = QtCore.QLineF(QtCore.QLine(start_pos, end_pos))
        angle = vector.angle()
        if (0 < angle < 45) or (315 < angle):
            self.setPixmap(QtGui.QPixmap('model-of-life/src/right.png'))
        elif 45 <= angle <= 135:
            self.setPixmap(QtGui.QPixmap('model-of-life/src/back.png'))
        elif 135 < angle < 225:
            self.setPixmap(QtGui.QPixmap('model-of-life/src/left.png'))
        elif 225 <= angle <= 315:
            self.setPixmap(QtGui.QPixmap('model-of-life/src/front.png'))
        self.animation.setEndValue(end_pos)
        self.animation.setDuration(int(vector.length()/self.speed)*1000)
        self.animation.start()
        self.animation.finished.connect(lambda: self.setPixmap(QtGui.QPixmap('model-of-life/src/front.png')))
        self.energy -= int(vector.length()/100)


# Value of eating an apple depends on current and maximum energy of the frog
    def calculate_eat_apple_value(self):
        if self.energy <= 0.05 * self.max_energy:
            return 100
        elif self.energy > 0.5 * self.max_energy:
            return 0
        else:
            return int(1/75 * (self.energy-(0.05*self.max_energy)) ** 2 + 
                    (-8/3) * (self.energy-(0.05*self.max_energy)) + 100)


# Class AppleTree, that has main Apple Tree's characteristics and functions
class AppleTree(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.setGeometry(QtCore.QRect(10, 15, 256, 256))
        self.setText('')
        self.setPixmap(QtGui.QPixmap('model-of-life/src/tree-7.png'))
        self.setScaledContents(True)
        self.inventory = Inventory()
        self.inventory.apples_in_inventory = 7


# If apple was plucked, tree will change icon
    def pluck_apple(self):
        if self.inventory.apples_in_inventory > 0:
            self.inventory.apples_in_inventory -= 1
            QtCore.QTimer().singleShot(8000, 
            lambda: self.setPixmap(QtGui.QPixmap('model-of-life/src/tree-'+f'{self.inventory.apples_in_inventory}'+'.png')))
        return self.inventory.apples_in_inventory

# Apple grows if function grow_new() allows
    def grow_apple(self):
        if self.inventory.apples_in_inventory < 7:
            self.inventory.apples_in_inventory += 1
            self.setPixmap(QtGui.QPixmap('model-of-life/src/tree-'+f'{self.inventory.apples_in_inventory}'+'.png'))
            return self.inventory.apples_in_inventory


# Class WoodTree, that has main Wood Tree's characteristics and functions
class WoodTree(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.setGeometry(QtCore.QRect(30, 600, 170, 170))
        self.setText('')
        self.setPixmap(QtGui.QPixmap('model-of-life/src/wood-tree.png'))
        self.setScaledContents(True)
        self.inventory = Inventory()
        self.inventory.wood_in_inventory = 150
    
    
# If tree was cutted, tree will change the icon
    def cut_tree(self):
        if self.inventory.wood_in_inventory > 0:
            self.inventory.wood_in_inventory -= 150
            QtCore.QTimer().singleShot(8000, 
            lambda: self.setPixmap(QtGui.QPixmap('model-of-life/src/cutted-tree.png')))
            return self.inventory.wood_in_inventory


# Tree grows if function grow_new() allows
    def grow_tree(self):
        if self.inventory.wood_in_inventory == 0:
            self.inventory.wood_in_inventory += 150
            self.setPixmap(QtGui.QPixmap('model-of-life/src/wood-tree.png'))
            return self.inventory.wood_in_inventory


# Class Inventory. Every frog and chest have it
class Inventory():
    def __init__(self):
        self.apples_in_inventory = 0
        self.wood_in_inventory = 0


# Class Chest, that has main Chest's characteristics and functions
class Chest(QPushButton):
    def __init__(self, parent):
        super().__init__(parent)
        self.setGeometry(QtCore.QRect(1100, 150, 104, 80))
        self.setText('')
        self.setIcon(QtGui.QIcon('model-of-life/src/chest.png'))
        self.setStyleSheet("background-color: rgba(255, 255, 255, 0);\nborder: none;")
        self.setIconSize(QtCore.QSize(104, 80))
        self.inventory = Inventory()


# Class Home, that has main Home's characteristics and functions
class Home(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.setGeometry(QtCore.QRect(1300, 150, 175, 175))
        self.setText('')
        self.max_capacity = 2
        self.required_wood = 500
        self.tier = 1
        self.models = [ 'model-of-life/src/house-first-tier.png', 'model-of-life/src/house-second-tier.png',
                        'model-of-life/src/house-third-tier.png', 'model-of-life/src/house-fourth-tier.png',
                        'model-of-life/src/house-fifth-tier.png', 'model-of-life/src/house-sixth-tier.png',
                        'model-of-life/src/house-seventh-tier.png']
        self.setPixmap(QtGui.QPixmap(self.models.pop(0)))
        self.setScaledContents(True)


# When frog upgrades the house, it change his icon and has a bigger capacity
    def upgrade_house(self):
        if len(self.models) > 0:
            self.max_capacity = int((self.max_capacity * 1.5)+0.5)
            self.tier += 1
            self.required_wood = (-25*self.tier**5+(4625/6)*self.tier**4-8250*self.tier**3+
                                  (241375/6)*self.tier**2-88225*self.tier+70500)
            self.setGeometry(self.x()-7, self.y()-7, self.width()+14, self.height()+14)
            QtCore.QTimer().singleShot(8000, 
            lambda: self.setPixmap(QtGui.QPixmap(self.models.pop(0))))


# After clicking on the Chest, opens a window and shows Chest's Inventory
class ChestInfo(QLabel):
    def __init__(self, parent, apples, wood):
        super().__init__(parent)
        self.setGeometry(400, 225, 800, 450)
        self.setPixmap(QtGui.QPixmap('model-of-life/src/ChestInfo.png'))
        self.setScaledContents(True)
        self.hide()
        self.apples_info = QLabel(text=str(apples), parent=self)
        self.wood_info = QLabel(text=str(wood), parent=self)
        self.close_button = QPushButton(self)
        self.close_button.setIcon(QtGui.QIcon('model-of-life/src/close.png'))
        self.close_button.setIconSize(QtCore.QSize(32, 32))
        self.close_button.setGeometry(55, 55, 32, 32)
        self.close_button.setStyleSheet("background-color: rgba(255, 255, 255, 0);\nborder: none;")
        font = QtGui.QFont()
        font.setPixelSize(40)
        self.apples_info.setGeometry(500, 190, 300, 50)
        self.wood_info.setGeometry(500, 300, 300, 50)
        self.apples_info.setFont(font)
        self.wood_info.setFont(font)
        border = QGraphicsDropShadowEffect(self,
            blurRadius=9.0,                   
            color=QtGui.QColor("#000000"),
            offset=QtCore.QPointF(0.0, 0.0)  
        )
        border2 = QGraphicsDropShadowEffect(self,
            blurRadius=9.0,                   
            color=QtGui.QColor("#000000"),
            offset=QtCore.QPointF(0.0, 0.0)  
        )
        self.apples_info.setGraphicsEffect(border)
        self.wood_info.setGraphicsEffect(border2)
        self.close_button.clicked.connect(lambda: self.hide())


# After clicking on Menu button, opens a window with information about the frogs
class Information(QLabel):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setPixmap(QtGui.QPixmap('model-of-life/src/information.png'))
        self.setGeometry(200, 112, 1200, 675)
        self.setScaledContents(True)
        self.close_button = QPushButton(self)
        self.close_button.setIcon(QtGui.QIcon('model-of-life/src/close.png'))
        self.close_button.setIconSize(QtCore.QSize(32, 32))
        self.close_button.setGeometry(45, 45, 32, 32)
        self.close_button.setStyleSheet("background-color: rgba(255, 255, 255, 0);\nborder: none;")
        self.scrollArea = QtWidgets.QScrollArea(self)
        self.scrollArea.setGeometry(QtCore.QRect(100, 75, 995, 500))
        self.scrollArea.setStyleSheet("background-color: rgba(0, 0, 0, 0);\nborder: none;")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollArea.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, 
        QtWidgets.QSizePolicy.Policy.Fixed)
        self.scrollArea.setStyleSheet("""
                    QWidget {
                        background-color: rgba(0, 0, 0, 0);
                        border: none;}
                    QScrollBar:vertical {
                        background-color: rgba(0, 0, 0, 0);
                        border: none;}
                    QScrollBar::handle:vertical {
                        background-color: qlineargradient(spread:pad, 
                        x1:0.463054, y1:0.0965909, x2:0.487685, y2:0.813, 
                        stop:0 rgba(0, 158, 61, 255), 
                        stop:1 rgba(0, 188, 84, 255));
                        border-radius: 7px;
                        min-height: 10px;
                      }
                    QScrollBar::add-line:vertical {
                        background: none;
                        height: 10px;
                        subcontrol-position: bottom+5px;
                        subcontrol-origin: margin;
                      }

                    QScrollBar::sub-line:vertical {
                        background: none;
                        height: 10px;
                        subcontrol-position: top-5px;
                        subcontrol-origin: margin;
                      }
                    QScrollBar::up-arrow:vertical { 
                        height: 0px; 
                        width: 0px 
                      }
                    QScrollBar::down-arrow:vertical {
                        height: 0px; 
                        width: 0px
                      }  
                    """)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.label = QtWidgets.QLabel(self)
        self.label.setFixedSize(950, 120)
        self.label.setMinimumHeight(120)
        self.label.setText('Information')
        font = QtGui.QFont()
        font.setPixelSize(95)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout.addWidget(self.label, alignment=QtCore.Qt.AlignmentFlag.AlignTop)
        self.w = QtWidgets.QWidget()
        self.w.setLayout(self.verticalLayout)
        self.scrollArea.setWidget(self.w)
        self.close_button.clicked.connect(lambda: self.hide())


# Short info about every frog
class FrogInfo(QtWidgets.QWidget):
    def __init__(self, parent, name: str) -> None:
        super().__init__(parent)
        icon = QLabel(self)
        icon.setPixmap(QtGui.QPixmap('model-of-life/src/front.png'))
        icon.setScaledContents(True)
        icon.setGeometry(5, 5, 64, 64)
        icon.setMinimumHeight(64)
        info = QLabel(self)
        font = QtGui.QFont()
        font.setPixelSize(40)
        info.setGeometry(80, 5, label_width, 64)
        info.setMinimumHeight(64)
        info.setFont(font)
        info.setText('   '+name)
        

def main():
    app = QApplication(sys.argv)
    window = Field()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()