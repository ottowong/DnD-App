import sys
import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtSql import *
from PyQt5.QtGui import *
import time
import re
# import win32api, win32con, win32gui
import socket
import pickle
import createGameWindow
import createCharacterWindow
import characterSheetWindow


class mainFormDlg(QWidget):

    def sendChatMessage(self):
        message = self.chatLineEdit.text()
        if(message!=""):
            data = [9,self.username,self.password,message]
            self.chatBox.addItem(self.username+": "+message+"\n")
            self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.tcp_client.connect((self.host_ip, self.server_port))
            self.tcp_client.sendall(pickle.dumps(data))

            received = pickle.loads(self.tcp_client.recv(1024))
            self.tcp_client.close()
            if(received[0]):
                self.chatBox.addItem(received[1]+"\n")
                self.chatBox.scrollToBottom()

        self.chatLineEdit.clear()

    # JOIN GAME STUFF
    def updateCharacters(self):
        try:
            self.charactersListBox.clear()
            gameId = self.gameList[self.gamesListBox.indexFromItem(self.gamesListBox.selectedItems()[0]).row()][0]
            self.joinGameButton.setEnabled(False)
            self.deleteCharacterButton.setEnabled(False)
            self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.characterListFormatted = []
            self.characterList = []
            print("updating characters")
            data = [4,self.username,self.password,self.userId,gameId]
            self.tcp_client.connect((self.host_ip, self.server_port))
            self.tcp_client.sendall(pickle.dumps(data))

            received = pickle.loads(self.tcp_client.recv(1024))
            self.tcp_client.close()
            for character in received:
                # self.characterListFormatted.append("id: "+str(character[0])+", "+str(character[1]))
                self.characterListFormatted.append(str(character[1]))
                self.characterList.append(character)
                character[0] = str(character[0])
                self.charactersListBox.addItems(self.characterListFormatted)
        except Exception as e:
            print(e)



        print("updated characters")

    def updateGames(self):
        self.gamesListBox.clear()
        self.joinGameButton.setEnabled(False)
        self.joinGameDmButton.setEnabled(False)
        self.deleteGameButton.setEnabled(False)
        self.createCharacterButton.setEnabled(False)
        self.deleteCharacterButton.setEnabled(False)
        self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.gameListFormatted = []
        self.gameList = []
        print("updating games")
        data = [5,self.username,self.password]
        self.tcp_client.connect((self.host_ip, self.server_port))
        self.tcp_client.sendall(pickle.dumps(data))

        received = pickle.loads(self.tcp_client.recv(1024))
        self.tcp_client.close()

        for game in received:
            print(game)
            # self.characterListFormatted.append("id: "+str(character[0])+", "+str(character[1]))
            gameStartString = ""
            if(game[3] == self.userId):
                gameStartString += "DM "
            else:
                gameStartString += "        "
            if(game[2]):
                #  - locked
                gameStartString += "* "
            else:
                #  - unlocked
                gameStartString += "   "
            self.gameListFormatted.append(gameStartString+str(game[1])+"")


            self.gameList.append(game)
            game[0] = str(game[0])

        self.gamesListBox.addItems(self.gameListFormatted)
        print("updated games")

    def joinGameButtonClicked(self):
        try:
            print("join")
            # print(self.mainLayout.currentIndex())
            gameIndex = self.gamesListBox.indexFromItem(self.gamesListBox.selectedItems()[0]).row()
            characterIndex = self.charactersListBox.indexFromItem(self.charactersListBox.selectedItems()[0]).row()
            game = self.gameList[gameIndex]
            print(game)
            character = self.characterList[characterIndex]
            print(character)
            self.currentGameId = int(game[0])
            self.currentGameName = game[1]
            self.currentCharId = int(character[0])
            print("currentCharId: ",self.currentCharId)
            self.currentCharName = character[1]
            self.characterSheetButton.setText(character[1])
            self.playerStatus = 1
            self.gameRightWidget.setTabEnabled(1,True)
            self.updateGame()
            self.mainLayout.setCurrentIndex(2)
            self.chatBox.clear()
            self.chatBox.addItem("Welcome to " + self.currentGameName + "\nType \"!r help\" \nfor help with dice commands.\n")

        except Exception as e:
            msg = QMessageBox(self)
            msg.setText("An error occurred when trying to join game")
            msg.setInformativeText("Make sure you haves selected both a game and a character.")
            msg.setWindowTitle("Error")
            # msg.setDetailedText(errorString)
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            # msg.buttonClicked.connect(self.ok)
            msg.exec_()
            print("error:",e)

    def deleteGame(self):
        print("delete game")
        index = ((self.gamesListBox.indexFromItem(self.gamesListBox.selectedItems()[0]).row()))
        msg = QMessageBox.question(self, "Confirm", "Are you sure you want to delete "+str(self.gameList[index][1])+"?", QMessageBox.Yes|QMessageBox.No)
        print(self.gameList[index])
        # msg.setText("Are you sure you want to delete "+str(self.characterList[index][1])+"?")
        # msg.setInformativeText("")
        # msg.setWindowTitle("Confirm")
        # msg.setDetailedText(errorString)
        if(msg == QMessageBox.Yes):
            self.delGame()
        # msg.exec_()

    def joinGameDmButtonClicked(self):

        try:
            print("join")
            # print(self.mainLayout.currentIndex())
            gameIndex = self.gamesListBox.indexFromItem(self.gamesListBox.selectedItems()[0]).row()
            game = self.gameList[gameIndex]
            print(game)
            self.currentGameId = int(game[0])
            self.currentGameName = game[1]
            # self.characterSheetButton.setText(character[1])
            self.playerStatus = 2
            self.gameRightWidget.setTabEnabled(1,False)
            self.updateGame()
            self.mainLayout.setCurrentIndex(2)
            self.chatBox.clear()
        except Exception as e:
            msg = QMessageBox(self)
            msg.setText("An error occurred when trying to join game")
            msg.setInformativeText("Make sure you haves selected both a game and a character.")
            msg.setWindowTitle("Error")
            # msg.setDetailedText(errorString)
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            # msg.buttonClicked.connect(self.ok)
            msg.exec_()
            print("error:",e)

    # END OF JOIN GAME STUFF

    def setLoggedInText(self):
        if(self.loggedIn):
            print("user is logged in")
            text = "Logged in as: "+self.username
            self.logoutButton.setVisible(True)
            self.logoutButton.setText("Logout")
        else:
            print("user is not logged in")
            text = "Not logged in"
            self.logoutButton.setVisible(False)
        self.loggedInLabel.setText(text)

    def createAccountClicked(self):
        self.mainLayout.setCurrentIndex(3)
        self.logoutButton.setVisible(True)
        self.logoutButton.setText("Back")
        self.createUsernameEdit.setText(self.usernameEdit.text())
        self.createPasswordEdit.setText(self.passwordEdit.text())

    def createAccount(self):

        errors = []
        errorString = ""
        msg = QMessageBox(self)

        self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        data = [8,self.createUsernameEdit.text(),self.createEmailEdit.text()]
        self.tcp_client.connect((self.host_ip, self.server_port))
        self.tcp_client.sendall(pickle.dumps(data))
        received = pickle.loads(self.tcp_client.recv(1024))
        print(received)
        self.tcp_client.close()
        if(received[0] == 1):
            errors.append("Username is already in use.")
        if(received[1] == 1):
            errors.append("Email is already in use.")

        if(self.createPasswordEdit.text() != self.createPasswordEdit2.text()):
            errors.append("Passwords do not match.")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.createEmailEdit.text()):
            errors.append("Email is invalid.")
        if not re.match(r"^[A-Za-z0-9]+(?:[ _-][A-Za-z0-9]+)*$", self.createUsernameEdit.text()):
            errors.append("Username is invalid.")
        if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$", self.createPasswordEdit.text()):
            errors.append("Password must contain at least one capital and lower case letter, at least one number, and be at least 8 digits long.")
        if(errors == []):


            self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            data = [7,self.createUsernameEdit.text(),self.createEmailEdit.text(),self.createPasswordEdit.text()]
            print(data)
            self.tcp_client.connect((self.host_ip, self.server_port))
            self.tcp_client.sendall(pickle.dumps(data))
            received = pickle.loads(self.tcp_client.recv(1024))
            print(received)
            self.tcp_client.close()
            if(received==1):
                successMsg = QMessageBox(self)
                successMsg.setText("Account created successfully")
                successMsg.setInformativeText("Please login")
                successMsg.setWindowTitle("Success")
                successMsg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                # successMsg.buttonClicked.connect(self.ok)
                successMsg.exec_()
                self.mainLayout.setCurrentIndex(0)
            else:
                pass
        else:

            for error in errors:
                errorString += error+"\n"
            msg.setText("Error when creating account")
            msg.setInformativeText("Please try again")
            msg.setWindowTitle("Error")
            msg.setDetailedText(errorString)
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            # msg.buttonClicked.connect(self.ok)
            msg.exec_()

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
            print("received:",received)
            msg = QMessageBox(self)
            if(received[0] == 1):
                self.loggedIn = 1
                self.userId = received[1]
                self.username = username
                self.password = password
                # msg.setText("Login success")
                # msg.setInformativeText("You are now logged in!")
                # msg.setWindowTitle("success")
                # msg.setDetailedText(":)")
                # msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                # msg.buttonClicked.connect(self.ok)
                self.setLoggedInText()
                self.updateGames()
                # self.updateCharacters()
                self.mainLayout.setCurrentIndex(1)
            else:
                msg.setText("Login failed")
                msg.setInformativeText("Please try again")
                msg.setWindowTitle("failure")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                # msg.buttonClicked.connect(self.ok)
                msg.exec_()

        finally:

            self.tcp_client.close()

    def logout(self):
        print("logout")
        self.resetVars()
        self.setLoggedInText()
        self.mainLayout.setCurrentIndex(0)

    def leaveGame(self):
        self.currentGameId = 0
        self.currentGameName = ""
        self.currentCharId = 0
        self.currentCharName = ""
        self.mainLayout.setCurrentIndex(1)

    def createGame(self):
        game = createGameWindow.mainFormDlg(self)
        game.exec_()

    def delChar(self):
        index = ((self.charactersListBox.indexFromItem(self.charactersListBox.selectedItems()[0]).row()))
        data = [10, self.username,self.password,self.characterList[index][0]]
        self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # Establish connection to TCP server and exchange data
            self.tcp_client.connect((self.host_ip, self.server_port))
            self.tcp_client.sendall(pickle.dumps(data))

            # Read data from the TCP server and close the connection
            received = pickle.loads(self.tcp_client.recv(1024))
            print("received:",received)
            msg = QMessageBox(self)
            if(received[0] == 1):
                self.updateCharacters()
            else:
                msg.setText("Delete failed!")
                msg.setInformativeText("Please try again")
                msg.setWindowTitle("failure")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                # msg.buttonClicked.connect(self.ok)
                msg.exec_()

        finally:

            self.tcp_client.close()
    def delGame(self):
        index = ((self.gamesListBox.indexFromItem(self.gamesListBox.selectedItems()[0]).row()))
        data = [20, self.username,self.password,self.gameList[index][0]]
        self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # Establish connection to TCP server and exchange data
            self.tcp_client.connect((self.host_ip, self.server_port))
            self.tcp_client.sendall(pickle.dumps(data))

            # Read data from the TCP server and close the connection
            received = pickle.loads(self.tcp_client.recv(1024))
            print("received:",received)
            msg = QMessageBox(self)
            if(received[0] == 1):
                self.updateGames()
                self.updateCharacters()
            else:
                msg.setText("Delete failed!")
                msg.setInformativeText("Please try again")
                msg.setWindowTitle("failure")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                # msg.buttonClicked.connect(self.ok)
                msg.exec_()

        finally:

            self.tcp_client.close()

    def deleteCharacter(self):
        index = ((self.charactersListBox.indexFromItem(self.charactersListBox.selectedItems()[0]).row()))
        msg = QMessageBox.question(self, "Confirm", "Are you sure you want to delete "+str(self.characterList[index][1])+"?", QMessageBox.Yes|QMessageBox.No)
        print(self.characterList[index])
        # msg.setText("Are you sure you want to delete "+str(self.characterList[index][1])+"?")
        # msg.setInformativeText("")
        # msg.setWindowTitle("Confirm")
        # msg.setDetailedText(errorString)
        if(msg == QMessageBox.Yes):
            self.delChar()
        # msg.exec_()

    def createCharacter(self):
        character = createCharacterWindow.mainFormDlg(self)
        character.exec_()

    def showCharacterSheet(self):
        charSheet = characterSheetWindow.mainFormDlg(self)
        charSheet.show()

    def updateGame(self):
        print("update game")
        self.gameNameLabel.setText(self.currentGameName)
        if(self.playerStatus == 2):
            self.currentCharName = "DM"
        self.characterNameLabel.setText("Playing as: "+self.currentCharName)

    def updateJoinButton(self):
        try:
            if(self.charactersListBox.selectedItems()[0] and self.gamesListBox.selectedItems()[0]):
                self.joinGameButton.setEnabled(True)
                self.deleteCharacterButton.setEnabled(True)
        except:
            self.joinGameButton.setEnabled(False)
            self.deleteCharacterButton.setEnabled(False)

    def updateJoinDmButton(self):
        self.updateJoinButton()
        self.updateCharacters()
        try:
            if(self.gamesListBox.selectedItems()[0]):
                self.createCharacterButton.setEnabled(True)
                if(self.userId == self.gameList[self.gamesListBox.indexFromItem(self.gamesListBox.selectedItems()[0]).row()][3]):
                    self.joinGameDmButton.setEnabled(True)
                    self.deleteGameButton.setEnabled(True)
                else:
                    self.joinGameDmButton.setEnabled(False)
                    self.deleteGameButton.setEnabled(False)
            else:
                self.joinGameDmButton.setEnabled(False)
                self.deleteGameButton.setEnabled(False)
                self.createCharacterButton.setEnabled(False)
        except:
            self.joinGameDmButton.setEnabled(False)
            self.deleteGameButton.setEnabled(False)
            self.createCharacterButton.setEnabled(False)


    def centerOnScreen(self):
        resolution = QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
        (resolution.height() / 2) - (self.frameSize().height() / 2))

    def resetVars(self):
        # 0 = nothing; 1 = player; 2 = DM
        self.playerStatus = 0

        self.loggedIn = 0
        self.userId = -1
        self.username = ""
        self.password = ""
        self.currentGameId = 0
        self.currentGameName = ""
        self.currentCharId = 0
        self.currentCharName = ""

    def setupLoginPage(self):
        # LogoutRow
        self.logoutRow = QHBoxLayout()
        self.logoutButton = QPushButton("Logout")
        self.logoutButton.setDefault(False)
        self.logoutButton.setAutoDefault(False)
        self.logoutButton.setVisible(False)
        self.logoutButton.clicked.connect(self.logout)
        self.loggedInLabel = QLabel("Not logged in")
        self.logoutRow.addWidget(self.loggedInLabel)
        self.logoutRow.addStretch(1)
        self.logoutRow.addWidget(self.logoutButton)
        #

        # loginLayout
        self.loginLayout = QFormLayout()
        self.loginWidget = QWidget()
        self.loginWidget.setLayout(self.loginLayout)

        self.usernameEdit = QLineEdit()
        self.passwordEdit = QLineEdit()

        self.usernameEdit.returnPressed.connect(self.loginClicked)
        self.passwordEdit.returnPressed.connect(self.loginClicked)

        self.passwordEdit.setEchoMode(2)


        self.loginSubmitButton = QPushButton("Login")
        self.createAccountButton = QPushButton("Create Account")
        self.forgotPasswordButton = QPushButton("Forgot Password")

        self.loginSubmitButton.clicked.connect(self.loginClicked)

        self.createAccountButton.clicked.connect(self.createAccountClicked)
        self.forgotPasswordButton.clicked.connect(self.forgotPasswordClicked)


        self.loginLayout.addRow("username", self.usernameEdit)
        self.loginLayout.addRow("password", self.passwordEdit)
        self.loginLayout.addWidget(self.loginSubmitButton)
        self.loginLayout.addWidget(self.createAccountButton)
        # self.loginLayout.addWidget(self.forgotPasswordButton)
        pass

    def setupMenuPage(self):
        # menuLayout

        # font_id = QFontDatabase.addApplicationFont("Font Awesome 5 Free-Solid-900.otf")
        #
        # if font_id is not -1:
        #     font_db = QFontDatabase()
        #     self.font_styles = font_db.styles('FontAwesome')
        #     self.font_families = QFontDatabase.applicationFontFamilies(font_id)
        #     for font_family in self.font_families:
        #         self.fonty = font_db.font(font_family, self.font_styles[0], 12)
        #
        #



        # self.setStyleSheet(self.css.format())
        #
        # btn = QtGui.QToolButton(self)
        # btn.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        # btn.setFont(self.font)
        # btn.setText(unichr(int('e025', 16)))
        # btn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        #
        #
        self.menuLayout = QHBoxLayout()
        self.menuLeftLayout = QVBoxLayout()
        self.menuRightLayout = QVBoxLayout()
        self.menuWidget = QWidget()
        self.menuWidget.setLayout(self.menuLayout)

        self.gamesTitle = QLabel("Games")
        self.charactersTitle = QLabel("Characters")

        # self.gamesTitle.setFont(self.fonty)
        # self.gamesTitle.setText(unichr(int('e025', 16)))
        # self.charactersTitle

        self.createGameButton = QPushButton("Create Game")
        self.deleteGameButton = QPushButton("Delete Game")
        self.createCharacterButton = QPushButton("Create Character")
        self.deleteCharacterButton = QPushButton("Delete Character")
        self.deleteCharacterButton.clicked.connect(self.deleteCharacter)
        self.createCharacterButton.clicked.connect(self.createCharacter)
        self.createGameButton.clicked.connect(self.createGame)
        self.deleteGameButton.clicked.connect(self.deleteGame)

        self.createCharacterButton.setEnabled(False)

        self.joinGameButton = QPushButton("Join game with character")
        self.joinGameButton.setEnabled(False)

        self.joinGameButton.clicked.connect(self.joinGameButtonClicked)

        self.joinGameDmButton = QPushButton("Join game as DM")
        self.joinGameDmButton.setEnabled(False)
        self.deleteGameButton.setEnabled(False)

        self.joinGameDmButton.clicked.connect(self.joinGameDmButtonClicked)

        self.gamesListBox = QListWidget()
        self.gamesListBox.itemClicked.connect(self.updateJoinDmButton)
        # self.gamesListBox.setTextFormat(Qt.RichText)
        self.charactersListBox = QListWidget()
        self.charactersListBox.itemClicked.connect(self.updateJoinButton)

        # self.gamesListBox.setFont(self.fonty)
        # self.charactersListBox.setFont(self.fonty)

        self.menuLeftLayout.addWidget(self.gamesTitle)
        self.menuLeftLayout.addWidget(self.gamesListBox)
        self.menuLeftLayout.addWidget(self.createGameButton)
        self.menuLeftLayout.addWidget(self.deleteGameButton)
        self.menuLeftLayout.addWidget(self.joinGameDmButton)

        self.menuRightLayout.addWidget(self.charactersTitle)
        self.menuRightLayout.addWidget(self.charactersListBox)
        self.menuRightLayout.addWidget(self.createCharacterButton)
        self.menuRightLayout.addWidget(self.deleteCharacterButton)
        self.menuRightLayout.addWidget(self.joinGameButton)

        self.menuLayout.addLayout(self.menuLeftLayout)
        self.menuLayout.addLayout(self.menuRightLayout)

    def setupGamePage(self):
        # gameNameRow
        self.gameNameRow = QHBoxLayout()
        self.gameNameLabel = QLabel()
        self.gameNameLabel.setFont(self.headerFont)
        self.gameNameRow.addStretch(1)
        self.gameNameRow.addWidget(self.gameNameLabel)
        self.gameNameRow.addStretch(1)
        #

        # gameLeaveRow
        self.gameLeaveRow = QHBoxLayout()
        self.characterNameLabel = QLabel()
        self.gameLeaveButton = QPushButton("Leave Game")
        self.gameLeaveButton.clicked.connect(self.leaveGame)

        self.gameLeaveRow.addWidget(self.characterNameLabel)
        self.gameLeaveRow.addStretch(1)
        self.gameLeaveRow.addWidget(self.gameLeaveButton)
        #

        # gameLeftLayout
        self.gameLeftLayout = QVBoxLayout()
        self.mapTable = QTableView()
        self.mapModel = QStandardItemModel()
        self.mapTable.setModel(self.mapModel)
        self.gameLeftLayout.addWidget(self.mapTable)
        self.gameLeftLayout.setStretch(0,1)
        #

        # chatTabWidget
        self.chatTabWidget = QWidget()
        self.chatTabLayout = QVBoxLayout()
        self.chatTabWidget.setLayout(self.chatTabLayout)
        self.chatBox = QListWidget()
        self.chatLineEdit = QLineEdit()
        self.chatLineEdit.returnPressed.connect(self.sendChatMessage)
        self.chatLineEdit.setPlaceholderText("Type a message...")

        self.chatTabLayout.addWidget(self.chatBox)
        self.chatTabLayout.addWidget(self.chatLineEdit)
        #

        # characterTabWidget
        self.characterTabWidget = QWidget()
        self.characterTabLayout = QVBoxLayout()
        self.characterTabWidget.setLayout(self.characterTabLayout)

        self.characterSheetButton = QPushButton()
        self.characterSheetButton.clicked.connect(self.showCharacterSheet)
        self.characterTabLayout.addWidget(self.characterSheetButton)
        self.characterTabLayout.addStretch(1)
        #

        # settingsTabWidget
        self.settingsTabWidget = QWidget()
        #

        # gameRightWidget
        self.gameRightWidget = QTabWidget()
        self.gameRightWidget.addTab(self.chatTabWidget,"Chat")
        # if(self.playerStatus == 1):
        self.gameRightWidget.addTab(self.characterTabWidget,"Character")
        # else:
        # self.gameRightWidget.addTab(self.characterTabWidget,"Monsters")
        self.gameRightWidget.addTab(self.settingsTabWidget,"Settings")
        #
        # gameContentLayout
        self.gameContentLayout = QHBoxLayout()
        self.gameContentLayout.addLayout(self.gameLeftLayout)
        self.gameContentLayout.setStretchFactor(self.gameLeftLayout,3)
        self.gameContentLayout.addWidget(self.gameRightWidget)
        self.gameContentLayout.setStretchFactor(self.gameRightWidget,1)
        #

        # gameLayout
        self.gameLayout = QVBoxLayout()
        self.gameWidget = QWidget()
        self.gameWidget.setStyleSheet(".QWidget{border: 1px solid #bababa;}")
        self.gameWidget.setLayout(self.gameLayout)


        self.gameLayout.addLayout(self.gameNameRow)
        self.gameLayout.addLayout(self.gameLeaveRow)
        self.gameLayout.addLayout(self.gameContentLayout)
        self.gameLayout.setStretchFactor(self.gameContentLayout,1)

    def setupSignUpPage(self):
        # createAccountWidget
        self.createAccountWidget = QWidget()
        self.createAccountLayout = QFormLayout()
        self.createAccountWidget.setLayout(self.createAccountLayout)

        self.createUsernameEdit = QLineEdit()
        self.createEmailEdit = QLineEdit()
        self.createPasswordEdit = QLineEdit()
        self.createPasswordEdit2 = QLineEdit()
        self.registerButton = QPushButton("Register")
        self.registerButton.clicked.connect(self.createAccount)

        self.createUsernameEdit.returnPressed.connect(self.createAccount)
        self.createEmailEdit.returnPressed.connect(self.createAccount)
        self.createPasswordEdit.returnPressed.connect(self.createAccount)
        self.createPasswordEdit2.returnPressed.connect(self.createAccount)

        self.createPasswordEdit.setEchoMode(2)
        self.createPasswordEdit2.setEchoMode(2)

        self.createAccountLayout.addRow("Username", self.createUsernameEdit)
        self.createAccountLayout.addRow("Email", self.createEmailEdit)
        self.createAccountLayout.addRow("Password", self.createPasswordEdit)
        self.createAccountLayout.addRow("Reenter password", self.createPasswordEdit2)
        self.createAccountLayout.addWidget(self.registerButton)

    def setupGameDmPage(self):
        self.gameDmWidget = QWidget()

    def setupMainLayout(self):
        # mainLayout
        self.mainLayout = QStackedLayout()
        self.superMainLayout = QVBoxLayout()
        self.setLayout(self.superMainLayout)

        self.superMainLayout.addLayout(self.logoutRow)
        self.superMainLayout.addLayout(self.mainLayout)

        # self.menuLayout.addLayout(self.logoutRow)

        self.mainLayout.addWidget(self.loginWidget)
        self.mainLayout.addWidget(self.menuWidget)
        self.mainLayout.addWidget(self.gameWidget)
        self.mainLayout.addWidget(self.createAccountWidget)
        self.mainLayout.addWidget(self.gameDmWidget)

    def __init__(self, parent= None) :
        super(mainFormDlg, self).__init__(parent)
        # timer = time.perf_counter()
        self.setGeometry(0, 0, 1000, 600)
        splashImg = QPixmap('splash.png')
        self.splash = QSplashScreen(splashImg)
        self.splash.show()
        self.setWindowIcon(QIcon('icon.png'))
        self.setWindowTitle('DnD App')
        self.centerOnScreen()
        # self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.resetVars()

        self.host_ip = "localhost"
        self.server_port = 42069
        # fonts
        self.headerFont = QFont("Arial", 10, QFont.Bold);
        #
        self.setupLoginPage()

        self.setupMenuPage()

        self.setupGamePage()

        self.setupSignUpPage()

        self.setupGameDmPage()

        self.setupMainLayout()

        self.mainLayout.setCurrentIndex(0)
        # self.usernameEdit.setFocus()

        # leave this at the end
        self.splash.finish(self)
        # print(time.clock() - timer, "seconds loading time")

if __name__ == "__main__":
    print("start program")
    app = QApplication(sys.argv)
    mainWindow = mainFormDlg()
    mainWindow.show()
    sys.exit(app.exec_())
