import main
import parserFunctions

def test(inpath):
    with open(inpath, 'r') as infile:
        for x in main.sgfstr_sample(infile.read()):
            parserFunctions.showBoard(x)

#test("honinbo/BloodVomitingGame.sgf")
#test("honinbo/DosakusMasterpiece.sgf")
#test("honinbo/SeigenvsShusai.sgf")
#test("honinbo/ShusakuvsInseki.sgf")
#test("honinbo/ShuwavsInseki1.sgf")
#test("honinbo/ShuwavsInseki3.sgf")

#test("bagaller/bagaller-azlan.sgf")
#test("bagaller/bagaller-azlan-2.sgf")
#test("bagaller/bagaller-ben0.sgf")
#test("bagaller/bagaller-Dimon.sgf")
#test("bagaller/bagaller-jadad2.sgf")
#test("bagaller/bagaller-Joker7.sgf")
#test("bagaller/bagaller-misterious.sgf")
#test("bagaller/bagaller-yumenpass.sgf")
