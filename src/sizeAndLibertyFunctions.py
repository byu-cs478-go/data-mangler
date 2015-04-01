# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 11:18:35 2015

@author: christopher
"""

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
		if not found	    
                    groups.push(buildGroup(board, color, loc, set()))
                
    
    return list(groups)
            
def buildGroup(board, color, loc, group):
    if not isOnBoard(loc) or board[loc[0],loc[1]] != color or loc in group:
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
    
def isOnBoard(loc):
    return loc[0] >= 0 and loc[0] < 19 and loc[1] >= 0 and loc[1] < 19

def getSizes(board, groups):
    sizes = []
    for i in range(0, len(groups)):
        sizes.push(len(groups[i]))
    return sizes

def getPerimeters(board, groups):
    perimeters = []
    for i in range(0, len(groups)):
        perimeter = {}
        for j in range(0, len(groups[i])):
            loc = groups[i][j]
            # up
            perimeter[(loc[0] + 1, loc[1])] = True
            # down
            perimeter[(loc[0] - 1, loc[1])] = True
            # left
            perimeter[(loc[0], loc[1] - 1)] = True
            # right
            perimeter[(loc[0], loc[1] + 1)] = True
        perimeters[i] = len(perimeter)
    return perimeters
    
def getFirstOrderLiberties(board, groups):
    libertiesLists = []    
    for i in range(0, len(groups)):
        group = groups[i]
        liberties = {}
        for j in range(0, len(group)):
            loc = group[i]
            # up
            if isOnBoard((loc[0] + 1, loc[1])) and board[loc[0]][loc[1]] == 0:
                liberties[(loc[0] + 1, loc[1])] = True
            # down
            if isOnBoard((loc[0] - 1, loc[1])) and board[loc[0]][loc[1]] == 0:
                liberties[(loc[0] - 1, loc[1])] = True
            # left
            if isOnBoard((loc[0], loc[1] - 1)) and board[loc[0]][loc[1]] == 0:
                liberties[(loc[0], loc[1] - 1)] = True
            # right
            if isOnBoard((loc[0], loc[1] + 1)) and board[loc[0]][loc[1]] == 0:
                liberties[(loc[0], loc[1] + 1)] = True
                
        libertiesLists[i] = (liberties, len(liberties))
    return libertiesLists
    
def getSecondOrderLiberties(board, groups, firstOrderLiberties):
    libertiesLists = []    
    for i in range(0, len(groups)):
        group = groups[i]
        liberties = {}
        for j in range(0, len(group)):
            loc = group[i]
            # up
            if isOnBoard((loc[0] + 1, loc[1])) and not firstOrderLiberties[i][(loc[0] + 1, loc[1])] and board[loc[0] + 1][loc[1]] == 0:
                liberties[(loc[0] + 1, loc[1])] = True
            # down
            if isOnBoard((loc[0] - 1, loc[1])) and not firstOrderLiberties[i][(loc[0] - 1, loc[1])] and board[loc[0] - 1][loc[1]] == 0:
                liberties[(loc[0] - 1, loc[1])] = True
            # left
            if isOnBoard((loc[0], loc[1] - 1)) and not firstOrderLiberties[i][(loc[0], loc[1]) - 1] and board[loc[0]][loc[1] - 1] == 0:
                liberties[(loc[0], loc[1] - 1)] = True
            # right
            if isOnBoard((loc[0], loc[1] + 1)) and not firstOrderLiberties[i][(loc[0], loc[1]) + 1] and board[loc[0]][loc[1] + 1] == 0:
                liberties[(loc[0], loc[1] + 1)] = True
                
        libertiesLists[i] = (liberties, len(liberties))
    return libertiesLists
    
def getThirdOrderLiberties(board, groups, firstOrderLiberties, secondOrderLiberties):
    libertiesLists = []    
    for i in range(0, len(groups)):
        group = groups[i]
        liberties = {}
        for j in range(0, len(group)):
            loc = group[i]
            # up
            if isOnBoard((loc[0] + 1, loc[1])) and not firstOrderLiberties[i][(loc[0] + 1, loc[1])] and not secondOrderLiberties[i][(loc[0] + 1, loc[1])] and board[loc[0] + 1][loc[1]] == 0:
                liberties[(loc[0] + 1, loc[1])] = True
            # down
            if isOnBoard((loc[0] - 1, loc[1])) and not firstOrderLiberties[i][(loc[0] - 1, loc[1])] and not secondOrderLiberties[i][(loc[0] - 1, loc[1])] and board[loc[0] - 1][loc[1]] == 0:
                liberties[(loc[0] - 1, loc[1])] = True
            # left
            if isOnBoard((loc[0], loc[1] - 1)) and not firstOrderLiberties[i][(loc[0], loc[1]) - 1] and not secondOrderLiberties[i][(loc[0], loc[1]) - 1] and board[loc[0]][loc[1] - 1] == 0:
                liberties[(loc[0], loc[1] - 1)] = True
            # right
            if isOnBoard((loc[0], loc[1] + 1)) and not firstOrderLiberties[i][(loc[0], loc[1]) + 1] and not secondOrderLiberties[i][(loc[0], loc[1]) + 1] and board[loc[0]][loc[1] + 1] == 0:
                liberties[(loc[0], loc[1] + 1)] = True
                
        libertiesLists[i] = len(liberties)
    return libertiesLists
