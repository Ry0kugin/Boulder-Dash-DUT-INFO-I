from upemtk import *

CELL_NBX = 20
CELL_NBY = 10
CELL_SIZE = 34
HALF_SIZE = CELL_SIZE // 2
# WIDTH_WINDOW = CELL_SIZE * CELL_NBX
# HEIGHT_WINDOW = CELL_SIZE * CELL_NBY
WIDTH_WINDOW = 950
HEIGHT_WINDOW = 500


def drawVoid(coord, cellSize):
    """
    dessine une case vide

    :param tuple coord: couple (abscisse, ordonnee) de la case
    """
    return (
        rectangle(
            coord[0],
            coord[1],
            coord[0] + cellSize,
            coord[1] + cellSize,
            '#000',
            '#000'
        ),
    )


def drawWall(coord, cellSize):
    """
    dessine une case mur

    :param tuple coord: couple (abscisse, ordonnee) de la case
    """
    return (
        rectangle(
            coord[0],
            coord[1],
            coord[0] + cellSize,
            coord[1] + cellSize,
            '#666',
            '#666'
        ),
    )


def drawGrass(coord, cellSize):
    """
    dessine une case terre

    :param tuple coord: couple (abscisse, ordonnee) de la case
    """
    return (
        rectangle(
            coord[0],
            coord[1],
            coord[0] + cellSize,
            coord[1] + cellSize,
            '#850',
            '#850'
        ),
    )


def drawBoulder(coord, cellSize):
    """
    dessine une case boulet

    :param tuple coord: couple (abscisse, ordonnee) de la case
    """
    halfSize=int(cellSize/2)
    st=set(drawVoid(coord, cellSize))
    st.add(cercle(
        coord[0] + halfSize,
        coord[1] + halfSize,
        halfSize,
        '#888',
        '#aaa'
    ))
    return tuple(st)


def drawDiamond(coord, cellSize):
    """
    dessine une case diamant

    :param tuple coord: couple (abscisse, ordonnee) de la case
    """
    halfSize=int(cellSize/2)
    st=set(drawVoid(coord, cellSize))
    points = [
        (coord[0] + halfSize, coord[1]),
        (coord[0], coord[1] + halfSize),
        (coord[0] + halfSize, coord[1] + cellSize),
        (coord[0] + cellSize, coord[1] + halfSize)
    ]
    st.add(polygone(points, '#09f', '#0ff'))
    return tuple(st)

def drawRarestOrd(coord, cellSize):
    halfSize=int(cellSize/2)
    st=set(drawVoid(coord, cellSize))
    pointsOut = [
        (coord[0] + halfSize, coord[1]), # up
        (coord[0], coord[1] + halfSize), # left
        (coord[0] + halfSize, coord[1] + cellSize), # bottom
        (coord[0] + cellSize, coord[1] + halfSize) #right
    ]
    pointsIn = [
        (coord[0] + halfSize, coord[1] + halfSize/3),
        (coord[0] + halfSize/3, coord[1] + halfSize),
        (coord[0] + halfSize, coord[1] + cellSize - halfSize/3),
        (coord[0] + cellSize - halfSize/3, coord[1] + halfSize)
    ]
    pointsCore = [
        (coord[0] + halfSize, coord[1] + halfSize/1.5),
        (coord[0] + halfSize/1.5, coord[1] + halfSize),
        (coord[0] + halfSize, coord[1] + cellSize - halfSize/1.5),
        (coord[0] + cellSize - halfSize/1.5, coord[1] + halfSize)
    ]
    st.add(polygone(pointsOut, '#090', '#0f0'))
    st.add(polygone(pointsIn, '#990', '#ff0'))
    st.add(polygone(pointsCore, '#900', '#f00'))
    return tuple(st)

def drawOpened(coord, cellSize):
    return drawEnd(coord, cellSize, True)

def drawClosed(coord, cellSize):
    return drawEnd(coord, cellSize, False)

def drawEnd(coord, cellSize, finished=False):
    """
    dessine une case fin
    rouge si open false
    vert si open true

    :param tuple coord: couple (abscisse, ordonnee) de la case
    """
    halfSize=int(cellSize/2)
    colors = (("#0a0", "#0f0") if finished else ("#a00", "#f00"))
    return (rectangle(
        coord[0],
        coord[1],
        coord[0] + cellSize,
        coord[1] + cellSize,
        colors[0],
        colors[0]
    ),
    cercle(
        coord[0] + halfSize,
        coord[1] + halfSize,
        halfSize // 2,
        colors[1],
        colors[1]
    ))


def drawRockford(coord, cellSize):
    """
    dessine une case Rockford

    :param tuple coord: couple (abscisse, ordonnee) de la case
    """
    halfSize=int(cellSize/2)
    lst=list(drawVoid(coord, cellSize))
    lst.extend((cercle(
        coord[0] + halfSize,
        coord[1] + halfSize // 2,
        halfSize // 2,
        '#c80',
        '#f41'
    ),
    rectangle(
        coord[0] + halfSize // 2,
        coord[1] + halfSize,
        coord[0] + halfSize * 1.5,
        coord[1] + cellSize,
        '#c80',
        '#f41'
    )))
    return tuple(lst)

def drawSelected(coord, cellSize, color):
    return (
        rectangle(
            coord[0],
            coord[1],
            coord[0] + cellSize,
            coord[1] + cellSize,
            color,
            epaisseur=4
        )
    )


#  dictionnaire permettant d'appeler les fonctions de dessins
#  à partir du code issu de la génération d'une carte
renderCase = {
    '.': drawVoid,
    'W': drawWall,
    'G': drawGrass,
    'B': drawBoulder,
    'D': drawDiamond,
    'X': drawRarestOrd,
    'E': drawClosed,
    'R': drawRockford,
    'O': drawOpened,
    'S': drawSelected
}