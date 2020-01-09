from upemtk import donne_evenement, type_evenement, touche

event = {
    "game": None,
    "tk": None
}

def compute():
    ev = donne_evenement()
    event["tk"] = ev
    SetGameEventFromTkEvent(ev)

def SetGameEventFromTkEvent(ev):
    """
    renvoie la direction de rockford

    :param bool debug: active le mode debug

    """
    DIRECTIONS = ["Right", "Left", "Up", "Down"]
    type_ev=type_evenement(ev)
    if type_ev=="Touche":
        t=touche(event["tk"])
        if t in DIRECTIONS:
            event["game"]="move"
        elif t=="r":
            event["game"]="reset"
        elif t=="d":
            event["game"]="debug"
        elif t=="q":
            event["game"]="quitter"
        elif t=="s":
            event["game"]="save"
        elif t=="l":
            event["game"]="load"
        elif t=="Escape":
            event["game"]="return"
        else:
            event["game"]=None
    else: 
        event["game"]=None

def setGameEvent(ge):
    event["game"] = ge

def resetGameEvent():
    event["game"] = None

def getTkEvent():
    return event["tk"]