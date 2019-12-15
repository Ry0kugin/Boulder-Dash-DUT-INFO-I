from upemtk import texte, rectangle, type_evenement, clic_x, clic_y
from render import WIDTH_WINDOW, HEIGHT_WINDOW

buttons={}
textFields={}
bpositions={}
tpositions={}
#efface_tout()
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

def addButton(x, y, action=nullAction, ID="dummy", width=150, height=50, anchorx="c", anchory="c", textAnchor="c",text="", outlineColor="black", textColor="black", textSize=24, fill="", stroke=1):
    if ID=="dummy":
        ID="Button"+str(len(buttons))
    buttons[ID]={
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
        "action": action,
    }
    bpositions[ID]=[
        [buttons[ID]["ax"], buttons[ID]["bx"]],
        [buttons[ID]["ay"], buttons[ID]["by"]]
        ]

def setButton(ID, parameters):
    """
    Sets a parameter or multiple parameters of a button.
    :param 
    """
    assert type(ID)==str
    assert type(parameters)==dict
    for p in parameters:
        buttons[ID][p]=parameters[p]
        if p=="x" or p=="width":
            buttons[ID]["ax"]=buttons[ID]["x"]-buttons[ID]["width"]/2
            buttons[ID]["bx"]=buttons[ID]["x"]+buttons[ID]["width"]/2
        elif p=="y" or p=="height":
            buttons[ID]["ay"]=buttons[ID]["y"]-buttons[ID]["height"]/2
            buttons[ID]["by"]=buttons[ID]["y"]+buttons[ID]["height"]/2

def remButton(ID):
    buttons.pop(ID, None)

def logicButtons(ev):
    type_ev=type_evenement(ev)
    if type_ev=="ClicGauche":
        pos=(clic_x(ev), clic_y(ev))
        print(pos)
        for b in bpositions:
            print(bpositions[b])
            if bpositions[b][0][0]<pos[0]<bpositions[b][0][1] and bpositions[b][1][0]<pos[1]<bpositions[b][1][1]:
                buttons[b]["action"]()

def resetButtons():
    global buttons
    buttons = {}

######## textFields ########

def addTextField(x, y, action=nullAction, ID="dummy", width=150, height=50, anchorx="c", anchory="c", textAnchor="c",text="", outlineColor="black", textColor="black", textSize=24, fill="", stroke=1):
    textFields[ID]={
        "x": (x if anchorx=="c" else (x-width/2 if anchorx=="r" else x+width/2)),
        "y": (y if anchory=="c" else (y-width/2 if anchory=="u" else y+width/2)),
        "ax": (x-width/2 if anchorx=="c" else (x-width if anchorx=="r" else x)),
        "ay": (y-height/2 if anchory=="c" else (y+width/2 if anchory=="u" else y)),
        "bx": (x+width/2 if anchorx=="c" else(x if anchorx=="r" else x+width)),
        "by": (y+height/2 if anchory=="c" else(y+height*2 if anchory=="u" else y+height)),
        "width": width,
        "height": height,
        "text": text,
        "outlineColor": outlineColor,
        "textColor": textColor,
        "fill": fill,
        "stroke": stroke,
        "textSize": textSize,
    }

def setTextField(ID, parameters):
    """
    Sets a parameter or multiple parameters of a button.
    :param 
    """
    assert type(ID)==str
    assert type(parameters)==dict
    for p in parameters:
        textFields[ID][p]=parameters[p]
        if p=="x" or p=="width":
            textFields[ID]["ax"]=textFields[ID]["x"]-textFields[ID]["width"]/2
            textFields[ID]["bx"]=textFields[ID]["x"]+textFields[ID]["width"]/2
        elif p=="y" or p=="height":
            textFields[ID]["ay"]=textFields[ID]["y"]-textFields[ID]["height"]/2
            textFields[ID]["by"]=textFields[ID]["y"]+textFields[ID]["height"]/2

def remTextField(ID):
    textFields.pop(ID, None)

def drawElements(remainTime, diamonds):
    #buttons#
    for b in buttons.keys():
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
    #textfields#
    for t in textFields:
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
            textFields[t]["x"],
            textFields[t]["y"],
            textFields[t]["text"],
            textFields[t]["textColor"],
            taille=textFields[t]["textSize"],
            ancrage="c"
        )
    #Time left#
    texte(WIDTH_WINDOW/32, 0, "Time left: "+str(remainTime), ("green" if remainTime>10 else "red"))
    #Diamonds#
    texte(WIDTH_WINDOW/2.7, 0, "Diamonds: "+str(diamonds[0])+"/"+str(diamonds[1]), ("red" if diamonds[0]<diamonds[1] else "green"))

def initUI():
    addButton(WIDTH_WINDOW, HEIGHT_WINDOW/16, anchorx="r",outlineColor="white", text="Reset", textColor="white")
    addButton(WIDTH_WINDOW, HEIGHT_WINDOW/4, anchorx="r",outlineColor="white", text="Debug", textColor="white")

def renderUI(ev, remainTime, diamonds):
    logicButtons(ev)
    drawElements(remainTime, diamonds)