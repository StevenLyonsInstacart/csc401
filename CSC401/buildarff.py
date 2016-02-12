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

def unTag(tweet):
    words = tweet.split(" ")
    untagged = ""
    for word in words:
        tag = word.split("/")
        untagged+= tag[0].lower()+" "
    return untagged
firstPerson = [" i ", " me ", " my ", " mine ", " we ", " us ", " our ", " ours "]
secondPerson = [" you ", " your ", " yours ", " u ", " ur ", " urs "]
thirdPerson = [" he ", " him ", " his ", " she ", " her ", " hers ", " it ", " its ", " they ", " them ", " their ",
               " theirs "]


def arffIt (tweet, polarity, twt):

    unTagged  = unTag(tweet)
    print(unTagged)
    #Persons
    twt.write(str(findWords(unTagged, firstPerson))+", ")
    twt.write(str(findWords(unTagged, secondPerson))+", ")
    twt.write(str(findWords(unTagged, thirdPerson))+", ")

    #Symbols
    twt.write(str(findWords(unTagged, [" , "]))+", ")
    twt.write(str(findWords(unTagged, [" : ", " ; "]))+", ")
    twt.write(str(findWords(unTagged, [" - "]))+", ")
    twt.write(str(findWords(unTagged, ["(", ")"]))+", ")
    twt.write(str(findWords(unTagged, [" ... "]))+", ")
    twt.write(str(findWords(unTagged, [" - "]))+", ")

    #PoS
    twt.write(str(partsOfSpeech(tweet, ["/VBD "]))+", ")
    twt.write(str(partsOfSpeech(tweet, ["/NN ", "/NNS "]))+", ")
    twt.write(str(partsOfSpeech(tweet, ["/NNP ", "/NNPS "]))+", ")
    twt.write(str(partsOfSpeech(tweet, ["/RB ", "/RBR ", "/RBS "]))+", ")
    twt.write(str(partsOfSpeech(tweet, ["/WDT ", "/WP ", "/WP$ ", "/WRB "]))+", ")

    #Still missing Future tense, Slang, maybe more

    #Polarity
    twt.write(str(polarity)+"\n")
    return 1

outFile = open(sys.argv[2], 'w')
with  open(sys.argv[1], "r") as twt:
    tweet = ""
    polarity = 0
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

