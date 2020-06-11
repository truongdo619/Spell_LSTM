import sys
sys.path.insert(0, './')
from load_data import word_indices, indices_word
from keras.preprocessing.sequence import pad_sequences
import numpy as np
import string
from keras.models import load_model

MAX_LEN = 10

_letters = ['a', 'ă', 'â', 'b', 'c', 'd', 'đ', 'e', 'ê', 'g', 'h', 'i', 'k', 'l', 'm', 'n', 'o', 'ô', 'ơ', 'p', 'q',
            'r', 's', 't', 'j', 'w', 'f', 'u', 'ư', 'v', 'x', 'y', 'á', 'à', 'ả', 'ã', 'ạ', 'ấ', 'ầ', 'ẩ', 'ẫ', 'ậ',
            'ắ', 'ằ', 'ẳ', 'ẵ', 'ặ', 'é', 'è', 'ẻ', 'ẽ', 'ẹ', 'ế', 'ề', 'ể', 'ễ', 'ệ', 'í', 'ì', 'ỉ', 'ĩ', 'ị', 'ó',
            'ò', 'ỏ', 'õ', 'ọ', 'ố', 'ồ', 'ổ', 'ỗ', 'ộ', 'ớ', 'ờ', 'ở', 'ỡ', 'ợ', 'ú', 'ù', 'ủ', 'ũ', 'ụ', 'ứ', 'ừ',
            'ử', 'ữ', 'ự', 'ý', 'ỳ', 'ỷ', 'ỹ', 'ỵ']

model = load_model('best_model.hdf5')

model.summary()


def correct(sentence):
    words=sentence.split()
    for i in range(11, len(words)):
        if (i < MAX_LEN):
            sen = words[:i]
        else:
            sen = words[i-MAX_LEN:i]
        word_need_check= words[i]

        print(word_need_check)
        encoded_sen = []

        for word in sen:
            encoded_sen.append(word_indices[word])
        X = np.asarray(encoded_sen).reshape(1,10)
        preds = model.predict(X, verbose=0)[0]
        m = max(preds)
        index = [i for i, j in enumerate(preds) if j == m]
        print(indices_word[index[0]])
        # words[i] = indices_word[index[0]]
        print("-------------------------")


def edit_distance_1(word):
    word = ENSURE_UNICODE(word).lower()
    if _check_if_should_check(word) is False:
        return {word}
    letters = _letters
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
    inserts = [L + c + R for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edit_distance_2(self, word):
    word = ENSURE_UNICODE(word).lower()
    return [
        e2 for e1 in edit_distance_1(word) for e2 in edit_distance_1(e1)
    ]

def _check_if_should_check(word):
    if len(word) == 1 and word in string.punctuation:
        return False
    try:
        float(word)
        return False
    except ValueError:
        pass
    return True


def ENSURE_UNICODE(s, encoding='utf-8'):
    if isinstance(s, bytes):
        return s.decode(encoding)
    return s

correct("giáo dục gia đình có những đặc trưng riêng nên nhà trường phải liên kết với gia đình để đảm bảo tính thống nhất toàn vẹn của".lower())