import main
import parserFunctions

def test(inpath):
    with open(inpath, 'r') as infile:
        for x in main.sgfstr_sample(infile.read()):
            parserFunctions.showBoard(x)

#test("BloodVomitingGame.sgf")
#test("DosakusMasterpiece.sgf")
#test("SeigenvsShusai.sgf")
#test("ShusakuvsInseki.sgf")
#test("ShuwavsInseki1.sgf")
#test("ShuwavsInseki3.sgf")
