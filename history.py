import joblib
import os

def usage(doc_id_list):
    if os.path.exists('history.pickle'):
        history_search = joblib.load('history.pickle')

    else:
        history_search = {}

    for doc_id in doc_id_list:
        history_search[doc_id] = history_search.get(doc_id, 0) + 1

    joblib.dump(history_search, 'history.pickle')