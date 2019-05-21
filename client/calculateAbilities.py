import math
def calcAbility(score):
    return math.floor((score - 10)/2)

if __name__ == "__main__":
    while(True):
        print(calcAbility(int(input("score: "))))
