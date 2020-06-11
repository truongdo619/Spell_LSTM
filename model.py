from keras.models import Sequential
from keras.layers import LSTM, Dense, Activation, Embedding, Dropout
from keras.optimizers import RMSprop, Adam
from keras.callbacks import ReduceLROnPlateau, EarlyStopping

def Spell_LSTM(MAX_LEN, len_vocab, learning_rate = 0.1):
    model = Sequential()
    model.add(Embedding(len_vocab, 32, input_length=MAX_LEN))
    model.add(LSTM(256))
    # Add new_dropout_layer
    model.add(Dropout(0.2))
    model.add(Dense(len_vocab))
    model.add(Activation('softmax'))

    # optimizer=RMSprop(lr=learning_rate)

    optimizer = Adam(learning_rate=learning_rate)
    reduce_lr = ReduceLROnPlateau(monitor='loss', factor=0.5,
                                  patience=2, min_lr=0.00001, verbose=1)
    overfit_callback = EarlyStopping(monitor='loss', min_delta=0, patience=10)
    model.compile(loss="categorical_crossentropy", optimizer=optimizer, metrics=['accuracy'])
    return model, reduce_lr, overfit_callback