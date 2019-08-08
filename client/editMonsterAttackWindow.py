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


    def updateLabels(self):
        data=[28,self.parent().parent().username,self.parent().parent().password,self.parent().attackToEdit]
        self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.tcp_client.connect((self.parent().parent().host_ip, self.parent().parent().server_port))
            self.tcp_client.sendall(pickle.dumps(data))

            received = pickle.loads(self.tcp_client.recv(1024))
            print(received)

            self.nameEdit.setText(received[0])
            if(received[1]):
                self.proficientBox.setCheckState(2)
            self.toHitBox.setCurrentIndex(received[2])
            self.toHitModBox.setValue(received[3])
            self.dmgEdit.setText(received[4])
            self.dmgBox.setCurrentIndex(received[5])
            self.dmgModBox.setValue(received[6])

        finally:
            self.tcp_client.close()

    def save(self):
        name = self.nameEdit.text()
        proficient = self.proficientBox.isChecked()
        toHitStat = self.toHitBox.currentIndex()
        toHitMod = self.toHitModBox.value()
        dmgDice = self.dmgEdit.text()
        dmgStat = self.dmgBox.currentIndex()
        dmgMod = self.dmgModBox.value()

        data=[29,self.parent().parent().username,self.parent().parent().password,name,proficient,toHitStat,toHitMod,dmgDice,dmgStat,dmgMod,self.parent().attackToEdit]
        self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.tcp_client.connect((self.parent().parent().host_ip, self.parent().parent().server_port))
            self.tcp_client.sendall(pickle.dumps(data))

            received = pickle.loads(self.tcp_client.recv(1024))
            print(received)

        finally:
            self.tcp_client.close()
            self.parent().fetchAttacks()
            self.parent().updateAttackTable()
            self.close()

    def centerOnScreen(self):
        resolution = QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
        (resolution.height() / 2) - (self.frameSize().height() / 2))

    def __init__(self, parent= None) :
        super(mainFormDlg, self).__init__(parent)
        timer = time.perf_counter()
        self.setGeometry(0, 0, 300, 100)

        print(self.parent().attackToEdit)

        self.setWindowIcon(QIcon('images/icon.png'))
        self.setWindowTitle('Editing Attack')
        self.centerOnScreen()

        self.mainLayout = QVBoxLayout()

        self.nameRow = QHBoxLayout()
        self.toHitRow = QHBoxLayout()
        self.dmgRow = QHBoxLayout()

        self.nameEdit = QLineEdit()

        self.toHitBox = QComboBox()
        self.toHitBox.addItems(self.parent().statsList)
        self.toHitModBox = QSpinBox()
        self.proficientBox = QCheckBox()

        self.dmgEdit = QLineEdit()
        self.dmgEdit.setPlaceholderText("1d6")
        self.dmgBox = QComboBox()
        self.dmgBox.addItems(self.parent().statsList)
        self.dmgModBox = QSpinBox()

        self.nameRow.addWidget(QLabel("Name:"))
        self.nameRow.addWidget(self.nameEdit)

        self.toHitRow.addWidget(QLabel("To Hit:"))
        self.toHitRow.addWidget(self.toHitBox)
        self.toHitRow.addWidget(QLabel("+"))
        self.toHitRow.addWidget(self.toHitModBox)
        self.toHitRow.addWidget(QLabel("+"))
        self.toHitRow.addWidget(self.proficientBox)
        self.toHitRow.addWidget(QLabel("Proficient"))
        self.toHitRow.addStretch(1)

        self.dmgRow.addWidget(QLabel("Damage:"))
        self.dmgRow.addWidget(self.dmgEdit)
        self.dmgRow.addWidget(QLabel("+"))
        self.dmgRow.addWidget(self.dmgBox)
        self.dmgRow.addWidget(QLabel("+"))
        self.dmgRow.addWidget(self.dmgModBox)


        self.saveButton = QPushButton("Save Changes")
        self.saveButton.clicked.connect(self.save)




        self.mainLayout.addLayout(self.nameRow)
        self.mainLayout.addLayout(self.toHitRow)
        self.mainLayout.addLayout(self.dmgRow)

        self.mainLayout.addWidget(self.saveButton)

        self.setLayout(self.mainLayout)

        self.updateLabels()

        # leave this at the end
        # self.splash.finish(self)
        print(time.clock() - timer, "seconds loading time")

if __name__ == "__main__":
    print("start program")
    app = QApplication([])
    mainWindow = mainFormDlg()
    mainWindow.show()
    sys.exit(app.exec_())
