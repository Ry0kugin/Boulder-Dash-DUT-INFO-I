# -*- coding: utf-8 -*-

from upemtk import *
from time import *
import render, logic, ui, IO


###############################################################################

if __name__ == '__main__':
    render.initWindow()
    ui.initUI()

    currentMap = IO.loadLevel()

    charlie, fallables, fall, end, startTime = logic.start(currentMap)
    remainTime = startTime
    render.renderCanvas(currentMap, charlie)
    debug = False

    while True:
        event=donne_evenement()

        direction = (0,0)
        if ui.focus == None:
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
            print ("DEBUG ACTIVATED" if debug else "DEBUG DEACTIVATED")

            ui.evenement = None
            continue

        if direction == "save":
            fileName = IO.save(currentMap, charlie, remainTime)
            print ("saved to : ", fileName)
            continue
    
        if direction == "load":
            fileName, currentMap, charlie, remainTime = IO.loadSave()
            fallables = logic.findFallable(currentMap)
            fall = True
            end = logic.findEnd(currentMap)
            print("load from : ", fileName)
            continue

        if(direction[0] != 0 or direction[1] != 0):
            charlie = logic.moveRockford(charlie, direction, currentMap, fallables, end)
            fall, charlie = logic.updatePhysic(fallables, False, charlie, currentMap)

        if fall:
            fall, charlie = logic.updatePhysic(fallables, fall, charlie, currentMap)

        remainTime = int(currentMap[0][0]) + int(startTime - logic.getTime())

        render.renderCanvas(currentMap, charlie)
        ui.logicUI(event)
        ui.updateStats(remainTime, (charlie[1], int(currentMap[0][1])))
        ui.renderUI()
        mise_a_jour()
        logic.status(remainTime, currentMap[0][0])
        

###############################################################################
