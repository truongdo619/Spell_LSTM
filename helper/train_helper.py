
import sys
sys.path.insert(0, './')
import os
from helper.read_helper import get_single_word_list

def get_vocab():
    # vocab = set()
    # with open("data_train/vocab") as fp:
    #     line = fp.readline()
    #     vocab.update([line.rstrip()])
    #     while line:
    #         line = fp.readline()
    #         vocab.update([line.rstrip()])
    vocab = get_single_word_list()
    vocab.add("<UNKNOWN>")
    vocab.add("<PAD>")
    vocab = sorted(vocab)
    word_indices=dict((c,i) for i, c in enumerate(vocab))
    indices_word=dict((i,c) for i, c in enumerate(vocab))
    return vocab, word_indices, indices_word

def merge_vocab():

    vocab = set()
    paths = get_data_path("vocab")
    for path in paths[:150]:
        print(path)
        with open(path) as fp:
            line = fp.readline()
            vocab.update([line.rstrip()])
            while line:
                line = fp.readline()
                vocab.update([line.rstrip()])
    outF = open("data_train/vocab", "w")
    for word in vocab:
        outF.write(word)
        outF.write("\n")
    print(len(vocab))
    return vocab

def get_data_path(key_word):
    base_path = "D://Spell_Check_folder/data_train_local"
    # base_path = "/run/media/kodiak/New Volume/Spell_Check_folder/data_train"
    files = []
    for r, d, f in os.walk(base_path):
        for file in f:
            if key_word in file:
                files.append(os.path.join(r, file))
    return files


def example():
    print(get_data_path("data"))

# example()