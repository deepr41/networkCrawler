import nltk
import torch
import math
import numpy as np
import pandas as pd
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

sentences = [
    "This church choir sings to the masses as they sing joyous songs from the book at a church.",
    "A choir singing at a baseball game.",
]

def main():
    infersent = infersentModel(1)
    infersent.build_vocab(sentences, tokenize=True)
    embeddings = infersent.encode(sentences, tokenize=True)

    similaritites = np.inner(embeddings,embeddings)
    print(similaritites)

    print(euclidianDistance(embeddings[0],embeddings[1]))
    print(cosineSimilarity(embeddings[0],embeddings[1]))
    print(np.inner(embeddings[0],embeddings[1]))

def readData(filename):
    df = pd.read_csv(filename, sep='\t',)
    print(df.head())

if __name__ == "__main__":
    main()
    # import sys
    # readData(sys.argv[1])
