# -*- coding: utf-8 -*-
from upemtk import mise_a_jour
import render, logic, ui, IO, game, animation, evenement, game, editor

###############################################################################

def move(levelSelected, levels, increment):
    levelSelected = (levelSelected + increment)%len(levels)
    moveRender(levels, levelSelected)
    return levelSelected

def moveRender(levels, levelSelected):
    ui.setObject("levelName", {"text": levels[levelSelected]})
    ui.setObject("levelSelected", {"text": str(levelSelected+1)+"/"+str(len(levels))})
    render.update(IO.loadLevel(level=levels[levelSelected])[1::],"levelSelection")

def choicePlaystyle():
    while not evenement.event["game"] == 'return':   
        evenement.compute()
        ui.logic(evenement.event["tk"])
        # home-play-selection
        if evenement.event["game"] == 'selection':
            ui.reset()
            ui.setBackground("black")
            levels = IO.getLevels("level")
            levelSelected = 0
            level = IO.loadLevel(level=levels[0])
            game.initSelectionLevel(level)
            moveRender(levels, levelSelected)

            while not evenement.event["game"] == 'return':   
                evenement.compute()
                ui.logic(evenement.event["tk"])
                if evenement.event["game"] == "right":
                    levelSelected = move(levelSelected, levels, 1)
                elif evenement.event["game"] == "left":
                    levelSelected = move(levelSelected, levels,-1)
                elif evenement.event["game"] == "play":
                    goInBlack()
                    game.play(levels[levelSelected])
                    backInBlack(game.initSelectionLevel, [levels[levelSelected]])
                    moveRender(levels, levelSelected)
                game.updateTime()
                ui.render(game.getFps())
                mise_a_jour()

            backInBlack(game.initPlayMenu)
        # home-play-random
        if evenement.event["game"] == 'play':
            ui.reset()
            ui.setBackground("black")

            game.play()

            backInBlack(game.initPlayMenu)

        game.updateTime()
        ui.render(game.getFps())
        mise_a_jour()


def goInBlack(go=None):
    ui.reset()
    ui.setBackground("black")
    if go:
        go()

def backInBlack(back, args=[]): # AC / DC
    ui.reset()
    ui.setBackground("black")
    back(*args)
    evenement.resetGameEvent()
    
        
if __name__ == '__main__':
    render.initWindow()
    # home
    game.initMenuUI()
    while not evenement.event["game"] == 'return':
        evenement.compute()
        ui.logic(evenement.event["tk"])
        # home-play
        if evenement.event["game"] == 'play':
            goInBlack(game.initPlayMenu)

            choicePlaystyle()

            backInBlack(game.initMenuUI)
        
        elif evenement.event["game"] == 'editor':
            goInBlack()
            
            editor.editor()

            backInBlack(game.initMenuUI)
            
        animation.update() # /!\ render.updateAnimations before ui.render
        game.updateTime()
        ui.render(game.getFps())
        mise_a_jour()




###############################################################################



        

###############################################################################
