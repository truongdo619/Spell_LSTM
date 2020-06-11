import numpy as np
import keras

class DataGenerator(keras.utils.Sequence):
    'Generates data for Keras'
    def __init__(self, list_batchs, labels, batch_size, n_classes, shuffle=True):
        'Initialization'
        self.batch_size = batch_size
        self.labels = labels
        self.list_batchs = list_batchs
        self.n_classes = n_classes
        self.shuffle = shuffle
        self.on_epoch_end()

    def __len__(self):
        'Denotes the number of batches per epoch'
        return len(self.list_batchs)

    def __getitem__(self, index):
        'Generate one batch of data'
        # Generate data
        X, Y = self.__data_generation(index)
        return X, Y

    def on_epoch_end(self):
        'Updates indexes after each epoch'
        if self.shuffle == True:
            np.random.shuffle(list(range(len(self.list_batchs))))

    def __data_generation(self, index):
        # Initialization
        X = np.load('data/batch' + str(index) + '.npy')
        Y = self.labels[index]

        return X, keras.utils.to_categorical(Y, num_classes=self.n_classes)



# params = {'dim': (32,32,32),
#           'batch_size': 64,
#           'n_classes': 6,
#           'shuffle': True}
#
# # Datasets
# partition = # IDs
# labels = # Labels
#
# # Generators
# training_generator = DataGenerator(partition['train'], labels, **params)
# validation_generator = DataGenerator(partition['validation'], labels, **params)
#
# # Design model
# model = Sequential()
# [...] # Architecture
# model.compile()
#
# # Train model on dataset
# model.fit_generator(generator=training_generator,
#                     validation_data=validation_generator,
#                     use_multiprocessing=True,
#                     workers=6)