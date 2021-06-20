import os
import jieba
import joblib
from utils import Vocab, Docs
from spelling_check import spelling_correcting
from doc_rank import rank
from history import usage

# 解析查询语句
def read_query(query_string):
    stop_words = joblib.load('processed_data_2/stop_wd.pickle')
    # query_string = query_string.replace(' ', '')  # 删除空格
    logic_words = ['AND', 'OR', 'NOT']
    reflection = {'AND': 1, 'OR': 2, 'NOT': 0}  # 映射

    jieba.load_userdict('logic_words.txt')
    if any(logic_word in query_string for logic_word in logic_words):  # 如果任何一个逻辑连接词出现，为布尔查询语句
        bool_flag = True

    else:
        bool_flag = False

    if not bool_flag:  # 自由文本模式，可以看做都是AND
        terms = jieba.lcut(query_string)  # 词项
        new_terms = []
        for term in terms:
            if term not in stop_words:
                new_terms.append(term)
        masks = [1] * len(new_terms)  # 掩码表示逻辑关系
        return new_terms, masks, bool_flag

    else:  # 布尔查询模式
        terms = []
        masks = []
        # word_list = query_string.split(' ')
        word_list = jieba.lcut(query_string)
        # 第一个词如果没有not修饰，可以看成是and修饰
        if word_list[0] != 'NOT':
            word_list.insert(0, 'AND')

        # 去除停用词
        new_word_list = []
        for i in range(len(word_list)):
            if word_list[i] not in stop_words and word_list[i] not in logic_words:
                new_word_list.append(word_list[i - 1])
                new_word_list.append(word_list[i])
        print(new_word_list)

        for i in range(len(new_word_list)):
            if new_word_list[i] not in logic_words:
                masks.append(reflection[new_word_list[i - 1]])
                terms.append(new_word_list[i])

        return terms, masks, bool_flag

def and_merge(doc_list1, doc_list2):  # A and B
    return list(set(doc_list1).intersection(set(doc_list2)))

def or_merge(doc_list1, doc_list2):  # A or B
    return list(set(doc_list1).union(doc_list2))

def not_merge(doc_list1, doc_list2):  # A not B
    return list(set(doc_list1).difference(set(doc_list2)))

def indexing_and_merge(terms, masks):
    inverted_index = joblib.load('./processed_data_2/in_index.pickle')  # 读取倒排索引
    vocab = joblib.load('./processed_data_2/vocab.pickle')
    docs = joblib.load('./processed_data_2/docs.pickle')

    doc_id_lists = []
    for item in terms:

        if isinstance(item, tuple):  # 括号内的词项先求并集
            tmp = inverted_index[vocab.word2id(item[0])][:]
            for i in range(1, len(item)):
                tmp = or_merge(tmp, inverted_index[vocab.word2id(item[i])])
            doc_id_lists.append(tmp)

        else:
            doc_id_lists.append(inverted_index[vocab.word2id(item)][:])

    func = [not_merge, and_merge, or_merge]  # 与或非操作集合

    # 如果masks的长度等于terms的长度，说明开头有一个NOT，为了保持操作的统一性可以在前面加一个全集
    if len(masks) == len(terms):
        u = list(docs.DocSet.values())[:]  # 全集
        doc_id_lists.insert(0, u)

    length = len(masks)
    cnt = 0
    while True:
        for i in range(len(masks)):
            if masks[i] == min(masks):  # 逻辑连接符和掩码大小对应，掩码越小，优先级越大
                doc_id_lists[i] = func[masks[i]](doc_id_lists[i], doc_id_lists[i + 1])
                del doc_id_lists[i + 1]
                del masks[i]
                cnt += 1
                break  # 一次只处理一个操作符，然后重新扫描

        if cnt >= length:
            break

    return doc_id_lists[0]

def retrieval(query_string):
    docs = joblib.load('./processed_data_2/docs.pickle')

    if query_string is None:  # 如果查询语句为空直接返回所有文档id
        return list(docs.re_DocSet.keys()), {}

    terms, masks, bool_flag = read_query(query_string)
    print(terms)
    terms = spelling_correcting(terms, 10)
    doc_id_list = indexing_and_merge(terms, masks)
    usage(doc_id_list)
    ranked_doc_id_list, scores = rank(terms, doc_id_list, bool_flag)
    return ranked_doc_id_list, scores


if __name__ == '__main__':
    res_doc_id_list, res_scores = retrieval('上海')
    print(res_doc_id_list)