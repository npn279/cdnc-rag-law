import sys
sys.path.append('')

import json
import logging
from datasets import load_dataset
from llama_index.core import Document

def _load_hf(dataset_name: str,
            split: str,
            content_column: str,
            token: str):
    """
    Load dataset from HuggingFace Datasets
    """

    ds = load_dataset(dataset_name, split=split, token=token)
    columns = ds.column_names
    metadata_columns = [c for c in columns if c != content_column]

    documents = []
    for i, doc in enumerate(ds):
        documents.append(Document(page_content=doc[content_column], metadata={k: doc[k] for k in metadata_columns}))

    return documents

def load_hf(dataset_name: str, split='train', content_column='content', token: str = None):
    try:
        dataset = load_dataset(dataset_name, split=split, token=token)
        # print(dataset)
        columns = dataset.column_names
        
        if content_column not in columns:
            raise Exception(f"Column {content_column} not in dataset {dataset_name}")
        
        metadata_columns = [c for c in columns if c != content_column]
        documents = [Document(text=d[content_column], metadata={c: d[c] for c in metadata_columns}, doc_id=dataset_name) for d in dataset]

        return documents
    except Exception as e:
        logging.error(f"LOAD HF: {e}")
        return []
    
def load_txt(file_path):
    try:
        with open(file_path, "r", encoding="utf8") as f:
            texts = f.read()

        return [Document(text=texts, metadata={}, doc_id=file_path)]
    except Exception as e:
        logging.error(f"LOAD TXT: {e}")
        return []

        

