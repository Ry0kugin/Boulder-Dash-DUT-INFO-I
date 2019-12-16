from upemtk import texte, rectangle, type_evenement, clic_x, clic_y, touche
from render import WIDTH_WINDOW, HEIGHT_WINDOW

buttons={}
textFields={}
panels={}
bpositions={}
tpositions={}
ppositions={}
focus=None
evenement=None

def setUIEvenement(ev):
    global evenement
    evenement=ev

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

######## Buttons ########
def nullAction():
    print("je suis un bouton")

def addButton(x, y, action=nullAction, arguments=[] ,ID=None, width=150, height=50, anchorx="c", anchory="c", textAnchor="c",text="", outlineColor="black", textColor="black", textSize=24, fill="", stroke=1,hidden=False):
    if ID==None:
        ID="Button"+str(len(buttons))
    buttons[ID]={
        "x": (x if anchorx=="c" else (x-width/2 if anchorx=="r" else x+width/2)),
        "y": (y if anchory=="c" else (y+height/2 if anchory=="u" else y-height/2)),
        "ax": (x-width/2 if anchorx=="c" else (x-width if anchorx=="r" else x)),
        "ay": (y-height/2 if anchory=="c" else (y if anchory=="u" else y-height)),
        "bx": (x+width/2 if anchorx=="c" else(x if anchorx=="r" else x+width)),
        "by": (y+height/2 if anchory=="c" else(y+height if anchory=="u" else y)),
        "width": width,
        "height": height,
        "anchorx": anchorx,
        "anchory": anchory,
        "text": text,
        "textAnchor": textAnchor,
        "outlineColor": outlineColor,
        "textColor": textColor,
        "fill": fill,
        "stroke": stroke,
        "textSize": textSize,
        "action": action,
        "args": arguments,
        "hidden": hidden
    }
    bpositions[ID]=[
        [buttons[ID]["ax"], buttons[ID]["bx"]],
        [buttons[ID]["ay"], buttons[ID]["by"]]
        ]

def setButton(ID, parameters):
    """
    Modifie un ou plusieurs paramètres d'un bouton.
    :param str ID: ID du bouton
    :param dict parameters: Paramètres à modifier
    """
    assert type(ID)==str
    assert type(parameters)==dict
    for p in parameters:
        buttons[ID][p]=parameters[p]
        if p=="x" or p=="width":
            width=buttons[ID]["width"]
            x=buttons[ID]["x"]
            anchorx=buttons[ID]["anchorx"]
            buttons[ID]["ax"]=(x-width/2 if anchorx=="c" else (x-width if anchorx=="r" else x))
            buttons[ID]["bx"]=(x+width/2 if anchorx=="c" else(x if anchorx=="r" else x+width))
        elif p=="y" or p=="height":
            height=buttons[ID]["height"]
            y=buttons[ID]["y"]
            anchory=buttons[ID]["anchory"]
            buttons[ID]["ay"]=(y-height/2 if anchory=="c" else (y if anchory=="u" else y-height))
            buttons[ID]["by"]=(y+height/2 if anchory=="c" else(y+height if anchory=="u" else y))

def drawButton(b):
    rectangle(
                buttons[b]["ax"],
                buttons[b]["ay"],
                buttons[b]["bx"],
                buttons[b]["by"],
                buttons[b]["outlineColor"],
                buttons[b]["fill"],
                buttons[b]["stroke"]
        )
    texte(
        buttons[b]["x"],
        buttons[b]["y"],
        buttons[b]["text"],
        buttons[b]["textColor"],
        taille=buttons[b]["textSize"],
        ancrage=buttons[b]["textAnchor"]
    )

def remButton(ID):
    buttons.pop(ID, None)

def resetButtons():
    buttons = {}

######## textFields ########
def addTextField(x, y, ID=None, width=150, height=30, anchorx="c", anchory="c", textAnchor="w",text="", outlineColor="black", textColor="black", textSize=18, fill="", stroke=1, hidden=False):
    if ID==None:
        ID="textField"+str(len(textFields))
    textFields[ID]={
        "x": (x if anchorx=="c" else (x-width/2 if anchorx=="r" else x+width/2)),
        "y": (y if anchory=="c" else (y-width/2 if anchory=="u" else y+width/2)),
        "ax": (x-width/2 if anchorx=="c" else (x-width if anchorx=="r" else x)),
        "ay": (y-height/2 if anchory=="c" else (y+width/2 if anchory=="u" else y)),
        "bx": (x+width/2 if anchorx=="c" else(x if anchorx=="r" else x+width)),
        "by": (y+height/2 if anchory=="c" else(y+height*2 if anchory=="u" else y+height)),
        "width": width,
        "height": height,
        "anchorx": anchorx,
        "anchory": anchory,
        "text": text,
        "textAnchor": textAnchor,
        "outlineColor": outlineColor,
        "textColor": textColor,
        "fill": fill,
        "stroke": stroke,
        "textSize": textSize,
        "hidden": hidden
    }
    tpositions[ID]=[
        [textFields[ID]["ax"], textFields[ID]["bx"]],
        [textFields[ID]["ay"], textFields[ID]["by"]]
        ]

def setTextField(ID, parameters):
    """
    Modifie un ou plusieurs paramètres d'un champ de texte.
    :param str ID: ID du textField
    :param dict parameters: Paramètres à modifier
    """
    assert type(ID)==str
    assert type(parameters)==dict
    for p in parameters:
        textFields[ID][p]=parameters[p]
        if p=="x" or p=="width":
            width=textFields[ID]["width"]
            x=textFields[ID]["x"]
            anchorx=textFields[ID]["anchorx"]
            textFields[ID]["ax"]=(x-width/2 if anchorx=="c" else (x-width if anchorx=="r" else x))
            textFields[ID]["bx"]=(x+width/2 if anchorx=="c" else(x if anchorx=="r" else x+width))
        elif p=="y" or p=="height":
            height=textFields[ID]["height"]
            y=textFields[ID]["y"]
            anchory=textFields[ID]["anchory"]
            textFields[ID]["ay"]=(y-height/2 if anchory=="c" else (y+width/2 if anchory=="u" else y))
            textFields[ID]["by"]=(y+height/2 if anchory=="c" else(y+height*2 if anchory=="u" else y+height))

def drawTextField(t):
    rectangle(
                textFields[t]["ax"],
                textFields[t]["ay"],
                textFields[t]["bx"],
                textFields[t]["by"],
                textFields[t]["outlineColor"],
                textFields[t]["fill"],
                textFields[t]["stroke"]
        )
    texte(
        textFields[t]["ax"],
        textFields[t]["ay"]+((textFields[t]["by"]-textFields[t]["ay"])/2),
        textFields[t]["text"],
        textFields[t]["textColor"],
        taille=textFields[t]["textSize"],
        ancrage=textFields[t]["textAnchor"]
    )

def remTextField(ID):
    """
    Supprime un champs de texte.
    :param str ID: ID du textField
    """
    textFields.pop(ID, None)

def resetTextFields():
    textFields = {}

######## Panels ########
def addPanel(x, y, ID=None, width=100, height=100, anchorx="c", anchory="c", outlineColor="gray", fill="gray", stroke=1, buttonChilds=[], textFieldChilds=[], panelChilds=[]):
    if ID==None:
        ID="Panel"+str(len(panels))
    panels[ID]={
        "x": (x if anchorx=="c" else (x-width/2 if anchorx=="r" else x+width/2)),
        "y": (y if anchory=="c" else (y-width/2 if anchory=="u" else y+width/2)),
        "ax": (x-width/2 if anchorx=="c" else (x-width if anchorx=="r" else x)),
        "ay": (y-height/2 if anchory=="c" else (y+width/2 if anchory=="u" else y)),
        "bx": (x+width/2 if anchorx=="c" else(x if anchorx=="r" else x+width)),
        "by": (y+height/2 if anchory=="c" else(y+height*2 if anchory=="u" else y+height)),
        "width": width,
        "height": height,
        "anchorx": anchorx,
        "anchory": anchory,
        "outlineColor": outlineColor,
        "fill": fill,
        "stroke": stroke,
        "buttonChilds": buttonChilds,
        "textFieldChilds": textFieldChilds,
        "panelChilds": panelChilds
    }
    ppositions[ID]=[
        [panels[ID]["ax"], panels[ID]["bx"]],
        [panels[ID]["ay"], panels[ID]["by"]]
        ]

def setPanel(ID, parameters):
    """
    Modifie un ou plusieurs paramètres d'un panneau.
    :param str ID: ID du panneau
    :param dict parameters: Paramètres à modifier
    """
    assert type(ID)==str
    assert type(parameters)==dict
    for p in parameters:
        panels[ID][p]=parameters[p]
        if p=="x" or p=="width":
            width=panels[ID]["width"]
            x=panels[ID]["x"]
            anchorx=panels[ID]["anchorx"]
            panels[ID]["ax"]=(x-width/2 if anchorx=="c" else (x-width if anchorx=="r" else x))
            panels[ID]["bx"]=(x+width/2 if anchorx=="c" else(x if anchorx=="r" else x+width))
        elif p=="y" or p=="height":
            height=panels[ID]["height"]
            y=panels[ID]["y"]
            anchory=panels[ID]["anchory"]
            panels[ID]["ay"]=(y-height/2 if anchory=="c" else (y+width/2 if anchory=="u" else y))
            panels[ID]["by"]=(y+height/2 if anchory=="c" else(y+height*2 if anchory=="u" else y+height))

def drawPanel(p):
    rectangle(
                panels[p]["ax"],
                panels[p]["ay"],
                panels[p]["bx"],
                panels[p]["by"],
                panels[p]["outlineColor"],
                panels[p]["fill"],
                panels[p]["stroke"]
        )
    if panels[p]["buttonChilds"]!=[]:
        for b in panels[p]["buttonChilds"]:
            drawButton(b)
    if panels[p]["textFieldChilds"]!=[]:
        for t in panels[p]["textFieldChilds"]:
            drawTextField(t)
    #if panels[p]["panelChilds"]!=[]:
    #    for e in panels[p]["panelChilds"]:
    #        drawPanel(e)

def remPanel(ID):
    """
    Supprime un champs de texte.
    :param str ID: ID du textField
    """
    if panels[ID]["buttonChilds"]!=[]:
        for b in panels[ID]["buttonChilds"]:
            remButton(b)
    if panels[ID]["textFieldChilds"]!=[]:
        for t in panels[ID]["textFieldChilds"]:
            remTextField(t)
    if panels[ID]["panelChilds"]!=[]:
        for p in panels[ID]["panelChilds"]:
            remPanel(p)
    panels.pop(ID, None)

def resetPanels():
    for p in panels.keys():
        remPanel(p)


######## Automation ########
def newPrompt(message):
    addTextField(WIDTH_WINDOW/2, HEIGHT_WINDOW*2/3, ID="prompt", outlineColor="white", hidden=True)
    addButton(WIDTH_WINDOW/2, HEIGHT_WINDOW*1.8/3, ID="prompt", outlineColor="", text=message, textAnchor="w", hidden=True)
    addPanel(WIDTH_WINDOW/2, HEIGHT_WINDOW/2, ID="prompt", width=WIDTH_WINDOW/1.1, height=HEIGHT_WINDOW/1.1, textFieldChilds=["prompt"], buttonChilds=["prompt"])

#####################################################################################

def initUI():
    RightXPos=WIDTH_WINDOW*2/3+(WIDTH_WINDOW/3/2)
    addButton(RightXPos, HEIGHT_WINDOW/16, action=setUIEvenement, arguments=["reset"], anchorx="c",outlineColor="white", text="Reset", textColor="white")
    addButton(RightXPos, HEIGHT_WINDOW/16*3, action=setUIEvenement, arguments=["debug"], anchorx="c", outlineColor="white", text="Debug", textColor="white")
    addButton(RightXPos, HEIGHT_WINDOW-1, action=quit, anchorx="c", anchory="d", outlineColor="white", text="Quitter", textColor="white")
    newPrompt("Hello !")

def raytracePanel(pos, p):
    if ppositions[p][0][0]<pos[0]<ppositions[p][0][1] and ppositions[p][1][0]<pos[1]<ppositions[p][1][1]:
        for b in panels[p]["buttonChilds"]:
            if raytraceButton(pos, b):
                buttons[b]["action"](*buttons[b]["args"])
                return True
        for t in panels[p]["textFieldChilds"]:
            if raytraceTextField(pos, t):
                return True
        focus={"ID":p, "type": "panel"}
        return True
    return False

def raytraceButton(pos, b):
    if bpositions[b][0][0]<pos[0]<bpositions[b][0][1] and bpositions[b][1][0]<pos[1]<bpositions[b][1][1]:
        focus=None
        return True
    return False

def raytraceTextField(pos, t):
    if tpositions[t][0][0]<pos[0]<tpositions[t][0][1] and tpositions[t][1][0]<pos[1]<tpositions[t][1][1]:
        focus={"ID":t, "type": "textField"}
        return True
    return False

def logicUI(ev):
    global focus
    type_ev=type_evenement(ev)
    if type_ev=="ClicGauche":
        pos=(clic_x(ev), clic_y(ev))
        for p in ppositions:
            if raytracePanel(pos, p):
                return
        for b in bpositions:
            if raytraceButton(pos, b):
                return buttons[b]["action"](*buttons[b]["args"])
        for t in tpositions:
            if raytraceTextField(pos, t):
                return
        focus=None
    if focus!=None and type_ev=="Touche":
        if focus["type"]=="textField":
            if (len(touche(ev))==1 and touche(ev).isalnum()):
                textFields[focus]["text"]+=touche(ev)
            elif touche(ev)=="BackSpace":
                textFields[focus]["text"]=textFields[focus]["text"][:-1]
            
        
        
def renderUI(remainTime, diamonds):
    #buttons#
    for b in buttons.keys():
        if not buttons[b]["hidden"]:
            drawButton(b)
    #textfields#
    for t in textFields.keys():
        if not textFields[t]["hidden"]:
            drawTextField(t)
    #Time left#
    texte(WIDTH_WINDOW/32, 0, "Time left: "+str(remainTime), ("green" if remainTime>10 else "red"))
    #Diamonds#
    texte(WIDTH_WINDOW/2.7, 0, "Diamonds: "+str(diamonds[0])+"/"+str(diamonds[1]), ("red" if diamonds[0]<diamonds[1] else "green"))
    
    for p in panels.keys():
        drawPanel(p)