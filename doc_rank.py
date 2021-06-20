import math
import joblib
from spelling_check import dismantling

# 根据统计数据排序
def rank_by_statistic(terms, doc_id_list):
    vocab = joblib.load('./processed_data_2/vocab.pickle')
    tf_idf = joblib.load('./processed_data_2/tf_idf.pickle')
    scores = {}

    for doc_id in doc_id_list:
        scores[doc_id] = 0

        for term in terms:
            if isinstance(term, tuple):
                for word in term:
                    scores[doc_id] += tf_idf[doc_id].get(vocab.word2id(word), 0)

            else:
                scores[doc_id] += tf_idf[doc_id].get(vocab.word2id(term), 0)

    return scores

# 根据文章影响力排序
def rank_by_influence(doc_id_list):
    quote_record = joblib.load('./processed_data_2/quote_record.pickle')
    quoted_record = joblib.load('./processed_data_2/quoted_record.pickle')

    scores = {}
    for doc_id in doc_id_list:
        scores[doc_id] = len(quoted_record.get(doc_id, []))

    for doc_i in doc_id_list:
        for doc_j in doc_id_list:
            if doc_i in quote_record[doc_j] and doc_i != doc_j:  # 如果dic_i被doc_j引用
                scores[doc_i] += scores[doc_j]  # doc_j的分数累加值doc_i上

    return scores

# 根据文章查询量历史排序
def rank_by_history(doc_id_list):
    history_search = joblib.load('history.pickle')

    scores = {}
    for doc_id in doc_id_list:
        scores[doc_id] = history_search.get(doc_id, 0)

    return scores


def rank(terms, doc_id_list, bool_flag):

    if bool_flag:  # 如果是布尔查询，则统计数据得分均为0
        statistic_scores = {}
        for doc_id in doc_id_list:
            statistic_scores[doc_id] = 0

    else:
        statistic_scores = rank_by_statistic(terms, doc_id_list)

    influence_scores = rank_by_influence(doc_id_list)
    history_scores = rank_by_history(doc_id_list)
    scores = {}

    # 将三组分数归一化
    statistic_sum = 0
    influence_sum = 0
    history_sum = 0
    for doc_id in doc_id_list:
        statistic_sum += statistic_scores[doc_id]
        influence_sum += influence_scores[doc_id]
        history_sum += history_scores[doc_id]

    for doc_id in doc_id_list:
        statistic_scores[doc_id] /= statistic_sum + 1  # 拉普拉斯平滑
        influence_scores[doc_id] /= influence_sum + 1
        history_scores[doc_id] /= history_sum + 1
        # 按2:2:1的比例综合三种分数
        scores[doc_id] = 0.8 * statistic_scores[doc_id] + 0.1 * influence_scores[doc_id] + 0.1 * history_scores[doc_id]

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    res = []
    for item in ranked:
        res.append(item[0])

    return res, scores

