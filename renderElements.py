from upemtk import *

CELL_NBX = 20
CELL_NBY = 10
CELL_SIZE = 29
HALF_SIZE = CELL_SIZE // 2
# WIDTH_WINDOW = CELL_SIZE * CELL_NBX
# HEIGHT_WINDOW = CELL_SIZE * CELL_NBY
WIDTH_WINDOW = 850
HEIGHT_WINDOW = 400

# def addObject(x, y, ID, layer, width, height, fill=None, hidden=None, otype=None):
#     global objects, renderQueue, positions
#     objects[ID] = {
#         "x": x,
#         "y": y,
#         "width": width,
#         "height": height,
#         "outlineColor": outlineColor,
#         "fill": fill,
#         "stroke": stroke,
#         "hidden": hidden,
#         "type": otype,
#     }
#     # if not renderQueue.__contains__(layer):
#     #    renderQueue[layer] = set()
#     # renderQueue[layer].add(ID)

#     lastLayer=len(renderQueue)-1
#     if lastLayer<layer:
#         if layer-lastLayer>EMPTY_LAYER_ABOVE_LIMIT:
#             print("UI Warning: layer", layer, "is more than", EMPTY_LAYER_ABOVE_LIMIT, "layer above the last layer", "("+lastLayer+"), defaulting to", lastLayer+1)
#             layer=lastLayer+1
#         for i in range(layer-lastLayer):
#             renderQueue.append(set())
#     objects[ID]["layer"]=layer
#     renderQueue[layer].add(ID)

#     if not positions.__contains__(layer):
#         positions[layer] = {}
#     positions[layer][ID] = [
#         [objects[ID]["ax"], objects[ID]["bx"]],
#         [objects[ID]["ay"], objects[ID]["by"]]
#     ]

def drawVoid(coord):
    """
    dessine une case vide

    :param tuple coord: couple (abscisse, ordonnee) de la case
    """
    rectangle(
        coord[0],
        coord[1],
        coord[0] + CELL_SIZE,
        coord[1] + CELL_SIZE,
        '#000',
        '#000'
    )


def drawWall(coord):
    """
    dessine une case mur

    :param tuple coord: couple (abscisse, ordonnee) de la case
    """
    rectangle(
        coord[0],
        coord[1],
        coord[0] + CELL_SIZE,
        coord[1] + CELL_SIZE,
        '#666',
        '#666'
    )


def drawGrass(coord):
    """
    dessine une case terre

    :param tuple coord: couple (abscisse, ordonnee) de la case
    """
    rectangle(
        coord[0],
        coord[1],
        coord[0] + CELL_SIZE,
        coord[1] + CELL_SIZE,
        '#850',
        '#850'
    )


def drawBoulder(coord):
    """
    dessine une case boulet

    :param tuple coord: couple (abscisse, ordonnee) de la case
    """
    drawVoid(coord)
    cercle(
        coord[0] + HALF_SIZE,
        coord[1] + HALF_SIZE,
        HALF_SIZE,
        '#888',
        '#aaa'
    )


def drawDiamond(coord):
    """
    dessine une case diamant

    :param tuple coord: couple (abscisse, ordonnee) de la case
    """
    drawVoid(coord)
    points = [
        (coord[0] + HALF_SIZE, coord[1]),
        (coord[0], coord[1] + HALF_SIZE),
        (coord[0] + HALF_SIZE, coord[1] + CELL_SIZE),
        (coord[0] + CELL_SIZE, coord[1] + HALF_SIZE)
    ]
    polygone(points, '#09f', '#0ff')


def drawEnd(coord, finished=False):
    """
    dessine une case fin
    rouge si open false
    vert si open true

    :param tuple coord: couple (abscisse, ordonnee) de la case
    """
    colors = (("#0a0", "#0f0") if finished else ("#a00", "#f00"))
    rectangle(
        coord[0],
        coord[1],
        coord[0] + CELL_SIZE,
        coord[1] + CELL_SIZE,
        colors[0],
        colors[0]
    )
    cercle(
        coord[0] + HALF_SIZE,
        coord[1] + HALF_SIZE,
        HALF_SIZE // 2,
        colors[1],
        colors[1]
    )


def drawRockford(coord):
    """
    dessine une case Rockford

    :param tuple coord: couple (abscisse, ordonnee) de la case
    """
    drawVoid(coord)
    cercle(
        coord[0] + HALF_SIZE,
        coord[1] + HALF_SIZE // 2,
        HALF_SIZE // 2,
        '#c80',
        '#f41'
    )
    rectangle(
        coord[0] + HALF_SIZE // 2,
        coord[1] + HALF_SIZE,
        coord[0] + HALF_SIZE * 1.5,
        coord[1] + CELL_SIZE,
        '#c80',
        '#f41'
    )
