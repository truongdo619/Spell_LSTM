from keras.models import Sequential
from keras.layers import LSTM, Dense, Activation
from keras.optimizers import RMSprop

def Spell_LSTM(MAX_LEN, len_vocab):
    model = Sequential()
    model.add(LSTM(128, input_shape=(MAX_LEN, len_vocab)))
    model.add(Dense(len_vocab))
    model.add(Activation('softmax'))
    optimizer=RMSprop(lr=0.1)
    model.compile(loss="categorical_crossentropy", optimizer=optimizer, metrics=['accuracy'])
    return model
