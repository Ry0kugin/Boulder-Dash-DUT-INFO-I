import IO
import logic
import render
import ui
import evenement
from upemtk import *

data = {}


def menu():
    ui.addButton(render.WIDTH_WINDOW / 2, render.HEIGHT_WINDOW *1/3, text="Jouer", textSize=18, textColor="white", outlineColor="white", action=play)
    ui.addButton(render.WIDTH_WINDOW / 2, render.HEIGHT_WINDOW *1.5/3, text="Jouer", textSize=18, textColor="white", outlineColor="white")
    ui.addButton(render.WIDTH_WINDOW / 2, render.HEIGHT_WINDOW *2/3, text="Jouer", textSize=18, textColor="white", outlineColor="white")
    while True:
        evenement.compute()
        ui.clearCanvas("black")

        ui.logic(evenement.event["tk"])
        ui.render()
        mise_a_jour()
        

def initGameUI():
    RightXPos = render.WIDTH_WINDOW * 2 / 3 + (render.WIDTH_WINDOW / 3 / 2)
    ui.addButton(RightXPos, render.HEIGHT_WINDOW / 16, action=ui.setUIEvenement, arguments=["reset"], anchorx="c", outlineColor="white", text="Reset", textColor="white")
    ui.addButton(RightXPos, render.HEIGHT_WINDOW / 16 * 3, action=ui.setUIEvenement, arguments=["debug"], anchorx="c", outlineColor="white", text="Debug", textColor="white", ID="debug")
    ui.addButton(RightXPos, render.HEIGHT_WINDOW / 16 * 5, action=ui.newPrompt, arguments=["Nom du fichier de sauvegarde", "Sauvegarder", True, IO.checkSaveName], anchorx="c", outlineColor="white", text="Sauvegarder", textColor="white", textSize=18)
    ui.addButton(RightXPos, render.HEIGHT_WINDOW - 1, action=logic.quitter, anchorx="c", anchory="d", outlineColor="white", text="Quitter", textColor="white")


def play():
    global data
    efface_tout()
    ui.reset()
    initGameUI()
    initData()
    IO.loadLevel(data)
    start(data)
    render.renderCanvas(data)

    while True:
        ui.clearCanvas("black")
        evenement.compute()
        direction = (0, 0)
        if ui.focus is None:
            direction = logic.getDirection(evenement.event["tk"], data["debug"])

        if evenement.event["game"] == "reset" or ui.evenement == "reset":
            initData()
            IO.loadLevel(data)
            start(data)
            render.renderCanvas(data)

            ui.evenement = None
            continue

        # if evenement.event["game"] == "debug" or ui.evenement == "debug":
        #     debug = (False if debug else True)
        #     print("DEBUG ACTIVATED" if debug else "DEBUG DEACTIVATED")

        #     ui.evenement = None
        #     continue

        if evenement.event["game"] == "save":
            ui.newPrompt("Nom de la sauvegarde:", "Sauvegarder")
            fileName = IO.save(data)
            print("Game saved to : ", fileName)
            continue

        if evenement.event["game"] == "load":
            fileName = IO.loadSave(data)
            logic.findFallable(data)
            logic.findEnd(data)
            print("load from : ", fileName)
            continue

        if evenement.event["game"] == "move":
            logic.moveRockford(data, direction)
            logic.updatePhysic(data)

        if data["fall"]["fallings"]:
            logic.updatePhysic(data)

        logic.computeRemainTime(data)
        render.renderCanvas(data)
        ui.logic(evenement.event)
        ui.updateStats(data["time"]["remain"], (data["diamonds"]["owned"], int(data["map"][0][1])))
        ui.render()
        #print(ui)
        mise_a_jour()
        logic.status(data)


def start(data):
    """
    initialise une partie

    :param list curMap: map actuel sous forme de liste

    >>> start([['150s', '1d'],['B', 'R', 'G'], ['.', 'E', 'D'], ['W', 'W', 'W']])
    ([(1, 1), 0], [(0, 1), (2, 2)], True)
    """
    logic.findRockford(data)  # refactoring
    logic.findFallable(data)
    logic.findEnd(data)
    data["time"]["start"] = logic.getTime()
    data["time"]["remain"] = data["time"]["start"]
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


