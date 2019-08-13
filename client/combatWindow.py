import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtSql import *
from PyQt5.QtGui import *
import time
# import win32api, win32con, win32gui
import socket
import pickle
import calculateAbilities

import bubbleSort


class mainFormDlg(QDialog) :

    def turnOrderClicked(self):
        try:
            data=[37,self.parent().username,self.parent().password,self.combatId]
            self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.tcp_client.connect((self.parent().host_ip, self.parent().server_port))
            self.tcp_client.sendall(pickle.dumps(data))

            received = pickle.loads(self.tcp_client.recv(1024))
            self.populateBoxes()
        except Exception as e:
            print(e)


    def addCharacterClicked(self):
        print("addCharacterClicked")

    def addMonsterClicked(self):
        print("addMonsterClicked")

    def loginClicked(self):

        try:
            data=[2,self.parent().username,self.parent().password]
            self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.tcp_client.connect((self.parent().host_ip, self.parent().server_port))
            self.tcp_client.sendall(pickle.dumps(data))

            received = pickle.loads(self.tcp_client.recv(1024))
            print(received)


        except Exception as e:
            print(e)
        finally:
            self.tcp_client.close()

    def populateBoxes(self):
        try:
            data=[36,self.parent().username,self.parent().password,self.combatId]
            self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.tcp_client.connect((self.parent().host_ip, self.parent().server_port))
            self.tcp_client.sendall(pickle.dumps(data))

            received = pickle.loads(self.tcp_client.recv(1024))
            print(received)

            self.allCharacters = received[0]
            self.allMonsters = received[1]

            self.turnOrder = []

            self.charNames = []
            for char in self.allCharacters:
                self.charNames.append(char[1])
                self.turnOrder.append(char)

            self.monsterNames = []
            for monster in self.allMonsters:
                self.monsterNames.append(monster[1])
                self.turnOrder.append(monster)

            self.characterBox.clear()
            self.monsterBox.clear()

            self.characterBox.addItems(self.charNames)
            self.monsterBox.addItems(self.monsterNames)

            self.turnOrder = bubbleSort.sort(self.turnOrder)
            self.turnOrderNames = []
            for i in range(0, len(self.turnOrder)):
                self.turnOrderNames.append(str(i+1)+". "+self.turnOrder[i][1]+" ("+str(self.turnOrder[i][2])+")")

            print(self.turnOrderNames)
            self.turnOrderBox.clear()
            self.turnOrderBox.addItems(self.turnOrderNames)


        except Exception as e:
            print(e)
        finally:
            self.tcp_client.close()

    def centerOnScreen(self):
        resolution = QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
        (resolution.height() / 2) - (self.frameSize().height() / 2))

    def __init__(self, parent= None) :
        super(mainFormDlg, self).__init__(parent)
        timer = time.perf_counter()
        self.setGeometry(0, 0, 700, 400)
        self.combatId = self.parent().currentClickedCombat
        self.setWindowIcon(QIcon('images/icon.png'))
        self.setWindowTitle('Combat')
        self.centerOnScreen()

        self.submitButton = QPushButton("Login")

        self.submitButton.clicked.connect(self.loginClicked)

        self.mainLayout = QHBoxLayout()

        self.turnOrderWidget = QWidget()
        self.turnOrderLayout = QVBoxLayout()
        self.turnOrderWidget.setLayout(self.turnOrderLayout)
        self.turnOrderLabel = QLabel("Turn Order")
        self.turnOrderBox = QListWidget()
        self.turnOrderButton = QPushButton("Roll for Turn Order")
        self.turnOrderButton.clicked.connect(self.turnOrderClicked)
        self.turnOrderButton.setDefault(False)
        self.turnOrderButton.setAutoDefault(False)
        self.turnOrderLayout.addWidget(self.turnOrderLabel)
        self.turnOrderLayout.addWidget(self.turnOrderBox)
        self.turnOrderLayout.addWidget(self.turnOrderButton)
        if(self.parent().playerStatus != 2):
            self.turnOrderButton.setEnabled(False)

        self.characterWidget = QWidget()
        self.characterLayout = QVBoxLayout()
        self.characterWidget.setLayout(self.characterLayout)
        self.characterLabel = QLabel("Characters")
        self.characterBox = QListWidget()
        self.addCharacterButton = QPushButton("Add Character")
        self.addCharacterButton.clicked.connect(self.addCharacterClicked)
        self.addCharacterButton.setDefault(False)
        self.addCharacterButton.setAutoDefault(False)
        self.characterLayout.addWidget(self.characterLabel)
        self.characterLayout.addWidget(self.characterBox)
        self.characterLayout.addWidget(self.addCharacterButton)
        if(self.parent().playerStatus != 2):
            self.addCharacterButton.setEnabled(False)

        self.monsterWidget = QWidget()
        self.monsterLayout = QVBoxLayout()
        self.monsterWidget.setLayout(self.monsterLayout)
        self.monsterLabel = QLabel("Monsters")
        self.monsterBox = QListWidget()
        self.addMonsterButton = QPushButton("Add Monster")
        self.addMonsterButton.clicked.connect(self.addMonsterClicked)
        self.addMonsterButton.setDefault(False)
        self.addMonsterButton.setAutoDefault(False)
        self.monsterLayout.addWidget(self.monsterLabel)
        self.monsterLayout.addWidget(self.monsterBox)
        self.monsterLayout.addWidget(self.addMonsterButton)
        if(self.parent().playerStatus != 2):
            self.addMonsterButton.setEnabled(False)


        self.mainLayout.addWidget(self.turnOrderWidget)
        self.mainLayout.addWidget(self.characterWidget)
        self.mainLayout.addWidget(self.monsterWidget)
        # self.mainLayout.addWidget(self.submitButton)

        self.setLayout(self.mainLayout)

        self.populateBoxes()

        # leave this at the end
        # self.splash.finish(self)
        print(time.clock() - timer, "seconds loading time")

if __name__ == "__main__":
    print("start program")
    app = QApplication([])
    mainWindow = mainFormDlg()
    mainWindow.show()
    sys.exit(app.exec_())
