from random import randint
def roll(message):

    maxModifier = 1000
    maxNumberOfRolls = 10
    maxNumberOfDice = 10
    maxSides = 1000

    helpstring = ("""
    format your messages in the format:
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
    or more than """+str(maxNumberOfDice)+""" different dice.
    """)



    counter = 0
    invalid = False
    if(str.lower(str(message).replace(" ","")) == "!rhelp"):
      return([True,helpstring])
    elif(str.lower(message).startswith("!r")):
      try:
          messagestring = str.lower(message)
          if(messagestring == "!r"):
              messagestring = "!r1d20"
          rollstring = ("You rolled: ")
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
              return([True,rollstring])
          else:
              return([True,"invalid input\nType:\n```!r help```\nfor help"])
      except Exception as e:
          return([True,"invalid input: "+str(e)+"\nType:\n```!r help```\nfor help"])
    else:
      return(False)

if __name__ == "__main__":
    while(True):
        print(roll(input("roll: "))[1])
