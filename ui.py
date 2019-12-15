from upemtk import texte, rectangle
from render import WIDTH_WINDOW, HEIGHT_WINDOW

buttons={}
#efface_tout()
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

def nullAction():
    print("je suis un bouton")

def addButton(x, y, action=nullAction, ID="Button"+str(len(buttons)), width=250, height=100, text="", outlineColor="black", textcolor="black", fill="", stroke=1):
    buttons[ID]={
        "x": x,
        "y": y,
        "ax": x-width/2, 
        "ay": y-height/2, 
        "bx": x+width/2, 
        "by": y+height/2,
        "text": text,
        "outlineColor": outlineColor,
        "textcolor": textcolor,
        "fill": fill,
        "stroke": stroke,
        "action": action,
    }

def setButton(ID, parameters):
    """
    Sets a parameter or multiple parameters of a button.
    :param 
    """
    assert type(ID)==str
    assert type(parameters)==dict
    for p in parameters:
        buttons[ID][p]=parameters[p]
        if p=="x":
            buttons[ID]["ax"]= x-width/2
            buttons[ID]["bx"]= x+width/2
        elif p=="y":
            buttons[ID]["ay"]= y-height/2
            buttons[ID]["by"]= y+height/2

def drawButtons():
    for b in buttonsz:
        rectangle(
                buttons[b]["ax"],
                buttons[b]["ay"],
                buttons[b]["bx"],
                buttons[b]["by"],
                buttons[b]["outlineColor"],
                buttons[b]["fill"],
                buttons[b]["stroke"]
        )
        texte()
    pass

def resetButtons():
    global Buttons
    buttons = {}


def drawTimeLeft(remainTime):
    texte(WIDTH_WINDOW/32, 0, "Time left: "+str(remainTime), ("green" if remainTime>10 else "red"))

def drawDiamonds(diamonds):
    texte(WIDTH_WINDOW/2.7, 0, "Diamonds: "+str(diamonds[0])+"/"+str(diamonds[1]), ("red" if diamonds[0]<diamonds[1] else "green"))

def initUI():
    pass

def renderUI(remainTime, diamonds):
    drawTimeLeft(remainTime)
    drawDiamonds(diamonds)
    #addButton(0, 0, 250, 100 , outlineColor="white", text="debug")