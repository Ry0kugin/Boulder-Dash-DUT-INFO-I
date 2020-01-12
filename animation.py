import ui, timer

animations={}
enabled=True

def update():
    """
    Met à jour toutes les animations.
    """
    if enabled:
        global animations
        toDelete=set()
        for anim in animations.keys():
            if animations[anim]["status"]==1:
                if timer.exists(anim+"timer"):
                    percentage=timer.getTimer(anim+"timer")/timer.timers[anim+"timer"]["size"]
                    ui.setObject(anim, {a[0]: a[1][0]+((a[1][1]*percentage)*(1 if a[1][2] else -1)) for a in animations[anim]["parameters"][animations[anim]["step"]].items()})
                elif animations[anim]["step"]<len(animations[anim]["time"])-1:
                    ui.setObject(anim, {a[0]: a[1][0]+((a[1][1])*(1 if a[1][2] else -1)) for a in animations[anim]["parameters"][animations[anim]["step"]].items()})
                    animations[anim]["step"]+=1
                    timer.new(animations[anim]["time"][animations[anim]["step"]], anim+"timer")
                elif not animations[anim]["permanent"]:
                    toDelete.add(anim)
                else:
                    ui.setObject(anim, {a[0]: a[1][0]+((a[1][1])*(1 if a[1][2] else -1)) for a in animations[anim]["parameters"][animations[anim]["step"]].items()})
                    animations[anim]["status"]=0
                    animations[anim]["step"]=0
        for e in toDelete:
            animations.pop(e)


def new(ID, time, parameters, autoStart=False):
    """
    Crée une nouvelle animation.
    :param string ID: ID de l'objet dans ui.objects
    :param tuple time: Temps total que va mettre l'animation à s'executer du début à la fin. Autant de valeurs peuvent être spécifiées que d'éléments dans parameters.
    :param tuple parameters: Tuple de un ou plusieurs dictionnaires contenant les paramètres à modifier pour chaque étape de l'animation.
    """
    animate(ID, time, parameters)
    animations[ID]["permanent"]=True
    animations[ID]["status"]=(1 if autoStart else 0)


def start(ID):
    """
    Démarre une animation si elle est en pause ou arrêtée.
    :param string ID: ID de l'objet dans ui.objects
    """
    if animations[ID]["status"]!=1:
        if animations[ID]["status"]==2:
            timer.start(ID+"timer")
        else:
            #timer.new(time, ID+"timer")
            pass
        animations[ID]["status"]=1    
    else:
        print("Animation warning: cannot start animation", ID+": animation already started")


def pause(ID):
    """
    Met en pause une animation si elle est en cours.
    :param string ID: ID de l'objet dans ui.objects
    """
    if animations[ID]["status"]==1:
        timer.pause(ID+"timer")
        animations[ID]["status"]=2
    else:
        print("Animation warning: cannot pause animation", ID+": animation", ("stopped" if animations[ID]["status"]==0 else "already paused"))


def stop(ID):
    """
    Arrête une animation si elle est en pause ou en cours.
    :param string ID: ID de l'objet dans ui.objects
    """
    if animations[ID]["status"]!=0:
        timer.stop(ID+"timer")
        animations[ID]["step"]=0
        animations[ID]["status"]=0
    else:
        print("Animation warning: cannot pause animation", ID+": animation already stopped")


def animate(ID, time, parameters):
    """
    Anime un objet (via une animation éphémère).
    :param string ID: ID de l'objet dans ui.objects
    :param list time: Temps total que va mettre l'animation à s'executer du début à la fin. Autant fr valeurs peuvent etre spécifiées que d'éléments dans parameters.
    :param list parameters: Tuple de un ou plusieurs dictionnaires contenant les paramètres à modifier pour chaque animation.
    """
    # assert type(ID)==str
    # assert type(time)==tuple
    # assert type(parameters)==tuple
    global animations
    if len(time)!=len(parameters):
        print("Animation warning: (ID: "+ID+") time parameter has not the same length than the number of parameters, aborting animation")
        return
    lastParameters={}
    for i in range(len(parameters)):
        for p in parameters[i].keys():
            try:
                currentValue=(ui.objects[ID][p] if p not in lastParameters.keys() else lastParameters[p])
            except KeyError as e:
                print("Animation warning: (ID: "+ID+") cannot find parameter", e, "aborting animation")
                # animations
                return
            if type(currentValue) not in (float, int):
                print("Animation warning: (ID: "+ID+") cannot animate parameter", "'"+p[0]+"', aborting animation")
                return
            lastParameters[p]=parameters[i][p]
            parameters[i][p]=(currentValue, abs(parameters[i][p]-currentValue),(True if parameters[i][p]>currentValue else False))
    animations[ID]={
        "time": tuple(time),
        "parameters": tuple(parameters),#abs(parameters[i][p]-currentValue),
        "permanent": False,
        "status": 1, # 0: stopped 1: ongoing 2: paused
        "step": 0
    }
    # time=sum(time)
    timer.new(time[0], ID+"timer")

def setEnabled(boolean):
    """
    Active ou désactive toutes les animations.
    :param bool boolean: True: activer les animations False: Désactiver les animations
    """
    global enabled
    enabled=boolean