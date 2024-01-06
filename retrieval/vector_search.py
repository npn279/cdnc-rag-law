import sys
sys.path.append("")

import os
import dotenv
dotenv.load_dotenv()

ES_HOST = os.getenv('ES_HOST')
EMBED_MODEL = os.getenv('EMBED_MODEL')

from utils.get_emb import get_emb
from elasticsearch import Elasticsearch
es = Elasticsearch(ES_HOST)


def vector_search(index_name: str, 
                  query: str, 
                  k: int = 5 # No. of results
):
    embeddings = get_emb(query)

    sem_search_result = es.search(
        index=index_name, 
        knn={
            "field": "embedding",
            "query_vector": embeddings,
            "k": k,
            "num_candidates": 100
        }
    )   

    return sem_search_result
