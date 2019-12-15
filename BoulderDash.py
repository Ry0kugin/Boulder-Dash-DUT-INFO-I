# -*- coding: utf-8 -*-

from upemtk import *
from time import *
from random import randint
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

def loadLevel(level):
    """
    charge la carte dans un format valide pour boulder dash

    :param list level: texte contenant les données d'une carte

    >>> loadLevel("150s 1d\\nabc\\ndef")
    [['150s', '1d'], ['a', 'b', 'c'], ['d', 'e', 'f']]
    """
    with open("level/"+level) as lvl:
        level=""
        for line in lvl:
            level+=line
    level = level.split("\n")
    levelLst = []
    # add option
    options = level[0].split()
    print(options)
    levelLst.append([options[0][0:-1], options[1][0:-1]])
    print(levelLst)
    # add map
    for i in range(1,len(level)):
        levelLst.append(list(level[i]))
    return levelLst



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

    currentMap = loadLevel("level_1")

    charlie, fallables, fall, end, startTime = logic.start(currentMap)
    remainTime = startTime
    render.renderCanvas(currentMap, charlie)
    fall = True
    debug = False

    while True:

        direction = getDirection(debug)

        if direction == "reset":
            currentMap = loadLevel("level_1")
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
        ui.drawTimeLeft(remainTime)

        render.renderCanvas(currentMap, charlie)
        mise_a_jour()
        logic.status(charlie, remainTime, currentMap[0][0], int(currentMap[0][1]))
        

###############################################################################
