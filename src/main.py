import sys
import os
import subprocess

# def tmpdir_init:
#     if not os.path.exists('tmp'):
#         os.makedirs('tmp')

# def sgfstr_sgfarray_convert (sgfstr):
#     for node in string.split(sgfstr, ';'):
#         if node.split()

def sgfarray_metadata_read():

def sgf_tree_build():
    pass

def sgfarray_step(old, sgfstr):
    

def sgf_process(sgfstr):
    # Get the states in the game that will be analyzed.
    states = sgf_states_get()

    # Run the analysis functions on the states.
    for state in states:
        



def sgffile_process(infile, outfile):
    # 
    pass



def main():
    if not os.path.exists(sys.argv[2]):
        os.makedirs(sys.argv[2])
    else:
        sys.exit("Error: Specified tmp directory already exits.")

    cmd = 'find ' + sys.argv[1] + ' -name \'*.sgf\''
    sp = subprocess.Popen(cmd, universal_newlines=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    for inpath in sp.communicate()[0].split('\n'):
        if inpath != '':
            outpath = sys.argv[2] + inpath[len(sys.argv[1]):] + ".mangle"
            if not os.path.exists(os.path.dirname(outpath)):
                os.makedirs(os.path.dirname(outpath))
            with open(inpath, 'r') as infile, open(outpath, 'w') as outfile:
                sgffile_process(infile, outfile)
