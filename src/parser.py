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

#Two closest friendly blocks
def twoClosestFriendlyBlocks(board, groups, firstOrderLiberties):
    friendlyBlocks = []
    colors = getColors(board, groups)
    for i, group in enumerate(groups):
        friendlyBlock = [(0,0) for x in range(2)] 
        cnt = 0
        closefriendlyGroupIndexes = []
        curColor = getColor(board, group[0])
        for j in range(1, 3):
            localPoints = getClosePointsWithDistance(group, j)
            # plot(localPoints)
            for loc in localPoints:
                if getColor(board, loc) == curColor:
                    friendlyIndex = getGroupIndexWithLoc(groups, loc)
                    if friendlyIndex not in closefriendlyGroupIndexes:
                        closefriendlyGroupIndexes.append(friendlyIndex)
                        friendlyBlock[cnt] = (boundingBoxSize(groups[friendlyIndex]), len(firstOrderLiberties[friendlyIndex]))
                        cnt += 1
                        if cnt == 2:
                            break
            if cnt == 2:
                break
        print friendlyBlock
        friendlyBlocks.append(friendlyBlock)
    return friendlyBlocks

def addClosePointsWithDistance(local, loc, dis):
    if dis == 1:
        close = []
        close.append(((loc[0] + 1), (loc[1])))
        close.append(((loc[0]), (loc[1])-1))
        close.append(((loc[0]), (loc[1])+1))
        close.append(((loc[0] -1), (loc[1])))
        for p in close:
            if isOnBoard(p):
                local.add(p)
        return

    for i in range(3):
        for j in range(3):
            np = ((loc[0] + j-1), (loc[1] + i-1))
            if isOnBoard(np):
                local.add(np)
    far = []
    far.append(((loc[0]), (loc[1]+2)))
    far.append(((loc[0]-2), (loc[1])))
    far.append(((loc[0]+2), (loc[1])))
    far.append(((loc[0]), (loc[1]-2)))
    
    for p in far:
        if isOnBoard(p):
            local.add(p)

def getClosePointsWithDistance(group, dis):
    local = Set()
    for loc in group:
        addClosePointsWithDistance(local, loc, 1)
    if dis == 1:
        return list(local - Set(group))
    elif dis == 2:
        far = Set()
        for loc in group:
            addClosePointsWithDistance(far, loc, 2)
        return list(far - local - Set(group))

def getGroupIndexWithLoc(groups, loc):
    for i, group in enumerate(groups):
        if loc in group:
            return i

#Two closest Adjacent opponent blocks
def twoClosestAdjacentOppoentBlocks(board, groups, firstOrderLiberties):
    opponentBlocks = []
    colors = getColors(board, groups)
    for i, group in enumerate(groups):
        opponentBlock = [(0,0) for x in range(2)] 
        cnt = 0
        closeOppGroupIndexes = []
        curColor = getColor(board, group[0])
        for j in range(1, 3):
            localPoints = getClosePointsWithDistance(group, j)
            # plot(localPoints)
            for loc in localPoints:
                if getColor(board, loc) == curColor * (-1):
                    oppIndex = getGroupIndexWithLoc(groups, loc)
                    # print oppIndex
                    if oppIndex not in closeOppGroupIndexes:
                        closeOppGroupIndexes.append(oppIndex)
                        opponentBlock[cnt] = (boundingBoxSize(groups[oppIndex]), len(firstOrderLiberties[oppIndex]))
                        cnt += 1
                        if cnt == 2:
                            break
            if cnt == 2:
                break
        print opponentBlock
        opponentBlocks.append(opponentBlock)
    return opponentBlocks

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

def getLocalPoints(locs):
    local = Set()
    for loc in locs:
        addClosePoints(local, loc)
    return local

def getLocalMajority(board, group):
    color = getColor(board, group[0])
    localPoints = getLocalPoints(group)
    # plot(localPoints)
    diff = 0
    for loc in localPoints:
        # x = p[0]
        # y = p[1]
        diff += getColor(board, loc)

    maj = diff
    if color == 1: # when white is 1
        maj = -diff
    return maj

#Local majorities
def getLocalMajorities(board, groups):
    localMajorities = []
    for group in groups:
        localMajority = getLocalMajority(board, group)
        localMajorities.append(localMajority)
    return localMajorities

def getCenterOfMass(locs):
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

#Center of masses
def getCenterOfMasses(groups):
    centerOfMasses = []
    for group in groups:
        centerOfMass = getCenterOfMass(group)
        centerOfMasses.append(centerOfMass)
    return centerOfMasses

def boundingBoxSize(group):
    boundingBoxSize = 0
    minPoint = [19, 19]
    maxPoint = [0,0]
    for loc in group:
        if loc[0] < minPoint[0]:
            minPoint[0] = loc[0]
        if loc[1] < minPoint[1]:
            minPoint[1] = loc[1]

        if loc[0] > maxPoint[0]:
            maxPoint[0] = loc[0]
        if loc[1] > maxPoint[1]:
            maxPoint[1] = loc[1]

    return (maxPoint[0] - minPoint[0]+1) * (maxPoint[1] - minPoint[1]+1)

# bounding box
def boundingBoxSizes(groups):
    boundingBoxSizes = []
    for group in groups:
        boundingBoxSize = boundingBoxSize(group)
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
    white = [(2,3), (1,2), (3,4), (1,4), (2,5), (0,0)]
    placeStones(board, black, white)
    groups = getGroups(board)

    twoClosestFriendlyBlocks(board, groups, getFirstOrderLiberties(board, groups))

    showBoard(board)


_main()