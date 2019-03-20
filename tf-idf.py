import pandas as pd
import numpy as np
import gensim.downloader as api
from gensim.models import TfidfModel
from gensim.corpora import Dictionary
import csv
import os
import multiprocessing as mp
import time
import sys


maxProcesses = 12
activeProcesses = 0
model = []


def fillDocs(doc,docName,maxDocLength):
    # docName = 'doc' + ,str(i+1)
    global model
    sys.stdout.write("\033[F")
    print('Doing '+ docName)
    rowArray = [0]*maxDocLength
    # print(model[doc])
    for word in model[doc]:
        rowArray[word[0]] = word[1]
    # print('finished '+docName)
    return rowArray


def getMatrix(corpus,model,maxDocLength,indexCol):
    dataDict = {}
    i = 0
    for doc in corpus:
        # print(model[doc])
        print()
        docName = 'doc' + str(i+1)
        dataDict[docName] = fillDocs(doc,docName,maxDocLength)
        i += 1

    # for key,item in dataDict.items():
    #     item1 = np.array(item)
    #     item2 = np.append(item1,np.zeros(maxDocLength - item1.size))
    #     dataDict[key] = item2
    #     assert(dataDict[key].size == maxDocLength)

    df = pd.DataFrame(dataDict,index=indexCol)
    print('Saving martix')
    df.to_csv('wordMatrix.csv')
    print('Saving done')

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
        sys.stdout.write("\033[F")
        print('Doc read '+ documentName)
        fileName = str(filePath + '/' + documentName)
        with open(fileName,'r') as doc:
            for line in doc.readlines():
                wordArray = wordArray + formatLine(line)
        datasetDict[fileId] = wordArray
    print()
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
    model = TfidfModel(corpus, smartirs='ntn') 

    maxDocLength = len(dct)
    print('Number of unique words', maxDocLength)
    print('Preparing Matrix')
    getMatrix(corpus,model,maxDocLength,index)


if __name__ == "__main__":
    main()