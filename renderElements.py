from upemtk import *

CELL_NBX = 20
CELL_NBY = 10
CELL_SIZE = 34
HALF_SIZE = CELL_SIZE // 2
# WIDTH_WINDOW = CELL_SIZE * CELL_NBX
# HEIGHT_WINDOW = CELL_SIZE * CELL_NBY
WIDTH_WINDOW = 900
HEIGHT_WINDOW = 500

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

def drawVoid(coord):
    """
    dessine une case vide

    :param tuple coord: couple (abscisse, ordonnee) de la case
    """
    return (
        rectangle(
            coord[0],
            coord[1],
            coord[0] + CELL_SIZE,
            coord[1] + CELL_SIZE,
            '#000',
            '#000'
        ),
    )


def drawWall(coord):
    """
    dessine une case mur

    :param tuple coord: couple (abscisse, ordonnee) de la case
    """
    return (
        rectangle(
            coord[0],
            coord[1],
            coord[0] + CELL_SIZE,
            coord[1] + CELL_SIZE,
            '#666',
            '#666'
        ),
    )


def drawGrass(coord):
    """
    dessine une case terre

    :param tuple coord: couple (abscisse, ordonnee) de la case
    """
    return (
        rectangle(
            coord[0],
            coord[1],
            coord[0] + CELL_SIZE,
            coord[1] + CELL_SIZE,
            '#850',
            '#850'
        ),
    )


def drawBoulder(coord):
    """
    dessine une case boulet

    :param tuple coord: couple (abscisse, ordonnee) de la case
    """
    st=set(drawVoid(coord))
    st.add(cercle(
        coord[0] + HALF_SIZE,
        coord[1] + HALF_SIZE,
        HALF_SIZE,
        '#888',
        '#aaa'
    ))
    return tuple(st)


def drawDiamond(coord):
    """
    dessine une case diamant

    :param tuple coord: couple (abscisse, ordonnee) de la case
    """
    st=set(drawVoid(coord))
    points = [
        (coord[0] + HALF_SIZE, coord[1]),
        (coord[0], coord[1] + HALF_SIZE),
        (coord[0] + HALF_SIZE, coord[1] + CELL_SIZE),
        (coord[0] + CELL_SIZE, coord[1] + HALF_SIZE)
    ]
    st.add(polygone(points, '#09f', '#0ff'))
    return tuple(st)


def drawEnd(coord, finished=False):
    """
    dessine une case fin
    rouge si open false
    vert si open true

    :param tuple coord: couple (abscisse, ordonnee) de la case
    """
    colors = (("#0a0", "#0f0") if finished else ("#a00", "#f00"))
    return (rectangle(
        coord[0],
        coord[1],
        coord[0] + CELL_SIZE,
        coord[1] + CELL_SIZE,
        colors[0],
        colors[0]
    ),
    cercle(
        coord[0] + HALF_SIZE,
        coord[1] + HALF_SIZE,
        HALF_SIZE // 2,
        colors[1],
        colors[1]
    ))


def drawRockford(coord):
    """
    dessine une case Rockford

    :param tuple coord: couple (abscisse, ordonnee) de la case
    """
    lst=list(drawVoid(coord))
    lst.extend((cercle(
        coord[0] + HALF_SIZE,
        coord[1] + HALF_SIZE // 2,
        HALF_SIZE // 2,
        '#c80',
        '#f41'
    ),
    rectangle(
        coord[0] + HALF_SIZE // 2,
        coord[1] + HALF_SIZE,
        coord[0] + HALF_SIZE * 1.5,
        coord[1] + CELL_SIZE,
        '#c80',
        '#f41'
    )))
    return tuple(lst)