import os
import dotenv
dotenv.load_dotenv()

import time
from pprint import pprint
import logging
logging.basicConfig(level=logging.INFO)

from utils.prompt_template import *
from db.elastic_search import ElasticSearch
from LLM.GEMINI import GEMINI
from LLM.OPENAI import OPENAI

es = ElasticSearch()
gemini = GEMINI()
openai = OPENAI(api_key=os.getenv('OPENAI_API_KEY'))
INDEX_NAME = os.getenv('INDEX_NAME')


def gen_queries(query):
    try:
        rewrite_prompt = """User (Original question): {query}\nLawie:"""
        queries = [query]
        rewrite_response = openai.get_response(prompt=rewrite_prompt.format(query=query), system_prompt=REWRITE_TEMPLATE, stream=False)
        rewrite_response = next(rewrite_response)
        return rewrite_response
        # if rewrite_response:
        #     queries = queries + rewrite_response.split('\n')
        # return queries
    except Exception as e:
        logging.error(f"GEN QUERIES: {e}")
        return [query]
    

rewrite_response = gen_queries("quan hệ với người cùng dòng máu là gì và sẽ bị xử phạt như thế nào")
print(rewrite_response)