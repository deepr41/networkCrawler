import pandas as pd
import gensim.downloader as api
from gensim.models import TfidfModel
from gensim.corpora import Dictionary
import csv
from os import path,mkdir,fsync

# with open("data.csv", "r") as f:
#     reader = csv.reader(f, delimiter=",")
#     for line in enumerate(reader):
#         listWord=[]
#         listWord.append(line[7].split())
# print(listWord)

# dct = Dictionary(listWord)

dataset = api.load("text8")
dct = Dictionary(dataset)

corpus = [dct.doc2bow(line) for line in dataset] 
model = TfidfModel(corpus)  
vector = {}

if(path.exists('./lr.csv')):
        aliasFile = open('lr.csv','a')
else:
    aliasFile = open('lr.csv','a')
    #aliasFile.write("slno,hostname\n")

for i in range(100):
    vector[i]=model[corpus[i]]
    finalFile.write(vector[i])
    
print(vector)

    

