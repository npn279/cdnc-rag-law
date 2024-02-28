import sys
sys.path.append('')

import os 
import dotenv
dotenv.load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_EMBEDDING_MODEL_NAME = os.getenv('OPENAI_EMBEDDING_MODEL_NAME')

from openai import OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)


def get_emb(text: str):
    """
    Get embedding from OpenAI API
    """
    response = client.embeddings.create(
        input=text,
        model=OPENAI_EMBEDDING_MODEL_NAME
    )

    return response


if __name__ == '__main__':
    text = 'Hello World'
    emb = get_emb(text)
    print(emb)