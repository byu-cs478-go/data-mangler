import main
import parserFunctions

def test(inpath):
    with open(inpath, 'r') as infile:
        for x in main.sgfstr_sample(infile.read()):
            parserFunctions.showBoard(x)
