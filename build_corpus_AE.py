import os
from random import randint, random
import re
import functools


class Prob(object):
    def __init__(self, name):
        self.name = name
        self.high = 0
        self.low = 0


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


def decode_time(time):
    year = int(time / 10000)
    month = int((time % 10000) / 100)
    day = int(time % 100)
    time_string = '{}年{}月{}日'.format(year, month, day)
    return time_string


def encode_time(time_string):
    tmp = re.search(r'(\d{4})年(\d{0,2})月(\d{0,2})日', time_string)
    year = int(tmp.group(1))
    month = int(tmp.group(2))
    day = int(tmp.group(3))
    return year * 10000 + month * 100 + day


# 获取引用
def get_quote(doc_name, quote_record, quoted_record, time_record):
    """
    :param quoted_record: 被引用记录表
    :param quote_record: 引用记录表
    :param doc_name: 当前文档名
    :param time_record: 时间记录表
    :return quoted, quoted_record: 引用的文档名， 更新后的引用记录表
    """

    candidates = {}
    # 定位文档名，取出待引用候选列表
    for (name, time) in time_record.items():
        if name != doc_name:
            candidates[name] = time

        else:
            break

    length = len(candidates)
    if length <= 50:
        return quote_record, quoted_record

    else:
        total = 0
        for name in candidates.keys():
            total += len(quoted_record[name])

        cumulative = 0
        prob_candidates = []
        # 计算概率分布，被引用的次数越多，就越有可能被再次引用
        for name in candidates.keys():
            doc = Prob(name)
            doc.low = cumulative
            doc.high = doc.low + len(quoted_record[name]) / total
            cumulative = doc.high
            prob_candidates.append(doc)

        ref_len = randint(0, 10)  # 随机引用论文篇幅
        if ref_len == 0:
            return quote_record, quoted_record

        cnt = 0
        while True:
            possibility = random()
            # print(possibility)
            for candidate in prob_candidates:
                # 概率命中概率区间 && 不重复引用 && 时间满足先后条件
                if candidate.low <= possibility < candidate.high and candidate.name not in quote_record[doc_name] \
                        and time_record[candidate.name] < time_record[doc_name]:
                    quote_record[doc_name].append(candidate.name)
                    quoted_record[candidate.name].append(doc_name)
                    cnt += 1
                    break
            if cnt == ref_len:
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
        quoted_record[doc_name].append(doc_name)  # 为了计算概率，开始时假设自己被自己引用了
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

        # 将作者、时间和参考文献写入文件中
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
    # 把自己从被引用列表中清除
    for name in quoted_record.keys():
        quoted_record[name].remove(name)
    print('{} done!'.format(dir_name))


if __name__ == '__main__':
    root_dir = 'data'
    process(root_dir)