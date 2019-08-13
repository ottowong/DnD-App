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
import calculateProficiency
import chooseTargetWindow

class mainFormDlg(QDialog) :

    def diceRoll(self, dice):
        self.currentDice = dice
        chooseTargetWindow.mainFormDlg(self).show()


    def updateStats(self):
        data=[11,self.parent().parent().username,self.parent().parent().password,self.currentId]
        self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.tcp_client.connect((self.parent().parent().host_ip, self.parent().parent().server_port))
            self.tcp_client.sendall(pickle.dumps(data))

            received = pickle.loads(self.tcp_client.recv(1024))

            self.charName = received[0]
            self.charStr = received[1]
            self.charInt = received[2]
            self.charDex = received[3]
            self.charCon = received[4]
            self.charWis = received[5]
            self.charCha = received[6]

            self.charLvl = received[33]

            self.proficiency = calculateProficiency.calcProficiency(self.charLvl)

        finally:
            self.tcp_client.close()

    def updateAttackTable(self):
        self.attacksModel.clear()
        self.attacksModel.setHorizontalHeaderLabels(["Name","Damage"])
        allRows = []
        for i in range(len(self.attacksList)):


            dmg = self.attacksList[i][6]
            if(self.attacksList[i][5] == 0):
                # str
                dmg += calculateAbilities.calcAbility(self.charStr)
            elif(self.attacksList[i][5] == 1):
                # dex
                dmg += calculateAbilities.calcAbility(self.charDex)
            elif(self.attacksList[i][5] == 2):
                # con
                dmg += calculateAbilities.calcAbility(self.charCon)
            elif(self.attacksList[i][5] == 3):
                # int
                dmg += calculateAbilities.calcAbility(self.charInt)
            elif(self.attacksList[i][5] == 4):
                # wis
                dmg += calculateAbilities.calcAbility(self.charWis)
            elif(self.attacksList[i][5] == 5):
                # cha
                dmg += calculateAbilities.calcAbility(self.charCha)

            currentRow = [self.attacksList[i][0],self.attacksList[i][4]+"+"+str(dmg)]
            allRows.append(currentRow)
        for value in allRows:
            row = []
            for item in value:
                cell = QStandardItem(str(item))
                row.append(cell)
            self.attacksModel.appendRow(row)

    def fetchAttacks(self):
        data=[12,self.parent().parent().username,self.parent().parent().password,self.currentId]
        self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.attacksList = []
        try:
            self.tcp_client.connect((self.parent().parent().host_ip, self.parent().parent().server_port))
            self.tcp_client.sendall(pickle.dumps(data))

            received = pickle.loads(self.tcp_client.recv(1024))
            print(received)
            self.attacksList = received
            print(self.attacksList)

        except Exception as e:
            msg = QMessageBox(self)
            msg.setText("An error occurred")
            msg.setWindowTitle("Error")
            # msg.setDetailedText(errorString)
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            # msg.buttonClicked.connect(self.ok)
            msg.exec_()
            print("error:",e)

    def tableClicked(self, a):

        if(a.column() == 1):
            message = (self.charName+" roll to damage with "+str(self.attacksModel.data(self.attacksModel.index(a.row(),0))))
            rollStr = self.attacksModel.itemFromIndex(a).text()
            self.diceRoll(rollStr)

    def centerOnScreen(self):
        resolution = QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
        (resolution.height() / 2) - (self.frameSize().height() / 2))

    def __init__(self, parent= None) :
        super(mainFormDlg, self).__init__(parent)
        timer = time.perf_counter()
        self.setGeometry(0, 0, 300, 100)

        self.setWindowIcon(QIcon('images/icon.png'))
        self.setWindowTitle('Attacks')
        self.centerOnScreen()

        self.currentThing = self.parent().currentClickedThing
        self.currentId = self.currentThing[0]
        self.combatId = self.parent().combatId
        print("thing")
        print(self.currentThing)
        print(self.currentId)

        self.attacksTable = QTableView(self)
        self.attacksTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.attacksTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.attacksTable.clicked.connect(self.tableClicked)
        self.attacksModel = QStandardItemModel(self)
        self.attacksTable.setModel(self.attacksModel)



        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.attacksTable)

        self.setLayout(self.mainLayout)

        self.fetchAttacks()
        self.updateStats()
        self.updateAttackTable()

        # leave this at the end
        # self.splash.finish(self)
        print(time.clock() - timer, "seconds loading time")

if __name__ == "__main__":
    print("start program")
    app = QApplication([])
    mainWindow = mainFormDlg()
    mainWindow.show()
    sys.exit(app.exec_())
