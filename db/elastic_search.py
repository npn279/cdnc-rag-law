import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from elasticsearch import Elasticsearch
from utils.get_emb import get_emb

class ElasticSearch:
    def __init__(self, host="http://localhost:9200"):
        self.es = Elasticsearch(host)

    def bm25_search(self, index_name, query, k=5, field="content"):
        res = self.es.search(
            index=index_name,
            body={
                "query": {
                    "match": {
                        field: query
                    }
                },
                "size": k
            }
        )
        return res
    
    def vector_search(self, index_name, query, k=5, **kwargs):
        field = kwargs.get("field", "embedding")

        embeddings = get_emb(query).data[0].embedding
        sem_search_result = self.es.search(
            index=index_name, 
            knn={
                "field": field,
                "query_vector": embeddings,
                "k": k,
                "num_candidates": 100
            }
        )   

        return sem_search_result
    
    def hybrid_search(self, index_name, query, k=5, ranking_constant=30, **kwargs):
        bm25_result = self.bm25_search(index_name, query, k, **kwargs)
        sem_result = self.vector_search(index_name, query, k, **kwargs)

        # RRF Score 
        rrf_results = {}
        for rank, hit in enumerate(sem_result['hits']['hits']):
            rrf_results[ hit['_id'] ] = {
                "_score": [1.0 / (ranking_constant + rank + 1)],
                "_source": hit['_source'],
            }

        for rank, hit in enumerate(bm25_result['hits']['hits']):
            if hit['_id'] in rrf_results:
                rrf_results[ hit['_id'] ]['_score'].append(1.0 / (ranking_constant + rank + 1))
            else:
                rrf_results[ hit['_id'] ] = {
                    "_score": [1.0 / (ranking_constant + rank + 1)],
                    "_source": hit['_source'],
                }

        for hit in rrf_results.values():
            hit['_score'] = sum(hit['_score'])

        rrf_results = dict(sorted(rrf_results.items(), key=lambda x: x[1]["_score"], reverse=True)[:k])
        return rrf_results
    
    def get_doc_by_id(self, index_name, id, k=1):
        result = self.es.search(
            index=index_name,
            body={
                "query": {
                    "match_phrase": {
                        "_id": id
                    }
                },
                "size": k
            }
        )

        return result
        
    