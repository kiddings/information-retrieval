import Levenshtein
import utils
import joblib
from Levenshtein import distance as calc_dis
import pypinyin

# 拆解括号
def dismantling(sequence):
    res = []
    for item in sequence:
        if isinstance(item, tuple):  # 如果item是个元组:
            for i in item:
                res.append(i)

        else:
            res.append(item)

    return res

# 取相似词语
def get_similitude(term, term_id, word_id_list, pronounce, k):
    # 获取term的拼音表示
    expression = ''
    tmp = pypinyin.pinyin(term, style=pypinyin.Style.TONE3)
    for i in tmp:
        expression += i[0]

    similar_words = {}  # 最相近的top_k

    for word_id in word_id_list:
        if len(similar_words) < k and word_id != term_id:
            similar_words[word_id] = calc_dis(expression, pronounce[word_id])

        else:
            # 更新最相似的top_k
            for (key, value) in similar_words.items():
                dis = calc_dis(expression, pronounce[word_id])
                if value > dis and term_id != word_id:
                    del similar_words[key]
                    similar_words[word_id] = dis
                    break

    # 排序
    ranked = sorted(similar_words.items(), key=lambda x: x[1], reverse=False)
    res = []
    for item in ranked:
        res.append(item[0])
    # res是doc_id的集合
    return res

# 拼写校正
def spelling_correcting(original_terms, expected):
    """
    :param original_terms: 原始查询词项序列
    :param expected: 文档频率阈值
    :return:
    """
    vocab = joblib.load('./processed_data_2/vocab.pickle')
    pronounce = joblib.load('./processed_data_2/pronounce.pickle')
    inverted_index = joblib.load('./processed_data_2/in_index.pickle')  # 读取倒排索引
    word_bag = list(vocab.WordBag.keys())[:]  # 获取词袋
    word_id_list = [vocab.word2id(word) for word in word_bag]

    res_terms = []
    for i in range(len(original_terms)):

        # 包含了两种情况：
        # 1、查询词项的文档频率没有达到阈值，能返回的结果可能会很少
        # 2、查询词项不在词典中，需要用别的词进行替换，且返回结果最好多一些
        if original_terms[i] not in vocab.WordBag.keys():  # 查询词项不在词典当中
            wrong_term = original_terms[i]  # 错误拼写词
            candidates = get_similitude(wrong_term, -1, word_id_list, pronounce, 5)  # -1表示没有这个词
            total_doc_freq = 0

            tmp = ()
            for candidate in candidates:
                if vocab.id2word(candidate) not in dismantling(res_terms):
                    # 查询语句应具有互异性
                    tmp += (vocab.id2word(candidate),)
                    total_doc_freq += len(inverted_index[candidate])

                    if total_doc_freq >= expected or candidate == candidates[-1]:
                        res_terms.append(tmp)
                        print('暂时没有找到包含\'{}\'的相关内容，已为您替换为：{}'.format(wrong_term, tmp))
                        break

        else:  # 查询词项在词典中
            term = original_terms[i]
            term_id = vocab.word2id(term)

            if len(inverted_index[term_id]) < expected:  # 如果查询词项的文档频率小于阈值
                candidates = get_similitude(term, term_id, word_id_list, pronounce, 5)
                total_doc_freq = len(inverted_index[term_id])

                tmp = (term, )
                for candidate in candidates:
                    if vocab.id2word(candidate) not in dismantling(res_terms):
                        # 查询语句应具有互异性
                        tmp += (vocab.id2word(candidate),)
                        total_doc_freq += len(inverted_index[candidate])

                        if total_doc_freq >= expected or candidate == candidates[-1]:
                            res_terms.append(tmp)
                            print('包含\'{}\'的相关内容较少，已为您扩充为{}'.format(term, [i for i in tmp]))
                            break
            else:
                res_terms.append(term)

    return res_terms

