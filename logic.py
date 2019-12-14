from upemtk import *
from render import WIDTH_WINDOW, HEIGHT_WINDOW
import ui
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

def findEnd(curMap):
    """
    trouve et renvoie Rockford, fonction appelé à chaque création de partie

    :param list curMap: map actuel sous forme de liste
    >>> findRockford([['150s', '1d'], ['B', 'R', 'G'], ['.', 'W', 'E']])
    [(2, 2), 0]
    """
    for i in range(1, len(curMap)):
        for j in range(len(curMap[i])):
            if curMap[i][j] == "E":
                return [(j,i), False]

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



def moveRockford(rockford, direction, curMap, fallables, endy):
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
    print(endy)
    aimCoord = sumTuple(rockford[0], direction)

    aimCell = getCell(aimCoord, curMap)

    enddoor = "Eo" if endy[1] else "E"

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
        charlie = changeRockfordPos(aimCoord, rockford, True)
        print(rockford[1], int(curMap[0][1]), rockford[1]==int(curMap[0][1]))
        if rockford[1]==int(curMap[0][1]):
            endy[1] = True
            print("in",endy)
            enddoor = "Eo"
            setCell(endy[0], curMap, enddoor)
        print("out",endy)
        return charlie

    elif aimCell == "Eo":
        setRockfordCell(rockford[0], aimCoord, curMap, aim=enddoor)
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
    end = findEnd(curMap)
    fall = True
    return rockford, fallables, fall, end

def status(rockford, remainTime, diamonds):
    """
    verifie si la partie de Rockford est gagnée ou perdue

    :param list rockford: rockford
    """
    if rockford == "win":
        ui.levelWin()
        quitter()
    elif rockford == "lose":
        ui.levelLose()
        quitter()

def quitter():
    """
    quitte la partie
    """
    attente_clic_ou_touche()
    exit("Merci")
