import numpy as np
from load_data import load
from model import Spell_LSTM
from keras.preprocessing.sequence import pad_sequences
import os

def get_data_path():
    base_path = "/run/media/kodiak/New Volume/Spell_Check_folder/data_train"
    files = []
    for r, d, f in os.walk(base_path):
        for file in f:
            if 'data' in file:
                files.append(os.path.join(r, file))
    return files


if __name__== "__main__":

    main_vocab = set()
    paths = get_data_path()

    for path in paths:
        print(path)
        sentences, next_words, word_indices, indices_word, vocab, MAX_LEN = load(path)
        main_vocab.update(vocab)

    print(len(main_vocab))

    # Y = np.zeros((len(sentences), len(vocab)), dtype=np.bool)
    #
    # encoded_docs = []
    # for sen in sentences:
    #     encoded_sen = []
    #     for word in sen:
    #         encoded_sen.append(word_indices[word])
    #     encoded_docs.append(encoded_sen)
    #
    # X = pad_sequences(encoded_docs, maxlen=MAX_LEN, padding='pre')
    #
    # for i, sen in enumerate(sentences):
    #     Y[i, word_indices[next_words[i]]] = 1
    #
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