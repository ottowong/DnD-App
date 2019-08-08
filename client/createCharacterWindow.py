import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtSql import *
from PyQt5.QtGui import *
import time
# import win32api, win32con, win32gui
import socket
import pickle

from calculateAbilities import calcAbility

class mainFormDlg(QDialog) :

    def raceChanged(self):
        # set minimum value to 8 temporarily so that values can be decreased if needed
        self.strEdit.setMinimum(8)
        self.intEdit.setMinimum(8)
        self.dexEdit.setMinimum(8)
        self.conEdit.setMinimum(8)
        self.wisEdit.setMinimum(8)
        self.chaEdit.setMinimum(8)

        # set minimum value to 17 temporarily so that values can be increased if needed
        self.strEdit.setMaximum(17)
        self.intEdit.setMaximum(17)
        self.dexEdit.setMaximum(17)
        self.conEdit.setMaximum(17)
        self.wisEdit.setMaximum(17)
        self.chaEdit.setMaximum(17)

        # subtract the previous racial modifiers from each box
        self.strEdit.setValue(self.strEdit.value() - self.raceStrMod)
        self.intEdit.setValue(self.intEdit.value() - self.raceIntMod)
        self.dexEdit.setValue(self.dexEdit.value() - self.raceDexMod)
        self.conEdit.setValue(self.conEdit.value() - self.raceConMod)
        self.wisEdit.setValue(self.wisEdit.value() - self.raceWisMod)
        self.chaEdit.setValue(self.chaEdit.value() - self.raceChaMod)

        # set variables to the new selected race
        index = self.raceEdit.currentIndex()
        print(self.raceList[index])
        self.raceStrMod = self.raceList[index][2]
        self.raceDexMod = self.raceList[index][3]
        self.raceConMod = self.raceList[index][4]
        self.raceIntMod = self.raceList[index][5]
        self.raceWisMod = self.raceList[index][6]
        self.raceChaMod = self.raceList[index][7]

        # add the new racial modifiers to each box
        self.strEdit.setValue(self.strEdit.value() + self.raceStrMod)
        self.intEdit.setValue(self.intEdit.value() + self.raceIntMod)
        self.dexEdit.setValue(self.dexEdit.value() + self.raceDexMod)
        self.conEdit.setValue(self.conEdit.value() + self.raceConMod)
        self.wisEdit.setValue(self.wisEdit.value() + self.raceWisMod)
        self.chaEdit.setValue(self.chaEdit.value() + self.raceChaMod)

        # set the new minimum value to 8 + the racial modifier
        self.strEdit.setMinimum(8 + self.raceStrMod)
        self.intEdit.setMinimum(8 + self.raceIntMod)
        self.dexEdit.setMinimum(8 + self.raceDexMod)
        self.conEdit.setMinimum(8 + self.raceConMod)
        self.wisEdit.setMinimum(8 + self.raceWisMod)
        self.chaEdit.setMinimum(8 + self.raceChaMod)

        # set the new maximum value to 15 + the racial modifier
        self.strEdit.setMaximum(15 + self.raceStrMod)
        self.intEdit.setMaximum(15 + self.raceIntMod)
        self.dexEdit.setMaximum(15 + self.raceDexMod)
        self.conEdit.setMaximum(15 + self.raceConMod)
        self.wisEdit.setMaximum(15 + self.raceWisMod)
        self.chaEdit.setMaximum(15 + self.raceChaMod)

        self.valChanged()


    def ok(self):
        print("ok")

    def finishClicked(self):
        print("create character")

        nameVar = (self.nameEdit.text())
        strVar = (self.strEdit.value())
        intVar = (self.intEdit.value())
        dexVar = (self.dexEdit.value())
        conVar = (self.conEdit.value())
        wisVar = (self.wisEdit.value())
        chaVar = (self.chaEdit.value())
        hpVar = (self.hpEdit.value())

        index = self.raceEdit.currentIndex()
        characterRace = self.raceList[index][0]

        characterClass = self.classList[self.classEdit.currentIndex()][0]

        data=[3,self.parent().username,self.parent().password,nameVar,strVar,intVar,dexVar,conVar,wisVar,chaVar,hpVar,self.parent().userId,characterRace,self.characterGame,characterClass]

        try:
            self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Establish connection to TCP server and exchange data
            self.tcp_client.connect((self.parent().host_ip, self.parent().server_port))
            self.tcp_client.sendall(pickle.dumps(data))

            # Read data from the TCP server
            received = pickle.loads(self.tcp_client.recv(1024))
            print("received",received)

        except Exception as e:
            print("ERROR: ",e)
        finally:
            # Close the connection
            self.tcp_client.close()
            # Close the window
            # self.parent().updateCharacters()
            self.parent().updateCharacters()
            self.close()

    def calculateScoreCost(self, num, mod):
        if(num == 14 + mod):
            num = num - 7
        elif(num == 15 + mod):
            num = num - 6
        else:
            num = num - 8
        return num - mod

    def valChanged(self):
        if(self.initialised):
            self.counter = 27
            self.counter -= self.calculateScoreCost(self.strEdit.value(), self.raceStrMod)
            self.counter -= self.calculateScoreCost(self.intEdit.value(), self.raceIntMod)
            self.counter -= self.calculateScoreCost(self.dexEdit.value(), self.raceDexMod)
            self.counter -= self.calculateScoreCost(self.conEdit.value(), self.raceConMod)
            self.counter -= self.calculateScoreCost(self.wisEdit.value(), self.raceWisMod)
            self.counter -= self.calculateScoreCost(self.chaEdit.value(), self.raceChaMod)

            self.counterLabel.setText("You have "+str(self.counter)+" points left to spend.")

            print(self.classList[self.classEdit.currentIndex()])
            print(self.classList[self.classEdit.currentIndex()][2])
            print(calcAbility(self.conEdit.value()))
            hp = self.classList[self.classEdit.currentIndex()][2] + calcAbility(self.conEdit.value())
            self.hpEdit.setValue(hp)



    def centerOnScreen(self):
        resolution = QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
        (resolution.height() / 2) - (self.frameSize().height() / 2))

    def __init__(self, parent= None) :
        super(mainFormDlg, self).__init__(parent)
        timer = time.perf_counter()
        self.setGeometry(0, 0, 300, 100)
        # splashImg = QPixmap('splash.png')
        # self.splash = QSplashScreen(splashImg)
        # self.splash.show()
        self.setWindowIcon(QIcon('images/icon.png'))
        self.setWindowTitle('Create Character')
        self.centerOnScreen()
        self.initialised = 0
        self.raceStrMod = 0
        self.raceDexMod = 0
        self.raceConMod = 0
        self.raceIntMod = 0
        self.raceWisMod = 0
        self.raceChaMod = 0

        self.characterGame = self.parent().gameList[self.parent().gamesListBox.indexFromItem(self.parent().gamesListBox.selectedItems()[0]).row()][0]

        self.counterLabel = QLabel("You have 27 points left to spend.")

        self.nameEdit = QLineEdit()
        self.raceEdit = QComboBox()
        self.classEdit = QComboBox()
        self.classEdit.currentIndexChanged.connect(self.valChanged)
        # self.raceEdit.connect(self.raceChanged)
        self.raceEdit.currentIndexChanged.connect(self.raceChanged)
        self.strEdit = QSpinBox()
        self.intEdit = QSpinBox()
        self.dexEdit = QSpinBox()
        self.conEdit = QSpinBox()
        self.wisEdit = QSpinBox()
        self.chaEdit = QSpinBox()
        self.hpEdit = QSpinBox()
        self.hpEdit.setReadOnly(True)

        self.strEdit.setValue(8)
        self.intEdit.setValue(8)
        self.dexEdit.setValue(8)
        self.conEdit.setValue(8)
        self.wisEdit.setValue(8)
        self.chaEdit.setValue(8)

        self.strEdit.setRange(8,15)
        self.intEdit.setRange(8,15)
        self.dexEdit.setRange(8,15)
        self.conEdit.setRange(8,15)
        self.wisEdit.setRange(8,15)
        self.chaEdit.setRange(8,15)

        self.strEdit.valueChanged.connect(self.valChanged)
        self.intEdit.valueChanged.connect(self.valChanged)
        self.dexEdit.valueChanged.connect(self.valChanged)
        self.conEdit.valueChanged.connect(self.valChanged)
        self.wisEdit.valueChanged.connect(self.valChanged)
        self.chaEdit.valueChanged.connect(self.valChanged)

        try:
            self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            data=[19,self.parent().username,self.parent().password]
            # Establish connection to TCP server and exchange data
            self.tcp_client.connect((self.parent().host_ip, self.parent().server_port))
            self.tcp_client.sendall(pickle.dumps(data))

            # Read data from the TCP server
            received = pickle.loads(self.tcp_client.recv(1024))
            self.raceList = []
            print("received",received)
            for race in received:
                self.raceList.append(race)
                self.raceEdit.addItem(race[1])
            print(self.raceList)
            # self.raceChanged()

        except Exception as e:
            print("ERROR: ",e)
        finally:
            # Close the connection
            self.tcp_client.close()

        try:
            self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            data=[21,self.parent().username,self.parent().password]
            # Establish connection to TCP server and exchange data
            self.tcp_client.connect((self.parent().host_ip, self.parent().server_port))
            self.tcp_client.sendall(pickle.dumps(data))

            # Read data from the TCP server
            received = pickle.loads(self.tcp_client.recv(1024))
            self.classList = []
            print("received",received)
            for clas in received:
                self.classList.append(clas)
                self.classEdit.addItem(clas[1])
            print(self.classList)

        except Exception as e:
            print("ERROR: ",e)
        finally:
            # Close the connection
            self.tcp_client.close()

        self.submitButton = QPushButton("Create Character")

        self.submitButton.clicked.connect(self.finishClicked)
        # self.createAccountButton.clicked.connect(self.createAccountClicked)
        # self.forgotPasswordButton.clicked.connect(self.forgotPasswordClicked)

        # self.startClicker = QShortcut(QKeySequence("F6"),self)

        # self.startClicker.activated.connect(self.start)

        self.mainLayout = QFormLayout()

        self.mainLayout.addRow("Character Name", self.nameEdit)
        self.mainLayout.addRow("Race", self.raceEdit)
        self.mainLayout.addRow("Class", self.classEdit)
        self.mainLayout.addRow("STR",self.strEdit)
        self.mainLayout.addRow("INT",self.intEdit)
        self.mainLayout.addRow("DEX",self.dexEdit)
        self.mainLayout.addRow("CON",self.conEdit)
        self.mainLayout.addRow("WIS",self.wisEdit)
        self.mainLayout.addRow("CHA",self.chaEdit)
        self.mainLayout.addRow("HP",self.hpEdit)
        self.mainLayout.addWidget(self.counterLabel)
        self.mainLayout.addWidget(self.submitButton)

        self.initialised = 1
        self.valChanged()

        self.setLayout(self.mainLayout)

        # leave this at the end
        # self.splash.finish(self)
        print(time.clock() - timer, "seconds loading time")

if __name__ == "__main__":
    print("start program")
    app = QApplication([])
    mainWindow = mainFormDlg()
    mainWindow.show()
    sys.exit(app.exec_())
