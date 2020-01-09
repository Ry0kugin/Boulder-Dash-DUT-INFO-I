import IO
import logic
import render
import ui
import uiElements
import evenement
import timer
import animation
from random import randint
from upemtk import *


data = {}
fps = 0


######## Menu ########

def initMenuUI():
    ui.setBackground("black")
    ui.addButton(render.WIDTH_WINDOW / 2, render.HEIGHT_WINDOW *0.8/3, width=render.WIDTH_WINDOW / 3, height=int(render.HEIGHT_WINDOW / 3), text="Jouer", textSize=42, textColor="white", outlineColor="white", action=evenement.setGameEvent, arguments=["play"])
    ui.addButton(render.WIDTH_WINDOW / 4, render.HEIGHT_WINDOW *1.8/3, width=render.WIDTH_WINDOW / 4, height=int(render.HEIGHT_WINDOW / 4), text="Scores", textSize=28, textColor="white", outlineColor="white")
    ui.addButton(3*render.WIDTH_WINDOW / 4, render.HEIGHT_WINDOW *1.8/3, width=render.WIDTH_WINDOW / 4, height=int(render.HEIGHT_WINDOW / 4), text="Editeur", textSize=28, textColor="white", outlineColor="white", action=editor)
    ui.addButton(render.WIDTH_WINDOW / 2, render.HEIGHT_WINDOW - 30, width=150, height=50 ,text="quitter", textSize=18, textColor="white", outlineColor="white", anchory="s", action=logic.quitter)
    ui.addButton(render.WIDTH_WINDOW - 85, render.HEIGHT_WINDOW - 10, text="settings", textSize=18, textColor="white", outlineColor="white", anchory="s")
    ui.addButton(render.WIDTH_WINDOW / 2, render.HEIGHT_WINDOW / 2, width=50, height=50, fill="white", polygonal=[(0,0),(1,0.5),(0,1)], action=evenement.setGameEvent, arguments=["play"])

    #print(ui.toRenderObjects)
    #ui.renderQueue[0].remove("text01")
    #ui.remObject("text01")
    # print(ui.renderQueue[0])
    # print(ui.objects["text01"]["layer"])
    


def menu():
    initMenuUI()
    while not evenement.event["game"] == 'return':
        evenement.compute()
        ui.logic(evenement.event["tk"])
        if evenement.event["game"] == 'play':
            ui.reset()
            ui.setBackground("black")
            ui.addButton(1.2*render.WIDTH_WINDOW / 4, render.HEIGHT_WINDOW * 1/3, width=render.WIDTH_WINDOW / 2.8, height=int(render.HEIGHT_WINDOW / 2), text="Select\nLevel", textSize=40, textColor="white", outlineColor="white")
            ui.addButton(2.8*render.WIDTH_WINDOW / 4, render.HEIGHT_WINDOW * 1/3, width=render.WIDTH_WINDOW / 2.8, height=int(render.HEIGHT_WINDOW / 2), text="unlimited\nRandom", textSize=40, textColor="white", outlineColor="white", action=play)
            ui.addButton(render.WIDTH_WINDOW / 2, render.HEIGHT_WINDOW * 2.3/3, width=render.WIDTH_WINDOW / 2.6, height=int(render.HEIGHT_WINDOW / 5), text="Load from Save", textSize=28, textColor="white", outlineColor="white")
            while not evenement.event["game"] == 'return':   
                evenement.compute()
                ui.logic(evenement.event["tk"])
                if evenement.event["game"] == 'selection':
                    pass
                updateTime()
                ui.render(getFps())
                mise_a_jour()
            ui.reset()
            ui.setBackground("black")
            initMenuUI()
            evenement.resetGameEvent()
        elif evenement.event["game"] == 'return':
            break
        # animation.update() # /!\ render.updateAnimations before ui.render
        updateTime()
        ui.render(getFps())
        mise_a_jour()


######## Editor ########

def initEditorUI():
    RightXPos = render.WIDTH_WINDOW * 2 / 2.2
    # Buttons
    ui.addButton(RightXPos, render.HEIGHT_WINDOW / 16, action=evenement.setGameEvent, arguments=["reset"], anchorx="c", outlineColor="white", text="Reset", textColor="white", layer=1)
    ui.addButton(RightXPos, render.HEIGHT_WINDOW / 16 * 4, action=ui.setUIEvenement, arguments=["debug"], anchorx="c", outlineColor="white", text="Debug", textColor="white", ID="debug", layer=1)
    ui.addButton(RightXPos, render.HEIGHT_WINDOW / 16 * 7, action=evenement.setGameEvent, arguments=["save"], anchorx="c", outlineColor="white", text="Sauvegarder", textSize=88, textColor="white", layer=1)
    ui.addButton(RightXPos, render.HEIGHT_WINDOW - 1, action=logic.quitter, anchorx="c", anchory="d", outlineColor="white", text="Quitter", textColor="white", layer=1)
    # Texts
    ui.addText(0, 0, ID="timeLeftText", anchorx="l", anchory="u", textColor="green")
    # textFields
    ui.addTextField(ui.objects["timeLeftText"]["bx"], 0, ID="timeLeftTextField", anchorx="l", anchory="u")
    #ui.addText(render.WIDTH_WINDOW / 4.2, 0, ID="diamondsText", anchory="u", textColor="red")
    #ui.addText(render.WIDTH_WINDOW / 2, 0, ID="scoreText", anchory="u", textColor="yellow")
    # Game canvas
    ui.addGameCanvas(0, render.HEIGHT_WINDOW/2, ID="gameCanvas", width=render.CELL_NBX*render.CELL_SIZE, height=render.CELL_NBY*render.CELL_SIZE, anchorx="l")

def editor():
    global data
    ui.reset()
    ui.setBackground("black")
    initEditorUI()
    initData()
    #IO.loadLevel(data)
    start(data)
    render.update(data, "gameCanvas")

    while True:
        evenement.compute()
        ui.logic(evenement.event["tk"])
        direction = (0, 0)
        if ui.focus is None:
            timer.start("game")
            direction = logic.getDirection(evenement.event["tk"], data["debug"])

            if evenement.event["game"] == "reset" or ui.evenement == "reset":
                initData()
                IO.loadLevel(data)
                start(data)
                render.update(data, "gameCanvas")
                ui.render()
                

                ui.evenement = None
                continue

            if evenement.event["game"] == "move":
                logic.moveRockford(data, direction)
                data["fall"]["fallings"] = True
                render.update(data, "gameCanvas")
                
            print("before after before", timer.getTimer("fallings", remain=True), timer.isOver("fallings"))
            if data["fall"]["fallings"] and timer.isOver("fallings"):
                print("before", timer.getTimer("fallings", remain=True))
                logic.updatePhysic(data)
                print("after", timer.getTimer("fallings", remain=True))
                render.update(data, "gameCanvas")

            if evenement.event["game"] == "save":
                timer.factor = 0
                ui.newPrompt("Nom de la sauvegarde:", "Sauvegarder", success=lambda: IO.save(data, ui.objects["prompt_2"]["text"]), checker=IO.checkSaveName, anyway=lambda: timer.setFactor(1))
                #fileName = IO.save(data)
                continue

            if evenement.event["game"] == "load":
                timer.pause("game") 
                fileName = IO.loadSave(data)
                logic.findFallable(data)
                logic.findEnd(data)
                print("load from : ", fileName)
                continue
        # if evenement.event["game"] == "debug" or ui.evenement == "debug":
        #     debug = (False if debug else True)
        #     print("DEBUG ACTIVATED" if debug else "DEBUG DEACTIVATED")

        #     ui.evenement = None
        #     continue

        updateStats(data["time"]["remain"], (data["diamonds"]["owned"], int(data["map"][0][1])), data["score"])
        updateTime()
        data["time"]["remain"] = timer.getTimer("game", int, remain=True)
        #print(timer.timers["game"]["progression"])
        if logic.status(data):
            logic.updateGameStatus()
            IO.loadLevel(data)
            start(data, keepScore=True)
            render.update(data, "gameCanvas")
        ui.render(getFps())
        mise_a_jour()
    ui.reset()
    initMenuUI()


######## Game ########

def initGameUI():
    RightXPos = render.WIDTH_WINDOW * 2 / 2.2
    # Buttons
    ui.addButton(RightXPos, render.HEIGHT_WINDOW / 16, action=evenement.setGameEvent, arguments=["reset"], anchorx="c", outlineColor="white", text="Reset", textColor="white", layer=1)
    ui.addButton(RightXPos, render.HEIGHT_WINDOW / 16 * 4, action=ui.setUIEvenement, arguments=["debug"], anchorx="c", outlineColor="white", text="Debug", textColor="white", ID="debug", layer=1)
    ui.addButton(RightXPos, render.HEIGHT_WINDOW / 16 * 7, action=evenement.setGameEvent, arguments=["save"], anchorx="c", outlineColor="white", text="Sauvegarder", textColor="white", textSize=18, layer=1)
    ui.addButton(RightXPos, render.HEIGHT_WINDOW - 1, action=logic.quitter, anchorx="c", anchory="d", outlineColor="white", text="Quitter", textColor="white", layer=1)
    ui.addButton(0, render.HEIGHT_WINDOW, outlineColor="white", textColor="white", text="retour", action=evenement.setGameEvent, arguments=["return"], anchorx="l", anchory="d")
    # Texts
    ui.addText(0, 0, ID="timeLeftText", anchorx="l", anchory="u", textColor="green")
    ui.addText(render.WIDTH_WINDOW / 4.2, 0, ID="diamondsText", anchory="u", textColor="red")
    ui.addText(render.WIDTH_WINDOW / 2, 0, ID="scoreText", anchory="u", textColor="yellow")
    # Game canvas
    ui.addGameCanvas(0, render.HEIGHT_WINDOW/2, ID="gameCanvas", width=render.CELL_NBX*render.CELL_SIZE, height=render.CELL_NBY*render.CELL_SIZE, anchorx="l")

def handleEvenement(evenement, args=[]):
    if evenement in ("reset", "move", "save", "load", "return"):
        if evenement!="return":
            evenementHandler[evenement](*args)
        return True
    return False

def resetGame():
    initData()
    IO.loadLevel(data)
    start(data)
    render.update(data, "gameCanvas")
    ui.render()

def moveRockford():
    logic.moveRockford(data, logic.getDirection(evenement.event["tk"], data["debug"]))
    data["fall"]["fallings"] = True
    render.update(data, "gameCanvas")

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

def play():
    global data
    ui.reset()
    ui.setBackground("black")
    initGameUI()
    initData()
    IO.loadLevel(data)
    start(data)
    render.update(data, "gameCanvas")

    while True:
        evenement.compute()
        ui.logic(evenement.event["tk"])
        #direction = (0, 0)
        if ui.focus is None:
            timer.start("game")
            gameEvenement=evenement.event["game"]
            if handleEvenement(gameEvenement): 
                if gameEvenement=="return":
                    break
                continue
            # if evenement.event["game"] ==             # if evenement.event["game"] == "reset" or ui.evenement == "reset":
            # if evenement.event["game"] == "reset" or ui.evenement == "reset":
            # if evenement.event["game"] == "reset" or ui.evenement == "reset":
            # if evenement.event["game"] == "reset" or ui.evenement == "reset":
            # if evenement.event["game"] == "reset" or ui.evenement == "reset":
            # if evenement.event["game"] == "reset" or ui.evenement == "reset":
            # if evenement.event["game"] == "reset" or ui.evenement == "reset":
            # if evenement.event["game"] == "reset" or ui.evenement == "reset":
            # if evenement.event["game"] == "reset" or ui.evenement == "reset":
            # if evenement.event["game"] == "reset" or ui.evenement == "reset":
            # if evenement.event["game"] == "reset" or ui.evenement == "reset":
            # if evenement.event["game"] == "reset" or ui.evenement == "reset":
            # if evenement.event["game"] == "reset" or ui.evenement == "reset":
            # if evenement.event["game"] == "reset" or ui.evenement == "reset":
            # if evenement.event["game"] == "reset" or ui.evenement == "reset":
            # if evenement.event["game"] == "reset" or ui.evenement == "reset":
            # if evenement.event["game"] == "reset" or ui.evenement == "reset":
            # if evenement.event["game"] == "reset" or ui.evenement == "reset":
            # if evenement.event["game"] == "reset" or ui.evenement == "reset":
            # if evenement.event["game"] == "reset" or ui.evenement == "reset":
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
            render.update(data, "gameCanvas")
        updateStats(data["time"]["remain"], (data["diamonds"]["owned"], int(data["map"][0][1])), data["score"])
        updateTime()
        data["time"]["remain"] = timer.getTimer("game", int, remain=True)
        #print(timer.timers["game"]["progression"])
        if logic.status(data):
            logic.updateGameStatus()
            IO.loadLevel(data)
            start(data, keepScore=True)
            render.update(data, "gameCanvas")
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
    ui.setObject("timeLeftText", {"text":"Time left: " + str(remainTime), "textColor":("green" if remainTime > 10 else "red")})
    # Diamonds#
    ui.setObject("diamondsText", {"text":"Diamonds: " + str(diamonds[0]), "textColor":("red" if diamonds[0] < diamonds[1] else "green")})
    # Score#
    ui.setObject("scoreText", {"text":"score: " + str(score)})

def updateTime():
    delta = timer.update()
    computeFps(delta)
