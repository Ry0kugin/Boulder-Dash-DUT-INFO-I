from upemtk import mise_a_jour, type_evenement , clic_x, clic_y
import ui, game, render, evenement, logic, IO

######## Editor ########

def initEditorUI():
    RightXPos = render.WIDTH_WINDOW * 2 / 2.2
    # Buttons
    ui.addButton(RightXPos, render.HEIGHT_WINDOW / 16, action=evenement.setGameEvent, arguments=["reset"], anchorx="c", outlineColor="white", text="Reset", textColor="white", layer=1)
    ui.addButton(RightXPos, render.HEIGHT_WINDOW, action=evenement.setGameEvent, arguments=["save"], anchorx="c", anchory="d",outlineColor="white", text="Sauvegarder", textSize=15, textColor="white", layer=1)
    # Texts
    ui.addText(0, 0, ID="timeLeftText", anchorx="l", anchory="u", textColor="green", text="Time left:")
    # textFields
    ui.addTextField(ui.objects["timeLeftText"]["bx"], 0, ID="timeLeftTextField", anchorx="l", anchory="u", outlineColor="white")
    #ui.addText(render.WIDTH_WINDOW / 4.2, 0, ID="diamondsText", anchory="u", textColor="red")
    #ui.addText(render.WIDTH_WINDOW / 2, 0, ID="scoreText", anchory="u", textColor="yellow")
    # Game canvas
    ui.addGameCanvas(0, render.HEIGHT_WINDOW/8, ID="gameCanvas", width=0, height=0, fill="green", anchorx="l", anchory="u")
    # cursor routine
    # ui.addLogicRoutine("editorCursor", updateCursor)

def editor():
    ui.reset()
    ui.setBackground("black")
    initEditorUI()
    game.initData()
    render.update(IO.loadLevel(level="level_1")[1::],"gameCanvas")
    #IO.loadLevel(data)
    # start(data)
    # render.update(data["map"], "gameCanvas")

    while not evenement.event["game"] == 'return':
        evenement.compute()
        ui.logic(evenement.event["tk"])
        updateCursor()
        # direction = (0, 0)
        if ui.focus is None:
            # timer.start("game")
            # direction = logic.getDirection(evenement.event["tk"], data["debug"])

            if evenement.event["game"] == "reset" or ui.evenement == "reset":
                game.initData()
                IO.loadLevel(data)
                start(data)
                render.update(data["map"][1::], "gameCanvas")
                ui.render()
                

                ui.evenement = None
                continue

            # if evenement.event["game"] == "move":
            #     logic.moveRockford(data, direction)
            #     data["fall"]["fallings"] = True
            #     render.update(data["map"], "gameCanvas")
                
            # print("before after before", timer.getTimer("fallings", remain=True), timer.isOver("fallings"))
            # if data["fall"]["fallings"] and timer.isOver("fallings"):
            #     print("before", timer.getTimer("fallings", remain=True))
            #     logic.updatePhysic(data)
            #     print("after", timer.getTimer("fallings", remain=True))
            #     render.update(data["map"], "gameCanvas")

            if evenement.event["game"] == "save":
                timer.factor = 0
                ui.newPrompt("Nom de la sauvegarde:", "Sauvegarder", success=lambda: IO.save(game.data, ui.objects["prompt_2"]["text"]), checker=IO.checkSaveName, anyway=lambda: timer.setFactor(1))
                #fileName = IO.save(data)
                continue

            if evenement.event["game"] == "load":
                timer.pause("game") 
                fileName = IO.loadSave(data)
                logic.findFallable(data)
                logic.findEnd(
                    
                    data)
                print("load from : ", fileName)
                continue
        # if evenement.event["game"] == "debug" or ui.evenement == "debug":
        #     debug = (False if debug else True)
        #     print("DEBUG ACTIVATED" if debug else "DEBUG DEACTIVATED")

        #     ui.evenement = None
        #     continue

        # updateStats(data["time"]["remain"], (data["diamonds"]["owned"], int(data["map"][0][1])), data["score"])
        # game.updateTime()
        # data["time"]["remain"] = timer.getTimer("game", int, remain=True)
        #print(timer.timers["game"]["progression"])
        # if logic.status(data):
        #     logic.updateGameStatus()
        #     IO.loadLevel(data)
        #     start(data, keepScore=True)
        #     render.update(data["map"], "gameCanvas")
        game.updateTime()
        ui.render(game.getFps())
        mise_a_jour()
    ui.reset()
    #game.initPlayMenu()


def updateCursor():
    ev=evenement.getTkEvent()
    if type_evenement(ev)=="Deplacement":
        pos=[clic_x(ev), clic_y(ev)]
        if ui.objects["gameCanvas"]["ax"] < pos[0] < ui.objects["gameCanvas"]["bx"] and ui.objects["gameCanvas"]["ay"] < pos[1] < ui.objects["gameCanvas"]["by"]:
            # pos[0]=pos[0]-ui.objects["gameCanvas"]["ax"]
            # pos[1]=pos[1]-ui.objects["gameCanvas"]["ay"]
            x=int((pos[0]-ui.objects["gameCanvas"]["ax"])/render.CELL_SIZE)
            y=int((pos[1]-ui.objects["gameCanvas"]["ay"])/render.CELL_SIZE)
            #currentMap=ui.objects["gameCanvas"]["squaresMap"]
            # print("cellSize - ", render.CELL_SIZE)
            # print("pos 1 - ", x)
            # print("pos 2 - ", y)
            # currentMap[int(ui.objects["gameCanvas"]["height"]/len(ui.objects["gameCanvas"]["squaresMap"]))+1][int(ui.objects["gameCanvas"]["width"]/len(ui.objects["gameCanvas"]["squaresMap"][0]))+1]='W'
            ui.setObject("gameCanvas", {"selected":(x,y)})
            # ui.objects["gameCanvas"]["selected"] = (x,y) 
            # ui.setObject("gameCanvas", {"squaresMap":currentMap})
            # render.update(currentMap ,"gameCanvas")
        else:
            ui.setObject("gameCanvas", {"selected":None})
            
    pass
