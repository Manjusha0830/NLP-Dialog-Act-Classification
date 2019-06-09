from math import log2
import sys

from string import punctuation

def getInnerData(start, end, text):
    innerText = ""
    if text.find(start) != -1:
        startword = text[text.find(start):text.find(end)]
        innerText = startword[len(start):]
    return innerText

def strip_stopwords(data):
	return ''.join(content for content in data if content not in punctuation)
def dialog(traindata,testdata):
    #traindata = open(r'C:\Users\manju\Desktop\Semester1\NLP\Assignment4\DialogAct.train',encoding="utf8")
    dialogtraindata = traindata.read()
    #print(dialogtraindata)
    traindata.close()
    #testdata = open(r'C:\Users\manju\Desktop\Semester1\NLP\Assignment4\DialogAct.test',encoding="utf8")
    dialogtestdata = testdata.read()
    #print(dialogtraindata)
    testdata.close()
    val1 = 0
    val2 = 0
    #stop_words = set(stopwords.words('english'))
    trainlabelDict = dict()
    dialogs = list(filter(None, dialogtraindata.split('Advisor:')))
    #print(str(len(dialogs)))
    for i in range(1,len(dialogs)):
        label = getInnerData('[',']',dialogs[i])
        lines =  dialogs[i-1].split('\n')
        for line in lines:
            if("Student:" in line):
                sentence = line[len("Student:"):]
                if label not in trainlabelDict:
                    trainlabelDict[label] = list()
                words = sentence.split(" ")
                for word in words :
                    word = word.strip('\n')
                    word = strip_stopwords(word)
                    if word != "":
                        trainlabelDict[label].append(word)

    testLabelDict = dict()
    testSentenceDict = dict()
    testLinesDict = dict()
    
    dialogs = list(filter(None, dialogtestdata.split('Advisor:')))
    
    
    for i in range(1,len(dialogs)):
        
        label = getInnerData('[',']',dialogs[i])
        if('pull-select]' in label):
            label = 'pull-select'

        testLabelDict[i] =label
        lines =  dialogs[i-1].split('\n')
        testLinesDict[i] = lines    
        for line in lines:
            if("Student:" in line):
                sentence = line[len("Student:"):]
                
                if i not in testSentenceDict:
                    testSentenceDict[i]=list()
                words = sentence.split(" ")
                for word in words :
                    word = word.strip('\n')
                    word = strip_stopwords(word)
                    #if word not in punctuation and word not in stop_words and word != "":
                    if word != "":
                        testSentenceDict[i].append(word)
    
    totalTrainWords = 0 
    labelprobdict = dict()
    
    for label in trainlabelDict:
        totalTrainWords += len(trainlabelDict[label])
    for label in trainlabelDict:
        labelprobdict[label] = len(trainlabelDict[label] )/ totalTrainWords
    labelDictUnique = dict()
    labelDictUniquenum = dict()
    for label in trainlabelDict:
        labelDictUnique[label] = list()
        labelDictUniquenum[label] = 0
        for word in trainlabelDict[label]:
            if word not in labelDictUnique[label]:
                labelDictUnique[label].append(word)
                labelDictUniquenum[label] += len(labelDictUnique[label])
                #labelDictUniquenum[label] += 1
    probWordDict = dict()
    
    finaldict = dict()
    
    for label in trainlabelDict.keys():
        #value1prob = 0
        for word in trainlabelDict[label]:
            if  word not in probWordDict:
                probWordDict[word] = dict()
            if  label not in probWordDict[word]:
                probWordDict[word][label] = 0
            value1 = trainlabelDict[label].count(word) + 1 
            value2 = len(trainlabelDict[label]) + labelDictUniquenum[label]
            prob = log2(value1/value2)
            probWordDict[word][label]  += prob 
            #value1prob +=prob
    
    for dialogCount in testSentenceDict.keys():
        probLabels = dict()
        
        for word in testSentenceDict[dialogCount]:
            if word in probWordDict:
                for label in probWordDict[word].keys():
                    if label not in probLabels:
                        probLabels[label] =0
                    probLabels[label] +=probWordDict[word][label] 
            
        maxValue = -sys.float_info.max
        finalsense =''
        for label in probLabels:
            #prob = probLabels[label]  + log2(labelprobdict[label])
            if probLabels[label] > maxValue:
                maxValue = probLabels[label]  * log2(labelprobdict[label])
                finalsense = label
        finaldict[dialogCount] = finalsense

    
    for key in finaldict:
        if key in testLabelDict:
            val2 += 1
            if testLabelDict[key] == finaldict[key]:
                val1 += 1
    accuracy  = (val1/val2) 
    
    print("Accuracy  =",accuracy*100)
    f = open('DialogAct.test.out','w') 
    for key in testLinesDict:
        if key in finaldict:
            for line in testLinesDict[key]:
                if("Student:" in line):
                    f.write(line)
                    f.write('\n')
            f.write("Advisor: [" + finaldict[key]+"]\n")
    f.close()
            

            
    

def main():
       
    input1 = sys.argv[1]
    input2 = sys.argv[2]
    trainfile = open(input1,encoding="utf8")
    testfile = open(input2,encoding="utf8")
    dialog(trainfile,testfile)
    
        
if __name__ == "__main__":
    main()