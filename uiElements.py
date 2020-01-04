from upemtk import rectangle, texte

objects = {}
positions = {0: {}}
renderQueue = {0: set()}
focus = None
exclusiveLayer = None
evenement = None
buttonCount = 0
textFieldCount = 0
textCount = 0
panelCount = 0


######## Objects ########
def addObject(x, y, ID, layer, width, height, anchorx, anchory, outlineColor=None, fill=None, stroke=None, hidden=None,
              isChild=None, otype=None):
    global objects, renderQueue, positions
    objects[ID] = {
        "x": (x if anchorx == "c" else (x - width / 2 if anchorx == "r" else x + width / 2)),
        "y": (y if anchory == "c" else (y + height / 2 if anchory == "u" else y - height / 2)),
        "ax": (x - width / 2 if anchorx == "c" else (x - width if anchorx == "r" else x)),
        "ay": (y - height / 2 if anchory == "c" else (y + width / 2 if anchory == "u" else y - height)),
        "bx": (x + width / 2 if anchorx == "c" else (x if anchorx == "r" else x + width)),
        "by": (y + height / 2 if anchory == "c" else (y + height * 2 if anchory == "u" else y)),
        "width": width,
        "height": height,
        "anchorx": anchorx,
        "anchory": anchory,
        "outlineColor": outlineColor,
        "fill": fill,
        "stroke": stroke,
        "hidden": hidden,
        "layer": layer,
        "type": otype,
        "isChild": isChild
    }
    try:
        renderQueue[layer]
    except KeyError:
        renderQueue[layer] = set()
    renderQueue[layer].add(ID)

    try:
        positions[layer]
    except KeyError:
        positions[layer] = {}
    positions[layer][ID] = [
        [objects[ID]["ax"], objects[ID]["bx"]],
        [objects[ID]["ay"], objects[ID]["by"]]
    ]


def setObject(ID, parameters):
    """
    Modifie un ou plusieurs paramètres d'un objet.
    :param str ID: ID de l'objet
    :param dict parameters: Paramètres à modifier
    """
    assert type(ID) == str
    assert type(parameters) == dict
    global objects, renderQueue
    for p in parameters:
        objects[ID][p] = parameters[p]
        if p == "x" or p == "width":
            width = objects[ID]["width"]
            x = objects[ID]["x"]
            anchorx = objects[ID]["anchorx"]
            objects[ID]["ax"] = (x - width / 2 if anchorx == "c" else (x - width if anchorx == "r" else x))
            objects[ID]["bx"] = (x + width / 2 if anchorx == "c" else (x if anchorx == "r" else x + width))
        elif p == "y" or p == "height":
            height = objects[ID]["height"]
            y = objects[ID]["y"]
            anchory = objects[ID]["anchory"]
            objects[ID]["ay"] = (y - height / 2 if anchory == "c" else (y if anchory == "u" else y - height))
            objects[ID]["by"] = (y + height / 2 if anchory == "c" else (y + height if anchory == "u" else y))
        elif p == "layer":
            renderQueue[parameters[p]].pop(ID, None)
            renderQueue[parameters[p]].append(ID)


def drawObject(ID):
    otype = objects[ID]["type"]
    if otype == "Button" or otype == "textField" or otype == "Text":
        if otype != "Text":
            rectangle(
                objects[ID]["ax"],
                objects[ID]["ay"],
                objects[ID]["bx"],
                objects[ID]["by"],
                objects[ID]["outlineColor"],
                objects[ID]["fill"],
                objects[ID]["stroke"]
            )
        texte(
            (objects[ID]["x"] if otype != "textField" else objects[ID]["ax"]),
            (objects[ID]["y"] if otype != "textField" else objects[ID]["ay"] + (
                        objects[ID]["by"] - objects[ID]["ay"]) / 2),
            objects[ID]["text"][-(objects[ID]["height"]):],
            objects[ID]["textColor"],
            taille=objects[ID]["textSize"],
            ancrage=objects[ID]["textAnchor"],
            police=objects[ID]["textFont"]
        )
    elif otype == "Panel":
        rectangle(
            objects[ID]["ax"],
            objects[ID]["ay"],
            objects[ID]["bx"],
            objects[ID]["by"],
            objects[ID]["outlineColor"],
            objects[ID]["fill"],
            objects[ID]["stroke"]
        )
        for c in objects[ID]["childs"]:
            drawObject(c)


def moveObject(ID, layer):
    setObject(ID, {"layer": layer})


def isObject(ID):
    try:
        objects[ID]
        return True
    except KeyError:
        return False


def remObject(ID):
    try:
        if objects[ID]["type"] == "Panel":
            if objects[ID]["childs"]:
                for o in objects[ID]["childs"]:
                    remObject(o)
        positions[objects[ID]["layer"]].pop(ID, None)
        renderQueue[objects[ID]["layer"]].remove(ID)
        objects.pop(ID, None)
    except KeyError as e:
        print("UI Warning: cannot remove unknown object", e)


######## Buttons ########
def nullAction():
    print("je suis un bouton")


def addButton(x, y, action=nullAction, arguments=[], ID=None, width=150, height=50, anchorx="c", anchory="c",
              textAnchor="c", text="", outlineColor="black", textColor="black", textSize=None, textFont="Monospace",
              fill="", stroke=1, hidden=False, layer=0, isChild=False):
    global objects, buttonCount
    if ID is None:
        ID = "Button" + str(buttonCount)
    if textSize is None:
        textSize = int(width / len(text))
    buttonCount += 1
    addObject(x, y, ID, layer, width, height, anchorx, anchory, outlineColor, fill, stroke, hidden, isChild,
              otype="Button")
    objects[ID]["text"] = text
    objects[ID]["textAnchor"] = textAnchor
    objects[ID]["textColor"] = textColor
    objects[ID]["textSize"] = textSize
    objects[ID]["action"] = action
    objects[ID]["args"] = arguments
    objects[ID]["textFont"] = textFont


######## textFields ########
def addTextField(x, y, ID=None, width=150, height=30, anchorx="c", anchory="c", textAnchor="w", text="",
                 outlineColor="black", textColor="black", textSize=18, fill="", textFont="Monospace", stroke=1,
                 hidden=False, layer=0, isChild=False):
    global objects, textFieldCount
    if ID is None:
        ID = "textField" + str(textFieldCount)
    textFieldCount += 1
    addObject(x, y, ID, layer, width, height, anchorx, anchory, outlineColor, fill, stroke, hidden, isChild,
              otype="textField")
    objects[ID]["text"] = text
    objects[ID]["textAnchor"] = textAnchor
    objects[ID]["textColor"] = textColor
    objects[ID]["textSize"] = textSize
    objects[ID]["textFont"] = textFont


######## Texts ########
def addText(x, y, ID=None, width=150, height=30, anchorx="c", anchory="c", textAnchor="w", text="", textColor="black",
            textSize=18, textFont="Monospace", hidden=False, layer=0, isChild=False):
    global objects, textCount
    if ID is None:
        ID = "textField" + str(textCount)
    textCount += 1
    addObject(x, y, ID, layer, width, height, anchorx, anchory, hidden, isChild, otype="Text")
    objects[ID]["text"] = text
    objects[ID]["textAnchor"] = textAnchor
    objects[ID]["textColor"] = textColor
    objects[ID]["textSize"] = textSize
    objects[ID]["textFont"] = textFont


######## Panels ########
def addPanel(x, y, ID=None, width=100, height=100, anchorx="c", anchory="c", outlineColor="gray", fill="gray", stroke=1,
             childs=[], hidden=False, layer=0, isChild=False):
    global objects, panelCount
    if ID is None:
        ID = "Panel" + str(panelCount)
    panelCount += 1
    addObject(x, y, ID, layer, width, height, anchorx, anchory, outlineColor, fill, stroke, hidden, isChild,
              otype="Panel")
    objects[ID]["childs"] = childs
