import main
import parserFunctions

def test(inpath):
    with open(inpath, 'r') as infile:
        for x in main.sgfstr_sample(infile.read())[:-1]:
            parserFunctions.showBoard(x)

#test("../test/data/honinbo/BloodVomitingGame.sgf")
#test("../test/data/honinbo/DosakusMasterpiece.sgf")
#test("../test/data/honinbo/SeigenvsShusai.sgf")
#test("../test/data/honinbo/ShusakuvsInseki.sgf")
#test("../test/data/honinbo/ShuwavsInseki1.sgf")
#test("../test/data/honinbo/ShuwavsInseki3.sgf")

#test("../test/data/bagaller/bagaller-azlan.sgf")
#test("../test/data/bagaller/bagaller-azlan-2.sgf")
#test("../test/data/bagaller/bagaller-ben0.sgf")
#test("../test/data/bagaller/bagaller-Dimon.sgf")
#test("../test/data/bagaller/bagaller-jadad2.sgf")
#test("../test/data/bagaller/bagaller-Joker7.sgf")
#test("../test/data/bagaller/bagaller-misterious.sgf")
#test("../test/data/bagaller/bagaller-yumenpass.sgf")
