from upemtk import rectangle, texte, efface, efface_tout
from renderElements import *

EMPTY_LAYER_ABOVE_LIMIT=2
objects = {}
toRenderObjects=[]
permanentObjects = {} #/!\ *chuckles* I'm in danger
positions = {}
#renderQueue = {}
renderQueue = [set()]
renderRoutines = {}
focus = None
exclusiveLayer = None
evenement = None
objectCount = 0

renderTable = {
    "Button": ((lambda x: drawButton(x)), 2),
    "textField": ((lambda x: drawTextField(x)), 2),
    "Text": ((lambda x: drawText(x)), 1),
    "Panel": ((lambda x: drawPanel(x)), 1),
    "gameCanvas": ((lambda x: drawGameCanvas(x)), 1)
}

def reset():
    global objects, positions, renderQueue, focus, exclusiveLayer, evenement, EMPTY_LAYER_ABOVE_LIMIT, objectCount, tkElementsCount
    EMPTY_LAYER_ABOVE_LIMIT=2
    objects.clear()
    #todelete=set()
    # for ID in objects.keys():
    #     if not objects[ID]["permanent"]:
    #         todelete.add(ID)
    # for ID in todelete:
    #     objects.pop(ID, None)
    #     for l in positions.keys():
    #         positions[l].pop(ID, None)
    #     for l in renderQueue:
    #         l.remove(ID)
    positions.clear()
    renderQueue.clear()
    renderQueue.append(set())
    renderRoutines.clear()
    focus = None
    exclusiveLayer = None
    evenement = None
    objectCount = 0


def reDraw():
    global renderQueue, toRenderObjects
    toRenderObjects=renderQueue


######## Objects ########
def addObject(x, y, layer, width, height, anchorx, anchory, ID=None, outlineColor=None, fill=None, stroke=None, hidden=None,
              isChild=None, otype=None, permanent=False):
    global objects, positions, objectCount
    if ID is None:
        ID = "object" + str(objectCount)
    objectCount+=1
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
        "type": otype,
        "isChild": isChild,
        "permanent": permanent,
        "tkObjects": None
    }
    updateLayers(ID, layer)
    if not positions.__contains__(layer):
        positions[layer] = {}
    positions[layer][ID] = [
        [objects[ID]["ax"], objects[ID]["bx"]],
        [objects[ID]["ay"], objects[ID]["by"]]
    ]
    print(toRenderObjects)
    return ID

def updateLayers(ID, layer):
    global renderQueue
    lastLayer=len(renderQueue)-1
    if lastLayer<layer:
        if layer-lastLayer>EMPTY_LAYER_ABOVE_LIMIT:
            print("UI Warning: layer", layer, "is more than", EMPTY_LAYER_ABOVE_LIMIT, "layer above the last layer", "("+lastLayer+"), defaulting to", lastLayer+1)
            layer=lastLayer+1
        for i in range(layer-lastLayer):
            renderQueue.append(set())
    objects[ID]["layer"]=layer
    renderQueue[layer].add(ID)
    updateObject(ID)


def updateObject(ID):
    global toRenderObjects
    if len(renderQueue)>len(toRenderObjects):
        for i in range(len(renderQueue)-len(toRenderObjects)):
            toRenderObjects.append(set())
    toRenderObjects[objects[ID]["layer"]].add(ID)


def setObject(ID, parameters):
    """
    Modifie un ou plusieurs paramètres d'un objet.
    :param str ID: ID de l'objet
    :param dict parameters: Paramètres à modifier
    """
    assert type(ID) == str
    assert type(parameters) == dict
    global objects, toRenderObjects
    modified=False
    for p in parameters:
        if objects[ID][p] != parameters[p]:
            modified=True
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
                updateLayers(ID, parameters[p])
    if modified:
        updateObject(ID)
    

def drawObject(ID):
    global renderTable
    try:
        objects[ID]["tkObjects"] = renderTable[objects[ID]["type"]][0](ID)
    except KeyError:
        print("UI Warning: Object with ID", ID, "could not be 'drawn': type", objects[ID]["type"], "is not registered in the render table.")
    
    # global tkElementsCount
    # otype = objects[ID]["type"]
    # if otype == "Button" or otype == "textField" or otype == "Text":
    #     if otype != "Text":
    #         rectangle(
    #             objects[ID]["ax"],
    #             objects[ID]["ay"],
    #             objects[ID]["bx"],
    #             objects[ID]["by"],
    #             objects[ID]["outlineColor"],
    #             objects[ID]["fill"],
    #             objects[ID]["stroke"],
    #             tag=""
    #         )
    #     texte(
    #         (objects[ID]["x"] if otype != "textField" else objects[ID]["ax"]),
    #         (objects[ID]["y"] if otype != "textField" else objects[ID]["ay"] + (
    #                     objects[ID]["by"] - objects[ID]["ay"]) / 2),
    #         objects[ID]["text"][-(objects[ID]["height"]):],
    #         objects[ID]["textColor"],
    #         taille=objects[ID]["textSize"],
    #         ancrage=objects[ID]["textAnchor"],
    #         police=objects[ID]["textFont"]
    #     )
    # elif otype == "Panel":
    #     rectangle(
    #         objects[ID]["ax"],
    #         objects[ID]["ay"],
    #         objects[ID]["bx"],
    #         objects[ID]["by"],
    #         objects[ID]["outlineColor"],
    #         objects[ID]["fill"],
    #         objects[ID]["stroke"]
    #     )
    #     for c in objects[ID]["childs"]:
    #         drawObject(c)
    # elif otype == "gameCanvas":
    #     rectangle(
    #         objects[ID]["ax"],
    #         objects[ID]["ay"],
    #         objects[ID]["bx"],
    #         objects[ID]["by"],
    #         objects[ID]["outlineColor"],
    #         objects[ID]["fill"],
    #         objects[ID]["stroke"]
    #     )

    #     for y in range(len(objects[ID]["squaresMap"])):
    #         for x in range(len(objects[ID]["squaresMap"][y])):
    #             x1 = x * CELL_SIZE + objects[ID]["ax"]
    #             y1 = y * CELL_SIZE + objects[ID]["ay"]
    #             renderCase[objects[ID]["squaresMap"][y][x]]((x1, y1))


def moveObject(ID, layer):
    setObject(ID, {"layer": layer})


def exists(ID):
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
        for o in objects[ID]["tkObjects"]:
            efface(t)
        objects.pop(ID, None)
    except KeyError as e:
        print("UI Warning: cannot remove unknown object", e)


######## Buttons ########
def nullAction():
    print("je suis un bouton")


def addButton(x, y, action=nullAction, arguments=[], ID=None, width=150, height=50, anchorx="c", anchory="c",
              textAnchor="c", text="", outlineColor="black", textColor="black", textSize=None, textFont="Monospace",
              fill="", stroke=1, hidden=False, layer=0, isChild=False, permanent=False):
    global objects
    if textSize is None:
        textSize = int(width / len(text))
    ID = addObject(x, y, layer, width, height, anchorx, anchory, ID, outlineColor, fill, stroke, hidden, isChild, otype="Button", permanent=permanent)
    objects[ID]["text"] = text
    objects[ID]["textAnchor"] = textAnchor
    objects[ID]["textColor"] = textColor
    objects[ID]["textSize"] = textSize
    objects[ID]["action"] = action
    objects[ID]["args"] = arguments
    objects[ID]["textFont"] = textFont


def drawButton(ID):
    return (
        rectangle(
            objects[ID]["ax"],
            objects[ID]["ay"],
            objects[ID]["bx"],
            objects[ID]["by"],
            objects[ID]["outlineColor"],
            objects[ID]["fill"],
            objects[ID]["stroke"]
        ),
        texte(
            objects[ID]["x"],
            objects[ID]["y"],
            objects[ID]["text"],
            objects[ID]["textColor"],
            taille=objects[ID]["textSize"],
            ancrage=objects[ID]["textAnchor"],
            police=objects[ID]["textFont"]
        )
    )
    #return (el1, el2)


######## textFields ########
def addTextField(x, y, ID=None, width=150, height=30, anchorx="c", anchory="c", textAnchor="w", text="",
                 outlineColor="black", textColor="black", textSize=18, fill="", textFont="Monospace", stroke=1,
                 hidden=False, layer=0, isChild=False, permanent=False):
    global objects
    ID = addObject(x, y, layer, width, height, anchorx, anchory, ID, outlineColor, fill, stroke, hidden, isChild, otype="textField", permanent=permanent)
    objects[ID]["text"] = text
    objects[ID]["textAnchor"] = textAnchor
    objects[ID]["textColor"] = textColor
    objects[ID]["textSize"] = textSize
    objects[ID]["textFont"] = textFont


def drawTextField(ID):
    return (
        rectangle(
            objects[ID]["ax"],
            objects[ID]["ay"],
            objects[ID]["bx"],
            objects[ID]["by"],
            objects[ID]["outlineColor"],
            objects[ID]["fill"],
            objects[ID]["stroke"]
        ),
        texte(
            objects[ID]["ax"],
            (objects[ID]["ay"] + (objects[ID]["by"] - objects[ID]["ay"]) / 2),
            objects[ID]["text"][-(objects[ID]["height"]):],
            objects[ID]["textColor"],
            taille=objects[ID]["textSize"],
            ancrage=objects[ID]["textAnchor"],
            police=objects[ID]["textFont"]
        )
    )


######## Texts ########
def addText(x, y, ID=None, width=150, height=30, anchorx="c", anchory="c", textAnchor="w", text="", textColor="black",
            textSize=18, textFont="Monospace", hidden=False, layer=0, isChild=False, permanent=False):
    global objects
    ID = addObject(x, y, layer, width, height, anchorx, anchory, hidden, ID,isChild, otype="Text", permanent=permanent)
    objects[ID]["text"] = text
    objects[ID]["textAnchor"] = textAnchor
    objects[ID]["textColor"] = textColor
    objects[ID]["textSize"] = textSize
    objects[ID]["textFont"] = textFont


def drawText(ID):
    return tuple(
        texte(
            objects[ID]["x"],
            objects[ID]["y"],
            objects[ID]["text"],
            objects[ID]["textColor"],
            taille=objects[ID]["textSize"],
            ancrage=objects[ID]["textAnchor"],
            police=objects[ID]["textFont"]
        )
    )


######## Panels ########
def addPanel(x, y, ID=None, width=100, height=100, anchorx="c", anchory="c", outlineColor="gray", fill="gray", stroke=1,
             childs=[], hidden=False, layer=0, isChild=False, permanent=False):
    global objects
    ID = addObject(x, y, layer, width, height, anchorx, anchory, ID, outlineColor, fill, stroke, hidden, isChild, otype="Panel", permanent=permanent)
    objects[ID]["childs"] = childs

def drawPanel(ID):
    returnValue = tuple(
        rectangle(
            objects[ID]["ax"],
            objects[ID]["ay"],
            objects[ID]["bx"],
            objects[ID]["by"],
            objects[ID]["outlineColor"],
            objects[ID]["fill"],
            objects[ID]["stroke"]
        )
    )
    for c in objects[ID]["childs"]: #Problem
        drawObject(c)
    return returnValue

######## Canevas ########
def addGameCanvas(x, y, ID=None, width=100, height=100, anchorx="c", anchory="c", outlineColor="red", fill="", stroke=1,
             squaresMap=[], hidden=False, layer=0, isChild=False):
    global objects
    ID = addObject(x, y, layer, width, height, anchorx, anchory, ID, outlineColor, fill, stroke, hidden, isChild, otype="gameCanvas")
    objects[ID]["squaresMap"] = squaresMap


def drawGameCanvas(ID):
    identifierList=[
        rectangle(
                objects[ID]["ax"],
                objects[ID]["ay"],
                objects[ID]["bx"],
                objects[ID]["by"],
                objects[ID]["outlineColor"],
                objects[ID]["fill"],
                objects[ID]["stroke"]
            )
    ]
    for y in range(len(objects[ID]["squaresMap"])):
        for x in range(len(objects[ID]["squaresMap"][y])):
            x1 = x * CELL_SIZE + objects[ID]["ax"]
            y1 = y * CELL_SIZE + objects[ID]["ay"]
            identifierList.extend(renderCase[objects[ID]["squaresMap"][y][x]]((x1, y1)))
    return tuple(identifierList)
