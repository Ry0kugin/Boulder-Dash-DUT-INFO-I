import IO
import logic
import render
import ui
from upemtk import *

data = {}

# map
# rockford
# diamonds_Onwed - diamonds_total 
# fallables - fall
# end
# startTime - remainTime
# debug

def menu():
    ui.addButton(render.WIDTH_WINDOW / 2, render.HEIGHT_WINDOW *1/3, text="Jouer", textSize=18, textColor="white", outlineColor="white", action=play)
    ui.addButton(render.WIDTH_WINDOW / 2, render.HEIGHT_WINDOW *1.5/3, text="Jouer", textSize=18, textColor="white", outlineColor="white")
    ui.addButton(render.WIDTH_WINDOW / 2, render.HEIGHT_WINDOW *2/3, text="Jouer", textSize=18, textColor="white", outlineColor="white")
    while True:
        event = donne_evenement()
        ui.clearCanvas("black")



        ui.logic(event)
        ui.render()
        mise_a_jour()
        

def initGameUI():
    RightXPos = render.WIDTH_WINDOW * 2 / 3 + (render.WIDTH_WINDOW / 3 / 2)
    ui.addButton(RightXPos, render.HEIGHT_WINDOW / 16, action=ui.setUIEvenement, arguments=["reset"], anchorx="c", outlineColor="white", text="Reset", textColor="white")
    ui.addButton(RightXPos, render.HEIGHT_WINDOW / 16 * 3, action=ui.setUIEvenement, arguments=["debug"], anchorx="c", outlineColor="white", text="Debug", textColor="white", ID="debug")
    ui.addButton(RightXPos, render.HEIGHT_WINDOW / 16 * 5, action=ui.newPrompt, arguments=["Nom du fichier de sauvegarde", "Sauvegarder", True, IO.checkSaveName], anchorx="c", outlineColor="white", text="Sauvegarder", textColor="white", textSize=18)
    ui.addButton(RightXPos, render.HEIGHT_WINDOW - 1, action=logic.quitter, anchorx="c", anchory="d", outlineColor="white", text="Quitter", textColor="white")


def play():
    efface_tout()
    ui.reset()
    initGameUI()
    currentMap = IO.loadLevel(data)
    charlie, fallables, fall, end, startTime = start(data["map"])
    remainTime = startTime
    render.renderCanvas(data["map"], charlie)
    debug = False

    while True:
        ui.clearCanvas("black")
        event = donne_evenement()
        direction = (0, 0)
        if ui.focus is None:
            direction = logic.getDirection(event, debug)

        if direction == "reset" or ui.evenement == "reset":
            currentMap = IO.loadLevel()
            charlie, fallables, fall, end, startTime = start(data["map"])
            remainTime = startTime
            render.renderCanvas(data["map"], charlie)

            ui.evenement = None
            continue

        if direction == "debug" or ui.evenement == "debug":
            debug = (False if debug else True)
            print("DEBUG ACTIVATED" if debug else "DEBUG DEACTIVATED")

            ui.evenement = None
            continue

        if direction == "save":
            # ui.newPrompt("Nom de la sauvegarde:", "Sauvegarder")
            fileName = IO.save(data["map"], charlie, remainTime)
            print("Game saved to : ", fileName)
            continue

        if direction == "load":
            fileName, data["map"], charlie, remainTime = IO.loadSave()
            fallables = logic.findFallable(data["map"])
            fall = True
            end = logic.findEnd(data["map"])
            print("load from : ", fileName)
            continue

        if direction[0] != 0 or direction[1] != 0:
            charlie = logic.moveRockford(charlie, direction, data["map"], fallables, end)
            fall, charlie = logic.updatePhysic(fallables, False, charlie, data["map"])

        if fall:
            fall, charlie = logic.updatePhysic(fallables, fall, charlie, data["map"])

        remainTime = int(data["map"][0][0]) + int(startTime - logic.getTime())

        render.renderCanvas(data["map"], charlie)
        ui.logic(event)
        ui.updateStats(remainTime, (charlie["diamonds"], int(data["map"][0][1])))
        ui.render()
        #print(ui)
        mise_a_jour()
        logic.status(remainTime, data["map"][0][0])


def start(curMap):
    """
    initialise une partie

    :param list curMap: map actuel sous forme de liste

    >>> start([['150s', '1d'],['B', 'R', 'G'], ['.', 'E', 'D'], ['W', 'W', 'W']])
    ([(1, 1), 0], [(0, 1), (2, 2)], True)
    """
    initData()
    rockford = logic.findRockford(curMap)  # refactoring
    fallables = logic.findFallable(curMap)
    end = logic.findEnd(curMap)
    fall = True
    startTime = logic.getTime()
    return rockford, fallables, fall, end, startTime


def initData():
    global data
    data["map"] = None
    data["rockford"] = None
    data["diamonds"] = {}
    data["diamonds"]["onwed"] = None
    data["diamonds"]["total"] = None
    data["fall"] = {}
    data["fall"]["fallables"] = {}
    data["fall"]["fallables"]["pos"] = None
    data["fall"]["fallables"]["falling"] = None
    data["fall"]["fallings"] = None
    data["time"] = {}
    data["time"]["start"] = None
    data["time"]["remain"] = None
    data["end"] = None
    data["debug"] = None
    print(data)


