import numpy as np
from load_data import vocab, word_indices, load_next_words, load_inputs
from model import Spell_LSTM
from keras.preprocessing.sequence import pad_sequences
from helper.train_helper import get_vocab, get_data_path
from progress.bar import Bar
import time
from helper.data_genertator import DataGenerator
from datetime import datetime
import json
from numpy import asarray, save
from keras.callbacks import ModelCheckpoint, CSVLogger

from keras import backend as K
import tensorflow as tf
jobs = 2 # it means number of cores
config = tf.ConfigProto(intra_op_parallelism_threads=jobs,
                         inter_op_parallelism_threads=jobs,
                         allow_soft_placement=True,
                         device_count={'CPU': jobs})
session = tf.Session(config=config)
K.set_session(session)

config = {}
with open('./config/config.json') as json_file:
    config = json.load(json_file)

class TrainModel(object):
    def __init__(self):
        self.input_cache = {}
        self.output_cache = {}
        self.batch_size = config["model"]["batch_size"]
        self.max_len = [5, 10, 15, 20]


    def chunks(self, lst, n):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    def write_log(self, content, is_title = False):
        logs = open("logs", "a")
        if is_title:
            logs.write("*************************************************\n")
            n = datetime.now()
            logs.write("%s\n" % n)
            logs.write("*************************************************\n")
        else:
            logs.write("-------------------------------------------------\n")
            logs.write(content + "\n")
        logs.close()

    def save_input_to_file(self, paths, MAX_LEN):
        start_time = time.time()
        batch_id = 0
        bar = Bar('Save input data', max=len(paths))
        for idx, path in enumerate(paths):
            encoded_docs = load_inputs(path)
            encoded_docs_chunks = list(self.chunks(encoded_docs, self.batch_size))
            for id, encoded_docs_chunk in enumerate(encoded_docs_chunks):
                X = pad_sequences(encoded_docs_chunk, maxlen=MAX_LEN, padding='pre', value=word_indices["<PAD>"])
                save('data/batch' + str(batch_id) + '.npy', asarray(X))
                batch_id += 1
            bar.next()
        bar.finish()
        print("--- %s seconds ---" % (time.time() - start_time))

    def load_labels(self, paths):
        result = []
        start_time = time.time()
        bar = Bar('Load output data', max=len(paths))
        print(paths)
        for idx, path in enumerate(paths):
            next_words = load_next_words(path)
            next_word_chunks = list(self.chunks(next_words, self.batch_size))
            result += next_word_chunks
            bar.next()
        bar.finish()
        print("--- %s seconds ---" % (time.time() - start_time))
        return result

    def train(self):
        paths = get_data_path("data")
        paths=paths[0:1]
        print("length of paths: " + str(len(paths)))
        for MAX_LEN in self.max_len:
            model, reduce_lr, overfit_callback = Spell_LSTM(config["model"]["MAX_LEN"], len(vocab))
            self.save_input_to_file(paths, MAX_LEN)
            labels = self.load_labels(paths)
            list_batchs = range(len(labels))
            params = {'batch_size': self.batch_size,
                      'n_classes': len(vocab),
                      'n_channels': 1,
                      'shuffle': True}
            training_generator = DataGenerator(list_batchs, labels, params['batch_size'], params['n_classes'],  params['shuffle'])
            print(model.summary())
            checkpoint = ModelCheckpoint("best_model_len_" + str(MAX_LEN) +".hdf5", monitor='loss', verbose=1,
                                         save_best_only=True, mode='auto', period=1)
            csv_logger = CSVLogger('log.csv', append=True, separator=';')
            model.fit_generator(generator=training_generator,
                                use_multiprocessing=False,
                                workers=6,
                                epochs=150,
                                callbacks=[reduce_lr, checkpoint, csv_logger])

        # model.fit(X, Y, epochs=1000, batch_size=128, callbacks=[reduce_lr, overfitCallback])
        # print("--- %s seconds ---" % (time.time() - start_time))
        # print("------------------------------------------------------------")
        # write_log("File " + path + " - " + "Chunk " + str(count))


if __name__ == "__main__":
    train_model = TrainModel()
    train_model.train()


