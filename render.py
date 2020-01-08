from upemtk import *
from renderElements import *
import ui, timer

###############################################################################


########################### Gestion de l'affichage ############################


def initWindow():
    cree_fenetre(WIDTH_WINDOW, HEIGHT_WINDOW)


def clearCanvas(color="black", img=None):
    """
    dessine l'arrière plan
    """
    efface_tout()
    if img:
        image(0, 0, "img/"+img, ancrage='n')
    else:
        color = color
        rectangle(
            0,
            0,
            WIDTH_WINDOW,
            HEIGHT_WINDOW,
            color,
            color
        ) 


def update(data, ID):
    """
    affiche l'ensemble des case de la carte dans data sur le gameCanvas spécifié.

    :param dict data: map actuelle dans un dictionnaire à la clé "map"
    :param string ID: ID dans ui.objects de l'objet de type gameCanvas sur lequel afficher
    """
    ui.setObject(ID, {"squaresMap": data["map"][1::]}, forceUpdate=True)
    #ui.objects[ID]["squaresMap"] = data["map"][1::]

    # ui.objects[ID]["squaresMap"]= [["." for x in range(CELL_NBX)] for y in range(CELL_NBY)]
    # for y in range(1, len(data["map"])):
    #     for x in range(0, len(data["map"][y])):
    #         ui.objects[ID]["squaresMap"][y-1][x] = data["map"][y][x]

