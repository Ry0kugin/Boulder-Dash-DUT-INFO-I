from upemtk import mise_a_jour, type_evenement , clic_x, clic_y
import ui, game, render, evenement, logic, IO, timer, language

######## Editor ########

def initEditorUI():
    """
    Initialise les éléments d'interface de l'éditeur de niveau.
    """
    RightXPos = render.WIDTH_WINDOW * 2 / 2.2
    # Buttons
    ui.addButton(RightXPos, render.HEIGHT_WINDOW / 16, action=evenement.setGameEvent, arguments=["reset"], anchorx="c", outlineColor="white", text=language.get("resetButton"), textColor="white", layer=1)
    ui.addButton(RightXPos, render.HEIGHT_WINDOW, action=evenement.setGameEvent, arguments=["save"], anchorx="c", anchory="d",outlineColor="white", text="Sauvegarder", textSize=15, textColor="white", layer=1)
    # Texts
    ui.addText(render.WIDTH_WINDOW*0.05, render.WIDTH_WINDOW*0.02, ID="timeLeftText", anchorx="l", anchory="u", textColor="green", text=language.get("timeText"), textFont="Monospace")
    # textFields
    ui.addTextField(ui.objects["timeLeftText"]["bx"], 0, ID="timeLeftTextField", anchorx="l", anchory="u", outlineColor="white")
    #ui.addText(render.WIDTH_WINDOW / 4.2, 0, ID="diamondsText", anchory="u", textColor="red")
    #ui.addText(render.WIDTH_WINDOW / 2, 0, ID="scoreText", anchory="u", textColor="yellow")
    # Game canvas
    ui.addCanvas(0, render.HEIGHT_WINDOW/8, ID="editorCanvas", width=0, height=0, fill="green", anchorx="l", anchory="u")
    ui.addCanvas(RightXPos, render.HEIGHT_WINDOW/8, ID="blockCanvas", width=0, height=0, fill="red", anchorx="c", anchory="u", cellSize=64, selected=[(0,0)])
    # cursor routine
    # ui.addLogicRoutine("editorCursor", updateCursor)

def editor(level=None):
    """
    Lance et fait fonctionner l'éditeur de niveau.
    :param list level: Niveau à charger
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
    render.update((IO.loadLevel(level=level)[1:] if level else [["." for x in range(editorWidth)] for y in range(editorHeight)]), "editorCanvas")
    render.update(blockMap, "blockCanvas")
    onPressed=False
    while not evenement.event["game"] == 'return':
        evenement.compute()
        ui.logic(evenement.event["tk"])
        tkEvent=evenement.getTkEvent()
        # print(type(ui.objects["blockCanvas"]["selected"]))
        if ui.focus is None:
            updateCursor(tkEvent, "editorCanvas", ui.objects["blockCanvas"]["squaresMap"][ui.objects["blockCanvas"]["selected"][0][1]][ui.objects["blockCanvas"]["selected"][0][0]], onPressed)
            updateCursor(tkEvent, "blockCanvas")
            # print(evenement.event["game"])
            if evenement.event["game"] == "reset":
                render.update([["." for x in range(editorWidth)] for y in range(editorHeight)], "editorCanvas")
                # ui.render(game.getFps())
                # continue
            elif evenement.event["game"] == "save":
                timer.factor = 0
                if level:
                    IO.save(ui.objects["editorCanvas"]["squaresMap"], level[1])
                else:
                    ui.newPrompt("Nom de la sauvegarde:", "Sauvegarder", success=lambda: IO.save(game.data, ui.objects["prompt_2"]["text"]), checker=IO.checkSaveName, anyway=lambda: timer.setFactor(1))
            if type_evenement(tkEvent)=="Deplacement":
                if "|" in str(tkEvent):
                    onPressed=True
                else:
                    onPressed=False

        game.updateTime()
        ui.render(game.getFps())
        mise_a_jour()
    ui.reset()


def writeMultipleBlocks(canvas, squaresMap, block):
    """
    Ecrit plusieurs blocs sur le canvas donné.
    :param string canvas: ID du canvas cible
    :param list squaresMap: Matrice du niveau
    :param string block: type de bloc à placer
    """
    for p in ui.objects["editorCanvas"]["selected"]:
        squaresMap[p[1]][p[0]]=block
    ui.setObject(canvas, {"selected":None})
    return squaresMap

def updateCursor(ev, canvas, block=None, onPressed=False):
    """
    Met à jour la position du curseur dans la matrice de l'éditeur de niveau.
    :param tuple ev: Evenement donné par upemtk
    :param string canvas: ID du canvas cible
    :param string block: type de bloc
    :param bool onPressed: condition vraie si le clic de la souris est resté enfoncé
    """
    evType=type_evenement(ev)
    # print(ev)
    # print(ui.objects["editorCanvas"]["selected"])
    if evType in ("Deplacement", "ClicGauche"):
        pos=[clic_x(ev), clic_y(ev)]
        multiSelection=ui.objects["editorCanvas"]["selected"] and len(ui.objects["editorCanvas"]["selected"])>1
        squaresMap=ui.objects[canvas]["squaresMap"]
        if ui.objects[canvas]["ax"] < pos[0] < ui.objects[canvas]["bx"]-1 and ui.objects[canvas]["ay"] < pos[1] < ui.objects[canvas]["by"]-1:
            
            x=int((pos[0]-ui.objects[canvas]["ax"])/ui.objects[canvas]["cellSize"])
            y=int((pos[1]-ui.objects[canvas]["ay"])/ui.objects[canvas]["cellSize"])
            if block:
                # print("inSquare")
                if not onPressed:
                    if multiSelection:
                        squaresMap=writeMultipleBlocks(canvas, squaresMap, block)
                    else:
                        ui.setObject(canvas, {"selected":[(x,y)]})
                else:
                    ui.setObject(canvas, {"selected":list(set((*ui.objects["editorCanvas"]["selected"],(x,y))))})
                    # ui.setObject(canvas, {"selected":[*ui.objects["editorCanvas"]["selected"],(x,y)]}) # Bad memory usage
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
                # print("notinSquare")
                if multiSelection:
                    squaresMap=writeMultipleBlocks(canvas, squaresMap, block)
                    render.update(squaresMap, canvas)
                    # onPressed=False
                    # return onPressed
                ui.setObject(canvas, {"selected":None})
            else:
                ui.setObject(canvas, {"selected":[ui.objects["blockCanvas"]["selected"][0], None]})
        # return onPressed
        
           
    
