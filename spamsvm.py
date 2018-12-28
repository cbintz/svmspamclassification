# spamsvm.py
import subprocess
import string


"""Spam detection via SVM"""

# CS 451 HW 4

# Group #: 1
# Names: Corinne Bintz, Mira Chugh

# global variables
datadir = 'data/'
trainlabels = datadir + 'training-labels.txt'

# svm train file 
svmtrainfile = datadir + 'my-train.svm'

# svm cv file 
svmcvfile = datadir + 'my-cv.svm'

# makes svm file from fake test labels
faketestlabels = 'fake-test-labels.txt'
fakesvmtestfile = 'fake-test.svm'

def main():
    """main program"""
    data = readlabelfile(trainlabels)
    testData = readlabelfile(faketestlabels)
    
    #split dataset 80% train, 20% cross-validation
    traindata = data[0:6400]
    cvdata = data[6400:]

    #make list of ham words from dictionary of word: frequency
    hamWordList = makeHamWordList(data)
    
    # words to make feature vector
    words = hamWordList[0:3000]
    print(words[0:10])
    
    makesvmfile(traindata, words, svmtrainfile)
    makesvmfile(cvdata, words, svmcvfile)
    makesvmfile(testData, words, fakesvmtestfile)
   
    # now train the model and classify
    train(.75)


def readlabelfile(labelfile):
    """reads label file and returns list of tuples (label, fname)"""
    data = []
    with open(labelfile) as fp:
        for line in fp:
            label, fname = line.split()
            data.append((int(label), fname))

    return data
    
def makesvmfile(data, words, svmfile):
    """extracts feature vector from each email and stores in svm format"""
    with open(svmfile, "w") as fp:
        for label, fname in data:

            # add label to line
            line = ""
            if label == 0:
                line = "-1 "
            else:
                line = "1 "

            # read the contents of each email:
            content = open(datadir + fname).read().split()
           
            # make feature vector based on given words 
            features = set()
            for word in content:
                if word in words:
                    feature_num = words.index(word) + 1
                    features.add(feature_num)

            features = (list(features))

            features.sort()
            for feature in features:
                line += str(feature) + ":1 " 
           
            fp.write(line + '\n');
    print("wrote", svmfile)

def makeWordList(data):
    """ makes sorted word list by frequency from word dictionary for all emails """
    dict = {}
   
    for label, fname in data:

    # read the contents of each email:
        content = open(datadir + fname).read().split()

        for word in content:
            if word not in string.punctuation: # exclude all punctuation
                if word in dict:
                    dict[word] += 1
                else:
                    dict[word] = 1

    sortedDict = sorted(dict, key=dict.get, reverse=True)
    return sortedDict

def makeSpamWordList(data):
    """ makes word dictionary and returns sorted word list by frequency for spam emails """
    spam_dict = {}
    for label, fname in data:

    # read the contents of each email:
        content = open(datadir + fname).read().split()

        for word in content:
            if word not in string.punctuation: 
                if label == 1: 
                    if word in spam_dict:
                        spam_dict[word] += 1 # if word is already in spam dict, increase it's frequency
                    else:
                        spam_dict[word] = 1 # if not, add it to the dict

    sortedList = sorted(spam_dict, key=spam_dict.get, reverse=True)
    return sortedList

def makeHamWordList(data):
     """ makes word dictionary and returns sorted word list by frequency for ham emails """
     ham_dict = {}
    # just some code to get you started:
     for label, fname in data:

    # read the contents of each email:
        content = open(datadir + fname).read().split()

        for word in content:
            if word not in string.punctuation: 
                if label ==0: 
                    if word in ham_dict:
                        ham_dict[word] += 1 # if word is already in ham dict, increase it's frequency
                    else:
                        ham_dict[word] = 1 # if not, add it to the dict

     sortedList = sorted(ham_dict, key=ham_dict.get, reverse=True)
     return sortedList
    
def makeUniqueWordList(spamList, hamList, type):
    """ makes unique word dictionary based on given type (ham or spam), 
     and returns sorted word list by frequency for type of email """
    uniqueDict = {}
    if type == 'spam':
        # make unique word list for spam emails
        for word in spamList:
            if word not in hamList:
                if word in uniqueDict.keys():
                    uniqueDict[word] += 1
                else:
                    uniqueDict[word] = 1
    else: 
        # make unique word list for ham emails
        for word in hamList:
            if word not in spamList:
                if word in uniqueDict.keys():
                    uniqueDict[word] += 1
                else:
                    uniqueDict[word] = 1
    sortedList = sorted(uniqueDict, key=uniqueDict.get, reverse=True)
    return sortedList


def train(c): 
    """ use subprocess.run to learn based on the training set, and then classify
    the training set and cross-validation set"""
    subprocess.run(["svm/svm_learn", "-c", str(c), "data/my-train.svm", "model.svm"])  # train the model
    subprocess.run(["svm/svm_classify", "data/my-train.svm", "model.svm"]) # accuracy on training set
    subprocess.run(["svm/svm_classify", "data/my-cv.svm", "model.svm"]) #accuracy on cv set
    subprocess.run(["svm/svm_classify", "fake-test.svm", "model.svm", "predictions.txt"]) 

if __name__ == "__main__":
    main()
