import nltk
import torch
nltk.download('punkt')

from models import InferSent
V = 2
MODEL_PATH = 'encoder/infersent%s.pickle' % V
params_model = {'bsize': 64, 'word_emb_dim': 300, 'enc_lstm_dim': 2048,
                'pool_type': 'max', 'dpout_model': 0.0, 'version': V}
infersent = InferSent(params_model)
infersent.load_state_dict(torch.load(MODEL_PATH))

W2V_PATH = 'dataset/fastText/crawl-300d-2M-subword.vec'
infersent.set_w2v_path(W2V_PATH)

sentences = [
    'a man is walking a dog',
    'a dog and a man were walking down the street',
    'chloroform causes you to faint'
]

# sentences2 = [x.encode('utf-8') for x in sentences]
infersent.build_vocab(sentences, tokenize=True)

embeddings = infersent.encode(sentences, tokenize=True)

infersent.visualize('A man plays an instrument.', tokenize=True)