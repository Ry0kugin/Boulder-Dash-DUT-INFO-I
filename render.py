from upemtk import *

###############################################################################


########################### Gestion de l'affichage ############################

CELL_NBX = 20
CELL_NBY = 10
CELL_SIZE = 42
HALF_SIZE = CELL_SIZE // 2
WIDTH_WINDOW = CELL_SIZE * CELL_NBX
HEIGHT_WINDOW = CELL_SIZE * CELL_NBY


def initWindow():
    cree_fenetre(WIDTH_WINDOW, HEIGHT_WINDOW)


def drawBackground():
    """
    dessine l'arrière plan
    """
    rectangle(
        0,
        0,
        WIDTH_WINDOW,
        HEIGHT_WINDOW,
        'red',
        'red'
    )


def drawVoid(coord):
    """
    dessine une case vide

    :param tuple coord: couple (abscisse, ordonnee) de la case
    """
    rectangle(
        coord[0],
        coord[1],
        coord[0] + CELL_SIZE,
        coord[1] + CELL_SIZE,
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
        coord[0] + CELL_SIZE,
        coord[1] + CELL_SIZE,
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
        coord[0] + CELL_SIZE,
        coord[1] + CELL_SIZE,
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
        coord[0] + HALF_SIZE,
        coord[1] + HALF_SIZE,
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
        (coord[0] + HALF_SIZE, coord[1]),
        (coord[0], coord[1] + HALF_SIZE),
        (coord[0] + HALF_SIZE, coord[1] + CELL_SIZE),
        (coord[0] + CELL_SIZE, coord[1] + HALF_SIZE)
    ]
    polygone(points, '#09f', '#0ff')


def drawEnd(coord, finished=False):
    """
    dessine une case fin
    rouge si open false
    vert si open true

    :param tuple coord: couple (abscisse, ordonnee) de la case
    """
    colors = (("#0a0", "#0f0") if finished else ("#a00", "#f00"))
    rectangle(
        coord[0],
        coord[1],
        coord[0] + CELL_SIZE,
        coord[1] + CELL_SIZE,
        colors[0],
        colors[0]
    )
    cercle(
        coord[0] + HALF_SIZE,
        coord[1] + HALF_SIZE,
        HALF_SIZE // 2,
        colors[1],
        colors[1]
    )


def drawRockford(coord):
    """
    dessine une case Rockford

    :param tuple coord: couple (abscisse, ordonnee) de la case
    """
    drawVoid(coord)
    cercle(
        coord[0] + HALF_SIZE,
        coord[1] + HALF_SIZE // 2,
        HALF_SIZE // 2,
        '#c80',
        '#f41'
    )
    rectangle(
        coord[0] + HALF_SIZE // 2,
        coord[1] + HALF_SIZE,
        coord[0] + HALF_SIZE * 1.5,
        coord[1] + CELL_SIZE,
        '#c80',
        '#f41'
    )


#  dictionnaire permettant d'appeler les fonctions de dessins
#  à partir du code issu de la génération d'une carte
renderCase = {
    '.': (lambda x: drawVoid(x)),
    'W': (lambda x: drawWall(x)),
    'G': (lambda x: drawGrass(x)),
    'B': (lambda x: drawBoulder(x)),
    'D': (lambda x: drawDiamond(x)),
    'E': (lambda x: drawEnd(x)),
    'R': (lambda x: drawRockford(x)),
    'O': (lambda x: drawEnd(x, True))
}


def renderCanvas(curMap, rockford):
    """
    affiche l'ensemble des case de la current Map

    :param list curMap: map actuel sous forme de liste
    """
    for y in range(1, len(curMap)):
        for x in range(0, len(curMap[y])):
            x1 = x * CELL_SIZE
            y1 = y * CELL_SIZE
            renderCase[curMap[y][x]]((x1, y1))
