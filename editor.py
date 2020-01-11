from upemtk import mise_a_jour, type_evenement , clic_x, clic_y
import ui, game, render, evenement, logic, IO, timer

######## Editor ########

def initEditorUI():
    RightXPos = render.WIDTH_WINDOW * 2 / 2.2
    # Buttons
    ui.addButton(RightXPos, render.HEIGHT_WINDOW / 16, action=evenement.setGameEvent, arguments=["reset"], anchorx="c", outlineColor="white", text="Reset", textColor="white", layer=1)
    ui.addButton(RightXPos, render.HEIGHT_WINDOW, action=evenement.setGameEvent, arguments=["save"], anchorx="c", anchory="d",outlineColor="white", text="Sauvegarder", textSize=15, textColor="white", layer=1)
    # Texts
    ui.addText(0, 0, ID="timeLeftText", anchorx="l", anchory="u", textColor="green", text="Time left:", textFont="Monospace")
    # textFields
    ui.addTextField(ui.objects["timeLeftText"]["bx"], 0, ID="timeLeftTextField", anchorx="l", anchory="u", outlineColor="white")

    #ui.addText(render.WIDTH_WINDOW / 4.2, 0, ID="diamondsText", anchory="u", textColor="red")
    #ui.addText(render.WIDTH_WINDOW / 2, 0, ID="scoreText", anchory="u", textColor="yellow")
    # Game canvas
    ui.addGameCanvas(0, render.HEIGHT_WINDOW/8, ID="editorCanvas", width=0, height=0, fill="green", anchorx="l", anchory="u")
    ui.addGameCanvas(RightXPos, render.HEIGHT_WINDOW/8, ID="blockCanvas", width=0, height=0, fill="red", anchorx="c", anchory="u", cellSize=64, selected=[(0,0)])
    # cursor routine
    # ui.addLogicRoutine("editorCursor", updateCursor)

def editor(squaresMap=None):
    """
    :param tuple squaresMap: (map, filename)
    """
    ui.reset()
    ui.setBackground("black")
    initEditorUI()
    blockMap=[
        ["W", "G"],
        [".", "B"],
        ["D", "X"],
        ["R", "E"],
        ]
    editorWidth = 20
    editorHeight = 12
    render.update((squaresMap if squaresMap else [["." for x in range(editorWidth)] for y in range(editorHeight)]), "editorCanvas")
    render.update(blockMap, "blockCanvas")
    while not evenement.event["game"] == 'return':
        evenement.compute()
        ui.logic(evenement.event["tk"])
        # print(type(ui.objects["blockCanvas"]["selected"]))
        updateCursor(evenement.getTkEvent(), "editorCanvas", ui.objects["blockCanvas"]["selected"][0])
        updateCursor(evenement.getTkEvent(), "blockCanvas")
        if ui.focus is None:
            # print(evenement.event["game"])
            if evenement.event["game"] == "reset":
                render.update([["." for x in range(editorWidth)] for y in range(editorHeight)], "editorCanvas")
                # ui.render(game.getFps())
                # continue
            elif evenement.event["game"] == "save":
                timer.factor = 0
                if squaresMap:
                    IO.save(ui.objects["editorCanvas"]["squaresMap"], squaresMap[1])
                else:
                    ui.newPrompt("Nom de la sauvegarde:", "Sauvegarder", success=lambda: IO.save(game.data, ui.objects["prompt_2"]["text"]), checker=IO.checkSaveName, anyway=lambda: timer.setFactor(1))
                continue
        game.updateTime()
        ui.render(game.getFps())
        mise_a_jour()
    ui.reset()


def updateCursor(ev, canvas, block=None):
    evType=type_evenement(ev)
    # print(type_evenement(ev))
    if evType in ("Deplacement", "ClicGauche"):
        pos=[clic_x(ev), clic_y(ev)]
        if ui.objects[canvas]["ax"] < pos[0] < ui.objects[canvas]["bx"] and ui.objects[canvas]["ay"] < pos[1] < ui.objects[canvas]["by"]:
            squaresMap=ui.objects[canvas]["squaresMap"]
            x=int((pos[0]-ui.objects[canvas]["ax"])/ui.objects[canvas]["cellSize"])
            y=int((pos[1]-ui.objects[canvas]["ay"])/ui.objects[canvas]["cellSize"])
            if block:
                ui.setObject(canvas, {"selected":[(x,y)]})
            else:
                ui.setObject(canvas, {"selected":[ui.objects["blockCanvas"]["selected"][0], (x,y)]})
            if evType == "ClicGauche":
                if block:
                    squaresMap[y][x]=block
                else:
                    ui.setObject(canvas, {"selected":[(x,y),ui.objects["blockCanvas"]["selected"][1]]})
                render.update(squaresMap, canvas)
        else:
            if block:
                ui.setObject(canvas, {"selected":None})
            else:
                ui.setObject(canvas, {"selected":[ui.objects["blockCanvas"]["selected"][0], None]})
           
            
    pass
