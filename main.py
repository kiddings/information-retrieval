from retrieval import retrieval
import argparse
import time
import joblib
import jieba.analyse
from build_corpus_AE import decode_time, encode_time
from display import draw_one_pic
import os

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Paper Retrieval System')
    parser.add_argument('--mode', type=str, default='search', help='[search, display]')
    parser.add_argument('--amout', type=int, default=20, help='Number of results returned')
    parser.add_argument('--query', type=str, default=None, help='Query statement')
    parser.add_argument('--author', type=str, default=None)
    parser.add_argument('--year_range', type=list, default=None)

    path_record = joblib.load('processed_data_2/path_record.pickle')
    time_record = joblib.load('processed_data_2/time_record.pickle')
    author_record = joblib.load('processed_data_2/author_record.pickle')
    docs = joblib.load('processed_data_2/docs.pickle')

    args = parser.parse_args()
    if args.mode == 'search':
        if args.query is None and args.author is None and args.year_range is None:
            print('You input nothing, please input something')
            exit(-1)

        start = time.time()
        res_doc_id_list, scores = retrieval(args.query)
        end = time.time()
        duration = end - start
        final = []

        if args.author is not None and args.year_range is not None:
            for doc_id in res_doc_id_list:
                time = time_record[doc_id]
                if args.year_range[0] <= time % 10000 <= args.year_range[1] and author_record[doc_id] == args.author:
                    final.append(doc_id)

        elif args.author is not None and args.year_range is None:
            for doc_id in res_doc_id_list:
                if author_record[doc_id] == args.author:
                    final.append(doc_id)

        elif args.author is None and args.year_range is not None:
            for doc_id in res_doc_id_list:
                time = time_record[doc_id]
                if args.year_range[0] <= time % 10000 <= args.year_range[1]:
                    final.append(doc_id)

        else:
            final = res_doc_id_list[:]

        print('query = {}, took {}s'.format(args.query, duration))

        if len(final) == 0:
            print('nothing found, please try another words')
            exit(0)

        des = min(args.amout, len(final))
        for i in range(des):
            doc_id = final[i]
            with open(path_record[doc_id], 'r', encoding='utf-8') as f:
                text = f.read()
                keywords = jieba.analyse.textrank(text, topK=10, withWeight=False, allowPOS=('ns', 'n', 'vn', 'v'))
                new_keywords = ''
                for word in keywords:
                    new_keywords += word
                    if word != keywords[-1]:
                        new_keywords += '，'

                author = author_record[doc_id]
                time = decode_time(time_record[doc_id])
                name = docs.id2name(doc_id)
                print('\n')
                print('{}  [{}]  <{}>'.format(i + 1, scores.get(doc_id, 0), name))
                print('Author: {}'.format(author))
                print('Time of publication: {}'.format(time))
                print('keywords: {}'.format(new_keywords))
                print('\n')

        print('input an index to show more information, input -1 to exit')
        while True:
            index = input('input the index:')
            index = int(index)
            if index == -1:
                break

            else:
                print('<{}>'.format(docs.id2name(final[index - 1])))
                with open(path_record[final[index - 1]], 'r', encoding='utf-8') as f:
                    text = f.read()
                print(text)
                draw_one_pic(final[index - 1])
                print('\n')

    elif args.mode == 'display':
        print('please input a name of an article to show its more information, input 0 to exit')
        while True:
            name = input('input the name:')

            if name == '0':
                break

            doc_id = docs.name2id(name)
            if doc_id not in docs.re_DocSet.keys():
                print('You input the wrong name')
                exit(0)

            with open(path_record[doc_id], 'r', encoding='utf-8') as f:
                text = f.read()
                keywords = jieba.analyse.textrank(text, topK=10, withWeight=False, allowPOS=('ns', 'n', 'vn', 'v'))
                new_keywords = ''
                for word in keywords:
                    new_keywords += word
                    if word != keywords[-1]:
                        new_keywords += '，'

                author = author_record[doc_id]
                time = decode_time(time_record[doc_id])
                print('\n')
                print('Title: <{}>'.format(name))
                print('Author: {}'.format(author))
                print('Time of publication: {}'.format(time))
                print('keywords: {}'.format(new_keywords))
                print(text)
                draw_one_pic(doc_id)
                print('\n')