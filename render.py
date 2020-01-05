from upemtk import *
from renderElements import *
import ui, timer

###############################################################################


########################### Gestion de l'affichage ############################

animations={}

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


def update(data, ID):
    """
    affiche l'ensemble des case de la current Map

    :param list curMap: map actuel sous forme de liste
    """

    ui.objects[ID]["squaresMap"] = data["map"][1::]

    # ui.objects[ID]["squaresMap"]= [["." for x in range(CELL_NBX)] for y in range(CELL_NBY)]
    # for y in range(1, len(data["map"])):
    #     for x in range(0, len(data["map"][y])):
    #         ui.objects[ID]["squaresMap"][y-1][x] = data["map"][y][x]

def animate(ID, time, parameters):
    # format de parameters:
    # "parametre": valeur
    global animations
    for p in parameters.keys():
        try:
            currentValue=ui.objects[ID][p]
        except KeyError as e:
            print("Render warning: (animate) cannot find parameter", e, "aborting animation")
            return
        if type(currentValue) is not (float or int):
            print("Render warning: (animate) cannot animate parameter", "'"+p[0]+"', aborting animation")
            return
        parameters[p]=(currentValue, parameters[p], (True if parameters[p]>currentValue else False))
    animations[ID]=parameters
    ui.addRenderRoutine(ID+"Animation", action=updateAnimation, arguments=[ID])
    timer.new(time, ID+"timer")

def updateAnimation(ID):
    percentage=timer.getTimer(ID+"timer")/timer.timers[ID+"timer"]["size"]
    for p in animations[ID].items():
        vector=abs(p[1][1]-p[1][0])
        ui.objects[ID][p[0]]=p[1][0]+((vector*percentage)*(1 if p[1][2] else -1))
    

def updateAnimations():
    global animations
    toDelete=set()
    for anim in animations.keys():
        if not timer.exists(anim+"timer"):
            toDelete.add(anim)
            ui.remRenderRoutine(anim+"Animation")
    for e in toDelete:
        animations.pop(e)
    print(animations)
