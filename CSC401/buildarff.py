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

def schema(outFile):
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
    outFile.write("@attribute score {0,4}\n")
    outFile.write("@data\n")

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
    outFile.write("@attribute score {0,4}\n")
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
    elif len(sys.argv) == 4:
        first = True
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
    else:
        #split the file based on the arguments (e.g. 2000 1000)
        #make counter for train files, same for test files
        #write first increment to test (1000 0), rest to train (2000 1000)
        #increment these each time

        first = True
        posNum = 0
        negNum = 0
        count = 0
        trainFile1100 = open("trainFile1100.arff","w")
        trainFile2200 = open("trainFile2200.arff","w")
        trainFile3300 = open("trainFile3300.arff","w")
        trainFile4400 = open("trainFile4400.arff","w")
        trainFile5500 = open("trainFile5500.arff","w")
        trainFile6600 = open("trainFile6600.arff","w")
        trainFile7700 = open("trainFile7700.arff","w")
        trainFile8800 = open("trainFile8800.arff","w")
        trainFile9900 = open("trainFile9900.arff","w")
        trainFile11000 = open("trainFile11000.arff","w")
        testFile1100 = open("testFile1100.arff","w")
        testFile2200 = open("testFile2200.arff","w")
        testFile3300 = open("testFile3300.arff","w")
        testFile3300 = open("testFile3300.arff","w")
        testFile4400 = open("testFile4400.arff","w")
        testFile5500 = open("testFile5500.arff","w")
        testFile6600 = open("testFile6600.arff","w")
        testFile7700 = open("testFile7700.arff","w")
        testFile8800 = open("testFile8800.arff","w")
        testFile9900 = open("testFile9900.arff","w")
        testFile11000 = open("testFile11000.arff","w")

        #Schema
        schema(trainFile1100)
        schema(trainFile2200)
        schema(trainFile3300)
        schema(trainFile4400)
        schema(trainFile5500)
        schema(trainFile6600)
        schema(trainFile7700)
        schema(trainFile8800)
        schema(trainFile9900)
        schema(trainFile11000)
        schema(testFile1100)
        schema(testFile2200)
        schema(testFile3300)
        schema(testFile4400)
        schema(testFile5500)
        schema(testFile6600)
        schema(testFile7700)
        schema(testFile8800)
        schema(testFile9900)
        schema(testFile11000)

        for line in twt:
            # print(posNum)
            # print(sys.argv[3])
            print(count)
            if line == '<A="4">\n' and posNum < int(sys.argv[3]) and count + 5500 >= int(sys.argv[4]):
                if first:
                    first = False
                    tweet = ""
                if tweet:
                    if 0 < count <= 6050:
                        arffIt(tweet, polarity, testFile1100)
                    elif count >= 6050:
                        arffIt(tweet, polarity, trainFile1100)
                    if 6050 <= count <= 6600:
                        arffIt(tweet, polarity, testFile2200)
                    elif count <= 6050 or count >= 6600:
                        arffIt(tweet, polarity, trainFile2200)
                    if 6600 <= count <= 7150:
                        arffIt(tweet, polarity, testFile3300)
                    elif count <= 6600 or count >= 7150:
                        arffIt(tweet, polarity, trainFile3300)
                    if 7150 <= count <= 7700:
                        arffIt(tweet, polarity, testFile4400)
                    elif count <= 7150 or count >= 7700:
                        arffIt(tweet, polarity, trainFile4400)
                    if 7700 <= count <= 8250:
                        arffIt(tweet, polarity, testFile5500)
                    elif count <= 7700 or count >= 8250:
                        arffIt(tweet, polarity, trainFile5500)
                    if 8250 <= count <= 8800:
                        arffIt(tweet, polarity, testFile6600)
                    elif count <= 8250 or count >= 8800:
                        arffIt(tweet, polarity, trainFile6600)
                    if 8800 <= count <= 9350:
                        arffIt(tweet, polarity, testFile7700)
                    elif count <= 8800 or count >= 9350:
                        arffIt(tweet, polarity, trainFile7700)
                    if 9350 <= count <= 9900:
                        arffIt(tweet, polarity, testFile8800)
                    elif count <= 9350 or count >= 9900:
                        arffIt(tweet, polarity, trainFile8800)
                    if 9900 <= count <= 10450:
                        arffIt(tweet, polarity, testFile9900)
                    elif count <= 9900 or count >= 10450:
                        arffIt(tweet, polarity, trainFile9900)
                    if 10450 <= count <= 11000:
                        arffIt(tweet, polarity, testFile11000)
                    elif count <= 10450:
                        arffIt(tweet, polarity, trainFile11000)
                polarity = 4
                tweet = ""
                posNum+=1
                count+=1
            elif line == '<A="0">\n' and negNum < int(sys.argv[3]) and count >= int(sys.argv[4]):
                if tweet:
                    if 0 < count <= 550:
                        arffIt(tweet, polarity, testFile1100)
                    elif count >= 550:
                        arffIt(tweet, polarity, trainFile1100)
                    if 550 <= count <= 1100:
                        arffIt(tweet, polarity, testFile2200)
                    elif count <= 550 or count >= 1100:
                        arffIt(tweet, polarity, trainFile2200)
                    if 1100 <= count <= 1650:
                        arffIt(tweet, polarity, testFile3300)
                    elif count <= 1100 or count >= 1650:
                        arffIt(tweet, polarity, trainFile3300)
                    if 1650 <= count <= 2200:
                        arffIt(tweet, polarity, testFile4400)
                    elif count <= 1650 or count >= 2200:
                        arffIt(tweet, polarity, trainFile4400)
                    if 2200 <= count <= 2750:
                        arffIt(tweet, polarity, testFile5500)
                    elif count <= 2200 or count >= 2750:
                        arffIt(tweet, polarity, trainFile5500)
                    if 2750 <= count <= 3300:
                        arffIt(tweet, polarity, testFile6600)
                    elif count <= 2750 or count >= 3300:
                        arffIt(tweet, polarity, trainFile6600)
                    if 3300 <= count <= 3850:
                        arffIt(tweet, polarity, testFile7700)
                    elif count <= 3300 or count >= 3850:
                        arffIt(tweet, polarity, trainFile7700)
                    if 3850 <= count <= 4400:
                        arffIt(tweet, polarity, testFile8800)
                    elif count <= 3850 or count >= 4400:
                        arffIt(tweet, polarity, trainFile8800)
                    if 4400 <= count <= 4950:
                        arffIt(tweet, polarity, testFile9900)
                    elif count <= 4400 or count >= 4950:
                        arffIt(tweet, polarity, trainFile9900)
                    if 4950 <= count <= 5500:
                        arffIt(tweet, polarity, testFile11000)
                    elif count <= 4950:
                        arffIt(tweet, polarity, trainFile11000)
                polarity = 0
                tweet = ""
                negNum+=1
                count+=1
            else:
                tweet+= line

