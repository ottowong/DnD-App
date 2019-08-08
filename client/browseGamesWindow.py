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

    def updateCharacters(self):
        self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.characterListFormatted = []
        self.characterList = []
        print("updating characters")
        data = [4,self.parent().username,self.parent().password,self.parent().userId]
        self.tcp_client.connect((self.parent().host_ip, self.parent().server_port))
        self.tcp_client.sendall(pickle.dumps(data))

        received = pickle.loads(self.tcp_client.recv(1024))
        self.tcp_client.close()

        for character in received:
            # self.characterListFormatted.append("id: "+str(character[0])+", "+str(character[1]))
            self.characterListFormatted.append(str(character[1]))
            self.characterList.append(character)
            character[0] = str(character[0])

        self.charactersListBox.addItems(self.characterListFormatted)
        print("updated characters")

    def updateGames(self):
        self.gamesListBox.clear()
        self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.gameListFormatted = []
        self.gameList = []
        print("updating games")
        data = [5,self.parent().username,self.parent().password]
        self.tcp_client.connect((self.parent().host_ip, self.parent().server_port))
        self.tcp_client.sendall(pickle.dumps(data))

        received = pickle.loads(self.tcp_client.recv(1024))
        self.tcp_client.close()

        for game in received:
            # self.characterListFormatted.append("id: "+str(character[0])+", "+str(character[1]))
            self.gameListFormatted.append(str(game[1]))
            self.gameList.append(game)
            game[0] = str(game[0])

        self.gamesListBox.addItems(self.gameListFormatted)
        print("updated games")

    def joinClicked(self):
        try:
            print("join")
            # print(self.parent().mainLayout.currentIndex())
            gameIndex = self.gamesListBox.indexFromItem(self.gamesListBox.selectedItems()[0]).row()
            characterIndex = self.charactersListBox.indexFromItem(self.charactersListBox.selectedItems()[0]).row()
            game = self.gameList[gameIndex]
            print(game)
            character = self.characterList[characterIndex]
            print(character)
            self.parent().currentGameId = int(game[0])
            self.parent().currentGameName = game[1]
            self.parent().currentCharId = int(character[0])
            self.parent().currentCharName = character[1]
            self.parent().characterSheetButton.setText(character[1])
            self.parent().playerStatus = 1
            self.parent().updateGame()
            self.parent().mainLayout.setCurrentIndex(2)
            self.close()
        except Exception as e:
            msg = QMessageBox()
            msg.setText("An error occurred when trying to join game")
            msg.setInformativeText("Make sure you haves selected both a game and a character.")
            msg.setWindowTitle("Error")
            # msg.setDetailedText(errorString)
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            # msg.buttonClicked.connect(self.ok)
            msg.exec_()
            print("error:",e)


    def centerOnScreen(self):
        resolution = QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
        (resolution.height() / 2) - (self.frameSize().height() / 2))

    def __init__(self, parent= None) :
        super(mainFormDlg, self).__init__(parent)
        timer = time.perf_counter()
        self.setGeometry(0, 0, 300, 100)

        self.setWindowIcon(QIcon('images/icon.png'))
        self.setWindowTitle('dnd app')
        self.centerOnScreen()

        self.submitButton = QPushButton("Join game with character")

        self.submitButton.clicked.connect(self.joinClicked)

        self.gamesListBox = QListWidget()
        self.charactersListBox = QListWidget()

        self.mainLayout = QFormLayout()

        self.mainLayout.addRow("Games", self.gamesListBox)
        self.mainLayout.addRow("Character", self.charactersListBox)

        self.mainLayout.addWidget(self.submitButton)

        self.setLayout(self.mainLayout)
        self.updateGames()
        self.updateCharacters()

        # leave this at the end
        # self.splash.finish(self)
        print(time.clock() - timer, "seconds loading time")

if __name__ == "__main__":
    print("start program")
    app = QApplication([])
    mainWindow = mainFormDlg()
    mainWindow.show()
    sys.exit(app.exec_())
