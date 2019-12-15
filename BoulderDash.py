# -*- coding: utf-8 -*-

from upemtk import *
from time import *
from random import * 
import render, logic, ui

###### Constants used for this game #######
    # level = [
    #     ['150s', '2d'],
    #     ["W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W",],
    #     ["W", "G", "G", "G", "G", "G", "G", ".", "G", "G", "D", "G", "B", "W",],
    #     ["W", "G", "B", "R", "B", "G", "G", "G", "G", "G", "G", ".", "G", "W",],
    #     ["W", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", ".", "G", "W",],
    #     ["W", "B", "G", "B", "B", "G", "G", "G", "G", "G", "G", "G", "G", "W",],
    #     ["W", "G", "G", ".", "B", "G", "G", "G", "G", "G", "G", "G", "G", "W",],
    #     ["W", "G", "G", "G", ".", "G", "G", ".", "G", "G", "G", "G", "E", "W",],
    #     ["W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W",]
    # ].copy()

###############################################################################




########################### Contrôle et chargement ############################

def loadLevel(level=None):
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
        with open("level/"+level) as lvl:
            level=""
            for line in lvl:
                level+=line
        level = level.split("\n")
        # add option
        options = level[0].split()
        print(options)
        levelLst.append([options[0][0:-1], options[1][0:-1]])
        print(levelLst)
        # add map
        for i in range(1,len(level)):
            levelLst.append(list(level[i]))
    
    return levelLst

def randomLevel():
    width = randint(6,14)
    height = randint(4,8)
    nbDiamonds = randint(1, (width+height)//3)
    nbBoulder = randint(1, (width+height)//4)
    nbVoid = randint(1, (width+height)//8)
    totalTime = randint(30,150)

    level = []
    level.append([totalTime, nbDiamonds])
    level.append(["W" for i in range(width)])
    for i in range(height-2):
        level.append(["W"]+["G"]*(width-2)+["W"])
    level.append(["W" for i in range(width)])

    positions = [(i,j) for i in range(1, width-1) for j in range(1, height-1)]
    shuffle(positions)
    for i in range(2+nbDiamonds+nbBoulder+nbVoid):
        x,y = positions[i][0], positions[i][1]
        if i==0:
            level[y+1][x] = "R"
        elif i<2:
            level[y+1][x] = "E"
        elif i<2+nbDiamonds:
            level[y+1][x] = "D"    
        elif i<2+nbDiamonds+nbBoulder:
            level[y+1][x] = "B"
        elif i<2+nbDiamonds+nbBoulder+nbVoid:
            level[y+1][x] = "."
    return level


def save(curMap, rockford, remainTime):
    fileName = "save 1"
    
    print(curMap)
    with open("saves/"+fileName, "w") as s:
        s.write("map :\n")
        s.write(str(curMap[0][0])+"s "+str(curMap[0][1])+"d\n")
        for i in range(1, len(curMap)):
            s.write("".join(curMap[i])+"\n")
        s.write("\n")

        s.write("rockford :\n")
        s.write(str(rockford[0][0])+"-"+str(rockford[0][1])+" "+str(rockford[1])+"\n\n")
        s.write("time :\n")
        s.write(str(remainTime)+"\n\n")
    return fileName

def loadSave():
    fileName = "save 1"
    








###############################################################################


###############################################################################

if __name__ == '__main__':
    render.initWindow()
    ui.initUI()

    currentMap = loadLevel()

    charlie, fallables, fall, end, startTime = logic.start(currentMap)
    remainTime = startTime
    render.renderCanvas(currentMap, charlie)
    fall = True
    debug = False

    while True:
        event=donne_evenement()
        direction = logic.getDirection(event, debug)

        if direction == "reset":
            currentMap = loadLevel()
            charlie, fallables, fall, end, startTime = logic.start(currentMap)
            remainTime = startTime
            render.renderCanvas(currentMap, charlie)
            continue

        if direction == "debug":
            debug = (False if debug else True)
            print ("DEBUG ACTIVATED" if debug else "DEBUG DEACTIVATED")
            continue

        if direction == "save":
            fileName = save(currentMap, charlie, remainTime)
            print ("saved to : " + fileName)
            continue

        if(direction[0] != 0 or direction[1] != 0):
            charlie = logic.moveRockford(charlie, direction, currentMap, fallables, end)
            fall, charlie = logic.updatePhysic(fallables, False, charlie, currentMap)

        if fall:
            fall, charlie = logic.updatePhysic(fallables, fall, charlie, currentMap)

        remainTime = int(currentMap[0][0]) + int(startTime - logic.getTime())

        render.renderCanvas(currentMap, charlie)
        ui.renderUI(event, remainTime, (charlie[1], int(currentMap[0][1])))
        mise_a_jour()
        logic.status(remainTime, currentMap[0][0])
        

###############################################################################
