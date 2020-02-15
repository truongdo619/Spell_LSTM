from keras.models import Sequential
from keras.layers import LSTM, Dense, Activation, Embedding
from keras.optimizers import RMSprop

def Spell_LSTM(MAX_LEN, len_vocab):
    model = Sequential()
    model.add(Embedding(len_vocab, 8, input_length=MAX_LEN))
    model.add(LSTM(128))
    model.add(Dense(len_vocab))
    model.add(Activation('softmax'))
    optimizer=RMSprop(lr=0.002)
    model.compile(loss="categorical_crossentropy", optimizer=optimizer, metrics=['accuracy'])
    return model
