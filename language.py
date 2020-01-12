locale = "fr"
dictionnary = {
    "fr": {
        "playButton":"Jouer",
        "scoreButton":"Scores",
        "editorButton":"Editeur",
        "levelSelectionButton": "Selection\nniveau",
        "quitButton": "Quitter",
        "randomButton": "Aléatoire\nInfini",
        "loadFromSaveButton": "Depuis sauvegarde",
        "playSelectedButton": "Lancer",
        "settingsButton": "Paramètres",
        "timeText": "Temps restant: ",
        "diamondsText": "Diamants: ",
        "scoreText": "score: ",
        "frenchButton": "Français",
        "englishButton": "English",
        "resetButton": "Réinitialiser",
        "debugButton": "Déboguer",
        "saveButton": "Sauvegarder"
    },
    "en": {
        "playButton":"Play",
        "scoreButton":"Scores",
        "editorButton":"Editor",
        "quitButton": "Quit",
        "levelSelectionButton": "Select\nLevel",
        "randomButton": "unlimited\nRandom",
        "loadFromSaveButton": "Load from Save",
        "playSelectedButton": "Launch",
        "settingsButton": "Settings",
        "timeText": "Time left: ",
        "diamondsText": "Diamonds: ",
        "scoreText": "score: ",
        "frenchButton": "Français",
        "englishButton": "English",
        "resetButton": "Reset",
        "debugButton": "Debug",
        "saveButton": "Save"
    }
}

def get(ID):
    """
    """
    try:
        return dictionnary[locale][ID]
    except KeyError as e:
        print("Language Warning: cannot get ID", e, "defaulting to empty string")
        return ""

def setLocale(name):
    global locale
    try:
        dictionnary[name]
    except KeyError as e:
        print("Language Warning: cannot set unknown locale", e, "defaulting to previous locale")
        return
    locale = name
