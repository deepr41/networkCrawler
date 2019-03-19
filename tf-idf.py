import pandas as pd
import numpy as np
import gensim.downloader as api
from gensim.models import TfidfModel
from gensim.corpora import Dictionary
import csv
import os
import multiprocessing as mp
import time


maxProcesses = 12
activeProcesses = 0
model = []


def fillDocs(doc,docName):
    # docName = 'doc' + str(i+1)
    global model
    print('Doing '+ docName)

    index = 0
    counter = 1
    rowArray = []
    while True:
        try:
            word = model[doc][index]
            if(word[0]==counter):
                rowArray.append(word[1])
                counter = counter + 1
                index += 1
            else:
                rowArray.append(np.float64(0))
                counter = counter + 1
        except:
            break
    # dataDict[docName] = rowArray
    print('finished '+docName)
    return rowArray


def getMatrix(corpus,model,maxDocLength,indexCol):
    dataDict = {}
    i = 0
    for doc in corpus:
        docName = 'doc' + str(i+1)
        dataDict[docName] = fillDocs(doc,docName)
        i += 1

    # processes = [mp.Process(target=fillDocs, args=(doc,i,dataDict)) for i,doc in enumerate(corpus)]

    # x = 0
    # while( True):
    #     global activeProcesses
    #     global maxProcesses
    #     print(activeProcesses,maxProcesses)
    #     if not(x<len(processes)):
    #         break
    #     # if(activeProcesses >= maxProcesses):
    #     #     time.sleep(5)
    #     # else:
    #         # activeProcesses += 1
    #     processes[x].start()
    #     x += 1

    # for p in processes:
    #     p.start()

    # for p in processes:
    #     p.join()


    for key,item in dataDict.items():
        item1 = np.array(item)
        item2 = np.append(item1,np.zeros(maxDocLength - item1.size))
        dataDict[key] = item2
        assert(dataDict[key].size == maxDocLength)

    df = pd.DataFrame(dataDict,index=indexCol)
    df.to_csv('wordMatrix.csv')

def formatLine(line):
    #should return array of words
    return line.split()


def main():
    # dataset = api.load("text8")
    datasetDict= {}
    dataset = []
    filePath = os.getcwd() +'/Documents'
    for documentName in os.listdir(filePath):
        wordArray = []
        fileId = documentName.split('.')[0]
        print('Doc read '+ documentName)
        fileName = str(filePath + '/' + documentName)
        with open(fileName,'r') as doc:
            for line in doc.readlines():
                wordArray = wordArray + formatLine(line)
        datasetDict[fileId] = wordArray

    for key in sorted(datasetDict):
        dataset.append(datasetDict[key])
    print('Preparing dictionary')
    dct = Dictionary(dataset)

    index = []
    for x in dct.items():
        index.append(x[1])
    # print(index)
    # print(len(index))
    print('Formating the docs to numbers')
    corpus = [dct.doc2bow(line) for line in dataset] 
    print('Calculating TFidf')
    global model
    model = TfidfModel(corpus)  
    maxDocLength = len(dct)
    print('Preparing Matrix')
    getMatrix(corpus,model,maxDocLength,index)


if __name__ == "__main__":
    main()