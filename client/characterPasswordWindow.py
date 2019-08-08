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

    def joinClicked(self):
        print("login")
        password = self.passwordEdit.text()
        data=[32,self.parent().username,self.parent().password,self.currentClickedGame[0],self.passwordEdit.text()]
        self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # Establish connection to TCP server and exchange data
            self.tcp_client.connect((self.host_ip, self.server_port))
            self.tcp_client.sendall(pickle.dumps(data))

            # Read data from the TCP server and close the connection
            received = pickle.loads(self.tcp_client.recv(1024))
            print(received)
            msg = QMessageBox()
            if(received):
                self.parent().characterPasswordCorrect()
                self.close()
            else:
                msg.setText("Incorrect password")
                msg.setInformativeText("Please try again")
                msg.setWindowTitle("failure")
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
        self.setGeometry(0, 0, 300, 50)
        # splashImg = QPixmap('splash.png')
        # self.splash = QSplashScreen(splashImg)
        # self.splash.show()
        self.setWindowIcon(QIcon('images/icon.png'))
        gameIndex = self.parent().gamesListBox.indexFromItem(self.parent().gamesListBox.selectedItems()[0]).row()
        self.currentClickedGame = self.parent().gameList[gameIndex]
        self.setWindowTitle(("Please enter password for " + self.currentClickedGame[1]))
        self.centerOnScreen()

        self.host_ip = "localhost"
        self.server_port = 42069
        self.passwordEdit = QLineEdit()

        self.passwordEdit.setEchoMode(2)


        self.submitButton = QPushButton("Join")


        self.submitButton.clicked.connect(self.joinClicked)

        self.mainLayout = QFormLayout()

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
