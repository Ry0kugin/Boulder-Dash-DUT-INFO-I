import IO
import logic
import render
import ui
import evenement
import timer
from random import randint
from upemtk import *

data = {}
fps = 0

def menu():
    ui.addButton(render.WIDTH_WINDOW / 2, render.HEIGHT_WINDOW *0.8/3, width=render.WIDTH_WINDOW / 3, height=int(render.HEIGHT_WINDOW / 3), text="JOUER", textSize=42, textColor="white", outlineColor="white", action=play)
    ui.addButton(render.WIDTH_WINDOW / 4, render.HEIGHT_WINDOW *1.8/3, width=render.WIDTH_WINDOW / 4, height=int(render.HEIGHT_WINDOW / 4), text="Score", textSize=28, textColor="white", outlineColor="white")
    ui.addButton(3*render.WIDTH_WINDOW / 4, render.HEIGHT_WINDOW *1.8/3, width=render.WIDTH_WINDOW / 4, height=int(render.HEIGHT_WINDOW / 4), text="Editeur", textSize=28, textColor="white", outlineColor="white")
    ui.addButton(render.WIDTH_WINDOW / 2, render.HEIGHT_WINDOW - 30, width=150, height=50 ,text="quitter", textSize=18, textColor="white", outlineColor="white", anchory="s", action=logic.quitter)
    ui.addButton(render.WIDTH_WINDOW - 85, render.HEIGHT_WINDOW - 10, text="settings", textSize=18, textColor="white", outlineColor="white", anchory="s")
    
    while True:
        evenement.compute()
        render.clearCanvas("black")

        ui.logic(evenement.event["tk"])
        delta = timer.update()
        computeFps(delta)
        render.updateAnimations() # /!\ render.updateAnimations before ui.render
        ui.render(getFps())
        mise_a_jour()
        

def initGameUI():
    RightXPos = render.WIDTH_WINDOW * 2 / 2.2
    ui.addButton(RightXPos, render.HEIGHT_WINDOW / 16, action=evenement.setGameEvent, arguments=["reset"], anchorx="c", outlineColor="white", text="Reset", textColor="white", layer=1)
    ui.addButton(RightXPos, render.HEIGHT_WINDOW / 16 * 4, action=ui.setUIEvenement, arguments=["debug"], anchorx="c", outlineColor="white", text="Debug", textColor="white", ID="debug", layer=1)
    ui.addButton(RightXPos, render.HEIGHT_WINDOW / 16 * 7, action=evenement.setGameEvent, arguments=["save"], anchorx="c", outlineColor="white", text="Sauvegarder", textColor="white", textSize=18, layer=1)
    ui.addButton(RightXPos, render.HEIGHT_WINDOW - 1, action=logic.quitter, anchorx="c", anchory="d", outlineColor="white", text="Quitter", textColor="white", layer=1)
    ui.addGameCanvas(0, render.HEIGHT_WINDOW/2, ID="gameCanvas", width=render.CELL_NBX*render.CELL_SIZE, height=render.CELL_NBY*render.CELL_SIZE, anchorx="l")


def play():
    global data
    efface_tout()
    ui.reset()
    initGameUI()
    initData()
    IO.loadLevel(data)
    start(data)
    render.update(data, "gameCanvas")

    while True:
        render.clearCanvas("black")
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

                ui.evenement = None
                continue

            if evenement.event["game"] == "move":
                logic.moveRockford(data, direction)
                logic.updatePhysic(data)
                render.update(data, "gameCanvas")

            if data["fall"]["fallings"]:
                logic.updatePhysic(data)
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

        ui.updateStats(data["time"]["remain"], (data["diamonds"]["owned"], int(data["map"][0][1])), data["score"])
        delta = timer.update()
        computeFps(delta)
        ui.render(getFps())
        #print(ui)
        mise_a_jour()
        data["time"]["remain"] = timer.getTimer("game", int, remain=True)
        print(timer.timers["game"]["progression"])
        if logic.status(data):
            logic.updateGameStatus()
            IO.loadLevel(data)
            start(data, keepScore=True)

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
    data["debug"] = None
    return data


def computeFps(delta):
    global fps
    fps = int(1/(delta+0.00000001))

def getFps():
    global fps
    return fps
