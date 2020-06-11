# -*- coding: utf8 -*-
import gzip, csv
import os
import json
import pathlib
from collections import Counter
import subprocess
from glob import glob
import sys
sys.path.insert(0, './')

def get_single_word_list():
    list = load_uni_gram()
    try:
        with open('data_train/tu_viettat.txt', encoding="utf-8") as f:
            for line in f:
                list.add(line.split()[0].lower())
            f.close()
        with open('data_train/vi-dontu.dic', encoding="utf-8") as f:
            f.readline()
            for line in f:
                str = line.replace('\n', '').lower()
                if not str in list:
                    list.add(str)
            f.close()
        return list
    except:
        pass

def get_content_by_gz(file_path):
    with gzip.open(file_path, 'rt', encoding="utf-8") as f:
        file_content = f.read()
    return file_content


def get_content(file_path):
    with open(file_path) as f:
        s = f.read()
    return s


def get_files_in_folder(folder_path):
    files_absolute_path = []
    files_name = None
    for root, dirs, files in os.walk(os.path.abspath(folder_path)):
        files_name = files
        for file in files:
            if '.DS_Store' not in file:
                files_absolute_path.append(os.path.join(root, file))
    return files_absolute_path, files_name


def get_files_absolute_in_folder(folder_path):
    files_absolute_path, files_name = get_files_in_folder(folder_path)
    return files_absolute_path


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


def load_timestamp_format_jsonl_from_gz(file_gz_path, data_space_no=1, min_length_per_line=5):
    """
    :param file_gz_path:
    :param data_space_no: thứ tự dấu cách chưa data VD: timestamp datajson
    :param min_length_per_line:
    :return:
    """
    output_objs = []
    for text in get_content_by_gz(file_gz_path).split('\n'):
        try:
            if text is None or text == '':
                return []
            text_data = ' '.join(text.split(' ')[data_space_no:])
            # print(text_data)
            if len(text_data) >= min_length_per_line:
                obj = json.loads(text_data)
                output_objs.append(obj)
        except Exception as e:
            print(e)
    return output_objs


def get_sub_folders_in_folder(folder_path):
    sub_folders = glob(folder_path + "/*/")

    return sub_folders


def create_folder_if_not_exist(folder_path):
    pathlib.Path(folder_path).mkdir(parents=True, exist_ok=True)


def get_sub_folders_and_file_name_in_folder(folder_path):
    sub_folders = glob(folder_path + "/*/")
    files_name = [file_path.split('/')[-2] for file_path in sub_folders]
    return sub_folders, files_name


def load_json(file_path):
    with open(file_path) as f:
        data = json.load(f)
    return data


def store_json(object, file_output_path):
    os.makedirs(os.path.dirname(file_output_path), exist_ok=True)
    with open(file_output_path, 'w') as fp:
        json.dump(object, fp, ensure_ascii=False, sort_keys=True, indent=1)


def store_file(content, file_output_path):
    os.makedirs(os.path.dirname(file_output_path), exist_ok=True)
    with open(file_output_path, 'w+') as fh:
        fh.write(str(content))


def store_gz(content, file_output_path, is_append=False):
    os.makedirs(os.path.dirname(file_output_path), exist_ok=True)
    # print('prepare store gz', file_output_path)
    if is_append:
        with gzip.open(file_output_path, 'ab') as f:
            f.write(content.encode('utf-8'))
    else:
        with gzip.open(file_output_path, 'wb') as f:
            f.write(content.encode('utf-8'))


def store_jsons_perline_in_file(jsons_obj, file_output_path, is_append=False):
    os.makedirs(os.path.dirname(file_output_path), exist_ok=True)
    if is_append:
        with gzip.open(file_output_path, 'ab') as f:
            for idx, json_obj in enumerate(jsons_obj):
                if idx == 0:
                    f.write((json.dumps(json_obj, ensure_ascii=False)).encode('utf-8'))
                else:
                    f.write(('\n' + json.dumps(json_obj, ensure_ascii=False)).encode('utf-8'))
    else:
        with gzip.open(file_output_path, 'wb') as f:
            for idx, json_obj in enumerate(jsons_obj):
                if idx == 0:
                    f.write((json.dumps(json_obj, ensure_ascii=False)).encode('utf-8'))
                    # f.write((json.dumps(json_obj, ensure_ascii=False)))
                else:
                    f.write(('\n' + json.dumps(json_obj, ensure_ascii=False)).encode('utf-8'))


def store_jsons_perline_in_file_non_compress(jsons_obj, file_output_path, is_append=False):
    os.makedirs(os.path.dirname(file_output_path), exist_ok=True)
    if (is_append):
        with open(file_output_path, 'ab') as f:
            for json_obj in jsons_obj:
                f.write((json.dumps(json_obj, ensure_ascii=False) + '\n').encode('utf-8'))
    else:
        with open(file_output_path, 'wb') as f:
            for json_obj in jsons_obj:
                f.write((json.dumps(json_obj, ensure_ascii=False) + '\n').encode('utf-8'))


def get_content_from_csv_callback(file_input_path, process_callback):
    with open(file_input_path, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            process_callback(row)


def get_content_from_csv(file_input_path):
    output = []
    with open(file_input_path, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            output.append(row)
    return output


def list_uid_to_csv(list_uid, file_path):
    with open(file_path, 'w', newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        for data in list_uid:
            wr.writerow([int(data)])
            # wr.writerow([data])


def wccount(file_path):
    out = subprocess.Popen(['wc', '-l', file_path],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT
                           ).communicate()[0]
    return int(out.partition(b' ')[0])


def wcgzcount(file_path):
    count = 0
    try:
        bashCommand = "zcat " + file_path + " | wc -l"
        # print(bashCommand)
        out = os.popen(bashCommand)
        data = out.read()
        count = int(data.split('\n')[0])
        out.close()
    except Exception as e:
        print(e)
    return count


def count_line_all_gz(folder_path):
    # print('count ', folder_uid_path)
    # files_absolute_path, files_name = get_files_in_folder(folder_path)
    count = 0
    bashCommand = "zcat " + folder_path + "/*.gz | wc -l"
    # print(bashCommand)
    try:
        print('prepare: ', bashCommand)
        out = os.popen(bashCommand)
        data = out.read()
        count = int(data.split('\n')[0])
        out.close()
    except Exception as e:
        print(e)
    print('counted', count, ': ', bashCommand)
    return count


def read_config_file():
    with open("./config.json", 'r') as f:
        data = json.load(f)
    return data

def write_url_list_file(data):
    with open("./config/urlList.json", 'w') as f:
        json.dump(data, f)

def load_uni_gram(thres_hold = 200):
    uni_gram = Counter()
    with open("data_train/unigram.txt", mode="r", encoding="utf-8") as fobj:
        uni_gram.update(json.load(fobj))
    return set(key for key, value in uni_gram.items() if value >= thres_hold)

# print(len(get_single_word_list()))