from random import randint, shuffle
import logic, render, ui


def loadLevel(level=None, fromData=False):
    """
    charge la carte dans un format valide pour boulder dash

    :param list level: texte contenant les données d'une carte

    >>> loadLevel("150s 1d\\nabc\\ndef")
    [['150s', '1d'], ['a', 'b', 'c'], ['d', 'e', 'f']]
    """
    levelLst = []
    if level == None:
        levelLst = randomLevel()
    else:
        if not fromData:
            with open("level/" + level) as lvl:
                level = ""
                for line in lvl:
                    level += line

        level = level.split("\n")
        print(level)
        # add option
        options = level[0].split()
        levelLst.append([options[0][0:-1], options[1][0:-1]])
        # add map
        for i in range(1, len(level)):
            levelLst.append(list(level[i]))
        print(levelLst)
    return levelLst


def randomLevel():
    width = randint(6, 14)
    height = randint(4, 8)
    nbDiamonds = randint(1, (width + height) // 3)
    nbBoulder = randint(1, (width + height) // 4)
    nbVoid = randint(1, (width + height) // 8)
    totalTime = randint(30, 150)

    level = [[totalTime, nbDiamonds], ["W" for i in range(width)]]
    for i in range(height - 2):
        level.append(["W"] + ["G"] * (width - 2) + ["W"])
    level.append(["W" for i in range(width)])

    positions = [(i, j) for i in range(1, width - 1) for j in range(1, height - 1)]
    shuffle(positions)
    for i in range(2 + nbDiamonds + nbBoulder + nbVoid):
        x, y = positions[i][0], positions[i][1]
        if i == 0:
            level[y + 1][x] = "R"
        elif i < 2:
            level[y + 1][x] = "E"
        elif i < 2 + nbDiamonds:
            level[y + 1][x] = "D"
        elif i < 2 + nbDiamonds + nbBoulder:
            level[y + 1][x] = "B"
        elif i < 2 + nbDiamonds + nbBoulder + nbVoid:
            level[y + 1][x] = "."
    return level


def save(curMap, rockford, remainTime):
    fileName = "save 1"

    print(curMap)
    with open("saves/" + fileName, "w") as fos:
        fos.write("-map-\n")
        fos.write(str(curMap[0][0]) + "s " + str(curMap[0][1]) + "d\n")
        for i in range(1, len(curMap)):
            fos.write("".join(curMap[i]) + "\n")
        fos.write("\n")

        fos.write("-rockford-\n")
        fos.write(str(rockford[0][0]) + "-" + str(rockford[0][1]) + " " + str(rockford[1]) + "\n\n")
        fos.write("-time-\n")
        fos.write(str(remainTime))
    return fileName


def checkSaveName():
    # JE SAIS C'EST DEGUEULASSE MAIS ON EST OBLIGES
    # PAS LE DROIT AUX IMPORTS
    try:
        with open("saves/" + ui.objects["prompt_2"]["text"]) as f:
            return False
    except:
        return True


def loadSave():
    fileName = "save 1"

    with open("saves/" + fileName, "r") as fis:
        currentData = ""
        curMap, rockford, time = "", [], 0
        for line in fis:
            if line == "\n":
                currentData = ""
            if currentData == "-map-":
                curMap += line
            elif currentData == "-rockford-":
                pos, diamonds = line.strip().split()
                x, y = pos.split("-")
                rockford = [(int(x), int(y)), int(diamonds)]
            elif currentData == "-time-":
                time = int(line.strip())
            line = line.strip()
            if line == "-map-" or line == "-rockford-" or line == "-time-":
                currentData = line

    return fileName, loadLevel(curMap.strip(), fromData=True), rockford, time
