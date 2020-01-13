# -*- coding: utf-8 -*-
from upemtk import mise_a_jour, donne_evenement
import render, logic, ui, IO, game, animation, evenement, game, editor

###############################################################################

def move(levelSelected, levels, increment, load):
    levelSelected = (levelSelected + increment)%len(levels)
    moveRender(levels, levelSelected, load)
    return levelSelected

def moveRender(levels, levelSelected, load):
    ui.setObject("levelName", {"text": levels[levelSelected]})
    ui.setObject("levelSelected", {"text": str(levelSelected+1)+"/"+str(len(levels))})
    render.update(load(level=levels[levelSelected])[1::],"levelSelection")

def levelSelectionMenu():
    """
    Fait fonctionner le menu de sélection d'un niveau enregistré.
    """
    goInBlack()
    levels = IO.getLevels("level")
    levelSelected = 0
    level = IO.loadLevel(level=levels[0])
    game.initSelectionLevel(level)
    moveRender(levels, levelSelected, IO.loadLevel)
    while not evenement.event["game"] == 'return':
        evenement.compute()
        ui.logic(evenement.event["tk"])
        if evenement.event["game"] == "right":
            levelSelected = move(levelSelected, levels, 1, IO.loadLevel)
        elif evenement.event["game"] == "left":
            levelSelected = move(levelSelected, levels,-1, IO.loadLevel)
        elif evenement.event["game"] == "play":
            goInBlack()
            game.play(levels[levelSelected], "s")
            backInBlack(game.initSelectionLevel, [levels[levelSelected]])
            moveRender(levels, levelSelected, IO.loadLevel)
        elif evenement.event["game"] == "edit":
            goInBlack()
            editor.editor(levels[levelSelected])
            backInBlack(game.initSelectionLevel, [levels[levelSelected]])
            moveRender(levels, levelSelected, IO.loadLevel)
        game.updateTime()
        animation.update()
        ui.render(game.getFps())
        mise_a_jour()
    backInBlack(game.initPlayMenu)

def levelSaveMenu():
    """
    Fait fonctionner le menu de sélection d'une sauvegarde.
    """
    goInBlack()
    levels = IO.getLevels("save")
    levelSelected = 0
    level = IO.loadSave(levels[0])
    game.initSaveLevel(level)
    moveRender(levels, levelSelected, IO.loadSave)

    while not evenement.event["game"] == 'return':   
        evenement.compute()
        ui.logic(evenement.event["tk"])
        if evenement.event["game"] == "right":
            levelSelected = move(levelSelected, levels, 1,IO.loadSave)
        elif evenement.event["game"] == "left":
            levelSelected = move(levelSelected, levels,-1,IO.loadSave)
        elif evenement.event["game"] == "play":
            goInBlack()
            game.play(levels[levelSelected], "l")
            backInBlack(game.initSaveLevel, [levels[levelSelected]])
            moveRender(levels, levelSelected, IO.loadSave)
        game.updateTime()
        animation.update()
        ui.render(game.getFps())
        mise_a_jour()

    backInBlack(game.initPlayMenu)

def choicePlaystyleMenu():
    """
    Fait fonctionner le menu de sélection du mode de jeu.
    """
    while not evenement.event["game"] == 'return':   
        evenement.compute()
        ui.logic(evenement.event["tk"])
        # home:play:selection
        if evenement.event["game"] == 'selection':
            levelSelectionMenu()
        # home:play:save
        if evenement.event["game"] == 'save': 
            levelSaveMenu()
        # home:play:random
        if evenement.event["game"] == 'play':
            goInBlack()
            game.play(mode="r")
            backInBlack(game.initPlayMenu)

        game.updateTime()
        ui.render(game.getFps())
        mise_a_jour()



def scoresMenu():
    scores = IO.loadScore()
    levels = [key for key in scores["s"]]
    selected = 0
    game.initScores(scores)
    while not evenement.event["game"] == 'return':   
        evenement.compute()
        ui.logic(evenement.event["tk"])

        if evenement.event["game"] == "up":
            selected += 1
            for i in range(4):
                ui.setObject("ltext"+str(i+1), {"text": levels[(selected+i)%len(levels)] + " - "+ str(scores["s"][levels[(selected+i)%len(levels)]][0]) + "\n\t"+scores["s"][levels[(selected+i)%len(levels)]][1]})
        elif evenement.event["game"] == "down":
            selected -= 1 
            for i in range(4):
                ui.setObject("ltext"+str(i+1), {"text": levels[(selected+i)%len(levels)] + " - "+ str(scores["s"][levels[(selected+i)%len(levels)]][0]) + "\n\t"+scores["s"][levels[(selected+i)%len(levels)]][1]})

        game.updateTime()
        animation.update()
        ui.render(game.getFps())
        mise_a_jour()

def goInBlack(go=None):
    """
    Réinitialise l'UI et met le fond d'interface en noir.
    """
    animation.clearAnimation()
    ui.reset()
    ui.setBackground("black")
    if go:
        go()

def backInBlack(back, args=[]): # AC / DC
    """
    Réinitialise l'UI, met le fond d'interface en noir, exécute la fonctions spécifiée avec ses arguments et réinitialise les événements de jeu.
    :param function back: Fonction à éxecuter
    :param list args: Liste des arguments de la fonction back
    """
    goInBlack()
    back(*args)
    evenement.resetGameEvent()
    
        
if __name__ == '__main__':
    render.initWindow()
    # home
    game.initMenuUI()
    while not evenement.event["game"] == 'return':
        # ev=donne_evenement()
        # if ev[0]!='RAS':
        #     print(ev)
        evenement.compute()
        ui.logic(evenement.event["tk"])
        # home:play
        if evenement.event["game"] == 'play':
            goInBlack(game.initPlayMenu)
            choicePlaystyleMenu()
            backInBlack(game.initMenuUI)
        # home:editor
        elif evenement.event["game"] == 'editor':
            goInBlack()
            editor.editor()
            backInBlack(game.initMenuUI)
        elif evenement.event["game"] == 'score':
            goInBlack()
            scoresMenu()
            backInBlack(game.initMenuUI)
            
        game.updateTime()
        animation.update() # /!\ render.updateAnimations before ui.render
        ui.render(game.getFps())
        mise_a_jour()




###############################################################################



        

###############################################################################
