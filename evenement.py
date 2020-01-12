from upemtk import donne_evenement, type_evenement, touche

event = {
    "game": None,
    "tk": None
}

def compute(inGame=False):
    """

    """
    ev = donne_evenement()
    event["tk"] = ev
    SetGameEventFromTkEvent(ev,inGame)
    clearEventQueue()

def SetGameEventFromTkEvent(ev, inGame):
    """
    renvoie la direction de rockford
    :param tuple ev: Evenement donné par upemtk
    """
    type_ev=type_evenement(ev)
    if type_ev=="Touche":
        t=touche(event["tk"])
        if t in "Right":
            event["game"]="move" if inGame else "right" 
        elif t in "Left":
            event["game"]="move" if inGame else "left"
        elif t in "Up":
            event["game"]="move" if inGame else "up"
        elif t in "Down":
            event["game"]="move" if inGame else "down"
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
    """
    Modifie l'événement interne au jeu.
    :param string ge: Evenement à insérer
    """
    event["game"] = ge

def resetGameEvent():
    """
    Réinitialise l'événement interne au jeu.
    """
    event["game"] = None

def getTkEvent():
    """
    Retourne l'événement donné par upemtk.
    """
    return event["tk"]

def clearEventQueue():
    """
    Corrige le système de pile d'événements de upemtk.
    """
    while type_evenement(donne_evenement()) != "RAS":
        #print("videur d'event entre à l'action")
        1
    