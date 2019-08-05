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


    def ok(self):
        print("ok")

    def finishClicked(self):
        print("create monster")

        nameVar = (self.nameEdit.text())
        strVar = (self.strEdit.value())
        intVar = (self.intEdit.value())
        dexVar = (self.dexEdit.value())
        conVar = (self.conEdit.value())
        wisVar = (self.wisEdit.value())
        chaVar = (self.chaEdit.value())
        hpVar = (self.hpEdit.value())



        data=[33,self.parent().username,self.parent().password,nameVar,strVar,intVar,dexVar,conVar,wisVar,chaVar,hpVar,self.parent().userId]

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
            self.parent().updateMonsters()
            self.close()


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
        self.setWindowIcon(QIcon('icon.png'))
        self.setWindowTitle('Create Monster')
        self.centerOnScreen()
        self.initialised = 0


        self.characterGame = self.parent().gameList[self.parent().gamesListBox.indexFromItem(self.parent().gamesListBox.selectedItems()[0]).row()][0]


        self.nameEdit = QLineEdit()
        self.strEdit = QSpinBox()
        self.intEdit = QSpinBox()
        self.dexEdit = QSpinBox()
        self.conEdit = QSpinBox()
        self.wisEdit = QSpinBox()
        self.chaEdit = QSpinBox()
        self.hpEdit = QSpinBox()





        self.submitButton = QPushButton("Create Monster")

        self.submitButton.clicked.connect(self.finishClicked)
        # self.createAccountButton.clicked.connect(self.createAccountClicked)
        # self.forgotPasswordButton.clicked.connect(self.forgotPasswordClicked)

        # self.startClicker = QShortcut(QKeySequence("F6"),self)

        # self.startClicker.activated.connect(self.start)

        self.mainLayout = QFormLayout()

        self.mainLayout.addRow("Monster Name", self.nameEdit)
        self.mainLayout.addRow("STR",self.strEdit)
        self.mainLayout.addRow("INT",self.intEdit)
        self.mainLayout.addRow("DEX",self.dexEdit)
        self.mainLayout.addRow("CON",self.conEdit)
        self.mainLayout.addRow("WIS",self.wisEdit)
        self.mainLayout.addRow("CHA",self.chaEdit)
        self.mainLayout.addRow("HP",self.hpEdit)
        self.mainLayout.addWidget(self.submitButton)

        self.initialised = 1

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
