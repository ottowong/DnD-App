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

        data=[3,self.parent().username,self.parent().password,nameVar,strVar,intVar,dexVar,conVar,wisVar,chaVar,hpVar,self.parent().userId]

        try:
            # Establish connection to TCP server and exchange data
            self.tcp_client.connect((self.parent().host_ip, self.parent().server_port))
            self.tcp_client.sendall(pickle.dumps(data))

            # Read data from the TCP server
            received = pickle.loads(self.tcp_client.recv(1024))
            print("received",received)

        except Exception as e:
            print("ERROR: "+e)
        finally:
            # Close the connection
            self.tcp_client.close()
            # Close the window
            # self.parent().updateCharacters()
            self.parent().updateCharacters()
            self.close()

    def calculateScoreCost(self, num):
        if(num == 14):
            num = num - 7
        elif(num == 15):
            num = num - 6
        else:
            num = num - 8
        return num

    def valChanged(self):
        self.counter = 27
        self.counter -= self.calculateScoreCost(self.strEdit.value())
        self.counter -= self.calculateScoreCost(self.intEdit.value())
        self.counter -= self.calculateScoreCost(self.dexEdit.value())
        self.counter -= self.calculateScoreCost(self.conEdit.value())
        self.counter -= self.calculateScoreCost(self.wisEdit.value())
        self.counter -= self.calculateScoreCost(self.chaEdit.value())

        self.counterLabel.setText("You have "+str(self.counter)+" points left to spend.")




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
        self.setWindowTitle('Create Character')
        self.centerOnScreen()

        self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.counterLabel = QLabel("You have 27 points left to spend.")

        self.nameEdit = QLineEdit()
        self.strEdit = QSpinBox()
        self.intEdit = QSpinBox()
        self.dexEdit = QSpinBox()
        self.conEdit = QSpinBox()
        self.wisEdit = QSpinBox()
        self.chaEdit = QSpinBox()
        self.hpEdit = QSpinBox()

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



        self.submitButton = QPushButton("Create Character")

        self.submitButton.clicked.connect(self.finishClicked)
        # self.createAccountButton.clicked.connect(self.createAccountClicked)
        # self.forgotPasswordButton.clicked.connect(self.forgotPasswordClicked)

        # self.startClicker = QShortcut(QKeySequence("F6"),self)

        # self.startClicker.activated.connect(self.start)

        self.mainLayout = QFormLayout()

        self.mainLayout.addRow("Character Name", self.nameEdit)
        self.mainLayout.addRow("STR",self.strEdit)
        self.mainLayout.addRow("INT",self.intEdit)
        self.mainLayout.addRow("DEX",self.dexEdit)
        self.mainLayout.addRow("CON",self.conEdit)
        self.mainLayout.addRow("WIS",self.wisEdit)
        self.mainLayout.addRow("CHA",self.chaEdit)
        self.mainLayout.addRow("HP",self.hpEdit)
        self.mainLayout.addWidget(self.counterLabel)
        self.mainLayout.addWidget(self.submitButton)


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
