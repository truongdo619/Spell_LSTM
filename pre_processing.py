import os
import sys

sys.path.insert(0, './')
import gzip
from underthesea import sent_tokenize, word_tokenize, pos_tag
import json
from helper.pre_processing_helper import formatSentence, delete_en_docs, convert_to_hp_path
import re
from helper.encoding_helper import convert_tcvn3_to_unicode, is_tcvn3_encoding
from helper.multithread_helper import multithread_helper
from helper.read_helper import write_url_list_file, store_gz
from concurrent.futures import ProcessPoolExecutor
from helper.train_helper import get_vocab

error = 0
num = 0
f = None
vocab = set()
path_index = 0
with open('config/urlList.json') as f:
    data = json.load(f)
files = data["path"]
content = ""
base_vocab, word_indices, indices_word = get_vocab()

def clean_text(text):
    global error
    '''Remove unwanted characters and extra spaces from the text'''

    error = 0
    text = re.sub(r'\.', ' ', text)
    text = re.sub(r'\(', ' ', text)
    text = re.sub(r'\)', ' ', text)
    text = re.sub(r'\?', ' ', text)
    text = re.sub(r'&', '', text)
    text = re.sub(r',', ' ', text)
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'/', ' ', text)
    text = re.sub(r'"', '', text)
    text = re.sub(r"'", '', text)
    text = re.sub(r"‘", '', text)
    text = re.sub(r"’", '', text)
    text = re.sub(r":", ' ', text)
    text = re.sub(r'“', '', text)
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


def occurrence_counter(target_string):
    return len(list(filter(lambda x: x in ["<NUMBER>", "<URL>", "<EMAIL>", "<DATE>", "<UNKNOWN>"], target_string.split(' '))))

def get_sentences_from_file(paths, idx, thres = 10):
    global base_vocab

    content =""
    num = 0
    error = 0
    print("---------------------------------------------- " + str(idx) + " ------------------------------------------------")
    vocab = set()
    for path in paths:
        print(str(idx) + "---------------" + path)
        try:
            with open(path, encoding="utf-8") as fs:
                data = fs.read()
                if (is_tcvn3_encoding(data)):
                    data = convert_tcvn3_to_unicode(data)
                tmp = sent_tokenize(data)

                for index in range(20, len(tmp) - 20):
                    if (len(tmp[index].split()) > 50):
                        tags = pos_tag(tmp[index])
                        sen = " ".join([tag[0] for tag in tags if tag[1] != "CH"])
                        line = formatSentence(sen)[0]
                        line = " ".join([word if word in base_vocab else "<UNKNOWN>" for word in line.split()])
                        print(line)
                        if (occurrence_counter(line) <= thres):
                            content += line + "\n"
                            # vocab.update(line.split())
                            num += 1

        except:
            pass
            error += 1

    store_gz(content, "data_train/data_" + str(idx) + ".gz")
    # # outF = open("data_train/vocab_" + str(idx), "w")
    # # for word in vocab:
    # #     outF.write(word)
    # #     outF.write("\n")
    # # outF.write("<PAD>")
    # # outF.close()
    # print("Number of lines: " + str(num))
    # print("Number of errors: " + str(error))

def main():
    global files
    print(len(files))
    get_sentences_from_file([files[0]], 1)
    # files = convert_to_hp_path(files)

    # delete_en_docs(data, ["nghốo", "riờng", "hiệncỏc", "độngvà", "dến", "cosử", "creativity", "suụng", "qỳa", "xuõn", "nghiepj", "lýchuyên"])
    # chunk_size = 100
    # chunks_end_range = []
    # for i in range(int(len(files) / chunk_size)):
    #     if(i < int(len(files) / chunk_size) - 1):
    #         chunks_end_range.append((i + 1)*chunk_size)
    #     else:
    #         chunks_end_range.append(len(files))
    # print(chunks_end_range)
    #
    # executor = ProcessPoolExecutor(max_workers=20)
    # for i in range(int(len(files) / chunk_size)):
    #     executor.submit(get_sentences_from_file, files[i * chunk_size: chunks_end_range[i]], i)


if __name__ == '__main__':
    main()