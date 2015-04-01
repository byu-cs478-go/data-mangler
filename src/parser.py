import numpy as np
import matplotlib.pyplot as plt
from sets import Set
from sizeAndLibertyFunctions import *

def getColor(board, loc):
    return board[loc[0]][loc[1]]


def getColors(board, groups):
    colors = []
    for group in groups:
        loc = group[0]
        color = getColor(board, loc)
        colors.append(color)
    return colors

def getOppIndexes(colors, myColor):
    oppIndex = []
    for i, color in enumerate(colors):
        if color != myColor:
            oppIndex.append(i)
    return oppIndex 

#Shared liberties
def sharedLiberties(board, groups, firstOrderLiberties):
    sharedLiberties = []
    colors = getColors(board, groups)
    for i, liberties in enumerate(firstOrderLiberties):
        oppIndexes = getOppIndexes(colors, colors[i])
        sharedLiberty = 0
        for liberty in liberties:
            for oppIndex in oppIndexes:
                if liberty in firstOrderLiberties[oppIndex]:
                    sharedLiberty += 1
                    break
        sharedLiberties.append(sharedLiberty)

    return sharedLiberties

#Two closest Adjacent opponent blocks
def twoClosestAdjacentOppoentBlockS(board, groups):
    

def addClosePoints(set, loc):
    for i in range(3):
        for j in range(3):
            np = ((loc[0] + j-1), (loc[1] + i-1))
            if isOnBoard(np):
                set.add(np)
    far = []
    far.append(((loc[0]), (loc[1]+2)))
    far.append(((loc[0]-2), (loc[1])))
    far.append(((loc[0]+2), (loc[1])))
    far.append(((loc[0]), (loc[1]-2)))
    
    for p in far:
        if isOnBoard(p):
            set.add(p)

def getLocalPoints(loc):
    local = Set()
    for p in loc:
        addClosePoints(local, p)
    return local

def localMajority(board, loc):
    color = board[loc[0][0]][loc[0][1]]

    localPoints = getLocalPoints(loc)
    plot(localPoints)
    diff = 0
    for p in localPoints:
        x = p[0]
        y = p[1]

        diff += board[x][y]

    maj = diff
    if color == 1: # when white is 1
        maj = -diff
    return maj

def centerOfMass(locs):
    distances = []
    for loc in locs:
        #up
        distances.append(18 - loc[1])

        #down
        distances.append(loc[1])

        #right
        distances.append(18 - loc[0])

        #lefty
        distances.append(loc[0])

    sortedDistance = sorted(distances)

    return (sortedDistance[0], sortedDistance[1])

# bounding box
def boundingBoxSize(groups):
    boundingBoxSizes = []
    for locs in groups:
        boundingBoxSize = 0
        minPoint = [19, 19]
        maxPoint = [0,0]
        for loc in locs:
            if loc[0] < minPoint[0]:
                minPoint[0] = loc[0]
            if loc[1] < minPoint[1]:
                minPoint[1] = loc[1]

            if loc[0] > maxPoint[0]:
                maxPoint[0] = loc[0]
            if loc[1] > maxPoint[1]:
                maxPoint[1] = loc[1]

        boundingBoxSize = (maxPoint[0] - minPoint[0]+1) * (maxPoint[1] - minPoint[1]+1)
        boundingBoxSizes.append(boundingBoxSize)
    return boundingBoxSizes

def plot(locs):
    a = []
    b = []
    for loc in locs:
        a.append(loc[1])
        b.append(loc[0])


    plt.figure('points')
    r = 100
    plt.scatter(a, b, marker='o', s=r, color='black')
    plt.xlim(0,19)
    plt.ylim(0,19)
    plt.show()

def showBoard(board):
    b_x = []
    b_y = []

    w_x = []
    w_y = []

    for y, row in enumerate(board):
        for x, p in enumerate(row):
            if p == -1:
                b_x.append(x)
                b_y.append(y)
            elif p == 1:
                w_x.append(x)
                w_y.append(y)

    r = 100
    plt.figure('board')
    plt.scatter(b_x, b_y, marker='o', s=r, color='black')
    plt.scatter(w_x, w_y, marker='o', s=r, color='gray')
    plt.xlim(0,19)
    plt.ylim(0,19)

    plt.show()

def placeStones(board, black, white):
    for p in black:
        board[p[0]][p[1]] = -1
    for p in white:
        board[p[0]][p[1]] = 1



def _main():
    board = [[0 for x in range(19)] for x in range(19)] 

    black = [(3,6), (4,5), (2,2), (3,2),(4,2), (4,3), (4,4),(4,6),(3,1)]
    white = [(2,3), (1,2), (3,4), (1,4), (2,5)]
    placeStones(board, black, white)
    groups = getGroups(board)

    print groups
    print '\n'
    print sharedLiberties(board, groups, getFirstOrderLiberties(board, groups))
    showBoard(board)


_main()