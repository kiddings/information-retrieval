import jieba
import os
from utils import Vocab, Docs
import re
from build_corpus_AE import decode_time, encode_time
import pypinyin
import math
import joblib

def get_stopwords():
    with open('stopwords.txt', 'r', encoding='utf-8') as f1:
        words = f1.read()
        stopwords = words.split('\n')
    return stopwords


vocab = Vocab()
docs = Docs()
dir_name = 'data_1'
time_record = {}  # 时间记录
quote_record = {}  # 引用记录
quoted_record = {}  # 被引用记录
author_record = {}  # 作者记录
stop_wd = get_stopwords()  # 停用词表
inverted_index = {}  # 倒排索引
path_recoord = {}  # 路径索引
tf = {}  # 词频
idf = {}  # 逆文档频率
tf_idf = {}
pronounce = {}

for file in os.listdir(dir_name):
    doc_name = file.replace('.txt', '')
    docs.add(doc_name)

cnt = 0
for file in os.listdir(dir_name):
    path = dir_name + '/' + file
    print(path)
    doc_name = file.replace('.txt', '')
    doc_id = docs.name2id(doc_name)
    path_recoord[doc_id] = path
    quote_record[doc_id] = []
    tf[doc_id] = {}  # 统计词频

    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
        # 获取引用信息和发布时间，并将这两个信息从文本中剔除
        quote_location = re.search(r'-参考文献-.*', text)
        time_location = re.search(r'-时间-.*', text)
        author_location = re.search(r'-作者-.*', text)
        quote_list = quote_location.group().replace('-参考文献-', '').split('，')
        time_string = time_location.group().replace('-时间-', '')

        # 记录作者信息
        author_record[doc_id] = author_location.group().replace('-作者-', '')

        # 记录时间信息
        time_record[doc_id] = encode_time(time_string)

        # 记录引用信息
        if quote_list == ['']:  # 若quote_list为空
            quote_record[doc_id] = []

        else:
            for quote_id in docs.names2ids(quote_list):
                quote_record[doc_id].append(quote_id)

                # 统计被引用信息
                if quote_id not in quoted_record.keys():
                    quoted_record[quote_id] = []
                    quoted_record[quote_id].append(doc_id)

                else:
                    quoted_record[quote_id].append(doc_id)

        # 剔除文本中的时间、引用和作者信息
        text = text.replace(quote_location.group(), '').replace(time_location.group(), '').replace(author_location.group(), '')

        # 删除非中文字符
        pattern = re.compile(r'[^\u4e00-\u9fa5]')
        text = re.sub(pattern, '', text)

        # 分词（暂时使用lcut)
        word_list = jieba.lcut(text)
        screened_word_list = []

        for word in word_list:
            if word not in stop_wd:
                # 更新词表
                vocab.add(word)
                word_id = vocab.word2id(word)

                # 记录发音信息
                if word_id not in pronounce.keys():
                    pin_yin = ''
                    tmp = pypinyin.pinyin(word, style=pypinyin.Style.TONE3)
                    for i in tmp:
                        pin_yin += i[0]
                    pronounce[word_id] = pin_yin

                tf[doc_id][word_id] = tf[doc_id].get(word_id, 0) + 1  # 统计词频

                # 构建倒排索引（最普通版本）
                if word_id not in inverted_index.keys():
                    inverted_index[word_id] = []
                    inverted_index[word_id].append(doc_id)

                else:
                    # 不重复添加
                    if doc_id not in inverted_index[word_id]:
                        inverted_index[word_id].append(doc_id)
    cnt += 1
    print(cnt)

# 计算逆文档频率
N = len(os.listdir(dir_name))
for word_id in inverted_index.keys():
    idf[word_id] = math.log(N / len(inverted_index[word_id]), 10)

# 计算tf-idf
for doc_id in tf.keys():
    tf_idf[doc_id] = {}
    for word_id in tf[doc_id].keys():
        tf_idf[doc_id][word_id] = tf[doc_id][word_id] * idf[word_id]


# 保存各个统计统计量
save_dir = 'processed_data_1'
joblib.dump(vocab, save_dir + '/' + 'vocab.pickle')
joblib.dump(docs, save_dir + '/' + 'docs.pickle')
joblib.dump(tf_idf, save_dir + '/' + 'tf_idf.pickle')
joblib.dump(inverted_index, save_dir + '/' + 'in_index.pickle')
joblib.dump(time_record, save_dir + '/' + 'time_record.pickle')
joblib.dump(quote_record, save_dir + '/' + 'quote_record.pickle')
joblib.dump(quoted_record, save_dir + '/' + 'quoted_record.pickle')
joblib.dump(author_record, save_dir + '/' + 'author_record.pickle')
joblib.dump(pronounce, save_dir + '/' + 'pronounce.pickle')
joblib.dump(stop_wd, save_dir + '/' + 'stop_wd.pickle')
joblib.dump(path_recoord, save_dir + '/' + 'path_record.pickle')



