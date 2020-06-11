import gzip
import time
from helper.train_helper import get_vocab
import json

vocab, word_indices, indices_word = get_vocab()
def read_by_line(filepath):
    lines=[]
    with gzip.open(filepath, 'rt', encoding="utf8") as fp:
        line = fp.readline()
        lines.append(line.split())
        while line:
            line = fp.readline()
            lines.append(line.split())
    lines=lines[:-1]
    return lines

def load_inputs(path, MAX_LEN):
    global word_indices
    lines = read_by_line(path)
    sentences=[]
    for line in lines:
        for i in range(1, len(line)):
            if (i >= MAX_LEN):
                sentences.append(line[i - MAX_LEN:i])
            else:
                sentences.append(line[:i])

    encoded_docs = []
    num = 0
    for sen in sentences:
        num += 1
        encoded_sen = []
        for word in sen:
            encoded_sen.append(word_indices[word])
        encoded_docs.append(encoded_sen)
    return encoded_docs

def load_next_words(path):
    global word_indices
    lines = read_by_line(path)
    next_words = []
    for line in lines:
        for i in range(1, len(line)):
            next_words.append(word_indices[line[i]])

    return next_words

# sentences, next_words = load("/run/media/kodiak/New Volume/Spell_Check_folder/data_train/data_8.gz")
