import numpy as np
from load_data import load
from model import Spell_LSTM


sentences, next_words, word_indices, indices_word, vocab, MAX_LEN = load()

print(len(sentences))
X=np.zeros((len(sentences), MAX_LEN, len(vocab)), dtype=np.bool)
Y=np.zeros((len(sentences), len(vocab)), dtype=np.bool)

# print(sentences)
for i, sen in enumerate(sentences):
    print(i)
    for k, word in enumerate(sen):
        X[i, k, word_indices[word]] = 1
    Y[i, word_indices[next_words[i]]] = 1

model = Spell_LSTM(MAX_LEN, len(vocab))

model.fit(X, Y, epochs=5, batch_size=128)
