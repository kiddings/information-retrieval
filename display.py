from pyecharts import options as opts
from pyecharts.charts import Graph
import os
import joblib
from build_corpus_AE import decode_time, encode_time
import webbrowser
from pyecharts.commons.utils import JsCode


def draw_one_pic(doc_id):
    quote_record = joblib.load('./processed_data_2/quote_record.pickle')
    quoted_record = joblib.load('./processed_data_2/quoted_record.pickle')
    time_record = joblib.load('./processed_data_2/time_record.pickle')
    docs = joblib.load('./processed_data_2/docs.pickle')
    author_record = joblib.load('./processed_data_2/author_record.pickle')

    # 定义类目
    categories_data = [opts.GraphCategory(name='self'), opts.GraphCategory(name='quote'),
                       opts.GraphCategory(name='quoted')]
    nodes_data = [opts.GraphNode(name=docs.id2name(doc_id), symbol_size=30, category=0,
                                 value=[decode_time(time_record[doc_id]), author_record[doc_id]])]
    tips_data = opts.TooltipOpts(trigger_on='click', formatter='{c}')

    # 引用文章节点
    for doc_i in quote_record.get(doc_id, []):
        node = opts.GraphNode(name=docs.id2name(doc_i), symbol_size=30, category=1,
                              value=[decode_time(time_record[doc_i]), author_record[doc_i]])
        nodes_data.append(node)

    # 被引用文章节点
    for doc_j in quoted_record.get(doc_id, []):
        node = opts.GraphNode(name=docs.id2name(doc_j), symbol_size=30, category=2,
                              value=[decode_time(time_record[doc_j]), author_record[doc_j]])
        nodes_data.append(node)

    links_data = []
    for i in range(1, len(nodes_data)):
        if nodes_data[i].get('category') == 1:
            links_data.append(opts.GraphLink(source=i, target=0,
                                             linestyle_opts=opts.LineStyleOpts(color='rgb(0,0,255)')
                                             ))

        else:
            links_data.append(opts.GraphLink(source=0, target=i,
                                             linestyle_opts=opts.LineStyleOpts(color='rgb(255,0,0)')
                                             ))

    c = (
        Graph(init_opts=opts.InitOpts(width='1000px', height='600px'))
            .add("", nodes_data, links_data, categories_data, tooltip_opts=tips_data, edge_symbol=['circle', 'arrow'],
                 repulsion=8000)
            .set_global_opts(title_opts=opts.TitleOpts(title="{}的引用关系图".format(docs.id2name(doc_id))))
            .render("one_pic.html")
    )

    webbrowser.open_new_tab('one_pic.html')

'''
def draw_all_pic(doc_id_list):
    quote_record = joblib.load('./processed_data_2/quote_record.pickle')
    quoted_record = joblib.load('./processed_data_2/quoted_record.pickle')
    time_record = joblib.load('./processed_data_2/time_record.pickle')
    docs = joblib.load('./processed_data_2/docs.pickle')
    author_record = joblib.load('./processed_data_2/author_record.pickle')

    tips_data = opts.TooltipOpts(trigger_on='click', formatter='{c}')

    nodes_data = []
    for doc_id in doc_id_list:
        for doc_i in quote_record.get(doc_id, []):
            nodes_data.append(opts.GraphNode(name=docs.id2name(doc_i), symbol_size=30,
                                             value=[decode_time(time_record[doc_i]), author_record[doc_i]]))
        for doc_j in quoted_record.get(doc_id, []):
            nodes_data.append(opts.GraphNode(name=docs.id2name(doc_j), symbol_size=30,
                                             value=[decode_time(time_record[doc_j]), author_record[doc_j]]))
        nodes_data.append(opts.GraphNode(name=docs.id2name(doc_id), symbol_size=30,
                                         value=[decode_time(time_record[doc_id]), author_record[doc_id]]))

    links_data = []
    for doc_id in doc_id_list:
        for doc_i in quote_record.get(doc_id, []):
            links_data.append(opts.GraphLink(source=docs.id2name(doc_i), target=docs.id2name(doc_id)))
        for doc_j in quoted_record.get(doc_id, []):
            links_data.append(opts.GraphLink(source=docs.id2name(doc_id), target=docs.id2name(doc_j)))

    print(links_data)

    # links_data = list(set(links_data))
    c = (
        Graph(init_opts=opts.InitOpts(width='1000px', height='600px'))
            .add("", nodes_data, links_data, tooltip_opts=tips_data, edge_symbol=['circle', 'arrow'],
                 repulsion=8000)
            .set_global_opts(title_opts=opts.TitleOpts(title='all relation'))
            .render("all_pic.html")
    )

    webbrowser.open_new_tab('all_pic.html')
'''
