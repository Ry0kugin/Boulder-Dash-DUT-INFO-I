# -*- coding: utf-8 -*-

from upemtk import *
from time import *
from random import randint

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
CELL_NBX = 20
CELL_NBY = 10
CELL_SIZE = 32
HALF_SIZE = CELL_SIZE//2
WIDTH_WINDOW = CELL_SIZE * CELL_NBX
HEIGHT_WINDOW = CELL_SIZE * CELL_NBY
DIRECTIONS = ["Right", "Left", "Up", "Down"]
###########################################

########## Very Useful fonctions ##########

def sumTuple(a,b):
    tmp = []
    for i in range(2):
        tmp.append(a[i] + b[i])
    tmp.append(a[2])
    return tuple(tmp) 

########################################### 

def loadLevel(level):
    level = level.split("\n")
    levelLst = []
    # add option
    levelLst.append(level[0].split())
    # add map
    for i in range(1,len(level)):
        levelLst.append(list(level[i]))
    return levelLst

def getDirection(debug=False):
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

def drawBackground():
    rectangle(
        0,
        0,
        WIDTH_WINDOW,
        HEIGHT_WINDOW,
        'black',
        'black'        
    )

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

def drawBoulder(coord, dead=False):
    if dead:
        rectangle(
            coord[0],
            coord[1],
            coord[0]+CELL_SIZE,
            coord[1]+CELL_SIZE,
            '#f00',
            '#f00'
        )
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
    drawBackground()
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

def foundFallable(curMap):
    fallables = []
    for i in range(1, len(curMap)):
        for j in range(len(curMap[i])):
            if curMap[i][j] == "B" or curMap[i][j] == "D":
                fallables.append((j,i))
    print("fallables: ",fallables)
    return fallables

def updateFallable(lastFa, newFa, fallables):
    lastFa = lastFa[0], lastFa[1]
    newFa = newFa[0], newFa[1]
    for i,fa in enumerate(fallables):
        if fa == lastFa:
            fallables[i] = newFa
            break



def getCell(coord, curMap):
    return curMap[coord[1]][coord[0]]

def setCell(coord, curMap, content):
    curMap[coord[1]][coord[0]] = content

def setRockfordCell(lastPos, newPos, curMap, aim="R"):
    setCell(lastPos, curMap, ".") 
    setCell(newPos, curMap, aim)

def moveRockford(rockford, direction, curMap, fallables):
    print(rockford)
    print(fallables)
    aimCoord = sumTuple(rockford, direction)

    aimCell = getCell(aimCoord, curMap)
    
    if aimCell == ".":
        print("Hey, it's a void")
        setRockfordCell(rockford, aimCoord, curMap)
        return aimCoord
    elif aimCell == "G":
        print("Dirty dancing!")
        setRockfordCell(rockford, aimCoord, curMap)
        return aimCoord
    elif aimCell == "B":
        if direction[1] == 0: # deplacer boulet uniquement si direction lateral
            behindBoulder = sumTuple(aimCoord,direction)
            if(getCell(behindBoulder, curMap) == "."):
                print("BOULDER DASH")
                setRockfordCell(rockford, aimCoord, curMap)
                setCell(behindBoulder, curMap, "B")
                updateFallable(aimCoord, behindBoulder, fallables)
                return aimCoord
    elif aimCell == "D":
        print("DIAMOND")
        setRockfordCell(rockford, aimCoord, curMap)
        fallables.remove((aimCoord[0], aimCoord[1]))
        return aimCoord[0], aimCoord[1], aimCoord[2]+1
    elif aimCell == "E":
        print("BRAVO!")
        setRockfordCell(rockford, aimCoord, curMap, aim="E")
        return "win"
    else:
        print("Useless...", aimCell, getCell(rockford,curMap))
    return rockford
    
def updatePhysic(fallables, fall, charlie, curMap):
    """
    met a jour la physique et return vrai
    si les fallables peuvent encore tomber
    """
    print("FALL")
    print(fallables)
    fallingNb = 0
    for i, fa in enumerate(fallables):
        faX = fa[0]
        faY = fa[1]
        print(fall, curMap[faY+1][faX])
        setC = False
        if fall and curMap[faY+1][faX] == "R":
            setC = True
            charlie = "lose"

        if curMap[faY+1][faX] == ".":
            setC = True
            fallables[i] = (faX, faY+1)
            fallingNb+=1
        
        if setC:
            setCell((faX, faY+1), curMap, curMap[faY][faX])
            setCell((faX, faY), curMap, ".")

    fall = (True if fallingNb else False)
        
    print("falling : ", fall)
    return fall, charlie

def start(curMap):
    charlie = trouveCharlie(curMap)  # refactoring
    charlie = (charlie[0],charlie[1],0)
    fallables = foundFallable(curMap)
    fall = True
    renderCanvas(curMap)
    return charlie, fallables, fall

def levelWin():
    texte(WIDTH_WINDOW/4, HEIGHT_WINDOW/2-24, "BRAVO!", "green")

def levelLose():
    texte(WIDTH_WINDOW/4, HEIGHT_WINDOW/2-12, "PERDU...", "red")

def status(charlie):
    if charlie == "win":
        levelWin()
        quitter()
    elif charlie == "lose":
        levelLose()
        quitter()

def quitter():
    attente_clic_ou_touche()
    exit("Merci")

def debugMode():
    pass

if __name__ == '__main__':
    cree_fenetre(WIDTH_WINDOW,HEIGHT_WINDOW)
    LEVEL_1 = "150s 1d\nWWWWWWWWWWWWWW\nWGGGGGG.GGDGBW\nWGBRBGGGGGG.GW\nWGGGGGGGGGG.GW\nWBGBBGGGGGGGGW\nWGG.BGGGGGGGGW\nWGGG.GG.GGGGEW\nWWWWWWWWWWWWWW"
    currentMap = loadLevel(LEVEL_1)

    charlie, fallables, fall = start(currentMap)
    fall = True
    debug = False

    while True:
        direction = getDirection(debug)
        if direction == "reset":
            currentMap = loadLevel(LEVEL_1)
            charlie, fallables, fall = start(currentMap)
            renderCanvas(currentMap)
            continue
        if direction == "debug":
            debug = (False if debug else True)
            print ("DEBUG ACTIVATED" if debug else "DEBUG DEACTIVATED")
            continue
        if(direction[0] != 0 or direction[1] != 0):
            charlie = moveRockford(charlie, direction, currentMap, fallables)
            fall, charlie = updatePhysic(fallables, False, charlie, currentMap)
        if fall:
            fall, charlie = updatePhysic(fallables, fall, charlie, currentMap)
        renderCanvas(currentMap)
        mise_a_jour()
        status(charlie)
        