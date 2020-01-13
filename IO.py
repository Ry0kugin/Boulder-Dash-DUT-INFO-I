from random import randint, shuffle
import logic, render, ui
from os import listdir
from os.path import isfile, join



def loadLevel(data=None, level=None, fromData=False):
    """
    charge la carte dans un format valide pour boulder dash

    :param list level: texte contenant les données d'une carte

    >>> loadLevel("150s 1d\\nabc\\ndef")
    [['150s', '1d'], ['a', 'b', 'c'], ['d', 'e', 'f']]
    """
    levelLst = []
    if data:
        data["map"] = []
    if level == None:
        if data:
            data["map"] = randomLevel(data)
        levelLst = randomLevel(data)
    else:
        if not fromData:
            with open("level/" + level) as lvl:
                level = ""
                for line in lvl:
                    level += line

        level = level.split("\n")
        # print(level)
        # add option
        options = level[0].split()
        levelLst.append([int(options[0][0:-1]), int(options[1][0:-1])])
        if data:
            data["map"].append([int(options[0][0:-1]), int(options[1][0:-1])])
        # add map
            data["Map"] = []
        for i in range(1, len(level)):
            if level[i]:
                levelLst.append(list(level[i]))
            if data:
                data["map"].append(list(level[i]))
    return levelLst

def randomLevel(data):
    width = randint(6, 14)
    height = randint(6, 8)
    nbDiamonds = randint(1, (width + height) // 3)
    nbBoulder = randint(1, (width + height) // 4)
    nbVoid = randint(1, (width + height) // 6)
    rarestOre = randint(0, 100) 
    totalTime = randint(30, 150)

    level = [[totalTime, nbDiamonds], ["W" for i in range(width)]]
    if data:
        data["map"] = [[totalTime, nbDiamonds], ["W" for i in range(width)]]
    for i in range(height - 2):
        level.append(["W"] + ["G"] * (width - 2) + ["W"])
        if data:
            data["map"].append(["W"] + ["G"] * (width - 2) + ["W"])
    level.append(["W" for i in range(width)])
    if data:
        data["map"].append(["W" for i in range(width)])

    positions = [(i, j) for i in range(1, width - 1) for j in range(1, height - 1)]
    shuffle(positions)
    for i in range(2 + nbDiamonds + nbBoulder + nbVoid + (1 if rarestOre < 1 else 0)):
        x, y = positions[i][0], positions[i][1]
        if i == 0:
            level[y + 1][x] = "R"
            if data:
                data["map"][y + 1][x] = "R"
        elif i < 2:
            level[y + 1][x] = "E"
            if data:
                data["map"][y + 1][x] = "E"
        elif i < 2 + nbDiamonds:
            level[y + 1][x] = "D"
            if data:
                data["map"][y + 1][x] = "D"
        elif i < 2 + nbDiamonds + nbBoulder:
            level[y + 1][x] = "B"
            if data:
                data["map"][y + 1][x] = "B"
        elif i < 2 + nbDiamonds + nbBoulder + nbVoid:
            level[y + 1][x] = "."
            if data:
                data["map"][y + 1][x] = "."
        elif rarestOre < 1:
            level[y + 1][x] = "X"
            if data:
                data["map"][y + 1][x] = "X"
    return level


def save(data, fileName, saveIn="saves"):


    with open(saveIn+"/" + fileName, "w") as fos:
        if type(data) == dict:
            fos.write(saveIn+"-map-\n")
            fos.write(str(data["map"][0][0]) + "s " + str(data["map"][0][1]) + "d\n")
            for i in range(1, len(data["map"])):
                fos.write("".join(data["map"][i]) + "\n")
            fos.write("\n")

            fos.write("-rockford-\n")
            fos.write(str(data["rockford"][0]) + "-" + str(data["rockford"][1]) + " " + str(data["diamonds"]["owned"]) + "\n\n")
            fos.write("-time-\n")
            fos.write(str(data["time"]["remain"]))
        else: 
            fos.write(str(data[0][0]) + "s " + str(data[0][1]) + "d\n")
            for i in range(1, len(data)-1):
                fos.write("".join(data[i]) + "\n")
            fos.write("".join(data[-1]))
    return fileName


def checkSaveName():
    if isfile("saves/" + ui.objects["prompt_2"]["text"]):
        return False
    else:
        return True


def loadSave(level, data=None):

    with open("saves/" + level, "r") as fis:
        currentData = ""
        curMap= ""
        for line in fis:
            if line == "\n":
                currentData = ""
            if currentData == "-map-":
                curMap += line
            elif currentData == "-rockford-":
                pos, diamonds = line.strip().split()
                x, y = pos.split("-")
                if data:
                    data["rockford"] = (int(x), int(y))
                    data["diamonds"]["owned"] = int(diamonds)
            elif currentData == "-time-":
                if data:
                    data["time"]["remain"] = int(line.strip())
            line = line.strip()
            if line == "-map-" or line == "-rockford-" or line == "-time-":
                currentData = line
    if data:
        data["map"] = loadLevel(level=curMap.strip(), fromData=True)
        return data["map"]
    return loadLevel(level=curMap.strip(), fromData=True)

def getLevels(getfrom="level" ,directory=None):
    path = None  
    if directory:
        path = directory
    else:
        if getfrom == "level":
            path="level"
        elif getfrom == "save":
            path="saves"
        else:
            print("/!\ Can only load from -level- or -save-")
            print("/!\ get -level-")
            path = getfrom
    return [f for f in listdir(path) if isfile(join(path, f))]
    
def loadScore():
    scores = {}
    with open("score/score", "r") as fis:
        currentSection = None
        for line in fis.readlines():
            if line.strip() == "<s>":
                currentSection = "s"
                continue
            elif line.strip() == "<r>":
                currentSection = "r"
                continue

            if currentSection == "s":
                if "s" not in scores:
                    scores["s"] = {}
                if len(line.strip()) != 0:
                    lvl, score, player = line.strip().split("#")
                    scores["s"][lvl] = (int(score), player)
            else: 
                if "r" not in scores:
                    scores["r"] = []
                score, player = line.strip().split("#")
                scores["r"].append((score, player))
    print(scores)
    return scores
            
        
    

def saveScore(scores):
    with open("score/score" , "w") as fos:
        fos.write("<s>\n")
        for lvl in scores["s"]:
            fos.write(lvl+"#"+str(scores["s"][lvl][0])+"#"+scores["s"][lvl][1]+"\n")
        fos.write("<r>\n")
        for score in scores["r"]:
            fos.write(str(score[0])+"#"+score[1]+"\n")
        
        