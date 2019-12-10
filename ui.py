from upemtk import texte
from render import WIDTH_WINDOW, HEIGHT_WINDOW

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