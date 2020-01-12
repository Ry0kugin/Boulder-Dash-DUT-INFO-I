from upemtk import texte, type_evenement, clic_x, clic_y, touche, donne_evenement, mise_a_jour, efface_tout, efface
from render import WIDTH_WINDOW, HEIGHT_WINDOW
from uiElements import *


######## Private IDs ########
# prompt
# prompt_1
# prompt_2
# prompt_3
# prompt_4


def setBackground(color):
    """
    Modifie la couleur d'arrière plan.
    :param string color: Couleur d'arrière plan
    """
    efface_tout()
    rectangle(0, 0, WIDTH_WINDOW, HEIGHT_WINDOW, color, color, 1)
    reDraw()


def clear():
    """
    Efface toute l'image.
    """
    efface_tout()


######## Routines ########

# Noms réservés pour ID:
# animation
def addRenderRoutine(ID, action, arguments=[]):
    """
    Ajoute une routine de rendu. C'est une fonction qui sera éxécutée à chaque rendu d'image.
    :param string ID: Identifiant de la routine
    :param function action: La fonction à éxécuter
    :param list arguments: Liste des arguments à passer à la fonction
    """
    global renderRoutines
    renderRoutines[ID]=(action, arguments)

def remRenderRoutine(ID):
    global renderRoutines
    """
    Supprime une routine de rendu.
    :param string ID: ID de la routine
    """
    if ID in renderRoutines:
        renderRoutines.pop(ID)
    else:
        print("UI Warning: cannot remove unknown render routine", ID)

def addLogicRoutine(ID, action, arguments=[]):
    """
    Ajoute une routine de logique. C'est une fonction qui sera éxécutée à chaque éxécution de la logique de l'interface.
    :param string ID: Identifiant de la routine
    :param function action: La fonction à éxécuter
    :param list arguments: Liste des arguments à passer à la fonction
    """
    global logicRoutines
    logicRoutines[ID]=(action, arguments)

def remLogicRoutine(ID):
    """
    Supprime une routine de logique.
    :param string ID: ID de la routine
    """
    global logicRoutines
    try:
        logicRoutines.pop(ID)
    except KeyError as e:
        print("UI Warning: cannot remove unknown logic routine", e)

######## Moteur logique ########

def checkClick(ID, pos):
    """
    Vérifie si l'objet donné a été ciblé par le clic.
    :param string ID: ID de l'objet
    :param tuple pos: tuple (x, y) de la position de la souris
    """
    global focus
    if objects[ID]["ax"] < pos[0] < objects[ID]["bx"] and objects[ID]["ay"] < pos[1] < objects[ID]["by"]:
        if objects[ID]["type"] == "Button":
            focus = None
            objects[ID]["action"](*objects[ID]["args"])
            return True
        elif objects[ID]["type"] == "textField":
            focus = {"ID": ID, "type": "textField"}
            return True
        elif objects[ID]["type"] == "Panel":
            focus = {"ID": ID, "type": "Panel"}
            return True
    return False


def logic(ev):
    """
    Exécute toutes les actions liées à la logique de l'interface, principalement la vérification des clics de la souris sur les boutons.
    :param tuple ev: Evenement de upemtk
    """
    global focus, exclusiveLayer
    type_ev = type_evenement(ev)
    for r in logicRoutines.values():
        r[0](*r[1])
    if type_ev == "ClicGauche":
        pos = (clic_x(ev), clic_y(ev))
        layers = set(range(len(renderQueue)-1, 0, -1))
        layers.add(0)
        if exclusiveLayer is None:
            for l in layers:
                for p in positions[l]:
                    if checkClick(p, pos):
                        return
        else:
            try:
                for p in positions[exclusiveLayer]:
                    if checkClick(p, pos):
                        return
            except KeyError as e:
                print("UI Warning: exclusive layer", e, "is non existent, defaulting to None")
                exclusiveLayer = None
                return
        focus = None
    elif focus is not None and type_ev == "Touche":
        if focus["type"] == "textField":
            key=touche(ev)
            if len(key) == 1 and key.isalnum():
                setObject(focus["ID"], {"text":objects[focus["ID"]]["text"]+key})
                #objects[focus["ID"]]["text"] += key
            elif key == "BackSpace":
                setObject(focus["ID"], {"text":objects[focus["ID"]]["text"][:-1]})
                #objects[focus["ID"]]["text"] = objects[focus["ID"]]["text"][:-1]
            elif key == "space":
                setObject(focus["ID"], {"text":objects[focus["ID"]]["text"]+" "})
                # objects[focus["ID"]]["text"] += " "


def render(text=None):
    """
    Exécute toutes les actions liées à au rendu de l'interface, principalement la gestion des objets à dessiner puis supprimer de la pile d'affichage.
    :param string text: texte affiché au dessus de toute l'interface en bas à gauche (utilisé pour le compteur d'images par seconde)
    """
    for r in renderRoutines.values():
        r[0](*r[1])
    buffer=getToRenderObjects()
    for l in buffer:
        for ID in l:
            if objects[ID]["tkObjects"]:
                for t in objects[ID]["tkObjects"]:
                    efface(t)
            drawObject(ID)
        l.clear()
    
    setToRenderObjects(buffer)
    efface("fps")
    if text:
        texte(0, HEIGHT_WINDOW, str(text) + " fps", "white", ancrage="sw", tag="fps")

######## Automation ########

condition = False
transaction = False


def actionPrompt(action, arguments, check, anyway, anywayArguments):
    global condition, transaction, exclusiveLayer
    condition = (transaction if check else True)
    if condition:
        if action:
            action(*arguments)
        if anyway:
            anyway(*anywayArguments)
        remRenderRoutine("promptRoutine")
        exclusiveLayer=None
        remObject("prompt")
        condition=False
        transaction=False


def checkPrompt(checker, checkerArguments):
    global transaction, focus
    if checker:
        transaction = checker(*checkerArguments)
        setObject("prompt_2", {"outlineColor":"Green" if transaction else "Red"})
        # objects["prompt_2"]["outlineColor"] = ("Green" if transaction else "Red")
    if not focus:
        focus = {"ID": "prompt", "type": "Panel"}
    elif focus["ID"] not in ("prompt","prompt_2"):
        focus = {"ID": "prompt", "type": "Panel"}
    


def newPrompt(message, buttonText, cancelable=True, checker=None, checkerArguments=[], cancel=None, cancelArguments=[],
              success=None, successArguments=[], anyway=None, anywayArguments=[]):
    global condition, transaction, exclusiveLayer, focus
    layer = len(renderQueue)
    childs = ["prompt_1", "prompt_2", "prompt_3"]
    addText(WIDTH_WINDOW / 2, HEIGHT_WINDOW * 1.6 / 4, ID=childs[0], text=message, isChild=True, layer=layer)
    addTextField(WIDTH_WINDOW / 2, HEIGHT_WINDOW * 2 / 4, ID=childs[1], outlineColor="white", isChild=True, layer=layer)
    addButton(WIDTH_WINDOW / 2, HEIGHT_WINDOW * 2.5 / 4, ID=childs[2], outlineColor="white", text=buttonText, textSize=18, action=actionPrompt, arguments=[success, successArguments, True, anyway, anywayArguments], layer=layer)
    if cancelable:
        childs.append("prompt_4")
        addButton(WIDTH_WINDOW / 2, HEIGHT_WINDOW * 3 / 4, ID=childs[3], outlineColor="white", text="Annuler", layer=layer, action=actionPrompt, arguments=[cancel, cancelArguments, False, anyway, anywayArguments])
    addPanel(WIDTH_WINDOW / 2, HEIGHT_WINDOW / 2, ID="prompt", width=WIDTH_WINDOW / 1.3, height=HEIGHT_WINDOW / 1.3, childs=childs, layer=layer)
    if not checker:
        transaction = True
    else:
        addRenderRoutine("promptRoutine", checkPrompt, [checker, checkerArguments])
    exclusiveLayer = layer
    
    focus = {"ID": "prompt", "type": "Panel"}



