import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtSql import *
from PyQt5.QtGui import *
import time
# import win32api, win32con, win32gui
import socket
import pickle

class mainFormDlg(QDialog) :

    def updateStuff(self):
        data=[39,self.parent().parent().username,self.parent().parent().password,self.gameId,self.combatId]
        self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.tcp_client.connect((self.parent().parent().host_ip, self.parent().parent().server_port))
            self.tcp_client.sendall(pickle.dumps(data))

            received = pickle.loads(self.tcp_client.recv(1024))
            print(received)

            self.monstersList = received

            for monster in self.monstersList:
                self.monstersBox.addItem(monster[1])

        except Exception as e:
            print(e)

        finally:
            self.tcp_client.close()


    def loginClicked(self):

        if(len(self.monstersBox.selectedItems()) == 0):
            self.close()
        monsterIds = []
        for item in self.monstersBox.selectedItems():
            monsterIds.append(self.monstersList[self.monstersBox.indexFromItem(item).row()][0])

        data=[41,self.parent().parent().username,self.parent().parent().password,monsterIds,self.combatId]
        self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.tcp_client.connect((self.parent().parent().host_ip, self.parent().parent().server_port))
            self.tcp_client.sendall(pickle.dumps(data))

            received = pickle.loads(self.tcp_client.recv(1024))
            print(received)


        except Exception as e:
            print(e)

        finally:
            self.tcp_client.close()
            self.parent().populateBoxes()
            self.close()


    def centerOnScreen(self):
        resolution = QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
        (resolution.height() / 2) - (self.frameSize().height() / 2))

    def __init__(self, parent= None) :
        super(mainFormDlg, self).__init__(parent)
        timer = time.perf_counter()
        self.setGeometry(0, 0, 300, 100)

        self.setWindowIcon(QIcon('images/icon.png'))
        self.setWindowTitle('Add Monster to Combat')
        self.centerOnScreen()

        self.gameId = self.parent().gameId
        self.combatId = self.parent().combatId

        self.monstersBox = QListWidget()
        self.monstersBox.setSelectionMode(QListWidget.ExtendedSelection)

        self.submitButton = QPushButton("Add to Combat")

        self.submitButton.clicked.connect(self.loginClicked)

        self.mainLayout = QVBoxLayout()

        self.mainLayout.addWidget(self.monstersBox)
        self.mainLayout.addWidget(self.submitButton)

        self.setLayout(self.mainLayout)

        self.updateStuff()

        # leave this at the end
        # self.splash.finish(self)
        print(time.clock() - timer, "seconds loading time")

if __name__ == "__main__":
    print("start program")
    app = QApplication([])
    mainWindow = mainFormDlg()
    mainWindow.show()
    sys.exit(app.exec_())
