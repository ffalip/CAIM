import numpy as np
'''
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import Q

def document_term_vector(client, index, id):
    """
    Returns the term vector of a document and its statistics a two sorted list of pairs (word, count)
    The first one is the frequency of the term in the document, the second one is the number of documents
    that contain the term

    :param client:
    :param index:
    :param id:
    :return:
    """
    termvector = client.termvectors(index=index, id=id, fields=['text'],
                                    positions=False, term_statistics=True)

    file_td = {}
    file_df = {}

    if 'text' in termvector['term_vectors']:
        for t in termvector['term_vectors']['text']['terms']:
            file_td[t] = termvector['term_vectors']['text']['terms'][t]['term_freq']
            file_df[t] = termvector['term_vectors']['text']['terms'][t]['doc_freq']
    return sorted(file_td.items()), sorted(file_df.items())

def normalize(tw):
    """
    Normalizes the weights in t so that they form a unit-length vector
    It is assumed that not all weights are 0
    :param tw:
    :return:
    """
    terms = []
    weights = []
    for t, w in tw.items():
        weights.append(w)

    weights = np.array(weights)

    norm = np.sqrt(np.sum(weights ** 2))

    for t,w in tw.items():
        tw[t] = w / norm

    return tw
    return None

def toTFIDF(client, index, file_id):
    """
    Returns the term weights of a document

    :param file:
    :return:
    """

    # Get the frequency of the term in the document, and the number of documents
    # that contain the term
    file_tv, file_df = document_term_vector(client, index, file_id)

    max_freq = max([f for _, f in file_tv])

    dcount = doc_count(client, index)


    tfidfw = {}
    for (t, w),(_, df) in zip(file_tv, file_df):
        tf_t = w/max_freq
        idf_t = np.log2(dcount/df)
        tfidfw[t] = tf_t * idf_t

    #print_term_weigth_vector(tfidfw)

    return normalize(tfidfw)

#Parametres
nrounds = 1
k       = 5
alpha   = 3
beta    = 1
R       = 6

client = Elasticsearch()
s = Search(using=client, index=index)
'''

#demanar query a l'usuari
user_query = input("Query: ").split()
print(user_query)

'''
q = Q('query_string',query=user_query[0])
for w in range(1, len(user_query)):
    q &= Q('query_string',query=user_query[1])

s = s.query(q)
response = s[0:k].execute()
tw_res = {}
for r in response:  # only returns a specific number of results
    tw = toTFIDF(client, 'news', r.meta.id)
    for t in tw:
        if t not in tw_res:
            tw_res[t] = 0
        tw_res[t] += tw[t]

    #print('ID= %s SCORE=%s' % (r.meta.id,  r.meta.score))
    #print('PATH= %s' % r.path)
    #print('TEXT: %s' % r.text[:50])
    #print('----------------------------------------------')

for t, w in tw_res.items():
    tw_res[t] = w / k

map_q = {}
for i in user_query:
    if i not in map_q:
        map_q[i] = 0
    map_q[i] += 1

max_freq_q = max(map_q.values())

for t, w in map_q.items():
    tf_t = w/max_freq
    map_q[t] = tf_t

map_q = normalize(map_q)
'''




