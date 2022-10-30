import csv

def savemoney(money, savename = ""):
    # saving the score(= the money) to a file 

    if savename != "":
        try:
            filepath = "./assets/saves/" + str(savename) + ".txt"
        except:
            pass
    # with no attributes it is assumed that the score should be saved to the standard location
    else:
        filepath = "./assets/saves/score.txt"
    
    with open(filepath, "w") as f:
        f.write(str(money))

def readmoney(savename = ""):
    # reading the score out of the saved file
    if savename != "":
        try:
            filepath = "./assets/saves/" + str(savename) + ".txt"
        except:
            pass
    # with no attributes it is assumed that the score should be saved to the standard location
    else:
        filepath = "./assets/saves/score.txt"
    
    with open(filepath, "r") as f:
        score = f.read()
    return score

#TODO: code the following functions
def saveladeraum():
    pass

def readladeraum():
    pass

def savetreibstoff():
    pass

def readtreibstoff():
    pass