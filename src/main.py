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



def sgf_node_parse(nodestr):
    pass

def sgfarray_metadata_read():
    pass

def sgf_tree_build():
    pass

def sgf_step_read(old, sgfstr):
    pass

def sgf_done_read(sgfstr)

def sgf_process(sgfstr):
    # Get the states in the game that will be analyzed.
    states = sgf_states_get()

    # Run the analysis functions on the states.
    for state in states:
        pass



def sgfboard_empty_gen():
    return [[0 for j in range (19)] for i in range(19)]



# def sgfstr_sgfboard_step(instr, oldboard):
#     newboard = copy.deepcopy(oldboard)

#     tmpstr = instr.lstrip()

#     # TODO Use a dict here? Assumes that lettering is
#     # lowercase. Assumes no spaces inside property. Is orientation
#     # going to be an issue?
#     if   tmpstr[0] == 'W':
#         newboard[ord(tmpstr[2]) - 96][ord(tmpstr[3]) - 96] = 1
#     elif tmpstr[1] == 'B':
#         newboard[ord(tmpstr[2]) - 96][ord(tmpstr[3]) - 96] = -1
#     elif:
#         return None
#     else:
#         # TODO Add additional diagnostic info. Global (cannot be set
#         # from?) variables?
#         sys.exit("Error: Unrecognized property.")



def sgfstr_states_gen(instr):
    boards = [sgfboard_empty_gen()]

    prop = [None, None, None]
    
    for x in instr:
        if   x == ' ' or x == '\t' or x == '\n':
            pass
        elif x == ';':
            pass
        elif x == '[':
            pass
        elif x == ']':
            newboard = copy.deepcopy(boards[-1])
            newboard[prop[1]][prop[2]] = prop[0]
            boards.append(newboard)
            prop = [None, None, None]    
        elif x == '(':
            pass
        elif x == ')':
            # if prop != [None, None, None]:
            #     sys.exit("Error: Premature property end.")
            # else:
            break
        elif x == 'W':
            if prop[0] == None:
                prop[0] = 1
        elif x == 'B':
            if prop[0] == None:
                prop[0] = -1
        # TODO Does not handle capital grid coordinates.
        elif x in (a,t):
            if prop[0] != None:
                if prop[1] == None:
                    prop[1] = ord(x) - 96
                elif prop[2] == None:
                    prop[2] = ord(x) - 96
                else:
                    sys.exit("Error: Too many coordinates in property.")
        else:
            sys.exit("Error: Parser broken.")

    return boards



def sgfstr_sample(instr):
    # TODO Consume metadata.

    states = [sgfboard_empty_gen()]

    while states[-1] != None:
        states.append(sgf_step_read(instr, states[-1]))

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
