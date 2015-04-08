import sys
import os
import subprocess
import copy
import math

from parserFunctions import *



class DataManglerException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)



# This header goes at the top of the generated .arff file. It includes
# the attribute specifiers and tags up to '@data'.
ARFFHEADER = ("@relation go\n\n"
              "@attribute groupsize NUMERIC\n"
              "@attribute perimetersize NUMERIC\n"
              "@attribute opponentsize NUMERIC\n"
              "@attribute firstorderliberties NUMERIC\n"
              "@attribute secondorderliberties NUMERIC\n"
              "@attribute thirdorderliberties NUMERIC\n"
              "@attribute sharedliberties NUMERIC\n"
              "@attribute caob0size NUMERIC\n"
              "@attribute caob0liberty NUMERIC\n"
              "@attribute caob1size NUMERIC\n"
              "@attribute caob1liberty NUMERIC\n"
              "@attribute cafb0size NUMERIC\n"
              "@attribute cafb0liberty NUMERIC\n"
              "@attribute cafb1size NUMERIC\n"
              "@attribute cafb1liberty NUMERIC\n"
              "@attribute localmajority NUMERIC\n"
              "@attribute centerofmass0 NUMERIC\n"
              "@attribute centerofmass1 NUMERIC\n"
              "@attribute bbsize NUMERIC\n"
              "@attribute class {alive, dead}\n\n"
              "@data\n")

# This variable controls the number of board samples taken from a
# given game.
SAMPLERATE = 3



def sgfboard_empty_gen(x, y):
    return [[0 for j in range (x)] for i in range(y)]



def sgfboard_merge(board, groups, s0, s1):
    # TODO Could we rework this to make it more efficient (by
    # returning and caching indices or something)

    # TODO Would an initial check to see if s0 and s1 are in the same group save time?

    # Initial values for s0group and s1group .
    s0group = None
    s1group = None

    # Find the indices of the groups containing s0 and s1.
    for x in groups:
        if s0 in x:
            # TODO is this a shallow copy?
            s0group = x
        if s1 in x:
            # TODO is this a shallow copy?
            s1group = x

    # TODO Can we eliminate this test?
    if s0group != s1group:
        s0group |= s1group
        groups.remove(s1group)

    # Not strictly necessary.
    return (board, groups)



def sgfboard_group_remove(board, group):
    # Remove the group from the board.
    for x in group:
        board[x[0]][x[1]] = 0

    # Remove the group from groups.
    group.remove(group)

    # Not strictly necessary.
    return (board, groups)



def sgfboard_capture(board, groups, s0, s1):
    # Find the group of s1. TODO Is there a better way to do this?
    s1group = None
    for x in groups:
        if s1 in x:
            # TODO Is this really a shallow copy?
            s1group = x

    # Test to see if the capture actually occurs.
    if getFirstOrderLiberties(board, [s1group]) == []:
        sgfboard_group_remove(board, s1group)

    # Not strictly necessary.
    return (board, groups)



def sgfboard_step(board, groups, color, xcoord, ycoord):
    # Place the stone.
    board[xcoord][ycoord] = color

    # Add the stone to its own group.
    groups.append({(xcoord, ycoord)})

    # TODO Make this a static variable?
    INTERFERENCE = {-2 : sgfboard_merge,
                    -1 : lambda x,y,z,a : None,
                     0 : sgfboard_capture,
                     1 : lambda x,y,z,a : None,
                     2 : sgfboard_merge,}

    # Check each of the stone's neighbors, merge groups if
    # neccesary, and analyze the board to find stones that
    # need to be removed.
    if 0 < xcoord:
        INTERFERENCE[color+board[xcoord-1][ycoord]](board, groups, (xcoord, ycoord),(xcoord-1, ycoord))

    if xcoord < 18:
        INTERFERENCE[color+board[xcoord+1][ycoord]](board, groups, (xcoord, ycoord),(xcoord+1, ycoord))

    if 0 < ycoord:
        INTERFERENCE[color+board[xcoord][ycoord-1]](board, groups, (xcoord, ycoord),(xcoord, ycoord-1))

    if ycoord < 18:
        INTERFERENCE[color+board[xcoord][ycoord+1]](board, groups, (xcoord, ycoord),(xcoord, ycoord+1))

    # Not strictly necessary.
    return (board, groups)
                        


def sgfstr_boards_gen(instr):
    boards = [sgfboard_empty_gen(19, 19)]
    # TODO Retain old groups for cache?
    groups = []
    # TODO Add dict for efficiency reasons.

    # TODO Does this consume metadata?
    start = instr.find(';', instr.find(';') + 1)

    prop = [None, None, None]
    
    for x in instr[start:]:
        # Ignore whitespace.
        if   x == ' ' or x == '\t' or x == '\n':
            pass

        # Syntax characters.
        elif x == ';':
            boards.append(copy.deepcopy(boards[-1]))
        elif x == '[':
            pass
        elif x == ']':
            if prop[0] != None:
                sgfboard_step(boards[-1], groups, prop[0], prop[1], prop[2])
                prop = [None, None, None]
            elif (prop[1] == None) or (prop[2] == None):
                raise DataManglerException("Error: Incomplete move specifier.")
        elif x == '(':
            pass
        elif x == ')':
            # if prop != [None, None, None]:
            #     sys.exit("Error: Premature property end.")
            # else:
            break

        # White and Black move processing. TODO This also detects
        # properties with W or B in them.
        elif x == 'W':
            if prop[0] == None:
                prop[0] = 1
        elif x == 'B':
            if prop[0] == None:
                prop[0] = -1
        # TODO Uncertain syntax. Does not handle capital grid
        # coordinates.
        elif ord(x) in range(ord('a'), ord('t')+1):
            if prop[0] != None:
                if prop[1] == None:
                    prop[1] = (ord(x) - 97)%19
                elif prop[2] == None:
                    prop[2] = (ord(x) - 97)%19
                else:
                    raise DataManglerException("Error: Too many coordinates in property.")

        # TODO Hack solution, handles the above noted issue with the
        # WB detector. Overlaps function with the double-else below.
        elif prop[0] != None:
            raise DataManglerException("Error: (likely) Un-handleable roperty has W or B in name.")

        # Fallthrough for characters we don't recognize or don't care
        # about.
        else:
            # Don't recognize (outside of a W or B property).
            if prop[0] == None:
                raise DataManglerException("Error: Parser unable to cope with file.")
            # Don't care (everywhere else).
            else:
                pass

    return boards



def sgfstr_sample(instr):
    boards = sgfstr_boards_gen(instr)
    # TODO There may be an unexpected trimming effect here that
    # removes games of insufficient length.
    inc = math.floor((len(boards)-1)/(SAMPLERATE + 1))
    sample = [boards[x] for x in range(inc,(len(boards)-1),inc)]
    sample.append(boards[-1])
    return sample



def sgfstr_process(instr):
    data = []

    boards = sgfstr_sample(instr)[:-1]
    finalgroups = getGroups(boards[-1])
    for board in boards:
        groups = getGroups(board)
        #liberties = getLiberties(board, groups)
        fols = getFirstOrderLiberties(board, groups)
        sols = getSecondOrderLiberties(board, groups, fols)
        tols = getThirdOrderLiberties(board, groups, fols, sols)
        slibs = sharedLiberties(board, groups, fols)
        boarddata = []
        for i,x in enumerate(groups):
            # TODO There is probably a way to make getPerimeters work
            # faster.
            per = getPerimeter(board, x)
            oadj = twoClosestAdjacentOpponentBlock(board, x, fols, groups)
            fadj = twoClosestAdjacentFriendlyBlock(board, x, fols, groups)
            com = getCenterOfMass(x)

            xset = set(x)
            label = False
            for y in finalgroups:
                label = xset.issubset(set(y)) or label

            boarddata.append([getSizes(board, [x])[0],
                              len(per),
                              # TODO Opponents might not work correctly.
                              # len(per) - [board[x][y] for x,y in per].count(0)
                              [board[x][y] for x,y in per].count(-board[x[0][0]][x[0][1]]),
                              len(fols[i]),
                              len(sols[i]),
                              len(tols[i]),
                              # TODO Protected liberties.
                              # TODO Auto-atari liberties.
                              slibs[i],
                              oadj[0][0],
                              oadj[0][1],
                              oadj[1][0],
                              oadj[1][1],
                              fadj[0][0],
                              fadj[0][1],
                              fadj[1][0],
                              fadj[1][1],
                              getLocalMajority(board, x),
                              com[0],
                              com[1],
                              boundingBoxSize(x),
                              # TODO Eyes.
                              'alive' if label else 'dead'
                          ])
        data.extend(boarddata)

    return data



def arfffile_write(outfile, data):
    # Prepend header.
    outfile.write(ARFFHEADER)

    # Dump the contents of data to the .arff file.
    for x in data:
        for y in x:
            outfile.write("\t" + str(y) + ",")
        outfile.write("\n")



def main_v(findpath, outpath):
    cmd = 'find ' + findpath + ' -name \'*.sgf\''
    sp = subprocess.Popen(cmd, universal_newlines=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    arffdata = []
    for inpath in sp.communicate()[0].split('\n'):
        if inpath != '':
            with open(inpath, 'r') as infile:
                print(inpath + " ")
                try:
                    x = sgfstr_process(infile.read())
                except DataManglerException:
                    print("failed.")
                else:
                    arffdata.extend(x)
                    print("succeeded.")

    with open(outpath, 'w') as arfffile:
        arfffile_write(arfffile, arffdata)



#def main():
main_v(sys.argv[1], sys.argv[2])
