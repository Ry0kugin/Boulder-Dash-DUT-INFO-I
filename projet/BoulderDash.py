# -*- coding: utf-8 -*-

from upemtk import *

###### Constants used for this game #######
LEVEL_1 = [
        ['150s', '1d'],
        ["W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W",],
        ["W", "G", "G", "G", "G", "G", "G", ".", "G", "G", "D", "G", "B", "W",],
        ["W", "G", "B", "R", "B", "G", "G", "G", "G", "G", "G", ".", "G", "W",],
        ["W", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", ".", "G", "W",],
        ["W", "B", "G", "B", "B", "G", "G", "G", "G", "G", "G", "G", "G", "W",],
        ["W", "G", "G", ".", "B", "G", "G", "G", "G", "G", "G", "G", "G", "W",],
        ["W", "G", "G", "G", ".", "G", "G", ".", "G", "G", "G", "G", "E", "W",],
        ["W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W",]
]
CELL_NBX = 20
CELL_NBY = 10
CELL_SIZE = 32
HALF_SIZE = CELL_SIZE//2
WIDTH_WINDOW = CELL_SIZE * CELL_NBX
HEIGHT_WINDOW = CELL_SIZE * CELL_NBY
###########################################

def drawVoid(coord):
    rectangle(
        coord[0],
        coord[1],
        coord[0]+CELL_SIZE,
        coord[1]+CELL_SIZE,
        '#000',
        '#000'
    )

def drawWall(coord):
    rectangle(
        coord[0],
        coord[1],
        coord[0]+CELL_SIZE,
        coord[1]+CELL_SIZE,
        '#666',
        '#666'
    )

def drawGrass(coord):
    rectangle(
        coord[0],
        coord[1],
        coord[0]+CELL_SIZE,
        coord[1]+CELL_SIZE,
        '#850',
        '#850'
    )

def drawBoulder(coord):
    drawVoid(coord)
    cercle(
        coord[0]+HALF_SIZE,
        coord[1]+HALF_SIZE,
        HALF_SIZE,
        '#888',
        '#aaa'
    )

def drawDiamond(coord):
    drawVoid(coord)
    points = [
        (coord[0]+HALF_SIZE, coord[1]),
        (coord[0], coord[1]+HALF_SIZE),
        (coord[0]+HALF_SIZE, coord[1]+CELL_SIZE),
        (coord[0]+CELL_SIZE, coord[1]+HALF_SIZE)
    ]
    polygone(points,'#09f','#0ff')

def drawEnd(coord):
    rectangle(
        coord[0],
        coord[1],
        coord[0]+CELL_SIZE,
        coord[1]+CELL_SIZE,
        '#0a0',
        '#0a0'
    )
    cercle(
        coord[0]+HALF_SIZE,
        coord[1]+HALF_SIZE,
        HALF_SIZE//2,
        '#0f0',
        '#0f0'
    )
    

def drawRockFord(coord):
    drawVoid(coord)
    cercle(
        coord[0]+HALF_SIZE,
        coord[1]+HALF_SIZE//2,
        HALF_SIZE//2,
        '#c80',
        '#f41'
    )
    rectangle(
        coord[0]+HALF_SIZE//2,
        coord[1]+HALF_SIZE,
        coord[0]+HALF_SIZE*1.5,
        coord[1]+CELL_SIZE,
        '#c80',
        '#f41'
    )

renderCase = {
    '.' : (lambda x : drawVoid(x)),
    'W' : (lambda x : drawWall(x)),
    'G' : (lambda x : drawGrass(x)),
    'B' : (lambda x : drawBoulder(x)),
    'D' : (lambda x : drawDiamond(x)),
    'E' : (lambda x : drawEnd(x)),
    'R' : (lambda x : drawRockFord(x))
}

def renderCanvas(curMap):
    for y in range(1,len(curMap)):
        for x in range(0, len(curMap[y])):
            x1 = x*CELL_SIZE
            y1 = y*CELL_SIZE
            renderCase[curMap[y][x]]((x1,y1))

if __name__ == '__main__':
    cree_fenetre(WIDTH_WINDOW,HEIGHT_WINDOW)
    datamap = list(LEVEL_1)

    while True:
        renderCanvas(datamap)
        attente_clic()
        break

