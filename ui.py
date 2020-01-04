from upemtk import texte, type_evenement, clic_x, clic_y, touche, donne_evenement, mise_a_jour, efface_tout
from render import WIDTH_WINDOW, HEIGHT_WINDOW
from uiElements import *


######## Private IDs ########
# prompt
# prompt_1
# prompt_2
# prompt_3
# prompt_4

def setUIEvenement(ev):
    global evenement
    evenement = ev


def getUIEvenement():
    global evenement
    tmp = evenement
    evenement = None
    return tmp


def levelWin():
    """
    affiche Victoire
    """
    texte(WIDTH_WINDOW / 4, HEIGHT_WINDOW / 2 - 24, "YOU WIN !", "green")


def levelLose():
    """
    affiche Défaite
    """
    texte(WIDTH_WINDOW / 4, HEIGHT_WINDOW / 2 - 12, "GAME OVER", "red")


######## Automation ########
condition = False
transaction = False


def actionPrompt(action, arguments, check):
    global condition, transaction, exclusiveLayer
    condition = (transaction if check else True)
    if condition:
        if action:
            action(*arguments)
        remRenderRoutine("promptRoutine")
        exclusiveLayer=None
        remObject("prompt")
        condition=False
        transaction=False

def checkPrompt(checker, checkerArguments):
    global transaction
    transaction = checker(*checkerArguments)
    objects["prompt_2"]["outlineColor"] = ("Green" if transaction else "Red")

def newPrompt(message, buttonText, cancelable=True, checker=None, checkerArguments=[], cancel=None, cancelArguments=[],
              success=None, successArguments=[]):
    global condition, transaction, exclusiveLayer
    layer = len(renderQueue)
    childs = ["prompt_1", "prompt_2", "prompt_3"]
    addText(WIDTH_WINDOW / 2, HEIGHT_WINDOW * 1.6 / 4, ID=childs[0], text=message, textAnchor="c", isChild=True, layer=layer)
    addTextField(WIDTH_WINDOW / 2, HEIGHT_WINDOW * 2 / 4, ID=childs[1], outlineColor="white", isChild=True, layer=layer)
    addButton(WIDTH_WINDOW / 2, HEIGHT_WINDOW * 2.5 / 4, ID=childs[2], outlineColor="white", text=buttonText, textSize=18, action=actionPrompt, arguments=[success, successArguments, True], layer=layer)
    if cancelable:
        childs.append("prompt_4")
        addButton(WIDTH_WINDOW / 2, HEIGHT_WINDOW * 3 / 4, ID=childs[3], outlineColor="white", text="Annuler", layer=layer, action=actionPrompt, arguments=[cancel, cancelArguments, False])
    addPanel(WIDTH_WINDOW / 2, HEIGHT_WINDOW / 2, ID="prompt", width=WIDTH_WINDOW / 1.3, height=HEIGHT_WINDOW / 1.3, childs=childs, layer=layer)
    if not checker:
        transaction = True
    else:
        addRenderRoutine("promptRoutine", checkPrompt, [checker, checkerArguments])
    exclusiveLayer = layer


def clearCanvas(color=None):
    efface_tout()
    if color is not None:
        rectangle(0, 0, WIDTH_WINDOW, HEIGHT_WINDOW, couleur=color, remplissage=color)


#####################################################################################

def checkClick(p, pos):
    global focus
    if objects[p]["ax"] < pos[0] < objects[p]["bx"] and objects[p]["ay"] < pos[1] < objects[p]["by"]:
        if objects[p]["type"] == "Button":
            focus = None
            objects[p]["action"](*objects[p]["args"])
            return True
        elif objects[p]["type"] == "textField":
            focus = {"ID": p, "type": "textField"}
            return True
        elif objects[p]["type"] == "Panel":
            focus = {"ID": p, "type": "Panel"}
            return True
    return False


def logic(ev):
    global focus, exclusiveLayer
    type_ev = type_evenement(ev)
    if type_ev == "ClicGauche":
        pos = (clic_x(ev), clic_y(ev))
        layers = set(range(len(renderQueue)-1, 0, -1))#sorted(list(renderQueue.keys()), reverse=True)
        layers.add(0)
        print(layers)
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
    if focus is not None and type_ev == "Touche":
        if focus["type"] == "textField":
            if len(touche(ev)) == 1 and touche(ev).isalnum():
                objects[focus["ID"]]["text"] += touche(ev)
            elif touche(ev) == "BackSpace":
                objects[focus["ID"]]["text"] = objects[focus["ID"]]["text"][:-1]


def updateStats(remainTime, diamonds):
    # Time left#
    texte(WIDTH_WINDOW / 32, 0, "Time left: " + str(remainTime), ("green" if remainTime > 10 else "red"))
    # Diamonds#
    texte(WIDTH_WINDOW / 2.7, 0, "Diamonds: " + str(diamonds[0]) + "/" + str(diamonds[1]),
          ("red" if diamonds[0] < diamonds[1] else "green"))


def render():
    global renderQueue
    for r in renderRoutines.values():
        r[0](*r[1])
    toDeleteObjects=dict()
    # à optimiser
    #layers = sorted(list(renderQueue.keys()), reverse=False)
    # for l in layers:
    #     for ID in renderQueue[l]:
    #         # if isObject(ID):
    #         #     drawObject(ID)
    #         # else:
    #         #     renderQueue[l].remove(ID)
            

    for layer in range(0, len(renderQueue)):
        for ID in renderQueue[layer]:
            try:
                if not (objects[ID]["hidden"] and objects[ID]["isChild"]):
                    drawObject(ID)
            except KeyError as e:
                print("UI Warning: cannot render unknown object", e, "object flagged for deletion")
                if not toDeleteObjects.__contains__(layer):
                    toDeleteObjects[layer]=set()
                toDeleteObjects[layer].add(ID)
    for i in toDeleteObjects.items():
        for ID in i[1]:
            renderQueue[i[0]].remove(ID)


    # delete ID from renderQueue if non existent
    # if toRemove!=[]:
    #    for e in toRemove:
    #        renderQueue[e[0]].pop(e[1])
