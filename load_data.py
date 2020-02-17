
import time

MAX_LEN=10

def read_by_line(filepath):
    vocab = set()
    lines=[]
    with open(filepath) as fp:
        line = fp.readline()
        lines.append(line.lower().split())
        vocab.update(line.lower().split())
        while line:
            line = fp.readline()
            lines.append(line.lower().split())
            vocab.update(line.lower().split())
    lines=lines[:-1]
    return lines, vocab

def load(path):
    lines, vocab=read_by_line(path)
    vocab=sorted(sorted(list(vocab)))
    vocab.append("")
    word_indices=dict((c,i+1) for i, c in enumerate(vocab))
    indices_word=dict((i+1,c) for i, c in enumerate(vocab))
    sentences=[]
    next_words=[]
    for line in lines:
        for i in range(1, len(line)):
            if (i >= MAX_LEN):
                sentences.append(line[i - MAX_LEN:i])
            else:
                sentences.append(line[:i])
            next_words.append(line[i])
    return sentences, next_words, word_indices, indices_word, vocab, MAX_LEN


# sentences, next_words, word_indices, indices_word, vocab, MAX_LEN = load()
