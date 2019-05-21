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
        self.close()

    def createAccountClicked(self):
        pass

    def forgotPasswordClicked(self):
        pass

    def loginClicked(self):
        print("login")
        username = self.usernameEdit.text()
        password = self.passwordEdit.text()
        data=[1,username,password]
        self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # Establish connection to TCP server and exchange data
            self.tcp_client.connect((self.host_ip, self.server_port))
            self.tcp_client.sendall(pickle.dumps(data))

            # Read data from the TCP server and close the connection
            received = pickle.loads(self.tcp_client.recv(1024))
            print(received)
            msg = QMessageBox()
            if(received[0] == 1):
                self.parent().loggedIn = 1
                self.parent().userId = received[1]
                self.parent().username = username
                self.parent().password = password
                # msg.setText("Login success")
                # msg.setInformativeText("You are now logged in!")
                # msg.setWindowTitle("success")
                # msg.setDetailedText(":)")
                # msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                # msg.buttonClicked.connect(self.ok)
                self.close()
            else:
                msg.setText("Login failed")
                msg.setInformativeText("Please try again")
                msg.setWindowTitle("failure")
                msg.setDetailedText(":(")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg.buttonClicked.connect(self.ok)
                msg.exec_()

        finally:

            self.tcp_client.close()
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
        self.setWindowTitle('dnd app')
        self.centerOnScreen()

        self.host_ip = "localhost"
        self.server_port = 42069

        self.usernameEdit = QLineEdit()
        self.passwordEdit = QLineEdit()

        self.passwordEdit.setEchoMode(2)


        self.submitButton = QPushButton("Login")
        self.createAccountButton = QPushButton("Create Account")
        self.forgotPasswordButton = QPushButton("Forgot Password")

        self.submitButton.clicked.connect(self.loginClicked)

        self.createAccountButton.clicked.connect(self.createAccountClicked)
        self.forgotPasswordButton.clicked.connect(self.forgotPasswordClicked)

        # self.startClicker = QShortcut(QKeySequence("F6"),self)

        # self.startClicker.activated.connect(self.start)

        self.mainLayout = QFormLayout()

        self.mainLayout.addRow("username", self.usernameEdit)
        self.mainLayout.addRow("password", self.passwordEdit)
        self.mainLayout.addWidget(self.submitButton)
        self.mainLayout.addWidget(self.createAccountButton)
        self.mainLayout.addWidget(self.forgotPasswordButton)


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
