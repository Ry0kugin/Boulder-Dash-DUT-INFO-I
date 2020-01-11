import IO
import logic
import render
import ui
import uiElements
import evenement
import timer
import animation
import editor
from random import randint
from upemtk import *


data = {}
fps = 0

def initPlayMenu():
    ui.addButton(1.2*render.WIDTH_WINDOW / 4, render.HEIGHT_WINDOW * 1/3, width=render.WIDTH_WINDOW / 2.8, height=int(render.HEIGHT_WINDOW / 2), text="Select\nLevel", textSize=40, textColor="white", outlineColor="white", action=evenement.setGameEvent, arguments=["selection"])
    ui.addButton(2.8*render.WIDTH_WINDOW / 4, render.HEIGHT_WINDOW * 1/3, width=render.WIDTH_WINDOW / 2.8, height=int(render.HEIGHT_WINDOW / 2), text="unlimited\nRandom", textSize=40, textColor="white", outlineColor="white", action=evenement.setGameEvent, arguments=["play"])
    ui.addButton(render.WIDTH_WINDOW / 2, render.HEIGHT_WINDOW * 2.3/3, width=render.WIDTH_WINDOW / 2.6, height=int(render.HEIGHT_WINDOW / 5), text="Load from Save", textSize=28, textColor="white", outlineColor="white")


def initMenuUI():
    ui.setBackground("black")
    ui.addButton(render.WIDTH_WINDOW / 2, render.HEIGHT_WINDOW *0.8/3, width=render.WIDTH_WINDOW / 3, height=int(render.HEIGHT_WINDOW / 3), text="Jouer", textSize=42, textColor="white", outlineColor="white", action=playButton, ID="playButton")
    ui.addButton(render.WIDTH_WINDOW / 4, render.HEIGHT_WINDOW *1.8/3, width=render.WIDTH_WINDOW / 4, height=int(render.HEIGHT_WINDOW / 4), text="Scores", textSize=28, textColor="white", outlineColor="white")
    ui.addButton(3*render.WIDTH_WINDOW / 4, render.HEIGHT_WINDOW *1.8/3, width=render.WIDTH_WINDOW / 4, height=int(render.HEIGHT_WINDOW / 4), text="Editeur", textSize=28, textColor="white", outlineColor="white", action=evenement.setGameEvent, arguments=["editor"])
    ui.addButton(render.WIDTH_WINDOW / 2, render.HEIGHT_WINDOW - 30, width=150, height=50 ,text="quitter", textSize=18, textColor="white", outlineColor="white", anchory="s", action=logic.quitter)
    ui.addButton(render.WIDTH_WINDOW - 85, render.HEIGHT_WINDOW - 10, text="settings", textSize=18, textColor="white", outlineColor="white", anchory="s")

def initSelectionLevel(level):
    ui.addButton(0 + render.WIDTH_WINDOW / 20, render.HEIGHT_WINDOW / 2, width=80, height=80, fill="white", stroke=5, polygonal=[(1,0),(0.2,0.5),(1,1)], action=evenement.setGameEvent, arguments=["left"])
    ui.addButton(render.WIDTH_WINDOW - render.WIDTH_WINDOW / 20, render.HEIGHT_WINDOW / 2, width=80, height=80, fill="white", stroke=5, polygonal=[(0,0),(0.8,0.5),(0,1)], action=evenement.setGameEvent, arguments=["right"])
    ui.addGameCanvas(render.WIDTH_WINDOW/2, render.HEIGHT_WINDOW/2, "levelSelection", fill="red", width=0, height=0, squaresMap=level)
    ui.addText(render.WIDTH_WINDOW/2, render.HEIGHT_WINDOW/9, "levelName", render.WIDTH_WINDOW/2, render.HEIGHT_WINDOW/8, text=" ", textColor="white", textSize=28)
    ui.addText(3*render.WIDTH_WINDOW/4, render.HEIGHT_WINDOW/9, "levelSelected", render.WIDTH_WINDOW/2, render.HEIGHT_WINDOW/8, text=" ", textColor="white", textSize=28)
    ui.addButton(render.WIDTH_WINDOW-1, render.HEIGHT_WINDOW-1, width=render.WIDTH_WINDOW/5, height=render.HEIGHT_WINDOW/8, anchorx="r" ,anchory="d", text="import Level", outlineColor="white", textColor="white")
    ui.addButton(render.WIDTH_WINDOW/2, 7*render.HEIGHT_WINDOW/8, width=render.WIDTH_WINDOW/4, height=render.HEIGHT_WINDOW/7, anchorx="c" ,anchory="c", text="Play", outlineColor="white", textColor="white", action=evenement.setGameEvent, arguments=["play"])

def playButton():
    # animation.animate("playButton", [0.1], [{"width":render.WIDTH_WINDOW / 2}])
    # while timer.exists("playButtontimer"):
    #     updateTime()
    #     animation.update()
    #     ui.render(getFps())
    #     mise_a_jour()
    evenement.setGameEvent("play")



######## Game ########

def initGameUI():
    RightXPos = render.WIDTH_WINDOW * 2 / 2.2
    # Buttons
    ui.addButton(RightXPos, render.HEIGHT_WINDOW / 16, action=evenement.setGameEvent, arguments=["reset"], anchorx="c", outlineColor="white", text="Reset", textColor="white", layer=1)
    ui.addButton(RightXPos, render.HEIGHT_WINDOW / 16 * 4, action=ui.setUIEvenement, arguments=["debug"], anchorx="c", outlineColor="white", text="Debug", textColor="white", ID="debug", layer=1)
    ui.addButton(RightXPos, render.HEIGHT_WINDOW / 16 * 7, action=evenement.setGameEvent, arguments=["save"], anchorx="c", outlineColor="white", text="Sauvegarder", textColor="white", textSize=18, layer=1)
    ui.addButton(RightXPos, render.HEIGHT_WINDOW - 1, action=logic.quitter, anchorx="c", anchory="d", outlineColor="white", text="Quitter", textColor="white", layer=1)
    # Texts
    ui.addText(0, 0, ID="timeLeftText", anchorx="l", anchory="u", textColor="green")
    ui.addText(ui.objects["timeLeftText"]["bx"]+render.WIDTH_WINDOW / 20, 0, ID="diamondsText", anchory="u", textColor="red")
    ui.addText(ui.objects["diamondsText"]["bx"]+render.WIDTH_WINDOW / 20, 0, ID="scoreText", anchorx='l', anchory="u", textColor="purple",)
    # Game canvas
    ui.addGameCanvas(0, render.HEIGHT_WINDOW/8, ID="gameCanvas", width=0, height=0, anchorx="l", anchory="u", cellSize=32)

def handleEvenement(evenement, args=[]):
    # evenement = "move" if evenement in ("Right", "Left", "Up", "Down")
    if evenement in ("reset", "move", "save", "load", "return"):
        if evenement!="return":
            evenementHandler[evenement](*args)
        return True
    return False

def resetGame():
    origin = data["origin"][:]
    mode = data["mode"]
    initData()
    if mode == "s":
        data["map"] = origin[:]
    else: 
        IO.loadLevel(data)
    start(data)
    render.update(data["map"][1::], "gameCanvas")
    ui.render()

def moveRockford():
    logic.moveRockford(data, logic.getDirection(evenement.event["tk"], data["debug"]))
    data["fall"]["fallings"] = True
    render.update(data["map"][1::], "gameCanvas")

def saveGame():
    timer.factor = 0
    timer.factor = 0
    ui.newPrompt("Nom de la sauvegarde:", "Sauvegarder", success=lambda: IO.save(data, ui.objects["prompt_2"]["text"]), checker=IO.checkSaveName, anyway=lambda: timer.setFactor(1))

def loadGame():
    timer.pause("game") 
    fileName = IO.loadSave(data)
    logic.findFallable(data)
    logic.findEnd(data)
    print("load from : ", fileName)

evenementHandler={
    "reset":resetGame,
    "move":moveRockford, 
    "save":saveGame, 
    "load":loadGame
}

def play(level=None):
    global data
    ui.reset()
    ui.setBackground("black")
    initGameUI()
    initData()
    if level:
        IO.loadLevel(data, level)
        data["mode"] = "s"
    else: 
        IO.loadLevel(data)
        data["mode"] = "r"
    start(data)
    render.update(data["map"][1::], "gameCanvas")

    while True:
        evenement.compute(inGame=True)
        ui.logic(evenement.event["tk"])
        #direction = (0, 0)
        if ui.focus is None:
            timer.start("game")
            gameEvenement=evenement.event["game"]
            if handleEvenement(gameEvenement): 
                if gameEvenement=="return":
                    break
                continue
            
            # if evenement.event["game"] == "reset" or ui.evenement == "reset":
            #     continue

            # elif evenement.event["game"] == "move":
                

            # elif evenement.event["game"] == "save":
                
            #     #fileName = IO.save(data)
            #     continue

            # elif evenement.event["game"] == "load":
                
            #     continue

            # elif evenement.event["game"] == 'return':
            #     break
        # if evenement.event["game"] == "debug" or ui.evenement == "debug":
        #     debug = (False if debug else True)
        #     print("DEBUG ACTIVATED" if debug else "DEBUG DEACTIVATED")

        #     ui.evenement = None
        #     continue

        logic.updatePhysic(data)
        if data["fall"]["fallings"]:
            render.update(data["map"][1::], "gameCanvas")
        updateStats(data["time"]["remain"], (data["diamonds"]["owned"], int(data["map"][0][1])), data["score"])
        updateTime()
        data["time"]["remain"] = timer.getTimer("game", int, remain=True)
        #print(timer.timers["game"]["progression"])
        win = logic.status(data)
        if win and data["mode"] == "s":
            logic.updateGameStatus()
            attente_clic_ou_touche()
            break
        if win:
            logic.updateGameStatus()
            IO.loadLevel(data)
            start(data, keepScore=True)
            render.update(data["map"][1::], "gameCanvas")
        ui.render(getFps())
        mise_a_jour()
    ui.reset()
    initMenuUI()


    

def start(data, keepScore=False):
    """
    initialise une partie

    :param list curMap: map actuel sous forme de liste

    >>> start([['150s', '1d'],['B', 'R', 'G'], ['.', 'E', 'D'], ['W', 'W', 'W']])
    ([(1, 1), 0], [(0, 1), (2, 2)], True)
    """
    logic.findRockford(data)  # refactoring
    logic.findFallable(data)
    logic.findEnd(data)
    timer.new(data["map"][0][0], "game")
    if not keepScore:
        data["score"] = 0
    data["time"]["remain"] = timer.getTimer("game", int, remain=True)
    data["debug"] = False
    data["origin"] = data["map"][:]


def initData():
    global data
    data["map"] = None
    data["rockford"] = None
    data["diamonds"] = {
        "owned":None,
        "total": None
    }
    data["fall"] = {
        "fallables":None,
        "fallings":None
    }
    data["score"] = None
    data["time"] = {
        "start":None,
        "remain":None,
        "total":None
    }
    data["end"] = {
        "pos":None,
        "open":None
    }
    data["mode"] = None,
    data["origin"] = None

def computeFps(delta):
    global fps
    if delta:
        fps = int(1/(delta))
    else:
        fps = "unlimited"

def getFps():
    global fps
    return fps

def updateStats(remainTime, diamonds, score):
    # Time left#
    # ui.setObject("timeLeftText", {"text":"Time left: " + str(remainTime), "textColor":("green" if remainTime > 10 else "red")})
    # Diamonds#
    ui.setObject("diamondsText", {"text":"Diamonds: " + str(diamonds[0]), "textColor":("red" if diamonds[0] < diamonds[1] else "green")})
    # Score#
    ui.setObject("scoreText", {"text":"score: " + str(score)})

def updateTime():
    delta = timer.update()
    computeFps(delta)
    return delta
