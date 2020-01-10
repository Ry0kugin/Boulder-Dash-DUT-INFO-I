# -*- coding: utf-8 -*-
from upemtk import mise_a_jour
import render, logic, ui, IO, game, animation, evenement, game, editor

###############################################################################

######## Menu ########


if __name__ == '__main__':
    render.initWindow()
    # home
    game.initMenuUI()
    animation.animate("playButton", [2.5, 5, 2.5], [{"x":render.WIDTH_WINDOW*0.25}, {"x":render.WIDTH_WINDOW*0.75}, {"x":ui.objects["playButton"]["x"]}])
    while not evenement.event["game"] == 'return':
        evenement.compute()
        ui.logic(evenement.event["tk"])
        # home-play
        if evenement.event["game"] == 'play':
            ui.reset()
            ui.setBackground("black")
            game.initPlayMenu()

            while not evenement.event["game"] == 'return':   
                evenement.compute()
                ui.logic(evenement.event["tk"])
                # home-play-selection
                if evenement.event["game"] == 'selection':
                    ui.reset()
                    ui.setBackground("black")
                    levels = IO.getLevels("level")
                    level = IO.loadLevel(level=levels[1])
                    game.initSelectionLevel(level)
                    render.update(level[1::],"levelSelection")

                    while not evenement.event["game"] == 'return':   
                        evenement.compute()
                        ui.logic(evenement.event["tk"])
                        if evenement.event["game"] == "right":
                            ui.setObject("levelName", {"text": "gueeeuuuu"})
                            render.update(IO.loadLevel()[1::] ,"levelSelection")
                        elif evenement.event["game"] == "left":
                            ui.setObject("levelName", {"text": "guaaaauu"})
                            render.update(IO.loadLevel()[1::],"levelSelection")
                        game.updateTime()
                        ui.render(game.getFps())
                        mise_a_jour()

                    ui.reset() 
                    ui.setBackground("black")
                    game.initPlayMenu()
                    evenement.resetGameEvent()
                # home-play-random
                if evenement.event["game"] == 'play':
                    ui.reset()
                    ui.setBackground("black")

                    game.play()

                    ui.reset()
                    ui.setBackground("black")
                    game.initPlayMenu()
                    evenement.resetGameEvent()

                game.updateTime()
                ui.render(game.getFps())
                mise_a_jour()
            ui.reset()
            ui.setBackground("black")
            game.initMenuUI()
            evenement.resetGameEvent()
        
        elif evenement.event["game"] == 'editor':
            ui.reset()
            ui.setBackground("black")
            
            editor.editor()

            ui.reset()
            ui.setBackground("black")
            game.initMenuUI()
            evenement.resetGameEvent()
            
        animation.update() # /!\ render.updateAnimations before ui.render
        game.updateTime()
        ui.render(game.getFps())
        mise_a_jour()


###############################################################################



        

###############################################################################
