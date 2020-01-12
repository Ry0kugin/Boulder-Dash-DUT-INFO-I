import IO
import logic
import render
import ui
import uiElements
import evenement
import timer
import animation
import editor
import language
from random import randint
from upemtk import *
from uiElements import POLYGONS


data = {}
fps = 0

def initPlayMenu():
    """
    Initialise les éléments d'interface du menu de sélection de mode de jeu.
    """
    ui.addButton(1.2*render.WIDTH_WINDOW / 4, render.HEIGHT_WINDOW * 1/3, width=render.WIDTH_WINDOW / 2.8, height=int(render.HEIGHT_WINDOW / 2),  polygonal=POLYGONS["octo"], text=language.get("levelSelectionButton"), textSize=40, textColor="white", outlineColor="white", action=evenement.setGameEvent, arguments=["selection"])
    ui.addButton(2.8*render.WIDTH_WINDOW / 4, render.HEIGHT_WINDOW * 1/3, width=render.WIDTH_WINDOW / 2.8, height=int(render.HEIGHT_WINDOW / 2),  polygonal=POLYGONS["octo"], text=language.get("randomButton"), textSize=40, textColor="white", outlineColor="white", action=evenement.setGameEvent, arguments=["play"])
    ui.addButton(render.WIDTH_WINDOW / 2, render.HEIGHT_WINDOW * 2.3/3, width=render.WIDTH_WINDOW / 2.6, height=int(render.HEIGHT_WINDOW / 5),  polygonal=POLYGONS["octo"], text=language.get("loadFromSaveButton"), textSize=28, textColor="white", outlineColor="white", action=evenement.setGameEvent, arguments=["save"])


def initMenuUI():
    """
    Initialise les éléments d'interface du menu principal du jeu.
    """
    ui.setBackground("black")
    ui.addButton(render.WIDTH_WINDOW / 2, render.HEIGHT_WINDOW *0.8/3, width=render.WIDTH_WINDOW / 3, height=int(render.HEIGHT_WINDOW / 3), polygonal=POLYGONS["octo"], text=language.get("playButton"), textSize=42, textColor="white", outlineColor="white", action=playButton, ID="playButton")
    ui.addButton(render.WIDTH_WINDOW / 4, render.HEIGHT_WINDOW *1.8/3, width=render.WIDTH_WINDOW / 4, height=int(render.HEIGHT_WINDOW / 4), polygonal=POLYGONS["octo"], text=language.get("scoreButton"), textSize=28, textColor="white", outlineColor="white")
    ui.addButton(3*render.WIDTH_WINDOW / 4, render.HEIGHT_WINDOW *1.8/3, width=render.WIDTH_WINDOW / 4, height=int(render.HEIGHT_WINDOW / 4), polygonal=POLYGONS["octo"], text=language.get("editorButton"), textSize=28, textColor="white", outlineColor="white", action=evenement.setGameEvent, arguments=["editor"])
    ui.addButton(render.WIDTH_WINDOW / 2, render.HEIGHT_WINDOW - 30, width=150, height=50, polygonal=POLYGONS["octo"], text=language.get("quitButton"), textSize=18, textColor="white", outlineColor="white", anchor="sc", action=logic.quitter)
    ui.addButton(render.WIDTH_WINDOW - 85, render.HEIGHT_WINDOW - 10, polygonal=POLYGONS["octo"], text=language.get("settingsButton"), textSize=18, textColor="white", outlineColor="white", anchor="sc")
    ui.addButton(render.WIDTH_WINDOW*0.05, render.HEIGHT_WINDOW*0.05, polygonal=POLYGONS["trapeze-up"], width=render.WIDTH_WINDOW*0.10  ,text="FR", action=setLanguage, arguments=["fr", initMenuUI], outlineColor="white", textColor="white")
    ui.addButton(render.WIDTH_WINDOW*0.05, render.HEIGHT_WINDOW*0.15, polygonal=POLYGONS["trapeze-down"], width=render.WIDTH_WINDOW*0.10 , text="EN", action=setLanguage, arguments=["en", initMenuUI], outlineColor="white", textColor="white")
    # ui.addButton(render.WIDTH_WINDOW*0.1, render.HEIGHT_WINDOW*0.15, text=language.get("englishButton"), action=ui.setBackground, arguments=["green"], outlineColor="white", textColor="white")

def initSaveLevel(level):
    """
    Initialise les éléments d'interface du menu de sélection d'une partie sauvegardée.
    """
    ui.addButton(render.WIDTH_WINDOW * 0.1, render.HEIGHT_WINDOW / 2, width=70, height=100, fill="white", stroke=5, polygonal=POLYGONS["left-arrow"], action=setLevelDirection, arguments=["left", "leftButton"], ID="leftButton")
    ui.addButton(render.WIDTH_WINDOW * 0.9, render.HEIGHT_WINDOW / 2, width=70, height=100, fill="white", stroke=5, polygonal=POLYGONS["right-arrow"], action=setLevelDirection, arguments=["right", "rightButton"], ID="rightButton")
    ui.addButton(render.WIDTH_WINDOW/2, 7*render.HEIGHT_WINDOW/8, width=render.WIDTH_WINDOW/4, height=render.HEIGHT_WINDOW/7, text=language.get("playSelectedButton"), outlineColor="white", textColor="white", action=evenement.setGameEvent, arguments=["play"], ID="playButton")
    
    animation.new("leftButton", [0.1, 0.1], [{"x":render.WIDTH_WINDOW * 0.05}, {"x":render.WIDTH_WINDOW * 0.1}])
    animation.new("rightButton", [0.1, 0.1], [{"x":render.WIDTH_WINDOW * 0.95}, {"x":render.WIDTH_WINDOW * 0.9}])

    ui.addText(render.WIDTH_WINDOW/2, render.HEIGHT_WINDOW/9, "levelName", render.WIDTH_WINDOW/2, render.HEIGHT_WINDOW/8, text=" ", textColor="white", textSize=28)
    ui.addText(3*render.WIDTH_WINDOW/4, render.HEIGHT_WINDOW/9, "levelSelected", render.WIDTH_WINDOW/2, render.HEIGHT_WINDOW/8, text=" ", textColor="white", textSize=28)
    
    ui.addCanvas(render.WIDTH_WINDOW/2, render.HEIGHT_WINDOW/2, "levelSelection", width=0, height=0, squaresMap=level)


def initSelectionLevel(level):
    """
    Initialise les éléments d'interface du menu de sélection d'un niveau sauvegardé.
    """
    initSaveLevel(level)
    ui.setObject("playButton", {"x":render.WIDTH_WINDOW*0.37})
    ui.addButton(render.WIDTH_WINDOW*0.63, 7*render.HEIGHT_WINDOW/8, width=render.WIDTH_WINDOW/4, height=render.HEIGHT_WINDOW/7, text="Edit", outlineColor="white", textColor="white", action=evenement.setGameEvent, arguments=["edit"])
    # ui.addButton(render.WIDTH_WINDOW/2, 7*render.HEIGHT_WINDOW/8, width=render.WIDTH_WINDOW/4, height=render.HEIGHT_WINDOW/7, anchorx="c" ,anchory="c", text="Play", outlineColor="white", textColor="white", action=evenement.setGameEvent, arguments=["play"])

def setLanguage(lang, fc=None, args=[]):
    """
    Modifie la langue du jeu.
    :param string lang: Nom de la langue à mettre en place
    :param function fc: Fonction à éxécuter après la modification
    :param list args: Arguments de la fonction
    """
    language.setLocale(lang)
    ui.reset()
    if fc:
        fc(*args)

def setLevelDirection(direction, ID):
    """
    Anime le bouton 'ID' (de gauche ou droite en fonction de 'direction') du menu de sélection d'un niveau/sauvegarde.
    :param string direction: direction "left" ou "right"
    :param string ID: ID de l'objet
    """
    animation.start(ID)
    evenement.setGameEvent(direction)

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
    """
    Initialise les éléments d'interface d'une partie.
    """
    RightXPos = render.WIDTH_WINDOW * 2 / 2.2
    # Buttons
    ui.addButton(RightXPos, render.HEIGHT_WINDOW / 16, action=evenement.setGameEvent, arguments=["reset"], outlineColor="white", text=language.get("resetButton"), textColor="white", layer=1)
    ui.addButton(RightXPos, render.HEIGHT_WINDOW / 16 * 4, action=evenement.setGameEvent, arguments=["debug"], outlineColor="white", text=language.get("debugButton"), textColor="white", ID="debug", layer=1)
    ui.addButton(RightXPos, render.HEIGHT_WINDOW / 16 * 7, action=evenement.setGameEvent, arguments=["save"], outlineColor="white", text=language.get("saveButton"), textColor="white", textSize=18, layer=1)
    ui.addButton(RightXPos, render.HEIGHT_WINDOW - 1, action=logic.quitter, anchor="sc", outlineColor="white", text=language.get("quitButton"), textColor="white", layer=1)
    # Texts
    ui.addText(render.WIDTH_WINDOW*0.05, render.WIDTH_WINDOW*0.02, ID="timeLeftText", anchor="nw", textColor="green", textFont="Monospace")
    ui.addText(render.WIDTH_WINDOW*0.25, render.WIDTH_WINDOW*0.02, ID="diamondsText", anchor="nw", textColor="red", textFont="Monospace")
    ui.addText(render.WIDTH_WINDOW*0.45,  render.WIDTH_WINDOW*0.02, ID="scoreText", anchor='nw', textColor="purple", textFont="Monospace")
    # Game canvas
    ui.addCanvas(0, render.HEIGHT_WINDOW/8, ID="gameCanvas", width=0, height=0, anchor="nw", cellSize=32)

def handleEvenement(evenement, args=[]):
    """
    Lance l'action liée à un événement via le dictionnaire 'evenementHandler'.
    :param string evenement: Evenement à traiter
    :param list args: Liste d'arguments à passer en paramètre de la fonction finale
    """
    # evenement = "move" if evenement in ("Right", "Left", "Up", "Down")
    if evenement in ("reset", "move", "save", "load", "return"):
        if evenement!="return":
            evenementHandler[evenement](*args)
        return True
    return False

def resetGame():
    """
    Réinitialise la partie et les données associées à celle-ci.
    """
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

def play(level=None, mode="r"):
    """
    Lance une partie.
    :param string level: Nom du niveau à charger
    :param string mode: Type de partie à jouer ("r": random "s": save "l":level)
    """
    global data
    print(level)
    ui.reset()
    ui.setBackground("black")
    initGameUI()
    initData()
    data["mode"] = mode
    if level and mode=="s":
        IO.loadLevel(data, level)
    elif level and mode=="l":
        IO.loadSave(level, data)
    else: 
        IO.loadLevel(data)
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
        logic.updateGameStatus()
        if win and data["mode"] == "s":
            attente_clic_ou_touche()
            break
        elif win:
            IO.loadLevel(data)
            start(data, keepScore=True)
            render.update(data["map"][1::], "gameCanvas")
        elif win==False:
            break
        ui.render(getFps())
        mise_a_jour()
    ui.reset()
    initMenuUI()


    

def start(data, keepScore=False):
    """
    Initialise une partie.
    :param list curMap: map actuelle sous forme de liste

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
    """
    Initialise les données nécessaires à une partie.
    """
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
    """
    Calcule le nombre d'images par seconde.
    :param float delta: Temps écoulé entre l'image précédente et l'image actuelle
    """
    global fps
    if delta:
        fps = int(1/(delta))
    else:
        fps = "unlimited"

def getFps():
    """
    Retourne le nombre d'images par seconde actuel.
    """
    global fps
    return fps

def updateStats(remainTime, diamonds, score):
    """
    Met à jour les statistiques de la partie et les textes les affichant.
    :param int remainTime: Temps restant dans la partie
    :param tuple diamonds: Tuple contenant en position 0 le nombre de diamants ramassés et en position 1 le nombre de diamants dans la partie
    :param int score: Score actuel du joueur dans la partie
    """
    # Time left#
    ui.setObject("timeLeftText", {"text":language.get("timeText") + str(remainTime), "textColor":("green" if remainTime > 10 else "red")})
    # Diamonds#
    ui.setObject("diamondsText", {"text":language.get("diamondsText") + str(diamonds[0]) + "/" + str(diamonds[1]), "textColor":("red" if diamonds[0] < diamonds[1] else "green"), "x":ui.objects["timeLeftText"]["x"]+longueur_texte(ui.objects["timeLeftText"]["text"])})
    # Score#
    ui.setObject("scoreText", {"text":language.get("scoreText") + str(score), "x":ui.objects["diamondsText"]["x"]+longueur_texte(ui.objects["diamondsText"]["text"])})

def updateTime():
    """
    Met à jour tous les timers et calcule le nombre d'images par seconde.
    """
    delta = timer.update()
    computeFps(delta)
    return delta
