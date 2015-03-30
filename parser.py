import numpy as np
import matplotlib.pyplot as plt
from sets import Set



#isOn board
def isOnBoard(loc):
    return loc[0] >= 0 and loc[0] < 19 and loc[1] >=0 and loc[1] < 19

#Protected liberties
def protectedLiberties():
    return null

#Auto-atari liberties
def autoAtariLiberties():
    return null

#Shared liberties
def sharedLiberties():
    return null

#Two closest Adjacent opponent blocks
def twoClosestAdjacentOppoentBlockS():
    return null

def addClosePoints(set, point):
    for i in range(3):
        for j in range(3):
            np = ((point[0] + i-1), (point[1] + j-1))
            if isOnBoard(np):
                set.add(np)
    far = []
    far.append(((point[0]), (point[1]+2)))
    far.append(((point[0]-2), (point[1])))
    far.append(((point[0]+2), (point[1])))
    far.append(((point[0]), (point[1]-2)))
    
    for p in far:
        if isOnBoard(p):
            set.add(p)

def getLocalPoints(points):
    local = Set()
    for p in points:
        addClosePoints(local, p)
    return local

def localMajority(board, points):
    color = board[points[0][1]][points[0][0]]

    localPoints = getLocalPoints(points)
    # plot(localPoints)
    diff = 0
    for p in localPoints:
        x = p[1]
        y = p[0]

        diff += board[x][y]

    maj = diff
    if color == 1: # when white is 1
        maj = -diff
    return maj

def centerOfMass(points):
    distances = []
    for point in points:
        #up
        distances.append(18 - point[1]) 

        #down
        distances.append(point[1])

        #right
        distances.append(18 - point[0])

        #lefty
        distances.append(point[0])

    sortedDistance = sorted(distances)

    return (sortedDistance[0], sortedDistance[1])

# bounding box
def boundingBoxSize(points):
    boundingBoxSize = 0

    minPoint = [19, 19]
    maxPoint = [0,0]

    for point in points:
        if point[0] < minPoint[0]:
            minPoint[0] = point[0]
        if point[1] < minPoint[1]:
            minPoint[1] = point[1]

        if point[0] > maxPoint[0]:
            maxPoint[0] = point[0]
        if point[1] > maxPoint[1]:
            maxPoint[1] = point[1]

    boundingBoxSize = (maxPoint[0] - minPoint[0]+1) * (maxPoint[1] - minPoint[1]+1)

    return boundingBoxSize

def plot(points):
    a = []
    b = []
    for p in points:
        a.append(p[0])
        b.append(p[1])


    plt.figure('points')
    r = 100
    plt.scatter(a, b, marker='o', s=r, color='black')
    plt.xlim(0,19)
    plt.ylim(0,19)
    plt.show()


def initBoard(row, col):
    return [[0 for x in range(col)] for x in range(row)] 

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
        board[p[1]][p[0]] = -1
    for p in white:
        board[p[1]][p[0]] = 1


def _main():
    board = initBoard(19, 19)

    black = [(3,6), (4,5), (2,2), (3,2),(4,2), (4,3), (4,4),(4,6)]
    white = [(2,3), (1,2), (3,4), (1,4), (2,5)]
    placeStones(board, black, white)

    print localMajority(board, black)
    showBoard(board)


_main()