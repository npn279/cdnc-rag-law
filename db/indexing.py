import sys
sys.path.append("")

import os
from dotenv import load_dotenv
load_dotenv()

from llama_index.core import StorageContext, ServiceContext, VectorStoreIndex, Settings
from llama_index.core.node_parser import LangchainNodeParser
from llama_index.embeddings.openai import OpenAIEmbedding
from langchain.text_splitter import RecursiveCharacterTextSplitter
from llama_index.vector_stores.elasticsearch import ElasticsearchStore
from db.dataloader import *

# ENVS
INDEX_NAME = os.getenv("INDEX_NAME")
HF_TOKEN = os.getenv("HF_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

Settings.embed_model = OpenAIEmbedding(model=os.getenv("OPENAI_EMBEDDING_MODEL_NAME"), api_key=OPENAI_API_KEY, embed_batch_size=16) 
# Load data
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=256)
node_parser = LangchainNodeParser(text_splitter)


def indexing_data(documents: list, index_name: str = None):
    try:
        # split parent documents to chunks
        nodes = node_parser.get_nodes_from_documents(documents)
        # indexing parent docs
        es_store = ElasticsearchStore(
            index_name=index_name,
            es_url='http://localhost:9200',
        )
        storage_context = StorageContext.from_defaults(vector_store=es_store)

        index = VectorStoreIndex(
            nodes=nodes,
            storage_context=storage_context,
            use_async=True
        )
        return nodes
    except Exception as e:
        print(e)
        return False

if __name__ == "__main__":
    luat_hinh_su = load_txt("data/Bo luat hinh su 2015 100.txt")
    luat_dan_su = load_txt("data/Luat dan su 2015.txt")
    luat_hanh_chinh = load_txt("data/Luat to tung hanh chinh 2015.txt")

    indexing_data(luat_hinh_su, INDEX_NAME)
    indexing_data(luat_dan_su, INDEX_NAME)
    indexing_data(luat_hanh_chinh, INDEX_NAME)
    
    # law_docs = load_hf(
    #     dataset_name="iamnguyen/cdnc_law",
    #     split='luat',
    #     content_column='text',
    #     token=HF_TOKEN
    # )
    # indexing_data(law_docs, INDEX_NAME)