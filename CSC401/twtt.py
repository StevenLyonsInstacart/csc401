import csv
count = 0
tweetNum=0
tweets = []

def check_abbrev(word):
    f = open('/u/cs401/Wordlists/abbrev.english', 'r')
    for line in f:
        if word in line:
            return True
        return False
    f.close()

def sanitize(text):
    newText = []
    for word in text:
        if word:
            if word[0] == '@' or word[0] == '#':
                word = word[1:]
            newText.append(word)
    return newText

def own_line(text):
    #run through abbrev.english to ensure these don't cause a new line
    #else, whenever coming across an exclamation point, full stop, or question mark, move sentence onto a new line,
    #but if there's multiple don't split, need to be on the same line
    
    newText = []
    for word in text:
        if len(word) > 2:
            if word[-1] == '!' or word[-1] == '?' or word[-1] == '.':
                if check_abbrev(word) == False:
                    newText.append(word)
                    newText.append("\n")
                else:
                    newText.append(word)
            else:
                newText.append(word)
    return newText 

def punctuation_separator(text):
    #append a space before a clitic or a piece of punctuation
    newText = []
    for word in text:
        if len(word) > 2:
            if word[-1] == '!' or word[-1] == '?' or word[-1] == '.' or word[-2] == "'":
                newText.append(" ")
            newText.append(word)
    return newText     


with open('/u/cs401/A1/tweets/training.1600000.processed.noemoticon.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        if (count>44000 and count<49500):
            tweets.append([row[0], row[5][1:-1]])
            tweetNum+= 1
        if 844000 < count < 849500:
            tweets.append([row[0], row[5][1:-1]])
            tweetNum+= 1

        count = count + 1
    for tweet in tweets:
        tweet[1] = tweet[1].split(" ")
        tweet[1] = sanitize(tweet[1])
        tweet[1] = own_line(tweet[1])
        #tweet[1] = punctuation_separator(tweet[1])
        print(tweet)
    print("done")
