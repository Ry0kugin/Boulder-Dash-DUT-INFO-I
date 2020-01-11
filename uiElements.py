from upemtk import rectangle, texte, efface, efface_tout, polygone
from copy import deepcopy
from renderElements import *

EMPTY_LAYER_ABOVE_LIMIT=2
objects = {}
toRenderObjects=[]
permanentObjects = {} #/!\ *chuckles* I'm in danger
positions = {}
#renderQueue = {}
renderQueue = [set()]
renderRoutines = {}
logicRoutines = {}
focus = None
exclusiveLayer = None
evenement = None
objectCount = 0

renderTable = {
    "Button": (lambda x: drawButton(x)),
    "textField": (lambda x: drawTextField(x)),
    "Text": (lambda x: drawText(x)),
    "Panel": (lambda x: drawPanel(x)),
    "gameCanvas": (lambda x: drawGameCanvas(x)),
    "Polygon": (lambda x: drawPolygon(x))
}

anchorTable = {

}

def reset():
    global objects, positions, renderQueue, focus, exclusiveLayer, evenement, EMPTY_LAYER_ABOVE_LIMIT, objectCount
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
    logicRoutines.clear()
    focus = None
    exclusiveLayer = None
    evenement = None
    objectCount = 0


def reDraw():
    global renderQueue, toRenderObjects
    toRenderObjects=deepcopy(renderQueue)


    # for l in range(len(renderQueue)):
    #     for ID in renderQueue[l]:
    #         toRenderObjects[l].add(ID)


######## Objects ########
def addObject(x, y, layer, width, height, anchorx, anchory, ID=None, outlineColor=None, fill=None, stroke=None, hidden=None,
              isChild=None, otype=None, permanent=False):
    global objects, positions, objectCount
    if ID is None:
        ID = "object" + str(objectCount)
    objectCount+=1
    if otype!="Text":
        x = (x if anchorx == "c" else (x - width / 2 if anchorx == "r" else x + width / 2))
        y = (y if anchory == "c" else (y + height / 2 if anchory == "u" else y - height / 2))
    objects[ID] = {
        "x": x,
        "y": y,
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
    return ID

def updateLayers(ID, layer):
    global renderQueue
    lastLayer=len(renderQueue)-1
    if lastLayer<layer:
        if layer-lastLayer>EMPTY_LAYER_ABOVE_LIMIT:
            print("UI Warning: layer", layer, "is more than", EMPTY_LAYER_ABOVE_LIMIT, "layer above the last layer", "("+lastLayer+"), defaulting to", lastLayer+1)
            layer=lastLayer+1
        for _ in range(layer-lastLayer):
            renderQueue.append(set())
    objects[ID]["layer"]=layer
    renderQueue[layer].add(ID)
    updateObject(ID)


def updateObject(ID):
    global toRenderObjects
    if len(renderQueue)>len(toRenderObjects):
        for _ in range(len(renderQueue)-len(toRenderObjects)):
            toRenderObjects.append(set())
    toRenderObjects[objects[ID]["layer"]].add(ID)
    


def setObject(ID, parameters, forceUpdate=False):
    """
    Modifie un ou plusieurs paramètres d'un objet.
    :param str ID: ID de l'objet
    :param dict parameters: Paramètres à modifier
    """
    assert type(ID) == str
    assert type(parameters) == dict
    global objects, toRenderObjects
    modified=False
    for p in parameters.keys():
        # if not modified:
        #     if p =="squaresMap" and objects[ID]["type"]=="gameCanvas":
        #         if objects[ID]["squaresMap"] and parameters[p]:
        #             # print(objects[ID]["squaresMap"])
        #             # try:
        #             for y in len(objects[ID]["squaresMap"]):
        #                 for x in len(y):
        #                     if parameters[p][y][x] != objects[ID]["squaresMap"][y][x]:
        #                         modified=True
        #                         break
        #             # except:
        #             #     print(objects[ID]["squaresMap"])
        #         else:
        #             modified=True
        #     elif parameters[p]!=objects[ID][p]:
        #         modified=True
        if objects[ID][p]!=parameters[p] or forceUpdate:
            modified=True
            objects[ID][p] = parameters[p]
            if p == "x" or p == "width":
                width = objects[ID]["width"]
                #print(width)
                #print(parameters[p])
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
    # try:
    objects[ID]["tkObjects"] = tuple(renderTable[objects[ID]["type"]](ID))
    # except KeyError:
    #     print("UI Warning: Object with ID", ID, "could not be 'drawn': type", objects[ID]["type"], "is not registered in the render table.")


def moveObject(ID, layer):
    setObject(ID, {"layer": layer})


def exists(ID):
    try:
        objects[ID]
        return True
    except KeyError:
        return False


def remObject(ID):
    global positions, renderQueue, objects
    try:
        if objects[ID]["type"] == "Panel":
            if objects[ID]["childs"]:
                for o in objects[ID]["childs"]:
                    remObject(o)
            positions[objects[ID]["layer"]].pop(ID, None)
            renderQueue[objects[ID]["layer"]].remove(ID)
            if objects[ID]["tkObjects"]:
                for o in objects[ID]["tkObjects"]:
                    efface(o)
            objects.pop(ID, None)
            reDraw()# A corriger
            return
        positions[objects[ID]["layer"]].pop(ID, None)
        renderQueue[objects[ID]["layer"]].remove(ID)
        if objects[ID]["tkObjects"]:
            for o in objects[ID]["tkObjects"]:
                efface(o)
        objects.pop(ID, None)
    except KeyError as e:
        print("UI Warning: cannot remove unknown object", e)


######## Buttons ########
def nullAction():
    print("je suis un bouton")


def addButton(x, y, action=nullAction, arguments=[], ID=None, width=150, height=50, anchorx="c", anchory="c",
              textAnchor="center", text="", outlineColor="black", textColor="black", textSize=18, textFont="Monospace",
              fill="", stroke=1, polygonal=None, hidden=False, layer=0, isChild=False, permanent=False):
    global objects
    # if textSize is None and text:
    #     textSize = int(width / len(text))
    ID = addObject(x, y, layer, width, height, anchorx, anchory, ID, outlineColor, fill, stroke, hidden, isChild, otype="Button", permanent=permanent)
    objects[ID]["text"] = text
    objects[ID]["textAnchor"] = textAnchor
    objects[ID]["textColor"] = textColor
    objects[ID]["textSize"] = textSize
    objects[ID]["action"] = action
    objects[ID]["args"] = arguments
    objects[ID]["textFont"] = textFont
    objects[ID]["polygonal"] = polygonal
    # [(x,y),(x,y),...]

def drawButton(ID):
    return (
        polygone(
            [(objects[ID]["ax"]+x*objects[ID]["width"],objects[ID]["ay"]+y*objects[ID]["height"]) for x,y in objects[ID]["polygonal"]],
            objects[ID]["outlineColor"],
            objects[ID]["fill"],
            objects[ID]["stroke"]
        ) if objects[ID]["polygonal"] else
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
            objects[ID]["textAnchor"],
            objects[ID]["textFont"],
            objects[ID]["textSize"]
        )
    )
    
######## Polygons ########
def addPolygon(x, y, ID=None, points=None,width=150, height=50, anchorx="c", anchory="c", outlineColor="black", fill="", stroke=1, hidden=False, layer=0, isChild=False):
    global objects
    # if textSize is None and text:
    #     textSize = int(width / len(text))
    ID = addObject(x, y, layer, width, height, anchorx, anchory, ID, outlineColor, fill, stroke, hidden, isChild, otype="Polygon")
    objects[ID]["points"]=points
    # [(x,y),(x,y),...]

def drawPolygon(ID):
    return (
        polygone(
            [(objects[ID]["ax"]+x*objects[ID]["width"],objects[ID]["ay"]+y*objects[ID]["height"]) for x,y in objects[ID]["points"]],
            objects[ID]["outlineColor"],
            objects[ID]["fill"],
            objects[ID]["stroke"]
        ))

######## textFields ########
def addTextField(x, y, ID=None, width=150, height=30, anchorx="c", anchory="c", text="",
                 outlineColor="black", textColor="black", textSize=18, fill="", textFont="Monospace", stroke=1,
                 hidden=False, layer=0, isChild=False, permanent=False):
    global objects
    ID = addObject(x, y, layer, width, height, anchorx, anchory, ID, outlineColor, fill, stroke, hidden, isChild, otype="textField", permanent=permanent)
    objects[ID]["text"] = text
    objects[ID]["textColor"] = textColor
    objects[ID]["textSize"] = textSize
    objects[ID]["textFont"] = textFont


def drawTextField(ID):
    i=0
    # if objects[ID]["text"]:
    #     while longueur_texte(objects[ID]["text"][-i:])>objects[ID]["width"]:
    #         i+=1
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
            objects[ID]["text"][-i:],
            objects[ID]["textColor"],
            taille=objects[ID]["textSize"],
            ancrage="w",
            police=objects[ID]["textFont"]
        )
    )


######## Texts ########
def addText(x, y, ID=None, width=150, height=30, anchorx="c", anchory="c", text="", textColor="black",
            textSize=18, textFont="Purisa", hidden=False, layer=0, isChild=False, permanent=False):
    global objects
    ID = addObject(x, y, layer, width, height, anchorx, anchory, ID, hidden=hidden, isChild=isChild, otype="Text", permanent=permanent)
    objects[ID]["text"] = text
    # objects[ID]["textAnchor"] = textAnchor
    objects[ID]["textColor"] = textColor
    objects[ID]["textSize"] = textSize
    objects[ID]["textFont"] = textFont
    


def drawText(ID):
    if objects[ID]["anchorx"]=="l":
        anchor="w"
    elif objects[ID]["anchorx"]=="r":
        anchor="e"
    else:
        anchor="center"
    return (
        texte(
            objects[ID]["x"],
            objects[ID]["y"],
            objects[ID]["text"],
            objects[ID]["textColor"],
            anchor,
            objects[ID]["textFont"],
            objects[ID]["textSize"]
        ),
    )


######## Panels ########
def addPanel(x, y, ID=None, width=100, height=100, anchorx="c", anchory="c", outlineColor="gray", fill="gray", stroke=1,
             childs=[], hidden=False, layer=0, isChild=False, permanent=False):
    global objects
    ID = addObject(x, y, layer, width, height, anchorx, anchory, ID, outlineColor, fill, stroke, hidden, isChild, otype="Panel", permanent=permanent)
    objects[ID]["childs"] = childs

def drawPanel(ID):
    returnValue = (
        rectangle(
            objects[ID]["ax"],
            objects[ID]["ay"],
            objects[ID]["bx"],
            objects[ID]["by"],
            objects[ID]["outlineColor"],
            objects[ID]["fill"],
            objects[ID]["stroke"]
        ),
    )
    for c in objects[ID]["childs"]: #Problem
        drawObject(c)
    return returnValue

######## Canvas ########
def addGameCanvas(x, y, ID=None, width=100, height=100, anchorx="c", anchory="c", outlineColor="", fill="", stroke=1,
             squaresMap=[], hidden=False, layer=0, isChild=False, selected=None, permanentSelected=None,cellSize=32):
    global objects
    ID = addObject(x, y, layer, width, height, anchorx, anchory, ID, outlineColor, fill, stroke, hidden, isChild, otype="gameCanvas")
    objects[ID]["squaresMap"] = squaresMap
    objects[ID]["selected"] = selected
    objects[ID]["cellSize"] = cellSize

def drawGameCanvas(ID):
    if len(objects[ID]["squaresMap"]):
        if len(objects[ID]["squaresMap"][0])*objects[ID]["cellSize"] < objects[ID]["width"]:
            setObject(ID, {"width": len(objects[ID]["squaresMap"][0])*objects[ID]["cellSize"]+1})
        if (len(objects[ID]["squaresMap"]))*objects[ID]["cellSize"] < objects[ID]["height"]:
            setObject(ID, {"height": (len(objects[ID]["squaresMap"]))*objects[ID]["cellSize"]+1})
        if len(objects[ID]["squaresMap"][0])*objects[ID]["cellSize"] > objects[ID]["width"]:
            setObject(ID, {"width": len(objects[ID]["squaresMap"][0])*objects[ID]["cellSize"]+1})
        if (len(objects[ID]["squaresMap"]))*objects[ID]["cellSize"] > objects[ID]["height"]:
            setObject(ID, {"height": (len(objects[ID]["squaresMap"]))*objects[ID]["cellSize"]+1})

    # if len(objects[ID]["squaresMap"]):
    #     if len(objects[ID]["squaresMap"][0])*CELL_SIZE < objects[ID]["width"]:
    #         bx = objects[ID]["ax"] + len(objects[ID]["squaresMap"][0])*CELL_SIZE
    #         setObject(ID, {"bx": bx})
    #         print("changed")
    #     if (len(objects[ID]["squaresMap"])-1)*CELL_SIZE < objects[ID]["height"]:
    #         by = objects[ID]["ay"] +  (len(objects[ID]["squaresMap"])-1)*CELL_SIZE
    #         setObject(ID, {"by": by})
    #         print("changed")

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
            x1, y1 = toCanvasCoord(ID, x,y)
            identifierList.extend(renderCase[objects[ID]["squaresMap"][y][x]]((x1+1, y1+1), objects[ID]["cellSize"]-2))
    if objects[ID]["selected"]:
        for p in objects[ID]["selected"]:
            if p:
                x,y = p[0], p[1]
                identifierList.append(renderCase["S"](toCanvasCoord(ID,x,y), objects[ID]["cellSize"], objects[ID]["fill"]))
    return tuple(identifierList)

def toCanvasCoord(ID,x,y):
    return (x * objects[ID]["cellSize"] + objects[ID]["ax"], y * objects[ID]["cellSize"] + objects[ID]["ay"])

def getToRenderObjects():
    return toRenderObjects

def setToRenderObjects(value):
    global toRenderObjects
    toRenderObjects=value