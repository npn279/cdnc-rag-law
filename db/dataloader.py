import sys
sys.path.append('')

import json
from datasets import load_dataset
from langchain.schema.document import Document


def load_hf(dataset_name: str,
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

