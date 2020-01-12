import time

timer = 0.0
timerCount=0
timers={}
timestamp=time.time()
factor=1
delta = 0

def new(size, ID=None, paused=False, permanent=False):
    """
    Crée un nouveau chronomètre.
    :param float size: Temps maximal que peut atteindre le chronomètre
    :param string ID: ID du chronomètre
    :param bool paused: Si vrai, le chronomètre sera en pause
    :param bool permanent: Si vrai, le chronomètre ne sera pas supprimé lorsqu'il dépassera son temps maximal
    """
    global timers, timerCount
    if ID==None:
        ID="timer"+str(timerCount)
    timerCount+=1
    timers[ID] = {
    "size":size,
    "progression":0.0,
    "paused":paused,
    "permanent":permanent
}


def update():
    """
    Met à jour tous les chronomètres.
    """
    global timers, timestamp, delta
    currentTime=time.time()
    deltaT = currentTime-timestamp
    timestamp = currentTime
    toDelete=set()
    for t in timers.keys():
        if timers[t]["progression"]<timers[t]["size"]:
            timers[t]["progression"]+= (0 if timers[t]["paused"] else delta*factor)
        elif not timers[t]["permanent"]:
            toDelete.add(t)
    for element in toDelete:
        timers.pop(element)
    delta = deltaT
    return deltaT

def start(ID):
    """
    Démarre un chronomètre.
    :param string ID: ID du chronomètre
    """
    global timers
    if ID in timers:
        timers[ID]["paused"]=False
    else:
        print("Timer warning: unknown timer ID:", ID)

def pause(ID):
    """
    Met en pause un chronomètre.
    :param string ID: ID du chronomètre
    """
    global timers
    if ID in timers:
        timers[ID]["paused"]=True
    else:
        print("Timer warning: unknown timer ID:", ID)

def stop(ID): 
    """
    Arrête et supprime un chronomètre.
    :param string ID: ID du chronomètre
    """
    global timers
    if ID in timers:
        finalTime = timers[ID]["progression"]
        timers.pop(ID)
        return finalTime
    else:
        print("Timer warning: unknown timer ID:", ID)

# def remove(ID):
#     global timers
#     try:
#         timers.pop(ID)
#     except KeyError as e:
#         print("Timer warning: cannot remove unknown timer ID:", e)

def setTimer(ID, size):
    """
    Enlève un temps à un chronomètre.
    :param string ID: ID du chronomètre
    :param float size: Temps à enlever
    """
    global timers
    if ID in timers:
        timers[ID]["progression"]-=size
    else:
        print("Timer warning: unknown timer ID:", ID)

def add(ID, size):
    """
    Ajoute un temps à un chronomètre.
    :param string ID: ID du chronomètre
    :param float size: Temps à ajouter
    """
    global timers
    if ID in timers:
        timers[ID]["progression"]+=size
    else:
        print("Timer warning: unknown timer ID:", ID)

def isOver(ID):
    """
    Retourne vrai si le chronomètre donné est fini.
    :param string ID: ID du chronomètre
    """
    return timers[ID]["progression"]>=timers[ID]["size"]

def restore(ID):
    """
    Réinitialise la progression d'un chronomètre.
    :param string ID: ID du chronomètre
    """
    timers[ID]["progression"] = 0.0

def getTimer(ID, returnType=float, remain=False):
    if ID in timers:
        return (returnType(timers[ID]["size"] - timers[ID]["progression"]) if remain else returnType(timers[ID]["progression"]))
    else:
        print("Timer warning: unknown timer ID:", ID)
    # except:
    #     exit("Timer error: wrong returnType specified")
    
   
    # if returnType==float:
    #     return float(timers[ID]["progression"])
    # elif returnType==int:
    #     return int(timers[ID]["progression"])

def getDelta():
    """
    Retourne le delta (temps écoulé entre la dernière image et l'image actuelle)
    """
    return delta

def reset():
    """
    Réinitialise toutes les données sur les chronomètres.
    """
    global timers, timerCount
    timers={}
    timerCount=0

def setFactor(value):
    """
    Modifie le multiplicateur du temps (Par exemple, 0: temps arrêté 1: temps normal -1: temps à l'envers).
    :param float value: Nouveau multiplicateur
    """
    global factor
    factor = value

def exists(ID):
    """
    Retourne vrai si le chronomètre donné existe.
    :param string ID: ID du chronomètre
    """
    if ID in timers:
        return True
    else:
        return False