import os
import dotenv
dotenv.load_dotenv()

from retrieval.bm25_search import bm25_search
from retrieval.vector_search import vector_search
from retrieval.hybrid_search import hybrid_search

INDEX_NAME = os.getenv('INDEX_NAME')


query = "Website của bộ công an là gì?"
results = hybrid_search(index_name=INDEX_NAME, query=query)

# for hit in results['hits']['hits']:
#     print(hit['_source']['content'])
#     print('-------------------')

for i, result in enumerate(results):
    print(i)
    print(result['content'])
    print('-------------------')