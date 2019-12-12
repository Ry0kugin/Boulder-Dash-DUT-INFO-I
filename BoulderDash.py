# -*- coding: utf-8 -*-

from upemtk import *
from time import *
from random import randint
import render, logic

###### Constants used for this game #######
    # level = [
    #     ['150s', '1d'],
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
    level = level.split("\n")
    levelLst = []
    # add option
    levelLst.append(level[0].split())
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
    if type_ev=="Touche" or debug:
        if debug:
            t=DIRECTIONS[randint(0,3)]
        else:
            t=touche(ev)
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
    else:
        direction=(0,0)
    return direction

###############################################################################


###############################################################################

if __name__ == '__main__':
    render.initWindow()

    LEVEL_1 = "150s 1d\nWWWWWWWWWWWWWW\nWGGGGGG.GGDGBW\nWGBRBGGGGGG.GW\n\
WGGGGGGGGGG.GW\nWBGBBGGGGGGGGW\nWGG.BGGGGGGGGW\n\
WGGG.GG.GGGGEW\nWWWWWWWWWWWWWW"

    currentMap = loadLevel(LEVEL_1)

    charlie, fallables, fall, end = logic.start(currentMap)
    render.renderCanvas(currentMap)
    fall = True
    debug = False

    while True:

        direction = getDirection(debug)

        if direction == "reset":
            currentMap = loadLevel(LEVEL_1)
            charlie, fallables, fall = logic.start(currentMap)
            render.renderCanvas(currentMap)
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

        render.renderCanvas(currentMap, rockford)
        mise_a_jour()
        logic.status(charlie, currentMap[0][0], int(currentMap[0][1]))

###############################################################################
