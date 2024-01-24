import os
import dotenv
dotenv.load_dotenv()

from db.elastic_search import ElasticSearch


es = ElasticSearch()
response = es.hybrid_search(index_name="cdnc_law", query="Tiền lương thử việc của người lao động được quy định như thế nào")

for doc in response:
    print(doc)
    print("====================================")
    # break

# for hit in response['hits']['hits']:
#     print(hit['_source']['content'])
#     print("====================================")