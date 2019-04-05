import nltk
import torch
import math
import numpy as np
import pandas as pd
from os import fsync
# import 
# nltk.download('punkt')

def euclidianDistance(emb1,emb2):
    sumTemp = 0
    for i in range(0, len(emb1)):
        sumTemp = (emb1[i] - emb2[i]) ** 2
    return math.sqrt(sumTemp)

def cosineSimilarity(emb1,emb2):
    from scipy import spatial
    return 1 - spatial.distance.cosine(emb1, emb2)

def infersentModel(V):
    from models import InferSent
    
    MODEL_PATH = 'encoder/infersent%s.pickle' % V
    params_model = {'bsize': 64, 'word_emb_dim': 300, 'enc_lstm_dim': 2048,
                    'pool_type': 'max', 'dpout_model': 0.0, 'version': V}
    infersent = InferSent(params_model)
    infersent.load_state_dict(torch.load(MODEL_PATH))
    if(V == 1):
        W2V_PATH = './dataset/GloVe/glove.840B.300d.txt'
    elif(V == 2):
        W2V_PATH = './dataset/GloVe/glove.840B.300d.txt'
    else:
        raise ValueError('Invalid V')
    infersent.set_w2v_path(W2V_PATH)
    return infersent


def main():
    filename = './SNLI Data/Google/snliTrainGoogle.csv'
    df = readData(filename)
    print('Calculating unique setences')
    sentences = uniqueSentence(df)
    print('unique sentences ready')
    infersent = infersentModel(1)
    print('Building vocab for model')
    infersent.build_vocab(sentences, tokenize=True)
    print('Encoding sentences')
    embeddings = infersent.encode(sentences, tokenize=True)
    print('Embedding done')
    embbedDict = dict()
    for index,sentence in enumerate(sentences):
        embbedDict[sentence] = embeddings[index]

    updateFile(df,embbedDict)


def uniqueSentence(df):
    sentences = set()
    for index,row in df.iterrows():
        sentences.add(str(row['sentence1']))
        sentences.add(str(row['sentence2']))
    return sentences

def updateFile(df,embbedDict):
    with open('./SNLI Data/Facebook/snliTrainFacebook.csv','w') as outfile:
        for index,row in df.iterrows():
            print(index)
            sent1 = row['sentence1']
            sent2 = row['sentence2']
            emb1 = embbedDict[sent1]
            emb2 = embbedDict[sent2]
            similarity = cosineSimilarity(emb1,emb2)
            finalString = ""+str(row['gold_label'])+","+str(row['sentence1'])+","+str(row['sentence2'])+","+str(row['google'])+","+str(similarity)+'\n'
            outfile.write(finalString)
            outfile.flush()
            fsync(outfile.fileno()) 


def readData(filename):
    df = pd.read_csv(filename,)
    df = df.replace(np.nan," ", regex=True)
    return df[91480:]

if __name__ == "__main__":
    main()
