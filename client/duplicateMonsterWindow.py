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


    def loginClicked(self):
        data=[40,self.parent().parent().username,self.parent().parent().password,self.charId,self.nameEdit.text()]
        self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.tcp_client.connect((self.parent().parent().host_ip, self.parent().parent().server_port))
            self.tcp_client.sendall(pickle.dumps(data))

            received = pickle.loads(self.tcp_client.recv(1024))
            print(received)

        finally:
            self.tcp_client.close()
            self.parent().parent().updateMonsters()
            self.close()


    def centerOnScreen(self):
        resolution = QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
        (resolution.height() / 2) - (self.frameSize().height() / 2))

    def __init__(self, parent= None) :
        super(mainFormDlg, self).__init__(parent)
        timer = time.perf_counter()
        self.setGeometry(0, 0, 300, 100)

        self.charId = self.parent().charId

        self.setWindowIcon(QIcon('images/icon.png'))
        self.setWindowTitle('dnd app')
        self.centerOnScreen()

        self.nameEdit = QLineEdit(self.parent().characterNameLabel.text())


        self.submitButton = QPushButton("Submit")
        self.submitButton.clicked.connect(self.loginClicked)

        self.mainLayout = QFormLayout()

        self.mainLayout.addRow("Name",self.nameEdit)
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
