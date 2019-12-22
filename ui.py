from upemtk import texte, type_evenement, clic_x, clic_y, touche, donne_evenement
from render import WIDTH_WINDOW, HEIGHT_WINDOW
from uiElements import *

######## Private IDs ########
# prompt_1
# prompt_2
# prompt_3
# prompt_4

def setUIEvenement(ev):
    global evenement
    evenement=ev

def getUIEvenement():
    global  evenement
    tmp=evenement
    evenement=None
    return tmp

def levelWin():
    """
    affiche Victoire
    """
    texte(WIDTH_WINDOW/4, HEIGHT_WINDOW/2-24, "YOU WIN !", "green")

def levelLose():
    """
    affiche Défaite
    """
    texte(WIDTH_WINDOW/4, HEIGHT_WINDOW/2-12, "GAME OVER", "red")

######## Automation ########
condition=False
transaction=False

def checkTransaction():
    condition=transaction

def newPrompt(message, buttonText, cancelable=True, action=None, arguments=None):
    layer=(len(renderQueue.keys()))
    addText(WIDTH_WINDOW/2, HEIGHT_WINDOW*1.6/4, ID="prompt_1", text=message, textAnchor="c", isChild=True, layer=layer)
    addTextField(WIDTH_WINDOW/2, HEIGHT_WINDOW*2/4, ID="prompt_2", outlineColor="white", isChild=True, layer=layer)
    addButton(WIDTH_WINDOW/2, HEIGHT_WINDOW*2.5/4, ID="prompt_3", outlineColor="white", text=buttonText, textSize=18)
    childs=["prompt_1", "prompt_2", "prompt_3"]
    if cancelable:
        addButton(WIDTH_WINDOW/2, HEIGHT_WINDOW*3/4, ID="prompt_4", outlineColor="white", text="Annuler")
        childs.append("prompt_4")
    addPanel(WIDTH_WINDOW/2, HEIGHT_WINDOW/2, ID="prompt", width=WIDTH_WINDOW/1.3, height=HEIGHT_WINDOW/1.3, childs=childs, layer=layer)
    while not condition:
        event=donne_evenement()
        logicUI(event)
        if action:
            transaction=action(*arguments)
            objects["prompt_2"]["outlineColor"]=("Green" if transaction else "Red")
        renderUI()

#####################################################################################

def initUI():
    RightXPos=WIDTH_WINDOW*2/3+(WIDTH_WINDOW/3/2)
    addButton(RightXPos, HEIGHT_WINDOW/16, action=setUIEvenement, arguments=["reset"], anchorx="c",outlineColor="white", text="Reset", textColor="white")
    addButton(RightXPos, HEIGHT_WINDOW/16*3, action=setUIEvenement, arguments=["debug"], anchorx="c", outlineColor="white", text="Debug", textColor="white")
    addButton(RightXPos, HEIGHT_WINDOW-1, action=quit, anchorx="c", anchory="d", outlineColor="white", text="Quitter", textColor="white")
    newPrompt("Nom de la sauvegarde:", "Sauvegarder")

def logicUI(ev):
    global focus
    type_ev=type_evenement(ev)
    if type_ev=="ClicGauche":
        pos=(clic_x(ev), clic_y(ev))
        layers=sorted(list(renderQueue.keys()), reverse=True)
        for l in layers:
            for p in positions[l]:
                #print(objects[p]["ax"], objects[p]["bx"], objects[p]["ay"], objects[p]["by"])
                if objects[p]["ax"]<pos[0]<objects[p]["bx"] and objects[p]["ay"]<pos[1]<objects[p]["by"]:
                    if objects[p]["type"]=="Button":
                        focus=None
                        return objects[p]["action"](*objects[p]["args"])
                    elif objects[p]["type"]=="textField":
                        focus={"ID":p, "type": "textField"}
                        return
                    elif objects[p]["type"]=="Panel":
                        focus={"ID":p, "type": "Panel"}
                        return
                # if raytracePanel(pos, p):
                #     return
                # if raytraceButton(pos, b):
                #     return buttons[b]["action"](*buttons[b]["args"])
                # if raytraceTextField(pos, t):
                #     return
        focus=None
    if focus!=None and type_ev=="Touche":
        if focus["type"]=="textField":
            if (len(touche(ev))==1 and touche(ev).isalnum()):
                objects[focus["ID"]]["text"]+=touche(ev)
            elif touche(ev)=="BackSpace":
                objects[focus["ID"]]["text"]=objects[focus["ID"]]["text"][:-1]
            
def updateStats(remainTime, diamonds):
    #Time left#
    texte(WIDTH_WINDOW/32, 0, "Time left: "+str(remainTime), ("green" if remainTime>10 else "red"))
    #Diamonds#
    texte(WIDTH_WINDOW/2.7, 0, "Diamonds: "+str(diamonds[0])+"/"+str(diamonds[1]), ("red" if diamonds[0]<diamonds[1] else "green"))

def renderUI():
    global renderQueue
    #à optimiser
    layers=sorted(list(renderQueue.keys()), reverse=False)
    for l in layers:
        for ID in renderQueue[l]:
            # if isObject(ID):
            #     drawObject(ID)
            # else:
            #     renderQueue[l].remove(ID)
            try:
                if not (objects[ID]["hidden"] and objects[ID]["isChild"]):
                    drawObject(ID)
            except KeyError as e:
                print("UI Warning: cannot render unknown object", e)
                
    #delete ID from renderQueue if non existent
    #if toRemove!=[]:
    #    for e in toRemove:
    #        renderQueue[e[0]].pop(e[1])

def reset():
    global objects, positions
    objects={}
    positions={}