from upemtk import *
from render import WIDTH_WINDOW, HEIGHT_WINDOW
from random import *
import ui
import render
import timer
from game import getFps, updateStats, updateTime

import time

################################## CONTSTANTS ##################################

GAME_STATUS = None
DIRECTIONS = ["Right", "Left", "Up", "Down"]

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

############################### Logique de jeu ################################

def getDirection(ev, debug=False):
    """
    renvoie la direction de rockford

    :param bool debug: active le mode debug

    """
    direction = 0
    type_ev=type_evenement(ev)
    t=None
    if type_ev=="Touche":
        t=touche(ev)
    elif debug:
        t=DIRECTIONS[randint(0,3)]
    else:
        return (0,0)
    if t==DIRECTIONS[0]:
        direction=(1,0)
    elif t==DIRECTIONS[1]:
        direction=(-1,0)
    elif t==DIRECTIONS[2]:
        direction=(0,-1)
    elif t==DIRECTIONS[3]:
        direction=(0,1)
    else:
        direction=(0,0)
    return direction

def findRockford(data):
    """
    trouve et renvoie Rockford, fonction appelée à chaque création de partie

    :param list curMap: map actuel sous forme de liste
    >>> findRockford([['150s', '1d'], ['B', 'R', 'G'], ['.', 'W', 'D']])
    [(1, 1), 0]
    """
    for i in range(1, len(data["map"])):
        for j in range(len(data["map"][i])):
            if data["map"][i][j] == "R":
                data["rockford"] = (j,i)
                data["diamonds"]["owned"] = 0

def findEnd(data):
    """
    trouve et renvoie Rockford, fonction appelée à chaque création de partie

    :param list curMap: map actuel sous forme de liste
    >>> findRockford([['150s', '1d'], ['B', 'R', 'G'], ['.', 'W', 'E']])
    [(2, 2), 0]
    """
    for i in range(1, len(data["map"])):
        for j in range(len(data["map"][i])):
            if data["map"][i][j] == "E" or data["map"][i][j] == "O":
                data["end"]["pos"] = (j,i)
                data["end"]["open"] = False

def findFallable(data):
    """
    Trouve et renvoie les fallables,
    fonction appelé à chaque création de partie

    :param list curMap: map actuel sous forme de liste
    >>> findFallable([['150s', '1d'], ['B', 'R', 'G'], ['.', 'W', 'D']])
    [(0, 1), (2, 2)]
    """
    timer.new(0.1, "fallings", permanent=True)
    data["fall"]["fallings"] = True
    data["fall"]["fallables"] = []
    for i in range(1, len(data["map"])):
        for j in range(len(data["map"][i])):
            if data["map"][i][j] == "B" or data["map"][i][j] == "D" or data["map"][i][j] == "X":
                data["fall"]["fallables"].append({"pos": (j,i), "falling": False})



def updateFallable(data, lastFa, newFa):
    """
    met à jour les fallables

    :param tuple lastFa: ancienne Position du Fallable
    :param tuple newFa: nouvelle Position du Fallable
    :param list fallables: liste de couple de fallable (abscisse, ordonnee)
    """
    for i,fa in enumerate(data["fall"]["fallables"]):
        if fa["pos"] == lastFa:
            data["fall"]["fallables"][i]["pos"] = newFa
            break



def getCell(data, coord):
    """
    Recupère la valeur de la cellule au ``coord`` spécifié

    :param tuple coord: couple (abscisse, ordonnee) de la case
    :param list curMap: map actuel sous forme de liste

    >>> getCell((2,1),[['150s', '1d'], ['B', 'R', 'G'], ['.', 'W', 'D']])
    'G'
    """
    #print(coord[1], coord[0])
    return data[coord[1]][coord[0]]



def setCell(curMap, coord, content):
    """
    met à jour la valeur de la cellule au ``coord`` spécifié par le ``content``

    :param tuple coord: couple (abscisse, ordonnee) de la case
    :param list curMap: map actuel sous forme de liste

    >>> getCell((2,1),[['150s', '1d'], ['B', 'R', 'G'], ['.', 'W', 'D']])
    'G'
    """
    curMap[coord[1]][coord[0]] = content



def setRockfordCell(curMap, lastPos, newPos, aim="R"):
    """
    met à jour la cellule de Rockford

    :param tuple lastFa: ancienne Position de Rockford
    :param tuple newFa: nouvelle Position de Rockford
    :param list curMap: map actuel sous forme de liste
    :param str aim: contenu de la cellule à remplacer
    """

    setCell(curMap, lastPos, ".")
    setCell(curMap, newPos, aim)



def changeRockfordPos(data, newPos, diamant=False):
    """
    change les positions de Rockford

    :param tuple newFa: nouvelle Position de Rockford
    :param list rockford: rockford
    :param bool diamant: diamant à ajouter

    >>> changeRockfordPos((2,3), [(1,1), 0], True)
    [(2, 3), 1]
    """

    data["rockford"] = newPos
    if diamant:
        data["diamonds"]["owned"] += 1



def moveRockford(data, direction):
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
        [['150s', '1d'],['Brender.update(data, "gameCanvas") ', 'R', 'G'], ['.', 'E', 'D']], [(0, 1), (2, 2)])
    [(2, 2), 1]

    >>> moveRockford([(1, 1), 0], (0,1), \
        [['150s', '1d'],['B', 'R', 'G'], ['.', 'E', 'D']], [(0, 1), (2, 2)])
    'win'



    (rockford), direction, (curMap), (fallables), endy
    """

    global GAME_STATUS

    aimCoord = sumTuple(data["rockford"], direction)

    aimCell = getCell(data["map"], aimCoord)

    enddoor = "O" if data["end"]["open"] else "E"

    if aimCell == ".":
        setRockfordCell(data["map"], data["rockford"], aimCoord)
        changeRockfordPos(data, aimCoord)

    elif aimCell == "G":
        setRockfordCell(data["map"], data["rockford"], aimCoord)
        changeRockfordPos(data, aimCoord)

    elif aimCell == "B":
        if direction[1] == 0: # deplacer boulet uniquement si direction lateral
            behindBoulder = sumTuple(aimCoord,direction)
            if(getCell(data["map"], behindBoulder) == "."):
                setRockfordCell(data["map"], data["rockford"], aimCoord)
                setCell(data["map"], behindBoulder, "B")
                updateFallable(data, aimCoord, behindBoulder)
                changeRockfordPos(data, aimCoord)

    elif aimCell == "D" or aimCell == "X":
        setRockfordCell(data["map"], data["rockford"], aimCoord)
        data["fall"]["fallables"].remove({"pos": aimCoord, "falling": False})
        changeRockfordPos(data, aimCoord, True)
        if aimCell =="D":
            timer.add("game", -10)
            data["score"] += 100
        else:
            timer.add("game", -1000)
            data["score"] += 10000
        if data["diamonds"]["owned"]==int(data["map"][0][1]):
            data["end"]["open"] = True
            enddoor = "O"
            setCell(data["map"], data["end"]["pos"], enddoor)

    elif aimCell == "O":
        setRockfordCell(data["map"], data["rockford"], aimCoord, aim=enddoor)
        GAME_STATUS = True
    




def updatePhysic(data): # Retirer rockford
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
    global GAME_STATUS
    if data["fall"]["fallings"] and timer.isOver("fallings"):
        nbFalling = 0
        for i, fa in enumerate(data["fall"]["fallables"]):
            faX = fa["pos"][0]
            faY = fa["pos"][1]
            if fa["falling"] and data["map"][faY+1][faX] == "R":
                setCell(data["map"], (faX, faY+1), data["map"][faY][faX])
                setCell(data["map"], (faX, faY), ".")
                GAME_STATUS = False
            if data["map"][faY+1][faX] == ".":
                setCell(data["map"], (faX, faY+1), data["map"][faY][faX])
                setCell(data["map"], (faX, faY), ".")
                data["fall"]["fallables"][i] = {"pos": (faX, faY+1), "falling": True}
                nbFalling += 1 

            elif (data["map"][faY][faX+1] == "." and data["map"][faY+1][faX+1] == ".") and (data["map"][faY-1][faX]!="D" and data["map"][faY-1][faX]!="B"):
                setCell(data["map"], (faX+1, faY), data["map"][faY][faX])
                setCell(data["map"], (faX, faY), ".")
                data["fall"]["fallables"][i] = {"pos": (faX+1, faY), "falling": True}
                nbFalling += 1

            elif (data["map"][faY][faX-1] == "." and data["map"][faY+1][faX-1] == ".") and (data["map"][faY-1][faX]!="D" and data["map"][faY-1][faX]!="B"):
                setCell(data["map"], (faX-1, faY), data["map"][faY][faX])
                setCell(data["map"], (faX, faY), ".")
                data["fall"]["fallables"][i] = {"pos": (faX-1, faY), "falling": True}
                nbFalling += 1
            else: 
                data["fall"]["fallables"][i]["falling"] = False
        if nbFalling > 0:
            print("before being restored", timer.getTimer("fallings", remain=True), timer.timers["fallings"]["progression"])
            timer.restore("fallings")
            print("after being restored", timer.getTimer("fallings", remain=True), timer.timers["fallings"]["progression"])     
            data["fall"]["fallings"] = True
        else:
            data["fall"]["fallings"] = False



def status(data):
    """
    verifie si la partie de Rockford est gagnée ou perdue

    :param list rockford: rockford
    """
    global GAME_STATUS
    if data["time"]["remain"] <= 0:
        GAME_STATUS = False
    if GAME_STATUS is not None:
        if GAME_STATUS:
            timer.new(1, ID="endScoreUpdate", permanent=True) # shadows the older timer /!\
            vector=data["time"]["remain"]*10
            currentTime=data["time"]["remain"]
            currentScore=data["score"]
            while not timer.isOver("endScoreUpdate"):
                currentVector=vector*(timer.timers["endScoreUpdate"]["progression"]/timer.timers["endScoreUpdate"]["size"])
                data["score"]=currentScore+int(currentVector)
                data["time"]["remain"]= currentTime+int(currentScore/10)
                
                updateStats(data["time"]["remain"], (data["diamonds"]["owned"], int(data["map"][0][1])), data["score"])
                updateTime()
                ui.render(getFps())
                mise_a_jour()
            data["score"]=currentScore+vector
            data["time"]["remain"]=0
            updateStats(data["time"]["remain"], (data["diamonds"]["owned"], int(data["map"][0][1])), data["score"])
            ui.render(getFps())

            
            endGame(True)
            if data["mode"] == "s":
                attente_clic_ou_touche()
            return True
        else:
            endGame(False)
            attente_clic_ou_touche()
            return False

def endGame(win):
    ui.addText(WIDTH_WINDOW / 4, HEIGHT_WINDOW / 2 - 24, text=("VOUS AVEZ GAGNE :)" if win else "VOUS AVEZ PERDU :("), textColor=("green" if win else"red"), ID="endText")
    ui.render(getFps())
    ui.remObject("endText")
    ui.render(getFps())

def updateGameStatus():
    global GAME_STATUS
    GAME_STATUS = None      


def quitter():
    """
    quitte la partie
    """
    exit("Merci d'avoir joué à notre jeu.\nRioven Studios")
