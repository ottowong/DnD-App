# DO NOT ALLOW COMMAS IN GAME NAMES
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


    def createClicked(self):
        print("create game")
        name = self.nameEdit.text()
        password = self.passwordEdit.text()
        data=[2,self.parent().username,self.parent().password,name,password,self.parent().userId]
        self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # Establish connection to TCP server and exchange data
            self.tcp_client.connect((self.parent().host_ip, self.parent().server_port))
            self.tcp_client.sendall(pickle.dumps(data))

            # Read data from the TCP server and close the connection
            received = pickle.loads(self.tcp_client.recv(1024))
            print(received)

        finally:
            self.tcp_client.close()
            self.parent().updateGames()
            self.close()


    def createAccountClicked(self):
        print("create account")

    def forgotPasswordClicked(self):
        print("forgot password")


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
        self.setWindowTitle('Create Game')
        self.centerOnScreen()

        self.nameEdit = QLineEdit()
        self.passwordEdit = QLineEdit()

        self.passwordEdit.setEchoMode(2)


        self.submitButton = QPushButton("Create Game")

        self.submitButton.clicked.connect(self.createClicked)
        # self.createAccountButton.clicked.connect(self.createAccountClicked)
        # self.forgotPasswordButton.clicked.connect(self.forgotPasswordClicked)

        # self.startClicker = QShortcut(QKeySequence("F6"),self)

        # self.startClicker.activated.connect(self.start)

        self.mainLayout = QFormLayout()

        self.mainLayout.addRow("game name", self.nameEdit)
        self.mainLayout.addRow("password", self.passwordEdit)
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
