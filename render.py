from upemtk import *
from renderElements import *
import ui

###############################################################################


########################### Gestion de l'affichage ############################


def clearCanvas(color=None):
    """
    dessine l'arrière plan
    """
    efface_tout()
    rectangle(
        0,
        0,
        WIDTH_WINDOW,
        HEIGHT_WINDOW,
        color,
        color
    )

def initWindow():
    cree_fenetre(WIDTH_WINDOW, HEIGHT_WINDOW)


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


def renderCanvas(data, ID):
    """
    affiche l'ensemble des case de la current Map

    :param list curMap: map actuel sous forme de liste
    """
    ui.objects[ID]["squaresMap"]= [["." for x in range(CELL_NBX)] for y in range(CELL_NBY)]
    for y in range(1, len(data["map"])):
        for x in range(0, len(data["map"][y])):
            ui.objects[ID]["squaresMap"][y-1][x] = data["map"][y][x]