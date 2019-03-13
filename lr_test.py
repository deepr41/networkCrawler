import pandas as pd
import gensim.downloader as api
from gensim.models import TfidfModel
from gensim.corpora import Dictionary
import csv

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

for i in range(1700):
    vector[i]=model[corpus[i]]
    
print(vector)

    

