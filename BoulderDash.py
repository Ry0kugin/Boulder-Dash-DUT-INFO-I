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

DIRECTIONS = ["Right", "Left", "Up", "Down"]
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
    nbDiamonds = randint(1, 8)
    nbBoulder = randint(2, 8)
    nbVoid = randint(1,8)
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



def getDirection(debug=False):
    """
    renvoie la direction de rockford

    :param bool debug: active le mode debug

    """
    direction = 0
    ev=donne_evenement()
    type_ev=type_evenement(ev)
    t=None
    if type_ev=="Touche":
        t=touche(ev)
    elif debug:
        t=DIRECTIONS[randint(0,3)]
    if t==DIRECTIONS[0]:
        direction=(1,0)
    elif t==DIRECTIONS[1]:
        direction=(-1,0)
    elif t==DIRECTIONS[2]:
        direction=(0,-1)
    elif t==DIRECTIONS[3]:
        direction=(0,1)
    elif t=="r":
        direction="reset"
    elif t=="d":
        direction="debug"
    else:
        direction=(0,0)
    return direction

###############################################################################


###############################################################################

if __name__ == '__main__':
    render.initWindow()

    currentMap = loadLevel()

    charlie, fallables, fall, end, startTime = logic.start(currentMap)
    remainTime = startTime
    render.renderCanvas(currentMap, charlie)
    fall = True
    debug = False

    while True:

        direction = getDirection(debug)

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

        if(direction[0] != 0 or direction[1] != 0):
            charlie = logic.moveRockford(charlie, direction, currentMap, fallables, end)
            fall, charlie = logic.updatePhysic(fallables, False, charlie, currentMap)

        if fall:
            fall, charlie = logic.updatePhysic(fallables, fall, charlie, currentMap)

        remainTime = int(currentMap[0][0]) + int(startTime - logic.getTime())

        render.renderCanvas(currentMap, charlie)
        print(charlie)
        ui.renderUI(remainTime, (charlie[1], int(currentMap[0][1])))
        mise_a_jour()
        logic.status(remainTime, currentMap[0][0])
        

###############################################################################
