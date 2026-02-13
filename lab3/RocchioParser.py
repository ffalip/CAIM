from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError
from elasticsearch.client import CatClient
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import Q
import numpy as np
import argparse

def doc_count(client, index):
    """
    Returns the number of documents in an index
    """
    return int(CatClient(client).count(index=[index], format='json')[0]['count'])

def document_term_vector(client, index, id):
    """
    Returns the term vector of a document and its statistics a two sorted list of pairs (word, count)
    The first one is the frequency of the term in the document, the second one is the number of documents
    that contain the term
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

def toTFIDF(client, index, file_id):
    """
    Returns the term weights of a document
    """
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

def normalize(tw):
    """
    Normalizes the weights in t so that they form a unit-length vector
    It is assumed that not all weights are 0
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



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--index', default=None, help='Index a buscar')
    parser.add_argument('--nhits', default=5, type=int, help='Nombre de docs a retornar')
    parser.add_argument('--rounds', default=5, type=int, help='Nombre de rondes')
    parser.add_argument('--alpha', default=0.9, type=float, help='Valor del paràmetre alpha')
    parser.add_argument('--beta', default=0.1, type=float, help='Valor del paràmetre beta')
    parser.add_argument('--qsize', default=3, type=int, help='mida màxima de les noves queries')
    parser.add_argument('--query', default=None, nargs=argparse.REMAINDER, help='Llista de paraules a buscar')

    args = parser.parse_args()

    #Parametres
    nrounds = args.rounds
    alpha   = args.alpha
    beta    = args.beta
    R       = args.qsize
    index   = args.index
    k       = args.nhits

    query = args.query
    print(query)
    try:
        client = Elasticsearch()
        s = Search(using=client, index=index)

        if query is not None:
            for i in range(0, nrounds):

                q = Q('query_string',query=query[0])
                for i in range(1, len(query)):
                    q &= Q('query_string',query=query[i])

                s = s.query(q)
                response = s[0:k].execute()

                map_q = {}
                for word in query:
                    if '^' in word:
                        wrd, val = word.split('^')
                        map_q[wrd] = float(val)
                    else:
                        map_q[word] = 1.0

                map_q = normalize(map_q)

                sumDocs = {} # calculem d1+d2+...+dk
                for r in response:
                    tw = toTFIDF(client, index, r.meta.id)
                    for t in tw:
                        sumDocs[t] = sumDocs.get(t,0) + tw[t]

                #q' = alpha * q + beta * sumDocs/k
                for t in map_q:
                    map_q[t] *= alpha

                for t in sumDocs:
                    sumDocs[t] *= beta

                new_q = {}
                for t in set(map_q) | set(sumDocs):
                    new_q[t] = map_q.get(t,0) + sumDocs.get(t,0)/k

                new_q = sorted(new_q.items(), key=lambda item: item[1], reverse=True)[:R]

                query = []
                for t, w in new_q:
                    query.append(t + '^' + str(w))
                print(query)


            #----------Resultat----------
            num_hits = response.hits.total['value']
            print(f'{num_hits} documents trobats, es mostren els {k} millors:')
            for r in response:
                print(f'ID= {r.meta.id} SCORE= {r.meta.score}')
                print(f'PATH= {r.path}')
                print(f'TEXT= {r.text[:50]}')
                print('----------------------------------------------')

        else:
            print('La query és nul·la')

    except NotFoundError:
        print(f'Index {index} no existeix')








