# -*- coding: utf-8 -*-

from upemtk import *
from time import *

###### Constants used for this game #######
LEVEL_1 = [
        ['150s', '1d'],
        ["W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W",],
        ["W", "G", "G", "G", "G", "G", "G", ".", "G", "G", "D", "G", "B", "W",],
        ["W", "G", "B", "R", "B", "G", "G", "G", "G", "G", "G", ".", "G", "W",],
        ["W", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", ".", "G", "W",],
        ["W", "B", "G", "B", "B", "G", "G", "G", "G", "G", "G", "G", "G", "W",],
        ["W", "G", "G", ".", "B", "G", "G", "G", "G", "G", "G", "G", "G", "W",],
        ["W", "G", "G", "G", ".", "G", "G", ".", "G", "G", "G", "G", "E", "W",],
        ["W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W",]
]
CELL_NBX = 20
CELL_NBY = 10
CELL_SIZE = 32
HALF_SIZE = CELL_SIZE//2
WIDTH_WINDOW = CELL_SIZE * CELL_NBX
HEIGHT_WINDOW = CELL_SIZE * CELL_NBY
###########################################

########## Very Useful fonctions ##########

def sumTuple(a,b):
    tmp = []
    for i in range(2):
        tmp.append(a[i] + b[i])
    tmp.append(a[2])
    return tuple(tmp) 

########################################### 

def getDirection():
    direction = 0
    ev=donne_evenement()
    type_ev=type_evenement(ev)
    if type_ev=="Touche":
        t=touche(ev)
        if t=="Right":
            direction=(1,0)
        elif t=="Left":
            direction=(-1,0)
        elif t=="Up":
            direction=(0,-1)
        elif t=="Down":
            direction=(0,1)
        else:
            direction=(0,0)
    else:
        direction=(0,0)
    return direction


def drawVoid(coord):
    rectangle(
        coord[0],
        coord[1],
        coord[0]+CELL_SIZE,
        coord[1]+CELL_SIZE,
        '#000',
        '#000'
    )

def drawWall(coord):
    rectangle(
        coord[0],
        coord[1],
        coord[0]+CELL_SIZE,
        coord[1]+CELL_SIZE,
        '#666',
        '#666'
    )

def drawGrass(coord):
    rectangle(
        coord[0],
        coord[1],
        coord[0]+CELL_SIZE,
        coord[1]+CELL_SIZE,
        '#850',
        '#850'
    )

def drawBoulder(coord):
    drawVoid(coord)
    cercle(
        coord[0]+HALF_SIZE,
        coord[1]+HALF_SIZE,
        HALF_SIZE,
        '#888',
        '#aaa'
    )

def drawDiamond(coord):
    drawVoid(coord)
    points = [
        (coord[0]+HALF_SIZE, coord[1]),
        (coord[0], coord[1]+HALF_SIZE),
        (coord[0]+HALF_SIZE, coord[1]+CELL_SIZE),
        (coord[0]+CELL_SIZE, coord[1]+HALF_SIZE)
    ]
    polygone(points,'#09f','#0ff')

def drawEnd(coord):
    rectangle(
        coord[0],
        coord[1],
        coord[0]+CELL_SIZE,
        coord[1]+CELL_SIZE,
        '#0a0',
        '#0a0'
    )
    cercle(
        coord[0]+HALF_SIZE,
        coord[1]+HALF_SIZE,
        HALF_SIZE//2,
        '#0f0',
        '#0f0'
    )
    

def drawRockford(coord):
    drawVoid(coord)
    cercle(
        coord[0]+HALF_SIZE,
        coord[1]+HALF_SIZE//2,
        HALF_SIZE//2,
        '#c80',
        '#f41'
    )
    rectangle(
        coord[0]+HALF_SIZE//2,
        coord[1]+HALF_SIZE,
        coord[0]+HALF_SIZE*1.5,
        coord[1]+CELL_SIZE,
        '#c80',
        '#f41'
    )

renderCase = {
    '.' : (lambda x : drawVoid(x)),
    'W' : (lambda x : drawWall(x)),
    'G' : (lambda x : drawGrass(x)),
    'B' : (lambda x : drawBoulder(x)),
    'D' : (lambda x : drawDiamond(x)),
    'E' : (lambda x : drawEnd(x)),
    'R' : (lambda x : drawRockford(x))
}

def renderCanvas(curMap):
    efface_tout()
    for y in range(1,len(curMap)):
        for x in range(0, len(curMap[y])):
            x1 = x*CELL_SIZE
            y1 = y*CELL_SIZE
            renderCase[curMap[y][x]]((x1,y1))

def trouveCharlie(curMap):
    for i in range(1, len(curMap)):
        for j in range(len(curMap[i])):
            if curMap[i][j] == "R":
                return (j,i)

def getCell(coord, curMap):
    return curMap[coord[1]][coord[0]]

def setCell(coord, curMap, content):
    curMap[coord[1]][coord[0]] = content


def moveRockford(rockford, direction, curMap):
    print(rockford)
    aimCoord = sumTuple(rockford, direction)

    aimCell = getCell(aimCoord, curMap)
    
    if aimCell == ".":
        print("Hey, it's a void")
        setCell(rockford, curMap, ".")   # refectoring à faire
        setCell(aimCoord, curMap, "R")
        return aimCoord
    elif aimCell == "G":
        print("Hey, it's a grass")
        setCell(rockford, curMap, ".")   # refectoring à faire
        setCell(aimCoord, curMap, "R")
        return aimCoord
    elif aimCell == "B":
        if direction[1] == 0:
            behindBoulder = sumTuple(aimCoord,direction)
            if(getCell(behindBoulder, curMap) == "."):
                print("BOULDER DASH")
                setCell(rockford, curMap, ".")   # refectoring à faire
                setCell(aimCoord, curMap, "R")
                setCell(behindBoulder, curMap, "B")
                return aimCoord
    elif aimCell == "D":
        print("DIAMOND")
        setCell(rockford, curMap, ".")   # refectoring à faire
        setCell(aimCoord, curMap, "R")
        return aimCoord[0], aimCoord[1], aimCoord[2]+1

    else:
        print("Useless...", aimCell, getCell(rockford,curMap))
    return rockford
    
def setPhysics():
    pass

def reset():
    pass

def levelWin():
    pass

def levelLose():
    pass

def debugMode():
    pass

if __name__ == '__main__':
    cree_fenetre(WIDTH_WINDOW,HEIGHT_WINDOW)
    datamap = list(LEVEL_1)

    charlie = trouveCharlie(datamap)
    charlie = (charlie[0],charlie[1],0)
    renderCanvas(datamap)


    while True:
        start = time()
        direction = getDirection()
        if(direction[0] != 0 or direction[1] != 0):
            charlie = moveRockford(charlie, direction, datamap)
            renderCanvas(datamap)
        mise_a_jour()
        end = time()
