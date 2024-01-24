import sys
sys.path.append("")

import os
from dotenv import load_dotenv
load_dotenv()

from llama_index import VectorStoreIndex
from llama_index.llms import OpenAI
from llama_index.storage.storage_context import StorageContext
from llama_index.service_context import ServiceContext
from llama_index.vector_stores import ElasticsearchStore
from llama_index.node_parser import LangchainNodeParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from db.dataloader import *

# ENVS
INDEX_NAME = os.getenv("INDEX_NAME")
HF_TOKEN = os.getenv("HF_TOKEN")

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
    law_docs = load_hf(
        dataset_name="iamnguyen/cdnc_law",
        split='luat',
        content_column='text',
        token=HF_TOKEN
    )
    indexing_data(law_docs, INDEX_NAME)