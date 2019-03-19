import pandas as pd
import numpy as np
import gensim.downloader as api
from gensim.corpora import Dictionary

dataset = api.load("text8")

dir = './Documents/'

for i,doc in enumerate(dataset):
    if(i%12 == 0 and i!= 0):
        break
    myString = ''
    print(i)
    for word in doc:
        myString = myString + ' ' + word
    myString = myString.strip()
    with open(dir+str(i+1)+'.txt','w') as myFile:
        myFile.write(myString)

# dct = Dictionary(dataset)
# index = []
# for (i,j) in dct.items():
#     index.append(j)
