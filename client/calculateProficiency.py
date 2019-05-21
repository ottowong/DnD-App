import math
def calcProficiency(level):
    return math.ceil(level/4) + 1

if __name__ == "__main__":
    while(True):
        print(calcProficiency(int(input("level: "))))
