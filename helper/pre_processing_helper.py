import re
from helper.read_helper import write_url_list_file
parenthesis_regex = re.compile('\(.+?\)')

def formatSentence(str):
    str = str.lower()
    #str = parenthesis_regex.sub('', str)
    tmp = match_special_syl(str)
    str = tmp[0]
    return (re.sub(
        r'[^a-zAÁÀẢÃẠÂẤẦẨẪẬĂẮẰẲẴẶEÉÈẺẼẸÊẾỀỂỄỆIÍÌỈĨỊOÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢUÚÙỦŨỤƯỨỪỬỮỰYÝỲỶỸỴĐaáàảãạâấầẩẫậăắằẳẵặeéèẻẽẹêếềểễệiíìỉĩịoóòỏõọôốồổỗộơớờởỡợuúùủũụưứừửữựyýỳỷỹỵđA-Z\s]',
        ' ', str), tmp[1])

def get_word_pos(s):
    r = re.compile("[a-zAÁÀẢÃẠÂẤẦẨẪẬĂẮẰẲẴẶEÉÈẺẼẸÊẾỀỂỄỆIÍÌỈĨỊOÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢUÚÙỦŨỤƯỨỪỬỮỰYÝỲỶỸỴĐaáàảãạâấầẩẫậăắằẳẵặeéèẻẽẹêếềểễệiíìỉĩịoóòỏõọôốồổỗộơớờởỡợuúùủũụưứừửữựyýỳỷỹỵđA-Z]+")
    return [[m.start(), m.end()] for m in r.finditer(s)]

def get_all_words(s, n):
    s = s.lower().replace('\xa0', '')
    s = re.sub(
        r'[^a-zAÁÀẢÃẠÂẤẦẨẪẬĂẮẰẲẴẶEÉÈẺẼẸÊẾỀỂỄỆIÍÌỈĨỊOÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢUÚÙỦŨỤƯỨỪỬỮỰYÝỲỶỸỴĐaáàảãạâấầẩẫậăắằẳẵặeéèẻẽẹêếềểễệiíìỉĩịoóòỏõọôốồổỗộơớờởỡợuúùủũụưứừửữựyýỳỷỹỵđA-Z\s]',
        ' ', s)
    tokens = [token for token in s.split(" ") if len(token) > 0]
    ngrams = zip(*[tokens[i:] for i in range(n)])
    ngrams = [" ".join(ngram) for ngram in ngrams]
    return ngrams

def match_special_syl(str):
    tmp = match_date(str)
    str = tmp[0]
    date = tmp[1]
    tmp = match_email(str)
    str = tmp[0]
    email = tmp[1]
    tmp = match_url(str)
    str = tmp[0]
    url = tmp[1]
    tmp = match_number(str)
    str = tmp[0]
    number = tmp[1]
    return ( str, { "date" : date, "email" : email, "url" : url, "number" : number})

def match_date(str):
    date = re.findall(r"\d+\/\d+\/\d+|\d+\/\d+|\d+-\d+-\d+|\d+-\d+", str)
    return (re.sub(r"\d+\/\d+\/\d+|\d+\/\d+|\d+-\d+-\d+|\d+-\d+", "DATE", str), date)

def match_email(str):
    email = re.findall(r"(\.|[a-z]|[A-Z]|[0-9])*@(\.|[a-z]|[A-Z]|[0-9])*", str)
    return (re.sub(r"(\.|[a-z]|[A-Z]|[0-9])*@(\.|[a-z]|[A-Z]|[0-9])*", "EMAIL", str), email)

def match_url(str):
    url = re.findall(r"(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})", str)
    return (re.sub(r"(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})", "URL", str), url)

def match_number(str):
    number = re.findall(r"\d+", str)
    return (re.sub(r"\d+", "NUMBER", str), number)

def delete_en_docs(data, words):
    deep_copy = data
    for path in data["path"]:
        print(path)
        with open(path, encoding="utf-8") as fs:
            content = fs.read()
        if any(word in content.lower() for word in words):
            deep_copy["path"].remove(path)
    print(len(deep_copy["path"]))
    write_url_list_file(deep_copy)

def convert_to_hp_path(files):
    return [ "/media/" + file[30:]  for file in files]

# print(formatSentence("Chiều ngày 7 6 tại trụ sở Thanh tra Chính phủ Phó Tổng Thanh tra Đặng Công Huẩn đã chủ trì cuộc họp Thường trực Hội đồng Thi đua khen thưởng về việc khen thưởng đối với các cá nhân tập thể có thành tích trong việc thực hiện Luật Phòng chống tham nhũng PCTN trình Thủ tướng Chính phủ"))