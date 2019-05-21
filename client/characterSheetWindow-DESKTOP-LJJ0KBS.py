import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtSql import *
from PyQt5.QtGui import *
import time
# import win32api, win32con, win32gui
import socket
import pickle


import random

import calculateAbilities
import calculateProficiency


class mainFormDlg(QDialog) :

    def statRoll(self, modifier, stat):
        message = "!r1d20+"+modifier
        data = [9,self.parent().username,self.parent().password,message]
        self.parent().chatBox.addItem(stat+" check for "+self.parent().username)
        self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_client.connect((self.parent().host_ip, self.parent().server_port))
        self.tcp_client.sendall(pickle.dumps(data))

        received = pickle.loads(self.tcp_client.recv(1024))
        self.tcp_client.close()
        if(received[0]):
            self.parent().chatBox.addItem(received[1]+"\n")
            self.parent().chatBox.scrollToBottom()

    def diceRoll(self, dice, msg):
        message = "!r"+dice
        data = [9,self.parent().username,self.parent().password,message]
        self.parent().chatBox.addItem(msg)
        self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_client.connect((self.parent().host_ip, self.parent().server_port))
        self.tcp_client.sendall(pickle.dumps(data))

        received = pickle.loads(self.tcp_client.recv(1024))
        self.tcp_client.close()
        if(received[0]):
            self.parent().chatBox.addItem(received[1]+"\n")
            self.parent().chatBox.scrollToBottom()


    def strClicked(self):
        self.statRoll(self.strLabel.text(), "Strength")
    def dexClicked(self):
        self.statRoll(self.dexLabel.text(), "Dexterity")
    def conClicked(self):
        self.statRoll(self.conLabel.text(), "Constitution")
    def intClicked(self):
        self.statRoll(self.intLabel.text(), "Intelligence")
    def wisClicked(self):
        self.statRoll(self.wisLabel.text(), "Wisdom")
    def chaClicked(self):
        self.statRoll(self.chaLabel.text(), "Charisma")

    def savStrClicked(self):
        self.statRoll(self.savStrModLabel.text(), "Strength Save")
    def savDexClicked(self):
        self.statRoll(self.savDexModLabel.text(), "Dexterity Save")
    def savConClicked(self):
        self.statRoll(self.savConModLabel.text(), "Constitution Save")
    def savIntClicked(self):
        self.statRoll(self.savIntModLabel.text(), "Intelligence Save")
    def savWisClicked(self):
        self.statRoll(self.savWisModLabel.text(), "Wisdom Save")
    def savChaClicked(self):
        self.statRoll(self.savChaModLabel.text(), "Charisma Save")



    def acrobaticsClicked(self):
        self.statRoll(self.acrobaticsLabel.text(), "Acrobatics")
    def animalHandlingClicked(self):
        self.statRoll(self.animalHandlingLabel.text(), "Animal Handling")
    def arcanaClicked(self):
        self.statRoll(self.arcanaLabel.text(), "Arcana")
    def athleticsClicked(self):
        self.statRoll(self.athleticsLabel.text(), "Athletics")
    def deceptionClicked(self):
        self.statRoll(self.deceptionLabel.text(), "Deception")
    def historyClicked(self):
        self.statRoll(self.historyLabel.text(), "History")
    def insightClicked(self):
        self.statRoll(self.insightLabel.text(), "Insight")
    def intimidationClicked(self):
        self.statRoll(self.intimidationLabel.text(), "Intimidation")
    def investigationClicked(self):
        self.statRoll(self.investigationLabel.text(), "Investigation")
    def medicineClicked(self):
        self.statRoll(self.medicineLabel.text(), "Medicine")
    def natureClicked(self):
        self.statRoll(self.natureLabel.text(), "Nature")
    def perceptionClicked(self):
        self.statRoll(self.perceptionLabel.text(), "Perception")
    def performanceClicked(self):
        self.statRoll(self.performanceLabel.text(), "Performance")
    def persuasionClicked(self):
        self.statRoll(self.persuasionLabel.text(), "Persuasion")
    def religionClicked(self):
        self.statRoll(self.religionLabel.text(), "Religion")
    def sleightOfHandClicked(self):
        self.statRoll(self.sleightOfHandLabel.text(), "Sleight of Hand")
    def stealthClicked(self):
        self.statRoll(self.stealthLabel.text(), "Stealth")
    def survivalClicked(self):
        self.statRoll(self.survivalLabel.text(), "Survival")


    def updateLabels(self):
        if(self.initialised):
            print("AAAAAAAAAAA")
            self.setWindowTitle(self.charName)
            self.characterNameLabel.setText(self.charName)

            self.charStr = self.strEdit.value()
            self.charInt = self.intEdit.value()
            self.charDex = self.dexEdit.value()
            self.charCon = self.conEdit.value()
            self.charWis = self.wisEdit.value()
            self.charCha = self.chaEdit.value()

            self.strLabel.setText(str(calculateAbilities.calcAbility(self.charStr)))
            self.intLabel.setText(str(calculateAbilities.calcAbility(self.charInt)))
            self.dexLabel.setText(str(calculateAbilities.calcAbility(self.charDex)))
            self.conLabel.setText(str(calculateAbilities.calcAbility(self.charCon)))
            self.wisLabel.setText(str(calculateAbilities.calcAbility(self.charWis)))
            self.chaLabel.setText(str(calculateAbilities.calcAbility(self.charCha)))
            self.proficiency = calculateProficiency.calcProficiency(self.levelEdit.value())
            self.proficiencyNumber.setText(str(self.proficiency))

            if(self.savStrBox.isChecked()):
                strProf = self.proficiency
            else:
                strProf = 0
            self.savStrModLabel.setText(str(calculateAbilities.calcAbility(self.charStr) + strProf))
            if(self.savDexBox.isChecked()):
                dexProf = self.proficiency
            else:
                dexProf = 0
            self.savDexModLabel.setText(str(calculateAbilities.calcAbility(self.charDex) + dexProf))
            if(self.savConBox.isChecked()):
                conProf = self.proficiency
            else:
                conProf = 0
            self.savConModLabel.setText(str(calculateAbilities.calcAbility(self.charCon) + conProf))
            if(self.savIntBox.isChecked()):
                intProf = self.proficiency
            else:
                intProf = 0
            self.savIntModLabel.setText(str(calculateAbilities.calcAbility(self.charInt) + intProf))
            if(self.savWisBox.isChecked()):
                wisProf = self.proficiency
            else:
                wisProf = 0
            self.savWisModLabel.setText(str(calculateAbilities.calcAbility(self.charWis) + wisProf))
            if(self.savChaBox.isChecked()):
                chaProf = self.proficiency
            else:
                chaProf = 0
            self.savChaModLabel.setText(str(calculateAbilities.calcAbility(self.charCha) + chaProf))


            if(self.acrobaticsBox.isChecked()):
                acrobaticsProf = self.proficiency
            else:
                acrobaticsProf = 0
            self.acrobaticsLabel.setText(str(calculateAbilities.calcAbility(self.charDex) + acrobaticsProf))
            if(self.animalHandlingBox.isChecked()):
                animalHandlingProf = self.proficiency
            else:
                animalHandlingProf = 0
            self.animalHandlingLabel.setText(str(calculateAbilities.calcAbility(self.charWis) + animalHandlingProf))
            if(self.arcanaBox.isChecked()):
                arcanaProf = self.proficiency
            else:
                arcanaProf = 0
            self.arcanaLabel.setText(str(calculateAbilities.calcAbility(self.charInt) + arcanaProf))
            if(self.athleticsBox.isChecked()):
                athleticsProf = self.proficiency
            else:
                athleticsProf = 0
            self.athleticsLabel.setText(str(calculateAbilities.calcAbility(self.charStr) + athleticsProf))
            if(self.deceptionBox.isChecked()):
                deceptionProf = self.proficiency
            else:
                deceptionProf = 0
            self.deceptionLabel.setText(str(calculateAbilities.calcAbility(self.charCha) + deceptionProf))
            if(self.historyBox.isChecked()):
                historyProf = self.proficiency
            else:
                historyProf = 0
            self.historyLabel.setText(str(calculateAbilities.calcAbility(self.charInt) + historyProf))
            if(self.insightBox.isChecked()):
                insightProf = self.proficiency
            else:
                insightProf = 0
            self.insightLabel.setText(str(calculateAbilities.calcAbility(self.charWis) + insightProf))
            if(self.intimidationBox.isChecked()):
                intimidationProf = self.proficiency
            else:
                intimidationProf = 0
            self.intimidationLabel.setText(str(calculateAbilities.calcAbility(self.charCha) + intimidationProf))
            if(self.investigationBox.isChecked()):
                investigationProf = self.proficiency
            else:
                investigationProf = 0
            self.investigationLabel.setText(str(calculateAbilities.calcAbility(self.charInt) + investigationProf))
            if(self.medicineBox.isChecked()):
                medicineProf = self.proficiency
            else:
                medicineProf = 0
            self.medicineLabel.setText(str(calculateAbilities.calcAbility(self.charWis) + medicineProf))
            if(self.natureBox.isChecked()):
                natureProf = self.proficiency
            else:
                natureProf = 0
            self.natureLabel.setText(str(calculateAbilities.calcAbility(self.charInt) + natureProf))
            if(self.perceptionBox.isChecked()):
                perceptionProf = self.proficiency
            else:
                perceptionProf = 0
            self.perceptionLabel.setText(str(calculateAbilities.calcAbility(self.charWis) + perceptionProf))
            if(self.performanceBox.isChecked()):
                performanceProf = self.proficiency
            else:
                performanceProf = 0
            self.performanceLabel.setText(str(calculateAbilities.calcAbility(self.charCha) + performanceProf))
            if(self.persuasionBox.isChecked()):
                persuasionProf = self.proficiency
            else:
                persuasionProf = 0
            self.persuasionLabel.setText(str(calculateAbilities.calcAbility(self.charCha) + persuasionProf))
            if(self.religionBox.isChecked()):
                religionProf = self.proficiency
            else:
                religionProf = 0
            self.religionLabel.setText(str(calculateAbilities.calcAbility(self.charInt) + religionProf))
            if(self.sleightOfHandBox.isChecked()):
                sleightOfHandProf = self.proficiency
            else:
                sleightOfHandProf = 0
            self.sleightOfHandLabel.setText(str(calculateAbilities.calcAbility(self.charDex) + sleightOfHandProf))
            if(self.stealthBox.isChecked()):
                stealthProf = self.proficiency
            else:
                stealthProf = 0
            self.stealthLabel.setText(str(calculateAbilities.calcAbility(self.charDex) + stealthProf))
            if(self.survivalBox.isChecked()):
                survivalProf = self.proficiency
            else:
                survivalProf = 0
            self.survivalLabel.setText(str(calculateAbilities.calcAbility(self.charWis) + survivalProf))




    def updateStats(self):
        data=[11,self.parent().username,self.parent().password]
        self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.tcp_client.connect((self.parent().host_ip, self.parent().server_port))
            self.tcp_client.sendall(pickle.dumps(data))

            received = pickle.loads(self.tcp_client.recv(1024))
            print(received)

            self.charName = received[0]
            self.charStr = received[1]
            self.charInt = received[2]
            self.charDex = received[3]
            self.charCon = received[4]
            self.charWis = received[5]
            self.charCha = received[6]
            self.charSavStr = received[7]
            self.charSavDex = received[8]
            self.charSavCon = received[9]
            self.charSavInt = received[10]
            self.charSavWis = received[11]
            self.charSavCha = received[12]
            self.charAcrobatics = received[13]
            self.charAnimalHandling = received[14]
            self.charArcana = received[15]
            self.charAthletics = received[16]
            self.charDeception = received[17]
            self.charHistory = received[18]
            self.charInsight = received[19]
            self.charIntimidation = received[20]
            self.charInvestigation = received[21]
            self.charMedicine = received[22]
            self.charNature = received[23]
            self.charPerception = received[24]
            self.charPerformance = received[25]
            self.charPersuasion = received[26]
            self.charReligion = received[27]
            self.charSleightOfHand = received[28]
            self.charStealth = received[29]
            self.charSurvival = received[30]
            self.charCurrentHp = received[31]
            self.charMaxHp = received[32]
            self.charLvl = received[33]
            self.charXp = received[34]
            self.charPersonalityTraits = received[35]
            self.charIdeals = received[36]
            self.charBonds = received[37]
            self.charFlaws = received[38]
            self.charId = received[39]

            # self.proficiency = calculateProficiency.calcProficiency(self.charLvl)

        finally:
            self.tcp_client.close()

    def updateBoxes(self):
        self.personalityTraitsBox.setText(self.charPersonalityTraits)
        self.idealsBox.setText(self.charIdeals)
        self.bondsBox.setText(self.charBonds)
        self.flawsBox.setText(self.charFlaws)

        self.levelEdit.setValue(self.charLvl)
        self.xpEdit.setValue(self.charXp)

        self.maxHpBox.setValue(self.charMaxHp)
        self.currentHpBox.setValue(self.charCurrentHp)

    def fetchAttacks(self):
        data=[12,self.parent().username,self.parent().password,self.charId]
        self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.attacksList = []
        try:
            self.tcp_client.connect((self.parent().host_ip, self.parent().server_port))
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
    def updateAttackTable(self):
        allRows = []
        for i in range(len(self.attacksList)):

            toHit = self.attacksList[i][3]
            if(self.attacksList[i][2] == 0):
                # str
                toHit += calculateAbilities.calcAbility(self.charStr)
            elif(self.attacksList[i][2] == 1):
                # dex
                toHit += calculateAbilities.calcAbility(self.charDex)
            elif(self.attacksList[i][2] == 2):
                # con
                toHit += calculateAbilities.calcAbility(self.charCon)
            elif(self.attacksList[i][2] == 3):
                # int
                toHit += calculateAbilities.calcAbility(self.charInt)
            elif(self.attacksList[i][2] == 4):
                # wis
                toHit += calculateAbilities.calcAbility(self.charWis)
            elif(self.attacksList[i][2] == 5):
                # cha
                toHit += calculateAbilities.calcAbility(self.charCha)
            if(self.attacksList[i][1]):
                toHit += self.proficiency

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


            currentRow = [self.attacksList[i][0],"1d20+"+str(toHit),self.attacksList[i][4]+"+"+str(dmg),"Edit"]
            allRows.append(currentRow)
        for value in allRows:
            row = []
            for item in value:
                cell = QStandardItem(str(item))
                row.append(cell)
            self.attacksModel.appendRow(row)
    def editAttack(self, a):
        print("edit attack")
        print(a)

    def newAttack(self):
        print("create new attack")

    def tableClicked(self, a):
        if(a.column() == 1):
            message = (self.charName+" roll to hit with "+str(self.attacksModel.data(self.attacksModel.index(a.row(),0))))
            rollStr = self.attacksModel.itemFromIndex(a).text()
            self.diceRoll(rollStr, message)
        elif(a.column() == 2):
            message = (self.charName+" roll for damage with "+str(self.attacksModel.data(self.attacksModel.index(a.row(),0))))
            rollStr = self.attacksModel.itemFromIndex(a).text()
            self.diceRoll(rollStr, message)
        elif(a.column() == 3):
            self.editAttack(self.attacksList[a.row()])


    def centerOnScreen(self):
        resolution = QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
        (resolution.height() / 2) - (self.frameSize().height() / 2) )

    def __init__(self, parent= None):
        super(mainFormDlg, self).__init__(parent)
        timer = time.perf_counter()
        # self.setGeometry(0, 0, 700, 600)
        self.setFixedSize(900, 600)
        # self.setMinimumWidth(750)
        # self.setMinimumHeight(600)
        self.initialised = 0
        self.statsList = ["STR","DEX","CON","INT","WIS","CHA"]
        self.updateStats()

        self.setWindowIcon(QIcon('icon.png'))
        self.centerOnScreen()
        self.fetchAttacks()

        self.superMainLayout = QVBoxLayout()
        self.setLayout(self.superMainLayout)
        self.mainWidget = QWidget()
        self.superMainLayout.setStretch(0,1)
        self.superMainLayout.addWidget(self.mainWidget)

        self.scrollArea = QScrollArea(self)
        self.scrollArea.setMinimumWidth(900)
        self.scrollArea.setMinimumHeight(600)
        self.scrollArea.setWidgetResizable(True)

        self.scrollArea.setWidget(self.mainWidget)

        self.characterNameLabel = QLabel()
        self.characterNameLabel.setStyleSheet("font-size:30px;")

        self.mainLayout = QVBoxLayout()
        self.mainWidget.setLayout(self.mainLayout)
        self.topRowLayout = QHBoxLayout()
        self.mainLayout.addLayout(self.topRowLayout)

        self.bottomRowLayout = QHBoxLayout()
        self.mainLayout.addLayout(self.bottomRowLayout)

        # leftColLayout
        self.leftColLayout = QVBoxLayout()
        self.mainStatsLayout = QHBoxLayout()
        self.leftColLayout.addLayout(self.mainStatsLayout)

        self.basicStatsLayout = QVBoxLayout()
        self.mainStatsLayout.addLayout(self.basicStatsLayout)

        self.moreStatsLayout = QVBoxLayout()
        self.mainStatsLayout.addLayout(self.moreStatsLayout)

        self.proficiencyWidget = QWidget()
        self.proficiencyWidget.setStyleSheet(".QWidget{border: 1px solid #000000;}")
        self.proficiencyRow = QHBoxLayout()
        self.proficiencyNumber = QLabel()
        self.proficiencyNumber.setStyleSheet("font-size:26px; font:bold;")
        self.proficiencyLabel = QLabel("Proficiency Bonus")
        self.proficiencyRow.addWidget(self.proficiencyNumber)
        self.proficiencyRow.addWidget(self.proficiencyLabel)
        self.proficiencyWidget.setLayout(self.proficiencyRow)
        self.basicStatsLayout.addWidget(self.proficiencyWidget)

        self.strWidget = QWidget()
        self.strLayout = QVBoxLayout()
        self.strWidget.setLayout(self.strLayout)
        self.strWidget.setStyleSheet(".QWidget{border: 1px solid #000000;}")
        self.basicStatsLayout.addWidget(self.strWidget)
        self.strButton = QPushButton("Strength")
        self.strButton.clicked.connect(self.strClicked)
        self.strLabel = QLabel(str(calculateAbilities.calcAbility(self.charStr)))
        self.strLabel.setStyleSheet("font-size: 36px; font:bold;")
        self.strLabel.setAlignment(Qt.AlignHCenter)
        self.strEdit = QSpinBox()
        self.strEdit.setValue(self.charStr)
        self.strEdit.valueChanged.connect(self.updateLabels)
        self.strEdit.setMinimum(8)
        self.strLayout.addWidget(self.strButton)
        self.strLayout.addWidget(self.strLabel)
        self.strLayout.addWidget(self.strEdit)

        self.dexWidget = QWidget()
        self.dexLayout = QVBoxLayout()
        self.dexWidget.setLayout(self.dexLayout)
        self.dexWidget.setStyleSheet(".QWidget{border: 1px solid #000000;}")
        self.basicStatsLayout.addWidget(self.dexWidget)
        self.dexButton = QPushButton("Dexterity")
        self.dexButton.clicked.connect(self.dexClicked)
        self.dexLabel = QLabel(str(calculateAbilities.calcAbility(self.charDex)))
        self.dexLabel.setStyleSheet("font-size: 36px; font:bold;")
        self.dexLabel.setAlignment(Qt.AlignHCenter)
        self.dexEdit = QSpinBox()
        self.dexEdit.setValue(self.charDex)
        self.dexEdit.valueChanged.connect(self.updateLabels)
        self.dexEdit.setMinimum(8)
        self.dexLayout.addWidget(self.dexButton)
        self.dexLayout.addWidget(self.dexLabel)
        self.dexLayout.addWidget(self.dexEdit)

        self.conWidget = QWidget()
        self.conLayout = QVBoxLayout()
        self.conWidget.setLayout(self.conLayout)
        self.conWidget.setStyleSheet(".QWidget{border: 1px solid #000000;}")
        self.basicStatsLayout.addWidget(self.conWidget)
        self.conButton = QPushButton("Constitution")
        self.conButton.clicked.connect(self.conClicked)
        self.conLabel = QLabel(str(calculateAbilities.calcAbility(self.charCon)))
        self.conLabel.setStyleSheet("font-size: 36px; font:bold;")
        self.conLabel.setAlignment(Qt.AlignHCenter)
        self.conEdit = QSpinBox()
        self.conEdit.setValue(self.charCon)
        self.conEdit.valueChanged.connect(self.updateLabels)
        self.conEdit.setMinimum(8)
        self.conLayout.addWidget(self.conButton)
        self.conLayout.addWidget(self.conLabel)
        self.conLayout.addWidget(self.conEdit)

        self.intWidget = QWidget()
        self.intLayout = QVBoxLayout()
        self.intWidget.setLayout(self.intLayout)
        self.intWidget.setStyleSheet(".QWidget{border: 1px solid #000000;}")
        self.basicStatsLayout.addWidget(self.intWidget)
        self.intButton = QPushButton("Intelligence")
        self.intButton.clicked.connect(self.intClicked)
        self.intLabel = QLabel(str(calculateAbilities.calcAbility(self.charInt)))
        self.intLabel.setStyleSheet("font-size: 36px; font:bold;")
        self.intLabel.setAlignment(Qt.AlignHCenter)
        self.intEdit = QSpinBox()
        self.intEdit.setValue(self.charInt)
        self.intEdit.valueChanged.connect(self.updateLabels)
        self.intEdit.setMinimum(8)
        self.intLayout.addWidget(self.intButton)
        self.intLayout.addWidget(self.intLabel)
        self.intLayout.addWidget(self.intEdit)

        self.wisWidget = QWidget()
        self.wisLayout = QVBoxLayout()
        self.wisWidget.setLayout(self.wisLayout)
        self.wisWidget.setStyleSheet(".QWidget{border: 1px solid #000000;}")
        self.basicStatsLayout.addWidget(self.wisWidget)
        self.wisButton = QPushButton("Wisdom")
        self.wisButton.clicked.connect(self.wisClicked)
        self.wisLabel = QLabel(str(calculateAbilities.calcAbility(self.charWis)))
        self.wisLabel.setStyleSheet("font-size: 36px; font:bold;")
        self.wisLabel.setAlignment(Qt.AlignHCenter)
        self.wisEdit = QSpinBox()
        self.wisEdit.setValue(self.charWis)
        self.wisEdit.valueChanged.connect(self.updateLabels)
        self.wisEdit.setMinimum(8)
        self.wisLayout.addWidget(self.wisButton)
        self.wisLayout.addWidget(self.wisLabel)
        self.wisLayout.addWidget(self.wisEdit)

        self.chaWidget = QWidget()
        self.chaLayout = QVBoxLayout()
        self.chaWidget.setLayout(self.chaLayout)
        self.chaWidget.setStyleSheet(".QWidget{border: 1px solid #000000;}")
        self.basicStatsLayout.addWidget(self.chaWidget)
        self.chaButton = QPushButton("Charisma")
        self.chaButton.clicked.connect(self.chaClicked)
        self.chaLabel = QLabel(str(calculateAbilities.calcAbility(self.charCha)))
        self.chaLabel.setStyleSheet("font-size: 36px; font:bold;")
        self.chaLabel.setAlignment(Qt.AlignHCenter)
        self.chaEdit = QSpinBox()
        self.chaEdit.setValue(self.charCha)
        self.chaEdit.valueChanged.connect(self.updateLabels)
        self.chaEdit.setMinimum(8)
        self.chaLayout.addWidget(self.chaButton)
        self.chaLayout.addWidget(self.chaLabel)
        self.chaLayout.addWidget(self.chaEdit)


        self.basicStatsLayout.addStretch(1)



        self.savingThrowsLayout = QVBoxLayout()



        self.savStrBox = QCheckBox()
        self.savDexBox = QCheckBox()
        self.savConBox = QCheckBox()
        self.savIntBox = QCheckBox()
        self.savWisBox = QCheckBox()
        self.savChaBox = QCheckBox()


        self.savStrModLabel = QLabel()
        self.savDexModLabel = QLabel()
        self.savConModLabel = QLabel()
        self.savIntModLabel = QLabel()
        self.savWisModLabel = QLabel()
        self.savChaModLabel = QLabel()

        self.acrobaticsBox = QCheckBox()
        self.animalHandlingBox = QCheckBox()
        self.arcanaBox = QCheckBox()
        self.athleticsBox = QCheckBox()
        self.deceptionBox = QCheckBox()
        self.historyBox = QCheckBox()
        self.insightBox = QCheckBox()
        self.intimidationBox = QCheckBox()
        self.investigationBox = QCheckBox()
        self.medicineBox = QCheckBox()
        self.natureBox = QCheckBox()
        self.perceptionBox = QCheckBox()
        self.performanceBox = QCheckBox()
        self.persuasionBox = QCheckBox()
        self.religionBox = QCheckBox()
        self.sleightOfHandBox = QCheckBox()
        self.stealthBox = QCheckBox()
        self.survivalBox = QCheckBox()

        self.acrobaticsLabel = QLabel()
        self.animalHandlingLabel = QLabel()
        self.arcanaLabel = QLabel()
        self.athleticsLabel = QLabel()
        self.deceptionLabel = QLabel()
        self.historyLabel = QLabel()
        self.insightLabel = QLabel()
        self.intimidationLabel = QLabel()
        self.investigationLabel = QLabel()
        self.medicineLabel = QLabel()
        self.natureLabel = QLabel()
        self.perceptionLabel = QLabel()
        self.performanceLabel = QLabel()
        self.persuasionLabel = QLabel()
        self.religionLabel = QLabel()
        self.sleightOfHandLabel = QLabel()
        self.stealthLabel = QLabel()
        self.survivalLabel = QLabel()


        self.savStrWidget = QWidget()
        self.savStrBox.stateChanged.connect(self.updateLabels)
        if(self.charSavStr):
            self.savStrBox.setCheckState(2)
        else:
            self.savStrBox.setCheckState(0)
        self.savStrLabel = QPushButton("Strength")
        self.savStrLabel.clicked.connect(self.savStrClicked)
        self.savStrRow = QHBoxLayout()
        self.savStrRow.addWidget(self.savStrBox)
        self.savStrRow.addWidget(self.savStrModLabel)
        self.savStrRow.addWidget(self.savStrLabel)
        self.savStrWidget.setLayout(self.savStrRow)
        self.savStrWidget.setStyleSheet(".QWidget{border: none;}")

        self.savDexWidget = QWidget()
        self.savDexBox.stateChanged.connect(self.updateLabels)
        if(self.charSavDex):
            self.savDexBox.setCheckState(2)
        else:
            self.savDexBox.setCheckState(0)
        self.savDexLabel = QPushButton("Dexterity")
        self.savDexLabel.clicked.connect(self.savDexClicked)
        self.savDexRow = QHBoxLayout()
        self.savDexRow.addWidget(self.savDexBox)
        self.savDexRow.addWidget(self.savDexModLabel)
        self.savDexRow.addWidget(self.savDexLabel)
        self.savDexWidget.setLayout(self.savDexRow)
        self.savDexWidget.setStyleSheet(".QWidget{border: none;}")

        self.savConWidget = QWidget()
        self.savConBox.stateChanged.connect(self.updateLabels)
        if(self.charSavCon):
            self.savConBox.setCheckState(2)
        else:
            self.savConBox.setCheckState(0)
        self.savConLabel = QPushButton("Constitution")
        self.savConLabel.clicked.connect(self.savConClicked)
        self.savConRow = QHBoxLayout()
        self.savConRow.addWidget(self.savConBox)
        self.savConRow.addWidget(self.savConModLabel)
        self.savConRow.addWidget(self.savConLabel)
        self.savConWidget.setLayout(self.savConRow)
        self.savConWidget.setStyleSheet(".QWidget{border: none;}")

        self.savIntWidget = QWidget()
        self.savIntBox.stateChanged.connect(self.updateLabels)
        if(self.charSavInt):
            self.savIntBox.setCheckState(2)
        else:
            self.savIntBox.setCheckState(0)
        self.savIntLabel = QPushButton("Intelligence")
        self.savIntLabel.clicked.connect(self.savIntClicked)
        self.savIntRow = QHBoxLayout()
        self.savIntRow.addWidget(self.savIntBox)
        self.savIntRow.addWidget(self.savIntModLabel)
        self.savIntRow.addWidget(self.savIntLabel)
        self.savIntWidget.setLayout(self.savIntRow)
        self.savIntWidget.setStyleSheet(".QWidget{border: none;}")

        self.savWisWidget = QWidget()
        self.savWisBox.stateChanged.connect(self.updateLabels)
        if(self.charSavWis):
            self.savWisBox.setCheckState(2)
        else:
            self.savWisBox.setCheckState(0)
        self.savWisLabel = QPushButton("Wisdom")
        self.savWisLabel.clicked.connect(self.savWisClicked)
        self.savWisRow = QHBoxLayout()
        self.savWisRow.addWidget(self.savWisBox)
        self.savWisRow.addWidget(self.savWisModLabel)
        self.savWisRow.addWidget(self.savWisLabel)
        self.savWisWidget.setLayout(self.savWisRow)
        self.savWisWidget.setStyleSheet(".QWidget{border: none;}")

        self.savChaWidget = QWidget()
        self.savChaBox.stateChanged.connect(self.updateLabels)
        if(self.charSavCha):
            self.savChaBox.setCheckState(2)
        else:
            self.savChaBox.setCheckState(0)
        self.savChaLabel = QPushButton("Charisma")
        self.savChaLabel.clicked.connect(self.savChaClicked)
        self.savChaRow = QHBoxLayout()
        self.savChaRow.addWidget(self.savChaBox)
        self.savChaRow.addWidget(self.savChaModLabel)
        self.savChaRow.addWidget(self.savChaLabel)
        self.savChaWidget.setLayout(self.savChaRow)
        self.savChaWidget.setStyleSheet(".QWidget{border: none;}")


        self.acrobaticsWidget = QWidget()
        self.acrobaticsBox.stateChanged.connect(self.updateLabels)
        if(self.charAcrobatics):
            self.acrobaticsBox.setCheckState(2)
        else:
            self.acrobaticsBox.setCheckState(0)
        self.acrobaticsButton = QPushButton("Acrobatics")
        self.acrobaticsButton.clicked.connect(self.acrobaticsClicked)
        self.acrobaticsRow = QHBoxLayout()
        self.acrobaticsRow.addWidget(self.acrobaticsBox)
        self.acrobaticsRow.addWidget(self.acrobaticsLabel)
        self.acrobaticsRow.addWidget(self.acrobaticsButton)
        self.acrobaticsWidget.setLayout(self.acrobaticsRow)
        self.acrobaticsWidget.setStyleSheet(".QWidget{border: none;}")

        self.animalHandlingWidget = QWidget()
        self.animalHandlingBox.stateChanged.connect(self.updateLabels)
        if(self.charAnimalHandling):
            self.animalHandlingBox.setCheckState(2)
        else:
            self.animalHandlingBox.setCheckState(0)
        self.animalHandlingButton = QPushButton("AnimalHandling")
        self.animalHandlingButton.clicked.connect(self.animalHandlingClicked)
        self.animalHandlingRow = QHBoxLayout()
        self.animalHandlingRow.addWidget(self.animalHandlingBox)
        self.animalHandlingRow.addWidget(self.animalHandlingLabel)
        self.animalHandlingRow.addWidget(self.animalHandlingButton)
        self.animalHandlingWidget.setLayout(self.animalHandlingRow)
        self.animalHandlingWidget.setStyleSheet(".QWidget{border: none;}")

        self.arcanaWidget = QWidget()
        self.arcanaBox.stateChanged.connect(self.updateLabels)
        if(self.charArcana):
            self.arcanaBox.setCheckState(2)
        else:
            self.arcanaBox.setCheckState(0)
        self.arcanaButton = QPushButton("Arcana")
        self.arcanaButton.clicked.connect(self.arcanaClicked)
        self.arcanaRow = QHBoxLayout()
        self.arcanaRow.addWidget(self.arcanaBox)
        self.arcanaRow.addWidget(self.arcanaLabel)
        self.arcanaRow.addWidget(self.arcanaButton)
        self.arcanaWidget.setLayout(self.arcanaRow)
        self.arcanaWidget.setStyleSheet(".QWidget{border: none;}")

        self.athleticsWidget = QWidget()
        self.athleticsBox.stateChanged.connect(self.updateLabels)
        if(self.charAthletics):
            self.athleticsBox.setCheckState(2)
        else:
            self.athleticsBox.setCheckState(0)
        self.athleticsButton = QPushButton("Athletics")
        self.athleticsButton.clicked.connect(self.athleticsClicked)
        self.athleticsRow = QHBoxLayout()
        self.athleticsRow.addWidget(self.athleticsBox)
        self.athleticsRow.addWidget(self.athleticsLabel)
        self.athleticsRow.addWidget(self.athleticsButton)
        self.athleticsWidget.setLayout(self.athleticsRow)
        self.athleticsWidget.setStyleSheet(".QWidget{border: none;}")

        self.deceptionWidget = QWidget()
        self.deceptionBox.stateChanged.connect(self.updateLabels)
        if(self.charDeception):
            self.deceptionBox.setCheckState(2)
        else:
            self.deceptionBox.setCheckState(0)
        self.deceptionButton = QPushButton("Deception")
        self.deceptionButton.clicked.connect(self.deceptionClicked)
        self.deceptionRow = QHBoxLayout()
        self.deceptionRow.addWidget(self.deceptionBox)
        self.deceptionRow.addWidget(self.deceptionLabel)
        self.deceptionRow.addWidget(self.deceptionButton)
        self.deceptionWidget.setLayout(self.deceptionRow)
        self.deceptionWidget.setStyleSheet(".QWidget{border: none;}")

        self.historyWidget = QWidget()
        self.historyBox.stateChanged.connect(self.updateLabels)
        if(self.charHistory):
            self.historyBox.setCheckState(2)
        else:
            self.historyBox.setCheckState(0)
        self.historyButton = QPushButton("History")
        self.historyButton.clicked.connect(self.historyClicked)
        self.historyRow = QHBoxLayout()
        self.historyRow.addWidget(self.historyBox)
        self.historyRow.addWidget(self.historyLabel)
        self.historyRow.addWidget(self.historyButton)
        self.historyWidget.setLayout(self.historyRow)
        self.historyWidget.setStyleSheet(".QWidget{border: none;}")

        self.insightWidget = QWidget()
        self.insightBox.stateChanged.connect(self.updateLabels)
        if(self.charInsight):
            self.insightBox.setCheckState(2)
        else:
            self.insightBox.setCheckState(0)
        self.insightButton = QPushButton("Insight")
        self.insightButton.clicked.connect(self.insightClicked)
        self.insightRow = QHBoxLayout()
        self.insightRow.addWidget(self.insightBox)
        self.insightRow.addWidget(self.insightLabel)
        self.insightRow.addWidget(self.insightButton)
        self.insightWidget.setLayout(self.insightRow)
        self.insightWidget.setStyleSheet(".QWidget{border: none;}")

        self.intimidationWidget = QWidget()
        self.intimidationBox.stateChanged.connect(self.updateLabels)
        if(self.charIntimidation):
            self.intimidationBox.setCheckState(2)
        else:
            self.intimidationBox.setCheckState(0)
        self.intimidationButton = QPushButton("Intimidation")
        self.intimidationButton.clicked.connect(self.intimidationClicked)
        self.intimidationRow = QHBoxLayout()
        self.intimidationRow.addWidget(self.intimidationBox)
        self.intimidationRow.addWidget(self.intimidationLabel)
        self.intimidationRow.addWidget(self.intimidationButton)
        self.intimidationWidget.setLayout(self.intimidationRow)
        self.intimidationWidget.setStyleSheet(".QWidget{border: none;}")

        self.investigationWidget = QWidget()
        self.investigationBox.stateChanged.connect(self.updateLabels)
        if(self.charInvestigation):
            self.investigationBox.setCheckState(2)
        else:
            self.investigationBox.setCheckState(0)
        self.investigationButton = QPushButton("Investigation")
        self.investigationButton.clicked.connect(self.investigationClicked)
        self.investigationRow = QHBoxLayout()
        self.investigationRow.addWidget(self.investigationBox)
        self.investigationRow.addWidget(self.investigationLabel)
        self.investigationRow.addWidget(self.investigationButton)
        self.investigationWidget.setLayout(self.investigationRow)
        self.investigationWidget.setStyleSheet(".QWidget{border: none;}")

        self.medicineWidget = QWidget()
        self.medicineBox.stateChanged.connect(self.updateLabels)
        if(self.charMedicine):
            self.medicineBox.setCheckState(2)
        else:
            self.medicineBox.setCheckState(0)
        self.medicineButton = QPushButton("Medicine")
        self.medicineButton.clicked.connect(self.medicineClicked)
        self.medicineRow = QHBoxLayout()
        self.medicineRow.addWidget(self.medicineBox)
        self.medicineRow.addWidget(self.medicineLabel)
        self.medicineRow.addWidget(self.medicineButton)
        self.medicineWidget.setLayout(self.medicineRow)
        self.medicineWidget.setStyleSheet(".QWidget{border: none;}")

        self.natureWidget = QWidget()
        self.natureBox.stateChanged.connect(self.updateLabels)
        if(self.charNature):
            self.natureBox.setCheckState(2)
        else:
            self.natureBox.setCheckState(0)
        self.natureButton = QPushButton("Nature")
        self.natureButton.clicked.connect(self.natureClicked)
        self.natureRow = QHBoxLayout()
        self.natureRow.addWidget(self.natureBox)
        self.natureRow.addWidget(self.natureLabel)
        self.natureRow.addWidget(self.natureButton)
        self.natureWidget.setLayout(self.natureRow)
        self.natureWidget.setStyleSheet(".QWidget{border: none;}")

        self.perceptionWidget = QWidget()
        self.perceptionBox.stateChanged.connect(self.updateLabels)
        if(self.charPerception):
            self.perceptionBox.setCheckState(2)
        else:
            self.perceptionBox.setCheckState(0)
        self.perceptionButton = QPushButton("Perception")
        self.perceptionButton.clicked.connect(self.perceptionClicked)
        self.perceptionRow = QHBoxLayout()
        self.perceptionRow.addWidget(self.perceptionBox)
        self.perceptionRow.addWidget(self.perceptionLabel)
        self.perceptionRow.addWidget(self.perceptionButton)
        self.perceptionWidget.setLayout(self.perceptionRow)
        self.perceptionWidget.setStyleSheet(".QWidget{border: none;}")

        self.performanceWidget = QWidget()
        self.performanceBox.stateChanged.connect(self.updateLabels)
        if(self.charPerformance):
            self.performanceBox.setCheckState(2)
        else:
            self.performanceBox.setCheckState(0)
        self.performanceButton = QPushButton("Performance")
        self.performanceButton.clicked.connect(self.performanceClicked)
        self.performanceRow = QHBoxLayout()
        self.performanceRow.addWidget(self.performanceBox)
        self.performanceRow.addWidget(self.performanceLabel)
        self.performanceRow.addWidget(self.performanceButton)
        self.performanceWidget.setLayout(self.performanceRow)
        self.performanceWidget.setStyleSheet(".QWidget{border: none;}")

        self.persuasionWidget = QWidget()
        self.persuasionBox.stateChanged.connect(self.updateLabels)
        if(self.charPersuasion):
            self.persuasionBox.setCheckState(2)
        else:
            self.persuasionBox.setCheckState(0)
        self.persuasionButton = QPushButton("Persuasion")
        self.persuasionButton.clicked.connect(self.persuasionClicked)
        self.persuasionRow = QHBoxLayout()
        self.persuasionRow.addWidget(self.persuasionBox)
        self.persuasionRow.addWidget(self.persuasionLabel)
        self.persuasionRow.addWidget(self.persuasionButton)
        self.persuasionWidget.setLayout(self.persuasionRow)
        self.persuasionWidget.setStyleSheet(".QWidget{border: none;}")

        self.religionWidget = QWidget()
        self.religionBox.stateChanged.connect(self.updateLabels)
        if(self.charReligion):
            self.religionBox.setCheckState(2)
        else:
            self.religionBox.setCheckState(0)
        self.religionButton = QPushButton("Religion")
        self.religionButton.clicked.connect(self.religionClicked)
        self.religionRow = QHBoxLayout()
        self.religionRow.addWidget(self.religionBox)
        self.religionRow.addWidget(self.religionLabel)
        self.religionRow.addWidget(self.religionButton)
        self.religionWidget.setLayout(self.religionRow)
        self.religionWidget.setStyleSheet(".QWidget{border: none;}")

        self.sleightOfHandWidget = QWidget()
        self.sleightOfHandBox.stateChanged.connect(self.updateLabels)
        if(self.charSleightOfHand):
            self.sleightOfHandBox.setCheckState(2)
        else:
            self.sleightOfHandBox.setCheckState(0)
        self.sleightOfHandButton = QPushButton("SleightOfHand")
        self.sleightOfHandButton.clicked.connect(self.sleightOfHandClicked)
        self.sleightOfHandRow = QHBoxLayout()
        self.sleightOfHandRow.addWidget(self.sleightOfHandBox)
        self.sleightOfHandRow.addWidget(self.sleightOfHandLabel)
        self.sleightOfHandRow.addWidget(self.sleightOfHandButton)
        self.sleightOfHandWidget.setLayout(self.sleightOfHandRow)
        self.sleightOfHandWidget.setStyleSheet(".QWidget{border: none;}")

        self.stealthWidget = QWidget()
        self.stealthBox.stateChanged.connect(self.updateLabels)
        if(self.charStealth):
            self.stealthBox.setCheckState(2)
        else:
            self.stealthBox.setCheckState(0)
        self.stealthButton = QPushButton("Stealth")
        self.stealthButton.clicked.connect(self.stealthClicked)
        self.stealthRow = QHBoxLayout()
        self.stealthRow.addWidget(self.stealthBox)
        self.stealthRow.addWidget(self.stealthLabel)
        self.stealthRow.addWidget(self.stealthButton)
        self.stealthWidget.setLayout(self.stealthRow)
        self.stealthWidget.setStyleSheet(".QWidget{border: none;}")

        self.survivalWidget = QWidget()
        self.survivalBox.stateChanged.connect(self.updateLabels)
        if(self.charSurvival):
            self.survivalBox.setCheckState(2)
        else:
            self.survivalBox.setCheckState(0)
        self.survivalButton = QPushButton("Survival")
        self.survivalButton.clicked.connect(self.survivalClicked)
        self.survivalRow = QHBoxLayout()
        self.survivalRow.addWidget(self.survivalBox)
        self.survivalRow.addWidget(self.survivalLabel)
        self.survivalRow.addWidget(self.survivalButton)
        self.survivalWidget.setLayout(self.survivalRow)
        self.survivalWidget.setStyleSheet(".QWidget{border: none;}")



        self.savingThrowsWidget = QWidget()
        self.savingThrowsWidget.setLayout(self.savingThrowsLayout)
        self.savingThrowsWidget.setStyleSheet(".QWidget{border: 1px solid #000000;}")
        self.skillsLayout = QVBoxLayout()
        self.skillsWidget = QWidget()
        self.skillsWidget.setLayout(self.skillsLayout)
        self.skillsWidget.setStyleSheet(".QWidget{border: 1px solid #000000;}")

        self.savingThrowsLayout.addWidget(self.savStrWidget)
        self.savingThrowsLayout.addWidget(self.savDexWidget)
        self.savingThrowsLayout.addWidget(self.savConWidget)
        self.savingThrowsLayout.addWidget(self.savIntWidget)
        self.savingThrowsLayout.addWidget(self.savWisWidget)
        self.savingThrowsLayout.addWidget(self.savChaWidget)
        self.savingThrowsLayout.addWidget(QLabel("Saving Throws"))



        self.skillsLayout.addWidget(self.acrobaticsWidget)
        self.skillsLayout.addWidget(self.animalHandlingWidget)
        self.skillsLayout.addWidget(self.arcanaWidget)
        self.skillsLayout.addWidget(self.athleticsWidget)
        self.skillsLayout.addWidget(self.deceptionWidget)
        self.skillsLayout.addWidget(self.historyWidget)
        self.skillsLayout.addWidget(self.insightWidget)
        self.skillsLayout.addWidget(self.intimidationWidget)
        self.skillsLayout.addWidget(self.investigationWidget)
        self.skillsLayout.addWidget(self.medicineWidget)
        self.skillsLayout.addWidget(self.natureWidget)
        self.skillsLayout.addWidget(self.perceptionWidget)
        self.skillsLayout.addWidget(self.performanceWidget)
        self.skillsLayout.addWidget(self.persuasionWidget)
        self.skillsLayout.addWidget(self.religionWidget)
        self.skillsLayout.addWidget(self.sleightOfHandWidget)
        self.skillsLayout.addWidget(self.stealthWidget)
        self.skillsLayout.addWidget(QLabel("Skills"))





        self.moreStatsLayout.addWidget(self.savingThrowsWidget)
        self.moreStatsLayout.addWidget(self.skillsWidget)
        #

        # midColLayout
        self.midColLayout = QVBoxLayout()
        # hp
        self.hpWidget = QWidget()
        self.hpWidget.setStyleSheet(".QWidget{border: 1px solid #000000;}")
        self.hpLayout = QVBoxLayout()
        self.hpWidget.setLayout(self.hpLayout)
        self.maxHpRow = QHBoxLayout()
        self.hpLayout.addLayout(self.maxHpRow)
        self.maxHpRow.addWidget(QLabel("Max HP"))
        self.maxHpBox = QSpinBox()
        self.maxHpRow.addWidget(self.maxHpBox)
        self.currentHpBox = QSpinBox()
        self.currentHpBox.setStyleSheet(".QSpinBox{font-size:26px;}")
        self.hpLayout.addWidget(self.currentHpBox)
        self.hpLayout.addWidget(QLabel("Current HP"))

        self.midColLayout.addWidget(self.hpWidget)
        # self.midColLayout.addWidget(self.currentHpBox)



        # attacks
        self.attacksWidget = QWidget()
        self.attacksWidget.setStyleSheet(".QWidget{border: 1px solid #000000;}")
        self.attacksLayout = QVBoxLayout()
        self.attacksWidget.setLayout(self.attacksLayout)
        self.attacksTable = QTableView(self)
        self.attacksTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.attacksTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.attacksTable.clicked.connect(self.tableClicked)
        self.attacksModel = QStandardItemModel(self)
        self.attacksModel.setHorizontalHeaderLabels(["Name","To Hit","Damage","Edit"])
        self.attacksTable.setModel(self.attacksModel)
        self.attacksLayout.addWidget(self.attacksTable)
        self.attacksLabelRow = QHBoxLayout()
        self.attacksLayout.addLayout(self.attacksLabelRow)
        self.newAttackButton = QPushButton("New Attack")
        self.newAttackButton.clicked.connect(self.newAttack)
        self.attacksLabelRow.addWidget(QLabel("Attacks"))
        self.attacksLabelRow.addWidget(self.newAttackButton)


        self.midColLayout.addWidget(self.attacksWidget)
        self.midColLayout.addStretch(1)
        #

        # rightColLayout
        self.rightColLayout = QVBoxLayout()

        self.personalityTraitsWidget = QWidget()
        self.personalityTraitsLayout = QVBoxLayout()
        self.personalityTraitsWidget.setLayout(self.personalityTraitsLayout)
        self.personalityTraitsWidget.setStyleSheet(".QWidget{border: 1px solid #000000;}")
        self.personalityTraitsBox = QTextEdit()
        self.personalityTraitsBox.setFixedHeight(100)
        self.personalityTraitsLayout.addWidget(self.personalityTraitsBox)
        self.personalityTraitsLayout.addWidget(QLabel("Personality Traits"))


        self.idealsWidget = QWidget()
        self.idealsLayout = QVBoxLayout()
        self.idealsWidget.setLayout(self.idealsLayout)
        self.idealsWidget.setStyleSheet(".QWidget{border: 1px solid #000000;}")
        self.idealsBox = QTextEdit()
        self.idealsBox.setFixedHeight(100)
        self.idealsLayout.addWidget(self.idealsBox)
        self.idealsLayout.addWidget(QLabel("Ideals"))


        self.bondsWidget = QWidget()
        self.bondsLayout = QVBoxLayout()
        self.bondsWidget.setLayout(self.bondsLayout)
        self.bondsWidget.setStyleSheet(".QWidget{border: 1px solid #000000;}")
        self.bondsBox = QTextEdit()
        self.bondsBox.setFixedHeight(100)
        self.bondsLayout.addWidget(self.bondsBox)
        self.bondsLayout.addWidget(QLabel("Bonds"))

        self.flawsWidget = QWidget()
        self.flawsLayout = QVBoxLayout()
        self.flawsWidget.setLayout(self.flawsLayout)
        self.flawsWidget.setStyleSheet(".QWidget{border: 1px solid #000000;}")
        self.flawsBox = QTextEdit()
        self.flawsBox.setFixedHeight(100)
        self.flawsLayout.addWidget(self.flawsBox)
        self.flawsLayout.addWidget(QLabel("Flaws"))

        self.rightColLayout.addWidget(self.personalityTraitsWidget)
        self.rightColLayout.addWidget(self.idealsWidget)
        self.rightColLayout.addWidget(self.bondsWidget)
        self.rightColLayout.addWidget(self.flawsWidget)


        self.rightColLayout.addStretch(1)
        #

        self.bottomRowLayout.addLayout(self.leftColLayout)
        self.bottomRowLayout.addLayout(self.midColLayout)
        self.bottomRowLayout.addLayout(self.rightColLayout)

        self.bottomRowLayout.setStretch(0,1)
        self.bottomRowLayout.setStretch(1,1)
        self.bottomRowLayout.setStretch(2,1)

        self.levelLayout = QFormLayout()
        self.levelEdit = QSpinBox()
        self.levelEdit.valueChanged.connect(self.updateLabels)
        self.levelEdit.setMinimum(1)
        self.levelEdit.setMinimumWidth(100)
        self.xpEdit = QSpinBox()
        self.levelLayout.addRow("Level",self.levelEdit)
        self.levelLayout.addRow("XP",self.xpEdit)


        self.topRowLayout.addWidget(self.characterNameLabel)
        self.topRowLayout.addStretch(1)
        self.topRowLayout.addLayout(self.levelLayout)

        self.mainLayout.setStretchFactor(self.leftColLayout,1)
        self.mainLayout.setStretchFactor(self.midColLayout,1)
        # self.mainLayout.setStretchFactor(self.rightColLayout,1)

        self.setLayout(self.superMainLayout)

        self.initialised = 1
        self.updateBoxes()
        self.updateLabels()
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
