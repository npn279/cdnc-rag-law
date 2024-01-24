import sys
sys.path.append('')

import os 
import dotenv
dotenv.load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
EMB_MODEL = os.getenv('EMB_MODEL')

from openai import OpenAI
client = OpenAI()


def get_emb(text: str):
    """
    Get embedding from OpenAI API
    """
    response = client.embeddings.create(
        input=text,
        model=EMB_MODEL
    )

    return response


if __name__ == '__main__':
    text = 'Hello World'
    emb = get_emb(text)
    print(emb)