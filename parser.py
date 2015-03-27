import numpy as np
import matplotlib.pyplot as plt


#isOn board
def isOnBoard(loc):
    return loc[0] >= 0 and loc[0] < 19 and loc[1] >=0 and loc[1] < 19

#Protected liberties


#Auto-atari liberties
def autoAtariLiberties():
    return null

#Shared liberties
def sharedLiberties():
    return null

#Two closest Adjacent opponent blocks
def twoClosestAdjacentOppoentBlockS():
    return null

def localMajority():
    return null

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

    print distances
    sortedDistance = sorted(distances)

    print sortedDistance
    return (sortedDistance[0], sortedDistance[1])

# bounding box
def boundingBoxSize(points):
    boundingBoxSize = 0

    minPoint = [10, 10]
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

    boundingBoxSize = (maxPoint[0] - minPoint[0]) * (maxPoint[1] - minPoint[1])

    return boundingBoxSize

def _main():
    points = [(1,1), (3,6), (2,3), (4,5)]
    area = boundingBoxSize(points)
    
    print centerOfMass(points)


_main()