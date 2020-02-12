
MAX_LEN=20

def read_by_line(filepath):
    vocab = set()
    lines=[]
    with open(filepath) as fp:
        line = fp.readline()
        lines.append(line.lower().split())
        while line:
            line = fp.readline()
            lines.append(line.lower().split())
            vocab.update(line.lower().split())
    lines=lines[:-1]
    return lines, vocab

def load():
    lines, vocab=read_by_line("data")
    vocab=sorted(sorted(list(vocab)))
    word_indices=dict((c,i) for i, c in enumerate(vocab))
    indices_word=dict((i,c) for i, c in enumerate(vocab))
    sentences=[]
    next_words=[]
    for line in lines:
        for i in range(len(line) - MAX_LEN):
            sentences.append(line[i:i+MAX_LEN])
            next_words.append(line[i+MAX_LEN])
    return sentences, next_words, word_indices, indices_word, vocab, MAX_LEN


# load()