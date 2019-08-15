import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtSql import *
from PyQt5.QtGui import *
import time
# import win32api, win32con, win32gui
import socket
import pickle
import bubbleSort

class mainFormDlg(QDialog) :

    def targetClicked(self):
        self.submitButton.setEnabled(True)
        self.currentClickedTarget = (self.turnOrder[((self.targetsBox.indexFromItem(self.targetsBox.selectedItems()[0]).row()))])
        print(self.currentClickedTarget)

    def populateBoxes(self):
        try:
            data=[36,self.parent().parent().parent().username,self.parent().parent().parent().password,self.combatId]
            self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.tcp_client.connect((self.parent().parent().parent().host_ip, self.parent().parent().parent().server_port))
            self.tcp_client.sendall(pickle.dumps(data))

            received = pickle.loads(self.tcp_client.recv(1024))
            print(received)

            self.allCharacters = received[0]
            self.allMonsters = received[1]

            self.turnOrder = []

            self.charNames = []
            for char in self.allCharacters:
                self.charNames.append(char[1])
                self.turnOrder.append([ char[0], char[1], char[2], 1 ])

            self.monsterNames = []
            for monster in self.allMonsters:
                self.monsterNames.append(monster[1])
                self.turnOrder.append([ monster[0], monster[1], monster[2], 0 ])

            self.turnOrder = bubbleSort.sort(self.turnOrder)
            self.turnOrderNames = []
            for i in range(0, len(self.turnOrder)):
                self.turnOrderNames.append(self.turnOrder[i][1])
            print("TURN ORDER")
            print(self.turnOrderNames)
            print(self.turnOrder)
            self.targetsBox.clear()
            self.targetsBox.addItems(self.turnOrderNames)


        except Exception as e:
            print(e)
        finally:
            self.tcp_client.close()


    def getTargets(self):
        pass

    def attackClicked(self):

        print("target",self.currentClickedTarget)
        if(self.type==1):
            data=[38,self.parent().parent().parent().username,self.parent().parent().parent().password,self.attack,self.currentClickedTarget,self.currentId,self.combatId]
        else:
            data=[44,self.parent().parent().parent().username,self.parent().parent().parent().password,self.attack,self.currentClickedTarget,self.currentId,self.combatId]
        self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.tcp_client.connect((self.parent().parent().parent().host_ip, self.parent().parent().parent().server_port))
            self.tcp_client.sendall(pickle.dumps(data))

            received = pickle.loads(self.tcp_client.recv(1024))
            if(received[0]):
                msg = QMessageBox(self)
                msg.setText("Your attack hit!")
                if(received[2]):
                    msg.setInformativeText("You dealt "+str(received[1])+" damage!\nTarget is dead!")
                    self.parent().parent().populateBoxes()
                    self.populateBoxes()
                else:
                    msg.setInformativeText("You dealt "+str(received[1])+" damage!")
                msg.setWindowTitle("Hit!")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg.exec_()
            else:
                msg = QMessageBox(self)
                msg.setText("Your attack missed!")
                msg.setWindowTitle("Miss!")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg.exec_()

        finally:
            self.tcp_client.close()
            self.close()
            self.parent().close()


    def centerOnScreen(self):
        resolution = QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
        (resolution.height() / 2) - (self.frameSize().height() / 2))

    def __init__(self, parent= None) :
        super(mainFormDlg, self).__init__(parent)
        timer = time.perf_counter()
        self.setGeometry(0, 0, 300, 350)

        self.type = self.parent().type

        self.attack = self.parent().currentAttack
        self.combatId = self.parent().combatId
        self.currentId = self.parent().currentId

        self.setWindowIcon(QIcon('images/icon.png'))
        self.setWindowTitle('Choose Target')
        self.centerOnScreen()

        self.targetsBox = QListWidget()
        self.targetsBox.itemClicked.connect(self.targetClicked)

        self.submitButton = QPushButton("Attack!")
        self.submitButton.setEnabled(False)
        self.submitButton.clicked.connect(self.attackClicked)

        self.mainLayout = QVBoxLayout()

        self.mainLayout.addWidget(self.targetsBox)
        self.mainLayout.addWidget(self.submitButton)

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
