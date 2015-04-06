import numpy as np
import matplotlib.pyplot as plt



def getGroups(board):
    groups = []
    for i in range(0, len(board)):
        for j in range(0, len(board[i])):
            color = board[i][j]
            if color == -1 or color == 1:
                loc = (i,j)
                found = False
                for group in groups:
                    if loc in group:
                        found = True
                        break
                if not found:
                    groups.append(buildGroup(board, color, loc, set()))
    result = []
    for group in groups:
        result.append(list(group))
    return result
            
def buildGroup(board, color, loc, group):
    if not isOnBoard(loc) or board[loc[0]][loc[1]] != color or loc in group:
        return group
    group.add(loc)
    # up
    group.union(buildGroup(board,color,(loc[0] + 1,loc[1]),group))
    # down
    group.union(buildGroup(board,color,(loc[0] - 1,loc[1]),group))
    # left
    group.union(buildGroup(board,color,(loc[0],loc[1] - 1),group))
    # right
    group.union(buildGroup(board,color,(loc[0],loc[1] + 1),group))    
    
    return group
  
def isOnBoard(loc):
    return loc[0] >= 0 and loc[0] < 19 and loc[1] >= 0 and loc[1] < 19

#get size of the groups
def getSizes(board, groups):
    sizes = []
    for i in range(0, len(groups)):
        sizes.append(len(groups[i]))
    return sizes

#get perimeters of the groups
def getPerimeter(board, group):
    perimeter = set()
    color = board[group[0][0]][group[0][1]]
    for loc in group:
        # up
        if loc[0] < 18 and board[loc[0] + 1][loc[1]] != color:
            perimeter.add((loc[0] + 1, loc[1]))
        # down
        if loc[0] > 0 and board[loc[0] - 1][loc[1]] != color:
            perimeter.add((loc[0] - 1, loc[1]))
        # left
        if loc[1] > 0 and board[loc[0]][loc[1] - 1] != color:
            perimeter.add((loc[0], loc[1] - 1))
        # right
        if loc[1] < 18 and board[loc[0]][loc[1] + 1] != color:
            perimeter.add((loc[0], loc[1] + 1))
    return perimeter

# def getFirstOrderLiberties(board, group):
#     return getPerimeter(board, group).count(0)
   
# get First-order Liberties 
def getFirstOrderLiberties(board, groups):
    libertiesLists = []    
    for group in groups:
        liberties = set()
        for stone in group:
            # up
            if isOnBoard((stone[0] + 1, stone[1])) and board[stone[0] + 1][stone[1]] == 0:
                liberties.add((stone[0] + 1, stone[1]))
            # down
            if isOnBoard((stone[0] - 1, stone[1])) and board[stone[0] - 1][stone[1]] == 0:
                liberties.add((stone[0] - 1, stone[1]))
            # left
            if isOnBoard((stone[0], stone[1] - 1)) and board[stone[0]][stone[1] - 1] == 0:
                liberties.add((stone[0], stone[1] - 1))
            # right
            if isOnBoard((stone[0], stone[1] + 1)) and board[stone[0]][stone[1] + 1] == 0:
                liberties.add((stone[0], stone[1] + 1))
        libertiesLists.append(liberties)
    return libertiesLists
  
#get Second-order Liberties
def getSecondOrderLiberties(board, groups, firstOrderLiberties):
    libertiesLists = []    
    for i in range(0, len(firstOrderLiberties)):
        fol = firstOrderLiberties[i]
        liberties = set()
        for loc in fol:
            # up
            if isOnBoard((loc[0] + 1, loc[1])) and (loc[0] + 1, loc[1]) not in firstOrderLiberties[i] and board[loc[0] + 1][loc[1]] == 0:
                liberties.add((loc[0] + 1, loc[1]))
            # down
            if isOnBoard((loc[0] - 1, loc[1])) and (loc[0] - 1, loc[1]) not in firstOrderLiberties[i] and board[loc[0] - 1][loc[1]] == 0:
                liberties.add((loc[0] - 1, loc[1]))
            # left
            if isOnBoard((loc[0], loc[1] - 1)) and (loc[0], loc[1] - 1) not in firstOrderLiberties[i] and board[loc[0]][loc[1] - 1] == 0:
                liberties.add((loc[0], loc[1] - 1))
            # right
            if isOnBoard((loc[0], loc[1] + 1)) and (loc[0], loc[1] + 1) not in firstOrderLiberties[i] and board[loc[0]][loc[1] + 1] == 0:
                liberties.add((loc[0], loc[1] + 1))
                
        libertiesLists.append(liberties)
    return libertiesLists

#get Third-order Liberties 
def getThirdOrderLiberties(board, groups, firstOrderLiberties, secondOrderLiberties):
    libertiesLists = []    
    for i in range(0, len(secondOrderLiberties)):
        sol = secondOrderLiberties[i]
        liberties = set()
        for loc in sol:
            # up
            if isOnBoard((loc[0] + 1, loc[1])) and (loc[0] + 1, loc[1]) not in firstOrderLiberties[i] and (loc[0] + 1, loc[1]) not in secondOrderLiberties[i] and board[loc[0] + 1][loc[1]] == 0:
                liberties.add((loc[0] + 1, loc[1]))
            # down
            if isOnBoard((loc[0] - 1, loc[1])) and (loc[0] - 1, loc[1]) not in firstOrderLiberties[i] and (loc[0] - 1, loc[1]) not in secondOrderLiberties[i] and board[loc[0] - 1][loc[1]] == 0:
                liberties.add((loc[0] - 1, loc[1]))
            # left
            if isOnBoard((loc[0], loc[1] - 1)) and (loc[0], loc[1] - 1) not in firstOrderLiberties[i] and (loc[0], loc[1] - 1) not in secondOrderLiberties[i] and board[loc[0]][loc[1] - 1] == 0:
                liberties.add((loc[0], loc[1] - 1))
            # right
            if isOnBoard((loc[0], loc[1] + 1)) and (loc[0], loc[1] + 1) not in firstOrderLiberties[i] and (loc[0], loc[1] + 1) not in secondOrderLiberties[i] and board[loc[0]][loc[1] + 1] == 0:
                liberties.add((loc[0], loc[1] + 1))
                
        libertiesLists.append(liberties)
    return libertiesLists

#get all the liberties
def getLiberties(board, groups):
    firstOrderLiberties = getFirstOrderLiberties(board, groups)
    secondOrderLiberties = getSecondOrderLiberties(board, groups, firstOrderLiberties)
    thirdOrderLiberties = getThirdOrderLiberties(board, groups, firstOrderLiberties, secondOrderLiberties)
    
    libertiesList = []
    for i in range(len(groups)):
        libertiesList.append((len(firstOrderLiberties[i]), len(secondOrderLiberties[i]), len(thirdOrderLiberties[i])))
        
    return libertiesList


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
def twoClosestAdjacentFriendlyBlocks(board, groups, firstOrderLiberties):
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
        print(friendlyBlock)
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
    local = set()
    for loc in group:
        addClosePointsWithDistance(local, loc, 1)
    if dis == 1:
        return list(local - set(group))
    elif dis == 2:
        far = set()
        for loc in group:
            addClosePointsWithDistance(far, loc, 2)
        return list(far - local - set(group))

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
        print(opponentBlock)
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
    local = set()
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
    return [getCenterOfMass(x) for x in groups]

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

def findGroup(loc, groups):
    
    for group in groups:
        if loc in group:
            return group
    return False

#getting the labels list: dead = 0, alive = 1, draw??
def getLabels(board, board2):
    groups = getGroups(board)
    groups2 = getGroups(board2)

    labels = []
    for group in groups:
        endGroup = findGroup(group[0], groups2)
        if endGroup:
            print set(group).difference(endGroup)
            if len(set(group).difference(endGroup)) == 0:
                labels.append(1)
            else:
                labels.append(0)
        else:
            labels.append(0)
    print labels

    return labels


def _main():
    board = [[0 for x in range(19)] for x in range(19)] 

    black = [(3,6), (4,5), (2,2), (3,2),(4,2), (4,3), (4,4),(4,6),(3,1)]
    white = [(2,3), (1,2), (3,4), (1,4), (2,5), (0,0), (10,10)]
    placeStones(board, black, white)
    groups = getGroups(board)

    black2 = [(4,5), (2,2), (3,2),(4,2), (4,3), (4,4),(4,6),(3,1)]
    white2 = [(2,3), (1,2), (3,4), (1,4), (2,5), (10,11)]

    board2 = [[0 for x in range(19)] for x in range(19)] 

    placeStones(board2, black2, white2)

    getLabels(board, board2)
    # showBoard(board2)


_main()
