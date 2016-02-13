import sys


def partsOfSpeech (tweet, list):
    total = 0
    for elem in list:
        total += tweet.count(elem)
    return total


def findWords (tweet, words):
    total = 0
    for word in words:
        total += tweet.count(word)
    return total


def numUpper(tweet):
    total = 0
    for word in tweet.split(" "):
        if word.isalpha():
            if word.upper() == word and len(word) > 2:
                total+=1
    return total

def tokenLen(tweet):
    sum = 0.0
    total = 0.0
    for word in tweet.split(" "):
        sum += len(word)
        total +=1
    if total == 0:
        return 0
    return sum/total

def unTag(tweet):
    words = tweet.split(" ")
    untagged = ""
    for word in words:
        tag = word.split("/")
        untagged+= tag[0].lower()+" "
    return untagged

def specialUnTag(tweet):
    words = tweet.split(" ")
    untagged = ""
    for word in words:
        tag = word.split("/")
        untagged+= tag[0]+" "
    return untagged

firstPerson = [" i ", " me ", " my ", " mine ", " we ", " us ", " our ", " ours "]
secondPerson = [" you ", " your ", " yours ", " u ", " ur ", " urs "]
thirdPerson = [" he ", " him ", " his ", " she ", " her ", " hers ", " it ", " its ", " they ", " them ", " their ",
               " theirs "]
slang = [" smh ",  " fwb ",  " lmfao ",  " lmao ",  " lms ",  " tbh ",  " ro ",  " wtf ",  " bff ",  " wyd ",  " lylc ",
         " brb ",  " atm ",  " imao ",  " sml ",  " btw ", " bw ",  " imho ",  " fyi ",  " ppl ",  " sob ",  " ttyl ",
         " imo ",  " ltr ",  " thx ",  " kk ",  " omg ",  " ttys ",  " afn ",  " bbs ",  " cya ", " ez ",  " f2f ",
         " gtr ", " ic ", " jk ", " k ", " ly " , " ya ", " nm ", " np ", " plz ", " ru ", " tc ", " tmi ",
         " ym ", " ur ", " u ", " sol "]


futureTenseUntagged = [" gonna ", " 'll "]
futureTenseTweet = [" will/MD", "going/VBG to/TO"]



def arffIt (tweet, polarity, twt):

    unTagged  = unTag(tweet)
    regular = specialUnTag(tweet)

    #Persons
    twt.write(str(findWords(unTagged, firstPerson))+", ")
    twt.write(str(findWords(unTagged, secondPerson))+", ")
    twt.write(str(findWords(unTagged, thirdPerson))+", ")
    twt.write(str(partsOfSpeech(tweet, ["/CC "]))+", ")
    twt.write(str(partsOfSpeech(tweet, ["/VBD "]))+", ")
    twt.write(str(findWords(unTagged, futureTenseUntagged) + findWords(tweet, futureTenseTweet))+", ")


    #Symbols
    twt.write(str(findWords(unTagged, [" , "]))+", ")
    twt.write(str(findWords(unTagged, [" : ", " ; "]))+", ")
    twt.write(str(findWords(unTagged, [" - "]))+", ")
    twt.write(str(findWords(unTagged, ["(", ")"]))+", ")
    twt.write(str(findWords(unTagged, [" ... "]))+", ")

    #PoS

    twt.write(str(partsOfSpeech(tweet, ["/NN ", "/NNS "]))+", ")
    twt.write(str(partsOfSpeech(tweet, ["/NNP ", "/NNPS "]))+", ")
    twt.write(str(partsOfSpeech(tweet, ["/RB ", "/RBR ", "/RBS "]))+", ")
    twt.write(str(partsOfSpeech(tweet, ["/WDT ", "/WP ", "/WP$ ", "/WRB "]))+", ")
    #print regular.split(" ")
    twt.write(str(findWords(unTagged, slang))+", ")
    twt.write(str(numUpper(regular))+", ")


    #Still missing Future tense, Slang, maybe more
    #Future Tense


    twt.write(str(float(len(unTagged.split(" ")) -1 -float(unTagged.count("\n")) ) / float(unTagged.count("\n")))+", ")   #sentences
    twt.write(str(tokenLen(unTagged))+", ")
    twt.write(str(unTagged.count("\n"))+", ")   #sentences
    twt.write(str(polarity)+"\n")               #polarity
    return 1

outFile = open(sys.argv[2], 'w')
with open(sys.argv[1], "r") as twt:
    tweet = ""
    polarity = 0
    #Schema
    outFile.write("@relation test\n")
    outFile.write("\n")
    outFile.write("@attribute firstPersonPronouns numeric\n")
    outFile.write("@attribute secondPersonPronouns numeric\n")
    outFile.write("@attribute thirdPersonPronouns numeric\n")
    outFile.write("@attribute coordinatingConjunctions numeric\n")
    outFile.write("@attribute pastTenseVerbs numeric\n")
    outFile.write("@attribute futureTenseVerbs numeric\n")
    outFile.write("@attribute commas numeric\n")
    outFile.write("@attribute colonsAndSemicolons numeric\n")
    outFile.write("@attribute dashes numeric\n")
    outFile.write("@attribute parentheses numeric\n")
    outFile.write("@attribute ellipses numeric\n")
    outFile.write("@attribute commonNouns numeric\n")
    outFile.write("@attribute properNouns numeric\n")
    outFile.write("@attribute adverbs numeric\n")
    outFile.write("@attribute whWords numeric\n")
    outFile.write("@attribute slang numeric\n")
    outFile.write("@attribute upperCaseWords numeric\n")
    outFile.write("@attribute lengthOfSentence numeric\n")
    outFile.write("@attribute lengthOfToken numeric\n")
    outFile.write("@attribute numberOfSentences numeric\n")
    outFile.write("\n")
    outFile.write("@data\n")
    if len(sys.argv) < 4:
        for line in twt:
            if line == '<A="4">\n':
                if tweet:
                    arffIt(tweet, polarity, outFile)
                polarity = 4
                tweet = ""
            elif line == '<A="0">\n':
                if tweet:
                    arffIt(tweet, polarity, outFile)
                polarity = 0
                tweet = ""
            else:
                tweet+= line
    else:
        first  = True
        posNum = 0
        negNum = 0
        for line in twt:
            print(posNum)
            print(sys.argv[3])
            if line == '<A="4">\n' and posNum < int(sys.argv[3]):
                if first:
                    first = False
                    tweet = ""
                if tweet:
                    arffIt(tweet, polarity, outFile)
                polarity = 4
                tweet = ""
                posNum+=1
            elif line == '<A="0">\n' and negNum < int(sys.argv[3]):
                if tweet:
                    arffIt(tweet, polarity, outFile)
                polarity = 0
                tweet = ""
                negNum +=1
            else:
                tweet+= line


