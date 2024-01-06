import sys
sys.path.append("")

import os 
import dotenv
dotenv.load_dotenv()

ES_HOST = os.getenv('ES_HOST')

from collections import defaultdict
from elasticsearch import Elasticsearch

from retrieval.bm25_search import bm25_search
from retrieval.vector_search import vector_search

es = Elasticsearch(ES_HOST)


def hybrid_search(
        index_name: str,
        query: str,
        alpha: float = 0.5,
        k: int = 5
):
    rrf_scores = hybrid_search_score(index_name, query, alpha=alpha, k=k)
    doc_ids = list(rrf_scores.keys())
    results = []

    for doc_id in doc_ids:
        result = es.search(
            index=index_name,
            body={
                "query": {
                    "match_phrase": {
                        "_id": doc_id
                    }
                },
                "size": 1
            }
        )
        results.append(result['hits']['hits'][0]['_source'])
    
    return results
        
def hybrid_search_score(index_name, query, alpha=0.5, k=5):
    vector_results = vector_search(index_name, query, k)
    bm25_results = bm25_search(index_name, query, k)
    bm25_results = normalize_bm25_scores(bm25_results)

    vector_ids = [hit['_id'] for hit in vector_results['hits']['hits']]
    bm25_ids = [hit['_id'] for hit in bm25_results['hits']['hits']]
    rrf_score = {}

    for rank, doc_id in enumerate(vector_ids):
        rank += 1
        rrf_score[doc_id] = [(1 - alpha) / rank]

    for rank, doc_id in enumerate(bm25_ids):
        rank += 1
        if doc_id not in vector_ids:
            rrf_score[doc_id] = [alpha / rank]
        else:
            rrf_score[doc_id].append(alpha / rank)

    min_score = get_min_score(rrf_score)

    for doc_id, scores in rrf_score.items():
        if len(scores) == 1:
            rrf_score[doc_id] = [min_score]
    
    rrf_score = {k: sum(v) for k, v in rrf_score.items()}
    rrf_score = {k: v for k, v in sorted(rrf_score.items(), key=lambda item: item[1], reverse=True)}
    return rrf_score

def normalize_bm25_scores(bm25):
    max_score = bm25['hits']['max_score']
    for hit in bm25['hits']['hits']:
        hit['_score'] = hit['_score'] / max_score
    return bm25

def get_min_score(rrf_score):
    return min([min(v) for v in rrf_score.values()])

