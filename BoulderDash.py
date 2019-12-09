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
###############################################################################

############################ Very Useful fonctions ############################

def sumTuple(a,b):
    """
    renvoie la somme des tuples a et b
    
    :param tuple a: couple (abscisse, ordonnee)
    :param tuple b: couleur de trait (défaut 'black')
    :return: renvoie la somme des tuples a et b

    >>> sumTuple((1,2),(2,4))
    (3, 6)
    """
    tmp = []
    for i in range(2):
        tmp.append(a[i] + b[i])
    return tuple(tmp)

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


########################### Gestion de l'affichage ############################



def drawBackground():
    """
    dessine l'arrière plan
    """
    rectangle(
        0,
        0,
        WIDTH_WINDOW,
        HEIGHT_WINDOW,
        'black',
        'black'        
    )



def drawVoid(coord):
    """
    dessine une case vide

    :param tuple coord: couple (abscisse, ordonnee) de la case
    """
    rectangle(
        coord[0],
        coord[1],
        coord[0]+CELL_SIZE,
        coord[1]+CELL_SIZE,
        '#000',
        '#000'
    )



def drawWall(coord):
    """
    dessine une case mur

    :param tuple coord: couple (abscisse, ordonnee) de la case
    """
    rectangle(
        coord[0],
        coord[1],
        coord[0]+CELL_SIZE,
        coord[1]+CELL_SIZE,
        '#666',
        '#666'
    )



def drawGrass(coord):
    """
    dessine une case terre

    :param tuple coord: couple (abscisse, ordonnee) de la case
    """
    rectangle(
        coord[0],
        coord[1],
        coord[0]+CELL_SIZE,
        coord[1]+CELL_SIZE,
        '#850',
        '#850'
    )



def drawBoulder(coord):
    """
    dessine une case boulet

    :param tuple coord: couple (abscisse, ordonnee) de la case
    """
    drawVoid(coord)
    cercle(
        coord[0]+HALF_SIZE,
        coord[1]+HALF_SIZE,
        HALF_SIZE,
        '#888',
        '#aaa'
    )



def drawDiamond(coord):
    """
    dessine une case diamant

    :param tuple coord: couple (abscisse, ordonnee) de la case
    """
    drawVoid(coord)
    points = [
        (coord[0]+HALF_SIZE, coord[1]),
        (coord[0], coord[1]+HALF_SIZE),
        (coord[0]+HALF_SIZE, coord[1]+CELL_SIZE),
        (coord[0]+CELL_SIZE, coord[1]+HALF_SIZE)
    ]
    polygone(points,'#09f','#0ff')



def drawEnd(coord):
    """
    dessine une case fin

    :param tuple coord: couple (abscisse, ordonnee) de la case
    """
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
    """
    dessine une case Rockford

    :param tuple coord: couple (abscisse, ordonnee) de la case
    """
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


# dictionnaire permettant d'appeler les fonctions de dessins
# à partir du code issu de la génération d'une carte
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
    """
    affiche l'ensemble des case de la current Map

    :param list curMap: map actuel sous forme de liste
    """
    efface_tout()
    drawBackground()
    for y in range(1,len(curMap)):
        for x in range(0, len(curMap[y])):
            x1 = x*CELL_SIZE
            y1 = y*CELL_SIZE
            renderCase[curMap[y][x]]((x1,y1))

###############################################################################


############################### Logique de jeu ################################

def findRockford(curMap):
    """
    trouve et renvoie Rockford, fonction appelé à chaque création de partie

    :param list curMap: map actuel sous forme de liste
    >>> findRockford([['150s', '1d'], ['B', 'R', 'G'], ['.', 'W', 'D']])
    [(1, 1), 0]
    """
    for i in range(1, len(curMap)):
        for j in range(len(curMap[i])):
            if curMap[i][j] == "R":
                return [(j,i), 0]



def findFallable(curMap):
    """
    Trouve et renvoie les fallables,
    fonction appelé à chaque création de partie

    :param list curMap: map actuel sous forme de liste
    >>> findFallable([['150s', '1d'], ['B', 'R', 'G'], ['.', 'W', 'D']])
    [(0, 1), (2, 2)]
    """
    fallables = []
    for i in range(1, len(curMap)):
        for j in range(len(curMap[i])):
            if curMap[i][j] == "B" or curMap[i][j] == "D":
                fallables.append((j,i))
    return fallables



def updateFallable(lastFa, newFa, fallables):
    """
    met à jour les fallables

    :param tuple lastFa: ancienne Position du Fallable
    :param tuple newFa: nouvelle Position du Fallable
    :param list fallables: liste de couple de fallable (abscisse, ordonnee)
    """
    for i,fa in enumerate(fallables):
        if fa == lastFa:
            fallables[i] = newFa
            break



def getCell(coord, curMap):
    """
    Recupère la valeur de la cellule au ``coord`` spécifié
    
    :param tuple coord: couple (abscisse, ordonnee) de la case
    :param list curMap: map actuel sous forme de liste

    >>> getCell((2,1),[['150s', '1d'], ['B', 'R', 'G'], ['.', 'W', 'D']])
    'G'
    """
    return curMap[coord[1]][coord[0]]



def setCell(coord, curMap, content):
    """
    met à jour la valeur de la cellule au ``coord`` spécifié par le ``content``
    
    :param tuple coord: couple (abscisse, ordonnee) de la case
    :param list curMap: map actuel sous forme de liste

    >>> getCell((2,1),[['150s', '1d'], ['B', 'R', 'G'], ['.', 'W', 'D']])
    'G'
    """
    curMap[coord[1]][coord[0]] = content



def setRockfordCell(lastPos, newPos, curMap, aim="R"):
    """
    met à jour la cellule de Rockford

    :param tuple lastFa: ancienne Position de Rockford
    :param tuple newFa: nouvelle Position de Rockford
    :param list curMap: map actuel sous forme de liste
    :param str aim: contenu de la cellule à remplacer
    """

    setCell(lastPos, curMap, ".") 
    setCell(newPos, curMap, aim)



def changeRockfordPos(newPos, rockford, diamant=False):
    """
    change les positions de Rockford
    
    :param tuple newFa: nouvelle Position de Rockford
    :param list rockford: rockford
    :param bool diamant: diamant à ajouter
    
    >>> changeRockfordPos((2,3), [(1,1), 0], True)
    [(2, 3), 1]
    """

    rockford[0] = newPos
    if diamant:
        rockford[1] += 1
    return rockford



def moveRockford(rockford, direction, curMap, fallables):
    """
    deplace rockford

    :param list rockford: rockford
    :param list rockford: couple direction (abscisse, ordonnee)
    :param list curMap: map actuel sous forme de liste
    :param list fallables: liste de couple de fallable (abscisse, ordonnee)

    >>> moveRockford([(1, 1), 0], (1,0), \
        [['150s', '1d'],['B', 'R', 'G'], ['.', 'E', 'D']], [(0, 1), (2, 2)])
    [(2, 1), 0]

    >>> moveRockford([(1, 1), 0], (1,1), \
        [['150s', '1d'],['B', 'R', 'G'], ['.', 'E', 'D']], [(0, 1), (2, 2)])
    [(2, 2), 1]

    >>> moveRockford([(1, 1), 0], (0,1), \
        [['150s', '1d'],['B', 'R', 'G'], ['.', 'E', 'D']], [(0, 1), (2, 2)])
    'win'
    """

    aimCoord = sumTuple(rockford[0], direction)

    aimCell = getCell(aimCoord, curMap)
     
    if aimCell == ".":
        setRockfordCell(rockford[0], aimCoord, curMap)
        return changeRockfordPos(aimCoord, rockford) 
    
    elif aimCell == "G":
        setRockfordCell(rockford[0], aimCoord, curMap)
        return changeRockfordPos(aimCoord, rockford)
    
    elif aimCell == "B":
        if direction[1] == 0: # deplacer boulet uniquement si direction lateral
            behindBoulder = sumTuple(aimCoord,direction)
            if(getCell(behindBoulder, curMap) == "."):
                setRockfordCell(rockford[0], aimCoord, curMap)
                setCell(behindBoulder, curMap, "B")
                updateFallable(aimCoord, behindBoulder, fallables)
                return changeRockfordPos(aimCoord, rockford)
    
    elif aimCell == "D":
        setRockfordCell(rockford[0], aimCoord, curMap)
        fallables.remove(aimCoord)
        return changeRockfordPos(aimCoord, rockford, True)
    
    elif aimCell == "E":
        setRockfordCell(rockford[0], aimCoord, curMap, aim="E")
        return "win"
    
    return rockford
    


def updatePhysic(fallables, fall, rockford, curMap):
    """
    met a jour la physique et return vrai
    si les fallables peuvent encore tomber

    :param list fallables: liste de couple de fallable (abscisse, ordonnee)
    :param bool fall: fallable tombe encore
    :param list rockford: rockford
    :param list curMap: map actuel sous forme de liste

    >>> updatePhysic([(0, 1), (2, 2)], False, \
        [(1, 1), 0], [['150s', '1d'],['B', 'R', 'G'], ['.', 'E', 'D'], ['W', 'W', 'W']])
    (True, [(1, 1), 0])
    >>> updatePhysic([(0, 1), (2, 2), (1, 1)], True, \
        [(1, 1), 0], [['150s', '1d'],['B', 'B', 'G'], ['.', 'R', 'D'], ['W', 'W', 'W']])
    (True, 'lose')
    """

    fallingNb = 0
    for i, fa in enumerate(fallables):
        faX = fa[0]
        faY = fa[1]
        setC = False
        if fall and curMap[faY+1][faX] == "R":
            setC = True
            rockford = "lose"

        if curMap[faY+1][faX] == ".":
            setC = True
            fallables[i] = (faX, faY+1)
            fallingNb+=1
        
        if setC:
            setCell((faX, faY+1), curMap, curMap[faY][faX])
            setCell((faX, faY), curMap, ".")

    fall = (True if fallingNb else False)
        
    return fall, rockford



def start(curMap):
    """
    initialise une partie

    :param list curMap: map actuel sous forme de liste

    >>> start([['150s', '1d'],['B', 'R', 'G'], ['.', 'E', 'D'], ['W', 'W', 'W']])
    ([(1, 1), 0], [(0, 1), (2, 2)], True)
    """

    rockford = findRockford(curMap)  # refactoring
    fallables = findFallable(curMap)
    fall = True
    return rockford, fallables, fall



def levelWin():
    """
    affiche Victoire
    """
    texte(WIDTH_WINDOW/4, HEIGHT_WINDOW/2-24, "BRAVO!", "green")



def levelLose():
    """
    affiche Défaite
    """

    texte(WIDTH_WINDOW/4, HEIGHT_WINDOW/2-12, "PERDU...", "red")


def status(rockford):
    """
    verifie si la partie de Rockford est gagné ou perdu

    :param list rockford: rockford
    """

    if charlie == "win":
        levelWin()
        quitter()
    elif charlie == "lose":
        levelLose()
        quitter()



def quitter():
    """
    quitte la partie
    """
    attente_clic_ou_touche()
    exit("Merci")

###############################################################################


###############################################################################

if __name__ == '__main__':
    cree_fenetre(WIDTH_WINDOW,HEIGHT_WINDOW)
    
    LEVEL_1 = "150s 1d\nWWWWWWWWWWWWWW\nWGGGGGG.GGDGBW\nWGBRBGGGGGG.GW\n\
WGGGGGGGGGG.GW\nWBGBBGGGGGGGGW\nWGG.BGGGGGGGGW\n\
WGGG.GG.GGGGEW\nWWWWWWWWWWWWWW"

    currentMap = loadLevel(LEVEL_1)

    charlie, fallables, fall = start(currentMap)
    renderCanvas(currentMap)
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

###############################################################################

