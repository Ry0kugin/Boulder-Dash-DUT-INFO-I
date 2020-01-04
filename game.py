import IO
import logic
import render
import ui
from upemtk import *


def menu():
    while True:
        event = donne_evenement()
        ui.addButton(render.WIDTH_WINDOW / 2, render.HEIGHT_WINDOW / 2, text="Jouer", textSize=18)
        ui.logic(event)
        ui.render()
        mise_a_jour()


def initGameUI():
    RightXPos = render.WIDTH_WINDOW * 2 / 3 + (render.WIDTH_WINDOW / 3 / 2)
    ui.addButton(RightXPos, render.HEIGHT_WINDOW / 16, action=ui.setUIEvenement, arguments=["reset"], anchorx="c",
                 outlineColor="white", text="Reset", textColor="white")
    ui.addButton(RightXPos, render.HEIGHT_WINDOW / 16 * 3, action=ui.setUIEvenement, arguments=["debug"], anchorx="c",
                 outlineColor="white", text="Debug", textColor="white", ID="debug")
    ui.addButton(RightXPos, render.HEIGHT_WINDOW / 16 * 5, action=ui.newPrompt,
                 arguments=["Nom du fichier de sauvegarde", "Sauvegarder", True, IO.checkSaveName], anchorx="c",
                 outlineColor="white", text="Sauvegarder", textColor="white", textSize=18)
    ui.addButton(RightXPos, render.HEIGHT_WINDOW - 1, action=logic.quitter, anchorx="c", anchory="d",
                 outlineColor="white", text="Quitter", textColor="white")


def startGame():
    initGameUI()
    currentMap = IO.loadLevel()
    charlie, fallables, fall, end, startTime = logic.start(currentMap)
    remainTime = startTime
    render.renderCanvas(currentMap, charlie)
    debug = False

    while True:
        event = donne_evenement()

        direction = (0, 0)
        if ui.focus is None:
            direction = logic.getDirection(event, debug)

        if direction == "reset" or ui.evenement == "reset":
            currentMap = IO.loadLevel()
            charlie, fallables, fall, end, startTime = logic.start(currentMap)
            remainTime = startTime
            render.renderCanvas(currentMap, charlie)

            ui.evenement = None
            continue

        if direction == "debug" or ui.evenement == "debug":
            debug = (False if debug else True)
            print("DEBUG ACTIVATED" if debug else "DEBUG DEACTIVATED")

            ui.evenement = None
            continue

        if direction == "save":
            # ui.newPrompt("Nom de la sauvegarde:", "Sauvegarder")
            fileName = IO.save(currentMap, charlie, remainTime)
            print("Game saved to : ", fileName)
            continue

        if direction == "load":
            fileName, currentMap, charlie, remainTime = IO.loadSave()
            fallables = logic.findFallable(currentMap)
            fall = True
            end = logic.findEnd(currentMap)
            print("load from : ", fileName)
            continue

        if direction[0] != 0 or direction[1] != 0:
            charlie = logic.moveRockford(charlie, direction, currentMap, fallables, end)
            fall, charlie = logic.updatePhysic(fallables, False, charlie, currentMap)

        if fall:
            fall, charlie = logic.updatePhysic(fallables, fall, charlie, currentMap)

        remainTime = int(currentMap[0][0]) + int(startTime - logic.getTime())

        render.renderCanvas(currentMap, charlie)
        ui.logic(event)
        ui.updateStats(remainTime, (charlie[1], int(currentMap[0][1])))
        ui.render()
        mise_a_jour()
        logic.status(remainTime, currentMap[0][0])
