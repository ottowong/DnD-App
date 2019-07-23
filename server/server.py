import pyodbc

import socketserver

import pickle

from random import randint

## Laptop
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-LJJ0KBS\\SQLEXPRESS;DATABASE=DB_dnd;Trusted_Connection=yes;')
## PC
# cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-F886FQR;DATABASE=DB_dnd;Trusted_Connection=yes;')

cursor = cnxn.cursor()

class Handler_TCPServer(socketserver.BaseRequestHandler):
    """
    The TCP Server class for demonstration.

    Note: We need to implement the Handle method to exchange data
    with TCP client.

    """
    def checkLoggedIn(self,u,p):
        loginSuccess=0
        userId = 0
        try:
            executeString = "select * from Tbl_user where username = ? and password = ? "
            cursor.execute(executeString, self.data[1], self.data[2])
            rows = cursor.fetchall()
            for row in rows:
                userId = row[0]
                loginSuccess = 1
        except Exception as e:
            print("error: " + str(e))
        toReturn = [loginSuccess,userId]
        print("returning:",toReturn)
        return (toReturn)


    def handle(self):
        # self.request - TCP socket connected to the client
        self.data = pickle.loads(self.request.recv(1024).strip())
        print("{} sent:".format(self.client_address[0]))
        print("RECEIVED: ",self.data)

        if(self.data[0] == 0):
            self.request.sendall(pickle.dumps(1))

        # FUNCTIONS THAT DO NOT REQUIRE USER TO BE LOGGED IN
        if(self.data[0] == 7):
            print("CREATE ACCOUNT")
            success = 0
            try:
                executeString = "insert into Tbl_user (username, email, password, confirmed) values (?, ?, ?, ?)"
                cursor.execute(executeString, self.data[1], self.data[2], self.data[3], 1)
                cnxn.commit()
                success = 1
            except Exception as e:
                print("error: " + str(e))
            self.request.sendall(pickle.dumps(success))



        elif(self.data[0] == 8):
            print("CHECK THAT USERNAME AND EMAIL IS NOT TAKEN ALREADY")
            alreadyExists = [0,0]
            try:
                executeString = ("select * from Tbl_user where username = ?")
                cursor.execute(executeString, self.data[1])
                rows = cursor.fetchall()
                for row in rows:
                    alreadyExists[0] = 1

                executeString = ("select * from Tbl_user where email = ?")
                cursor.execute(executeString, self.data[2])
                rows = cursor.fetchall()
                for row in rows:
                    alreadyExists[1] = 1
            except Exception as e:
                print("error: " + str(e))
            toSend = alreadyExists
            self.request.sendall(pickle.dumps(toSend))

        # CHECK THAT USER IS LOGGED IN FIRST
        elif(self.checkLoggedIn(self.data[1],self.data[2])[0] != True):
            print("INCORRECT LOGIN!")
            self.request.sendall(pickle.dumps([0]))

        elif(self.data[0] == 1):
            print("LOGIN")
            loginSuccess = 0
            userId = -1
            username = ""

            try:
                executeString = "select * from Tbl_user where username = ? and password = ? "
                cursor.execute(executeString, self.data[1], self.data[2])
                rows = cursor.fetchall()
                for row in rows:
                    userId = row[0]
                    loginSuccess = 1
            except Exception as e:
                print("error: " + str(e))
            toSend = [loginSuccess,userId]
            self.request.sendall(pickle.dumps(toSend))

        elif(self.data[0] == 2):
            print("CREATE GAME")
            success = 0
            try:
                executeString = "insert into Tbl_game (name, password) values (?, ?)"
                cursor.execute(executeString, self.data[3], self.data[4])
                cnxn.commit()
                cursor.execute("SELECT TOP 1 * FROM Tbl_game ORDER BY game_ID DESC")
                rows = cursor.fetchall()
                for row in rows:
                    print(row)
                    gameId = row[0]

                cursor.execute("insert into Tbl_gameUser (game_ID, user_ID, isDm) values ("+str(gameId)+","+str(self.data[5])+",1)")
                cnxn.commit()
                success = 1
            except Exception as e:
                print("error: " + str(e))
            self.request.sendall(pickle.dumps(success))

        elif(self.data[0] == 3):
            print("CREATE CHARACTER")
            success = 0
            try:
                executeString = "insert into Tbl_character (name, str,int,dex,con,wis,cha,savStr,savDex,savCon,savInt,savWis,savCha,acrobatics,animalHandling,arcana,athletics,deception,history,insight,intimidation,investigation,medicine,nature,perception,performance,persuasion,religion,sleightOfHand,stealth,survival,currentHp,maxHp,lvl,xp,personalityTraits,ideals,bonds,flaws,user_ID) values (?, ?, ?, ?, ?, ?, ?, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ?, ?, 1, 0, '', '', '', '', ?)"
                print(executeString, self.data[3], self.data[4], self.data[5], self.data[6], self.data[7], self.data[8], self.data[9], self.data[10], self.data[10], self.data[11])
                cursor.execute(executeString, self.data[3], self.data[4], self.data[5], self.data[6], self.data[7], self.data[8], self.data[9], self.data[10], self.data[10], self.data[11])
                cnxn.commit()
                success = 1
            except Exception as e:
                print("error: " + str(e))
            if(success):
                print("CHARACTER CREATED")
            else:
                print("FAILURE")
            self.request.sendall(pickle.dumps(success))

        elif(self.data[0] == 4):
            print("RETURN USER'S CHARACTERS")
            characters = []
            try:
                executeString = "select character_ID, name from Tbl_character where user_ID = ?"
                print(executeString, self.data[3])
                cursor.execute(executeString, self.data[3])
                rows = cursor.fetchall()
                for row in rows:
                    print(row)
                    characters.append([row[0],row[1]])
            except Exception as e:
                print("error: " + str(e))
            self.request.sendall(pickle.dumps(characters))

        elif(self.data[0] == 5):
            print("RETURN ALL GAMES")
            games = []
            try:
                executeString = "select game_ID, name, password from Tbl_game"
                print(executeString)
                cursor.execute(executeString)
                rows = cursor.fetchall()
                for row in rows:
                    print(row)
                    if(row[2]):
                        pw = 1
                    else:
                        pw = 0
                    games.append([row[0],row[1],pw])
            except Exception as e:
                print("error: " + str(e))
            self.request.sendall(pickle.dumps(games))

        elif(self.data[0] == 6):
            # JOIN A GAME (unused)
            print("JOIN GAME")
            # try:
            #     executeString = "select game_ID, name from Tbl_game"
            #     print(executeString)
            #     cursor.execute(executeString)
            #     rows = cursor.fetchall()
            #     for row in rows:
            #         print(row)
            #         games.append([row[0],row[1]])
            # except Exception as e:
            #     print("error: " + str(e))
            # self.request.sendall(pickle.dumps(games))
            pass

        elif(self.data[0] == 9):
            print("MANAGE CHAT MESSAGES")
            reply = 0
            message = self.data[3]

            maxModifier = 1000
            maxNumberOfRolls = 10
            maxNumberOfDice = 10
            maxSides = 1000

            helpstring = ("""format your messages in the format:
!r[number of dice]d[number of sides]
for example:
!r1d20
you can also add a modifier or roll
multiple dice by adding:
+[number]
or
+[number of dice]d[number of sides]
to the end of your message. e.g.
!r1d20+2d6+5
do not roll more than """+str(maxNumberOfRolls)+""" dice
with more than """+str(maxSides)+""" sides
with a modifier greater than """+str(maxModifier)+"""
or more than """+str(maxNumberOfDice)+""" different dice.""")



            counter = 0
            invalid = False
            if(str.lower(str(message).replace(" ","")) == "!rhelp"):
                reply = 1
                self.request.sendall(pickle.dumps([reply,helpstring]))
            elif(str.lower(message).startswith("!r")):
                try:
                    reply = 1
                    messagestring = str.lower(message)
                    if(messagestring == "!r"):
                        messagestring = "!r1d20"
                    rollstring = ("DICE: "+str(self.data[1])+" rolled: ")
                    rollsList = messagestring[2:].split("+")
                    for i in range(0,len(rollsList)):
                        rollsList[i] = rollsList[i].split("d")
                    if(len(rollsList) > maxNumberOfDice):
                        invalid = True
                    else:
                        for i in range(0,len(rollsList)):
                            if(len(rollsList[i]) == 2):
                                if(int(rollsList[i][0]) <= maxNumberOfRolls and int(rollsList[i][1]) <= maxSides):
                                    rollstring += "\n"+str(rollsList[i][0])+" d"+str(rollsList[i][1])+":"
                                    for a in range(0, int(rollsList[i][0])):

                                        rando = (randint(1, int(rollsList[i][1])))
                                        counter += rando
                                        if (a != 0):
                                            rollstring += ","
                                        rollstring += " "+str(rando)
                                else:
                                    invalid = True
                            elif(len(rollsList[i]) == 1):
                                if (int(rollsList[i][0]) > maxModifier):
                                    invalid = True
                                else:
                                    counter += int(rollsList[i][0])
                                    rollstring += "\n+ "+str(rollsList[i][0])
                    if(invalid == False):
                        rollstring += "\nresulting in: **"+str(counter)+"**"
                        self.request.sendall(pickle.dumps([reply,rollstring]))
                    else:
                        self.request.sendall(pickle.dumps([reply,"invalid input\nType:\n```!r help```\nfor help"]))
                except Exception as e:
                    self.request.sendall(pickle.dumps([reply,"invalid input: "+str(e)+"\nType:\n```!r help```\nfor help"]))
            else:
                self.request.sendall(pickle.dumps([False]))

        elif(self.data[0] == 10):
            print("DELETE CHARACTER")
            success = 0

            try:
                executeString = "select user_ID from Tbl_user where username = ? and password = ?"
                cursor.execute(executeString, self.data[1], self.data[2])
                rows = cursor.fetchall()
                for row in rows:
                    userId = row[0]
            except Exception as e:
                print("error: " + str(e))

            try:
                executeString = "delete from Tbl_character where character_ID = ? and user_ID = ?"
                cursor.execute(executeString, self.data[3], userId)
                cnxn.commit()
                success = 1
            except Exception as e:
                print("error: " + str(e))
            self.request.sendall(pickle.dumps([success]))

        elif(self.data[0] == 11):
            print("GET CHARACTER SHEET STATS")
            success = 0

            try:
                executeString = "select user_ID from Tbl_user where username = ? and password = ?"
                cursor.execute(executeString, self.data[1], self.data[2])
                rows = cursor.fetchall()
                for row in rows:
                    userId = row[0]

                executeString = """
                select
                    name,
                    str,
                    "int",
                    dex,
                    con,
                    wis,
                    cha,
                    savStr,
                    savDex,
                    savCon,
                    savInt,
                    savWis,
                    savCha,
                    acrobatics,
                    animalHandling,
                    arcana,
                    athletics,
                    deception,
                    history,
                    insight,
                    intimidation,
                    investigation,
                    medicine,
                    nature,
                    perception,
                    performance,
                    persuasion,
                    religion,
                    sleightOfHand,
                    stealth,
                    survival,
                    currentHp,
                    maxHp,
                    lvl,
                    xp,
                    personalityTraits,
                    ideals,
                    bonds,
                    flaws,
                    character_ID
                from
                  Tbl_character
                where
                  character_ID = ?
                """
                print(executeString, self.data[3])
                cursor.execute(executeString, self.data[3])
                rows = cursor.fetchall()
                for row in rows:
                    name = row[0]
                    stre = row[1]
                    inte = row[2]
                    dex = row[3]
                    con = row[4]
                    wis = row[5]
                    cha = row[6]
                    savStr = row[7]
                    savDex = row[8]
                    savCon = row[9]
                    savInt = row[10]
                    savWis = row[11]
                    savCha = row[12]
                    acrobatics = row[13]
                    animalHandling = row[14]
                    arcana = row[15]
                    athletics = row[16]
                    deception = row[17]
                    history = row[18]
                    insight = row[19]
                    intimidation = row[20]
                    investigation = row[21]
                    medicine = row[22]
                    nature = row[23]
                    perception = row[24]
                    performance = row[25]
                    persuasion = row[26]
                    religion = row[27]
                    sleightOfHand = row[28]
                    stealth = row[29]
                    survival = row[30]
                    currentHp = row[31]
                    maxHp = row[32]
                    lvl = row[33]
                    xp = row[34]
                    personalityTraits = row[35]
                    ideals = row[36]
                    bonds = row[37]
                    flaws = row[38]
                    character_ID = row[39]
                    success = 1


                reply = [name,stre,inte,dex,con,wis,cha,savStr,savDex,savCon,savInt,savWis,savCha,acrobatics,animalHandling,arcana,athletics,deception,history,insight,intimidation,investigation,medicine,nature,perception,performance,persuasion,religion,sleightOfHand,stealth,survival,currentHp,maxHp,lvl,xp,personalityTraits,ideals,bonds,flaws,character_ID]
                print(reply)
            except Exception as e:
                print("error: " + str(e))
            self.request.sendall(pickle.dumps(reply))

        elif(self.data[0] == 12):
            print("GET ATTACKS FOR CHARACTER")
            success = 0

            try:
                executeString = "select name,proficient,toHitStat,toHitMod,dmgDice,dmgStat,dmgMod,attack_ID from Tbl_characterAttack where character_ID = ?"
                cursor.execute(executeString, self.data[3])
                rows = cursor.fetchall()
                reply = []
                for row in rows:
                    name = row[0]
                    proficient = row[1]
                    toHitStat = row[2]
                    toHitMod = row[3]
                    dmgDice = row[4]
                    dmgStat = row[5]
                    dmgMod = row[6]
                    id = row[7]
                    reply.append([name,proficient,toHitStat,toHitMod,dmgDice,dmgStat,dmgMod,id])


                print(reply)
            except Exception as e:
                print("error: " + str(e))
            self.request.sendall(pickle.dumps(reply))

        elif(self.data[0] == 13):
            print("GET ATTACK FOR EDITING")
            success = 0

            try:
                executeString = "select name,proficient,toHitStat,toHitMod,dmgDice,dmgStat,dmgMod from Tbl_characterAttack where attack_ID = ?"
                cursor.execute(executeString, self.data[3])
                rows = cursor.fetchall()
                reply = []
                for row in rows:
                    name = row[0]
                    proficient = row[1]
                    toHitStat = row[2]
                    toHitMod = row[3]
                    dmgDice = row[4]
                    dmgStat = row[5]
                    dmgMod = row[6]
                reply = [name,proficient,toHitStat,toHitMod,dmgDice,dmgStat,dmgMod]


                print(reply)
            except Exception as e:
                print("error: " + str(e))
            self.request.sendall(pickle.dumps(reply))

        elif(self.data[0] == 14):
            print("UPDATE CHARACTER SHEET")
            success = 0

            try:
                executeString = """
UPDATE Tbl_character
SET
    name = ?
    ,str = ?
    ,int = ?
    ,dex = ?
    ,con = ?
    ,wis = ?
    ,cha = ?
    ,savStr = ?
    ,savDex = ?
    ,savCon = ?
    ,savInt = ?
    ,savWis = ?
    ,savCha = ?
    ,acrobatics = ?
    ,animalHandling = ?
    ,arcana = ?
    ,athletics = ?
    ,deception = ?
    ,history = ?
    ,insight = ?
    ,intimidation = ?
    ,investigation = ?
    ,medicine = ?
    ,nature = ?
    ,perception = ?
    ,performance = ?
    ,persuasion = ?
    ,religion = ?
    ,sleightOfHand = ?
    ,stealth = ?
    ,survival = ?
    ,currentHp = ?
    ,maxHp = ?
    ,lvl = ?
    ,xp = ?
    ,personalityTraits = ?
    ,ideals = ?
    ,bonds = ?
    ,flaws = ?
WHERE character_ID = ?
                """
                cursor.execute(executeString,self.data[3] ,self.data[4] ,self.data[5] ,self.data[6] ,self.data[7] ,self.data[8] ,self.data[9] ,self.data[10] ,self.data[11] ,self.data[12] ,self.data[13] ,self.data[14] ,self.data[15] ,self.data[16] ,self.data[17] ,self.data[18] ,self.data[19] ,self.data[20] ,self.data[21] ,self.data[22] ,self.data[23] ,self.data[24] ,self.data[25] ,self.data[26] ,self.data[27] ,self.data[28] ,self.data[29] ,self.data[30] ,self.data[31] ,self.data[32] ,self.data[33] ,self.data[34] ,self.data[35] ,self.data[36] ,self.data[37] ,self.data[38] ,self.data[39] ,self.data[40] ,self.data[41] ,self.data[42])
                cnxn.commit()
                success = 1
            except Exception as e:
                print("error: " + str(e))
            self.request.sendall(pickle.dumps(success))

        elif(self.data[0] == 15):
            print("UPDATE ATTACK")
            success = 0

            try:
                executeString = """
UPDATE Tbl_characterAttack
SET
    name = ?
    ,proficient = ?
    ,toHitStat = ?
    ,toHitMod = ?
    ,dmgDice = ?
    ,dmgStat = ?
    ,dmgMod = ?
WHERE attack_ID = ?
                """
                cursor.execute(executeString ,self.data[3] ,self.data[4] ,self.data[5] ,self.data[6] ,self.data[7] ,self.data[8] ,self.data[9] ,self.data[10])
                cnxn.commit()
                success = 1
            except Exception as e:
                print("error: " + str(e))
            self.request.sendall(pickle.dumps(success))

        elif(self.data[0] == 16):
            print("DELETE ATTACK")
            success = 0

            try:
                executeString = "delete from Tbl_characterAttack where attack_ID = ?"
                cursor.execute(executeString, self.data[3])
                cnxn.commit()
                success = 1
            except Exception as e:
                print("error: " + str(e))
            self.request.sendall(pickle.dumps([success]))

        elif(self.data[0] == 17):
            print("CREATE ATTACK")
            success = 0

            try:
                executeString = """
INSERT INTO Tbl_characterAttack
(
    name
    ,proficient
    ,toHitStat
    ,toHitMod
    ,dmgDice
    ,dmgStat
    ,dmgMod
    ,character_ID
)
VALUES
(
    ?
    ,?
    ,?
    ,?
    ,?
    ,?
    ,?
    ,?
)
                """
                cursor.execute(executeString ,self.data[3] ,self.data[4] ,self.data[5] ,self.data[6] ,self.data[7] ,self.data[8] ,self.data[9] ,self.data[10])
                cnxn.commit()
                success = 1
            except Exception as e:
                print("error: " + str(e))
            self.request.sendall(pickle.dumps(success))

        elif(self.data[0] == 18):
            print("CREATE MAP")
            success = 0

            try:
                executeString = """
INSERT INTO Tbl_characterAttack
(
    name
    ,proficient
    ,toHitStat
    ,toHitMod
    ,dmgDice
    ,dmgStat
    ,dmgMod
    ,character_ID
)
VALUES
(
    ?
    ,?
    ,?
    ,?
    ,?
    ,?
    ,?
    ,?
)
                """
                cursor.execute(executeString ,self.data[3] ,self.data[4] ,self.data[5] ,self.data[6] ,self.data[7] ,self.data[8] ,self.data[9] ,self.data[10])
                cnxn.commit()
                success = 1
            except Exception as e:
                print("error: " + str(e))
            self.request.sendall(pickle.dumps(success))


        # just send back ACK for data arrival confirmation
        else:
            print(self.data[0])
            self.request.sendall(pickle.dumps("message received"))







if __name__ == "__main__":
    HOST, PORT = "localhost", 42069
    print("server running")
    # Init the TCP server object, bind it to the localhost on 42069 port
    tcp_server = socketserver.TCPServer((HOST, PORT), Handler_TCPServer)

    # Activate the TCP server.
    # To abort the TCP server, press Ctrl-C.

    tcp_server.serve_forever()
