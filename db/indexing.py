import sys
sys.path.append('')

import os
import dotenv
dotenv.load_dotenv()

ES_HOST = os.getenv('ES_HOST')
INDEX_NAME = os.getenv('INDEX_NAME')
HF_TOKEN = os.getenv('HF_TOKEN')

from elasticsearch import Elasticsearch, helpers
es = Elasticsearch(ES_HOST)

from db.dataloader import load_hf
from utils.get_emb import get_emb
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import ElasticsearchStore
from langchain_community.embeddings import OpenAIEmbeddings


def indexing(documents):
    embedding = OpenAIEmbeddings()
    text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1024,
            chunk_overlap=256,
        )

    documents = text_splitter.split_documents(documents)
    db = ElasticsearchStore.from_documents(
        documents,
        embedding,
        es_url="http://localhost:9200",
        index_name="cdnc_hp",
    )




def _indexing(documents):
    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1024,
            chunk_overlap=256,
        )

        documents = text_splitter.split_documents(documents)
        docs = [{"_index": INDEX_NAME, "_source": {"content": doc.page_content, 
                                                   "metadata": doc.metadata, 
                                                   "embedding": get_emb(doc.page_content)}} 
                                                   for doc in documents]
        
        # bulk indexing
        helpers.bulk(es, docs, index=INDEX_NAME)
    except Exception as e:
        print('Indexing failed')
        print(e)
    
    return

if __name__ == '__main__':
    # documents = load_hf(dataset_name='iamnguyen/bgddt-2023', 
    #                     split='train[:10]', 
    #                     content_column='data', 
    #                     token=HF_TOKEN)
    # indexing(documents)

    documents = load_hf(dataset_name='iamnguyen/luat', 
                        split='train', 
                        content_column='data', 
                        token=HF_TOKEN)
    indexing(documents)

    # documents = load_hf(dataset_name='iamnguyen/hien_phap', 
    #                     split='train', 
    #                     content_column='data', 
    #                     token=HF_TOKEN)
    # indexing(documents)
