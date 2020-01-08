import time

timer = 0.0
timerCount=0
timers={}
timestamp=time.time()
factor=1
#delta = 0

def new(size, ID=None, paused=False, permanent=False):
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
    global timers, timestamp
    currentTime=time.time()
    delta = currentTime-timestamp
    timestamp = currentTime
    toDelete=set()
    for t in timers.keys():
        if timers[t]["progression"]<timers[t]["size"]:
            timers[t]["progression"]+= (0 if timers[t]["paused"] else delta*factor)
        elif timers[t]["permanent"]:
            setTimer(t ,0)
        else:
            toDelete.add(t)
    for element in toDelete:
        timers.pop(element)
    return delta

def start(ID):
    global timers
    try:
        timers[ID]["paused"]=False
    except KeyError as e:
        print("Timer warning: unknown timer ID:", e)

def pause(ID):
    global timers

    try:
        timers[ID]["paused"]=True
    except KeyError as e:
        print("Timer warning: unknown timer ID:", e)

def stop(ID): 
    global timers
    try:
        finalTime = timers[ID]["progression"]
        timers.pop(ID)
        return finalTime
    except KeyError as e:
        print("Timer warning: unknown timer ID:", e)

def setTimer(ID, size):
    global timers
    try:
        timers[ID]["progression"]=timers[ID]["progression"]-size
    except KeyError as e:
        print("Timer warning: unknown timer ID:", e)

def add(ID, progress):
    global timers
    try:
        timers[ID]["progression"]+=progress
    except KeyError as e:
        print("Timer warning: unknown timer ID:", e)

def getTimer(ID, returnType=float, remain=False):
    try:
        return (returnType(timers[ID]["size"] - timers[ID]["progression"]) if remain else returnType(timers[ID]["progression"]))
    except KeyError as e:
        print("Timer warning: unknown timer ID:", e)
    # except:
    #     exit("Timer error: wrong returnType specified")
    
   
    # if returnType==float:
    #     return float(timers[ID]["progression"])
    # elif returnType==int:
    #     return int(timers[ID]["progression"])


def reset():
    global timers, timerCount
    timers={}
    timerCount=0

def setFactor(value):
    global factor
    factor = value

def exists(ID):
    try:
        timers[ID]
        return True
    except KeyError:
        return False