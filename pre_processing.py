import os
import sys

sys.path.insert(0, './')
import gzip
from nltk.tokenize import sent_tokenize
import json
import re

error = 0
num = 0
f = None
vocab = set()

def clean_text(text):
    global error
    '''Remove unwanted characters and extra spaces from the text'''

    error = 0
    text = re.sub(r'\.', '', text)
    text = re.sub(r'\?', ' ', text)
    text = re.sub(r'&', ' ', text)
    text = re.sub(r'-', ' ', text)
    text = re.sub(r',', '', text)
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'\\', ' ', text)
    text = re.sub(r'/', ' ', text)
    text = re.sub(r'"', '', text)
    text = re.sub(r"'", '', text)
    text = re.sub(r"‘", '', text)
    text = re.sub(r"’", '', text)
    text = re.sub(r":", ' ', text)
    text = re.sub(r'“', '', text)
    text = re.sub(r'–', ' ', text)
    text = re.sub(r'”', '', text)
    text = re.sub(r'…', ' ', text)
    text = re.sub(r'÷', ' ', text)
    text = re.sub('\u200b', ' ', text)
    text = re.sub(r'!', ' ', text)
    text = re.sub(r'[{}@_*>()\\#%+=\[\]]', '', text)
    text = re.sub('a0', '', text)
    text = re.sub('\'92t', '\'t', text)
    text = re.sub('\'92s', '\'s', text)
    text = re.sub('\'92m', '\'m', text)
    text = re.sub('\'92ll', '\'ll', text)
    text = re.sub('\'91', '', text)
    text = re.sub('\'92', '', text)
    text = re.sub('\'93', '', text)
    text = re.sub('\'94', '', text)
    text = re.sub('\.', '. ', text)
    text = re.sub('\!', '! ', text)
    text = re.sub('\?', '? ', text)
    text = re.sub(' +', ' ', text)
    return text


def get_content_by_gz(file_path):
    with gzip.open(file_path, 'rt') as f:
        file_content = f.read()
    return file_content


def load_jsonl_from_gz(file_gz_path, min_length_per_line=5):
    output_objs = []
    for text in get_content_by_gz(file_gz_path).split('\n'):
        try:
            if len(text) >= min_length_per_line:
                obj = json.loads(text)
                output_objs.append(obj)
        except Exception as e:
            print(e)
    return output_objs


def get_gz_path():
    base_path = "/run/media/kodiak/New Volume/baomoi/content"
    files = []
    for r, d, f in os.walk(base_path):
        for file in f:
            if '.gz' in file:
                files.append(os.path.join(r, file))
    return files


def get_sentences_from_json(url):
    global vocab
    try:
        global num, error
        jsons = load_jsonl_from_gz(url)
        for item in jsons:
            tmp = [sens for sens in sent_tokenize(item['heading'])]
            for s in tmp:
                if (len(s.split()) > 50 and '\x11��c' not in s):
                    line = clean_text(s)
                    f.write(line + "\n")
                    vocab.update(line.lower().split())
                    num += 1
    except:
        pass
        error += 1


def main():
    global f, vocab
    files = get_gz_path()
    print(len(files))
    for i in range(len(files)):
        print(i)
        if (i % 10 == 0):
            f = open("data_train/data_part_" + str(int(i / 10 + 1)), "w")
        get_sentences_from_json(files[i])
    outF = open("data_train/vocab", "w")
    for word in vocab:
        outF.write(word)
        outF.write("\n")
    outF.write("<PAD>")
    outF.close()
    # multithread_helper(files, get_sentences_from_json)
    print("Number of lines: " + str(num))
    print("Number of dfsadfasdf: " + str(error))

if __name__ == '__main__':
    main()
