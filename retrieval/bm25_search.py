import sys
sys.path.append("")

import os
import dotenv
dotenv.load_dotenv()
ES_HOST = os.getenv('ES_HOST')

from elasticsearch import Elasticsearch
es = Elasticsearch(ES_HOST)


def bm25_search(index_name: str, 
                query: str, 
                k: int = 5 # No. of results
):
    results = es.search(
        index=index_name,
        body={
            "query": {
                "match": {
                    "content": query
                }
            },
            "size": k
        }
    )
    return results

