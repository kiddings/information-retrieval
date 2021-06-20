import os
from random import randint, random
import re
import functools
from build_corpus_AE import decode_time, encode_time

# 获取时间
def get_time():
    year = randint(1980, 2020)
    month = randint(1, 12)
    day = randint(1, 30)
    time = year * 10000 + month * 100 + day
    return time

# 获取作者名字
def get_author():
    first_names = []
    with open('百家姓.txt', 'r', encoding='utf-8') as f:
        text = f.read().replace('。', '').replace('，', '').replace('\n', '')
        for i in range(len(text)):
            first_names.append(text[i])

    last_names = first_names[:10]

    index_1 = randint(0, len(first_names) - 1)  # 姓
    index_2 = randint(0, len(last_names) - 1)  # 名

    return first_names[index_1] + last_names[index_2]


# 定义引用关系
def get_quote(doc_name, quote_record, quoted_record, time_record):
    """
    :param quoted_record: 被引用记录表
    :param quote_record: 引用记录表
    :param doc_name: 当前文档名
    :param time_record: 时间记录表
    :return quoted, quoted_record: 引用的文档名， 更新后的引用记录表
    """

    candidates = []
    # 定位文档名，去除带引用候选列表
    for name in time_record.keys():
        if name != doc_name:
            candidates.append(name)

        else:
            break

    if len(candidates) < 50:
        return quote_record, quoted_record

    else:
        ref_len = randint(0, 10)
        cnt = 0
        while True:
            index = randint(0, len(candidates) - 1)
            candidate = candidates[index]
            if candidate not in quote_record[doc_name] and time_record[candidate] < time_record[doc_name]:
                quote_record[doc_name].append(candidate)
                quoted_record[candidate] = doc_name
                cnt += 1
            if cnt >= ref_len:
                break
        return quote_record, quoted_record


def process(dir_name):
    quoted_record = {}
    quote_record = {}
    paths = []
    time_record = {}
    for file in os.listdir(dir_name):
        file_path = dir_name + '/' + file
        doc_name = file.replace('.txt', '')
        time_record[doc_name] = get_time()
        quoted_record[doc_name] = []
        quote_record[doc_name] = []
        paths.append(file_path)

    sorted_time_record = {}  # 经过排序的时间记录表
    tmp = sorted(time_record.items(), key=lambda x: x[1])
    for (name, time) in tmp:
        sorted_time_record[name] = time
    cnt = 0
    for path in paths:
        doc_name = path.split('/')[-1].replace('.txt', '')
        quote_record, quoted_record = get_quote(doc_name, quote_record, quoted_record, sorted_time_record)  # 获取引用的文档
        # 将时间和参考文献写入文件中
        with open(path, 'a', encoding='utf-8') as f:
            f.write('\n')
            f.write('-作者-')
            f.write(get_author())
            f.write('\n')
            f.write('-时间-')
            f.write(decode_time(time_record[doc_name]))
            f.write('\n')
            f.write('-参考文献-')
            for i in range(len(quote_record[doc_name])):
                f.write(quote_record[doc_name][i])
                if i != len(quote_record[doc_name]) - 1:
                    f.write('，')
        cnt += 1
        print(cnt)


if __name__ == '__main__':
    process('data_2')
