import sys
import os
import subprocess
import copy



# This header goes at the top of the generated .arff file. It includes
# the attribute specifiers and tags up to '@data'.
ARFFHEADER = ("")

# This variable controls the number of board samples taken from a
# given game.
SAMPLERATE = 1



def sgfboard_empty_gen():
    return [[0 for j in range (19)] for i in range(19)]



def sgfstr_states_gen(instr):
    boards = [sgfboard_empty_gen()]

    # TODO Consume metadata?
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
                boards[-1][prop[1]][prop[2]] = prop[0]
                # TODO Apply the rules here?
                prop = [None, None, None]
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
        # TODO Uncertain syntax. Does not handle capital grid coordinates.
        elif ord(x) in range(ord(a), ord(t)+1):
            if prop[0] != None:
                if prop[1] == None:
                    prop[1] = ord(x) - 96
                elif prop[2] == None:
                    prop[2] = ord(x) - 96
                else:
                    sys.exit("Error: Too many coordinates in property.")

        # Fallthrough for characters we don't recognize or don't care about.
        else:
            # Don't recognize (outside of a W or B property).
            if prop[0] == None:
                sys.exit("Error: Parser unable to cope with file.")
            # Don't care (everywhere else).
            else:
                pass

    return boards



def sgfstr_sample(instr):
    boards = sgfstr_boards_gen(instr)
    inc = floor((len(states)-1)/(SAMPLERATE + 1))
    return [states[x] for x in range(inc,(len(states)-1),inc)]



def sgfstr_process(instr):
    data = []

    boards = sgfstr_sample(instr)
    for board in boards:
        groups = getGroups(board)
        boarddata = [[x] for x in getSizes(board, groups)]
        data.extend(boarddata)

    return data



def arfffile_write(outfile, data):
    # Prepend header.
    outfile.write(ARFFHEADER)

    # Dump the contents of data to the .arff file.
    for x in data:
        for y in x:
            outfile.write("\t" + y + ",")
        outfile.write("\n")



def main():
    cmd = 'find ' + sys.argv[1] + ' -name \'*.sgf\''
    sp = subprocess.Popen(cmd, universal_newlines=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    arffdata = []
    for inpath in sp.communicate()[0].split('\n'):
        if inpath != '':
            with open(inpath, 'r') as infile:
                arffdata.extend(sgfstr_process(infile.read()))

    with open(sys.args[2], 'w') as arfffile:
        arfffile_write(arfffile, arffdata)
