import pandas as pd
import numpy as np
import gensim.downloader as api
from gensim.models import TfidfModel
from gensim.corpora import Dictionary
import csv
from os import path,mkdir,fsync

def zero(column,row): 
    return np.zeros([column,row])

def getMatrix(corpus,model):
    i = 0
    dataDict = {}
    maxDocLength = 0
    for doc in corpus:
        print('Doing doc ' + str(i),end = '   ')
        index = 0
        counter = 1
        rowArray = np.array([])
        while True:
            try:
                word = model[doc][index]
                if(word[0]==counter):
                    rowArray = np.append(rowArray,word[1])
                    counter = counter + 1
                    index += 1
                else:
                    rowArray = np.append(rowArray,np.float64(0))
                    counter = counter + 1
            except:
                break
        docName = 'doc' + str(i)
        i += 1 
        maxDocLength = max(rowArray.size,maxDocLength)
        print(maxDocLength)
        dataDict[docName] = rowArray
        if(i%5 == 0 and i!= 0):
            break
    for key,item in dataDict.items():
        dataDict[key] = np.append(item,np.zeros(maxDocLength - item.size))
        assert(dataDict[key].size == maxDocLength)
    df = pd.DataFrame(dataDict)
    df.to_csv('wordMatrix.csv',index=False)


def main():
    dataset = api.load("text8")
    dct = Dictionary(dataset)

    corpus = [dct.doc2bow(line) for line in dataset] 
    model = TfidfModel(corpus)  

    getMatrix(corpus,model)


if __name__ == "__main__":
    main()