import numpy as np
from load_data import load
from model import Spell_LSTM
from keras.preprocessing.sequence import pad_sequences

if __name__== "__main__":

    print(1)
    sentences, next_words, word_indices, indices_word, vocab, MAX_LEN = load()

    print(len(sentences))
    print(2)
    # X = np.zeros((len(sentences), MAX_LEN, len(vocab)), dtype=np.bool)
    Y = np.zeros((len(sentences), len(vocab)), dtype=np.bool)

    print(3)
    encoded_docs = []
    for sen in sentences:
        encoded_sen = []
        for word in sen:
            encoded_sen.append(word_indices[word])
        encoded_docs.append(encoded_sen)

    X = pad_sequences(encoded_docs, maxlen=MAX_LEN, padding='pre')

    print(4)
    for i, sen in enumerate(sentences):
        # print(i)
        # for k, word in enumerate(sen):
        #     X[i, k, word_indices[word]] = 1
        Y[i, word_indices[next_words[i]]] = 1


    print(5)
    # model = Spell_LSTM(MAX_LEN, len(vocab))
    #
    # print(model.summary())
    #
    # history = model.fit(X, Y, epochs=100, batch_size=128)


    # pyplot.plot(history.history['loss'])
    # pyplot.plot(history.history['val_loss'])
    # pyplot.title('model train vs validation loss')
    # pyplot.ylabel('loss')
    # pyplot.xlabel('epoch')
    # pyplot.legend(['train', 'validation'], loc='upper right')
    # pyplot.show()
    # model.save("model_%d.h5" % MAX_LEN)
    # print("Saved model to disk")