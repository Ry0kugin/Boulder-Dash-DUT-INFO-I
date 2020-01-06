import ui, timer

animations={}


def update():
    global animations
    toDelete=set()
    for anim in animations.keys():
        if timer.exists(anim+"timer"):
            if animations[anim]["status"]==1:
                percentage=timer.getTimer(anim+"timer")/timer.timers[anim+"timer"]["size"]
                for a in animations[anim].items():
                    ui.objects[anim][a[0]]=a[1]["initValue"]+((a[1]["vector"]*percentage)*(1 if a[1]["increment"] else -1))
        else:
            if not animations[anim]["permanent"]:
                toDelete.add(anim)
    for e in toDelete:
        animations.pop(e)


def new(ID, time, parameters, autoStart=False):
    """
    :param string ID: ID de l'objet dans ui.objects
    :param tuple time: Temps total que va mettre l'animation à s'executer du début à la fin. Autant fr valeurs peuvent etre spécifiées que d'éléments dans parameters.
    :param tuple parameters: Tuple de un ou plusieurs dictionnaires contenant les paramètres à modifier pour chaque animation.
    """
    animate(ID, time, parameters)
    animations[ID]["permanent"]=True
    animations[ID]["status"]=(1 if autoStart else 0)
    pass


def start(ID):
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
    if animations[ID]["status"]==1:
        timer.pause(ID+"timer")
        animations[ID]["status"]=2
    else:
        print("Animation warning: cannot pause animation", ID+": animation", ("stopped" if animations[ID]["status"]==0 else "already paused"))


def stop(ID):
    if animations[ID]["status"]!=0:
        timer.stop(ID+"timer")
        animations[ID]["status"]=0
    else:
        print("Animation warning: cannot pause animation", ID+": animation already stopped")


def animate(ID, time, parameters):
    """
    :param string ID: ID de l'objet dans ui.objects
    :param tuple time: Temps total que va mettre l'animation à s'executer du début à la fin. Autant fr valeurs peuvent etre spécifiées que d'éléments dans parameters.
    :param tuple parameters: Tuple de un ou plusieurs dictionnaires contenant les paramètres à modifier pour chaque animation.
    """
    global animations
    animations[ID]={
        "parameters": tuple(),
        "permanent": False,
        "status": 1 # 0: stopped 1: ongoing 2: paused
    }
    for i in range(len(parameters)):
        for p in parameters[i].keys():
            try:
                currentValue=ui.objects[ID][p]
            except KeyError as e:
                print("Animation warning: cannot find parameter", e, "aborting animation")
                animations
                return
            if type(currentValue) is not (float or int):
                print("Animation warning: cannot animate parameter", "'"+p[0]+"', aborting animation")
                return
            parameters[i][p]=(currentValue, abs(parameters[i][p]-currentValue),(True if parameters[i][p]>currentValue else False), False)
    animations[ID]={
        "initValue": currentValue,
        "vector": abs(parameters[i][p]-currentValue),
        "increment": (1 if parameters[i][p]>currentValue else -1),
    }
    timer.new(time, ID+"timer")