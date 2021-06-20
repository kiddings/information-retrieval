class Vocab(object):

    def __init__(self):
        self.WordBag = {}
        self.re_WordBag = {}  # 反词袋

    def add(self, word):
        if word not in self.WordBag.keys():
            length = len(self.WordBag)
            self.WordBag[word] = length
            self.re_WordBag[length] = word
    '''
    def words2ids(self, words):  # 把一个词语序列转换为id序列
        ids = []
        for word in words:
            ids.append(self.WordBag[word])
        return ids
        
    def ids2words(self, ids):  # 把一个id序列转换为词语序列
        words = []
        for index in ids:
            words.append(self.re_WordBag[index])
        return words
    '''

    def word2id(self, word):  # 取出某一个词的id，-1表示没有该词
        if word in self.WordBag.keys():
            return self.WordBag[word]
        else:
            return -1

    def id2word(self, index):  # 取出一个id对应的词语，-1表示没有该id
        if index in self.re_WordBag.keys():
            return self.re_WordBag[index]
        else:
            return -1


class Docs(object):

    def __init__(self):
        self.DocSet = {}
        self.re_DocSet = {}

    def add(self, doc_name):
        length = len(self.DocSet)
        self.DocSet[doc_name] = length
        self.re_DocSet[length] = doc_name

    def name2id(self, doc_name):
        return self.DocSet[doc_name]

    def names2ids(self, names):
        ids = []
        for name in names:
            ids.append(self.DocSet[name])

        return ids

    def id2name(self, doc_id):
        return self.re_DocSet[doc_id]

    def ids2names(self, ids):
        names = []
        for index in ids:
            names.append(self.re_DocSet[index])

        return names


if __name__ == '__main__':
    print('test')