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
    except Exception as e:
        logging.error(f"GEN QUERIES: {e}")
        return [query]

def gen_answer(query: str, history = [], k: int = 5, rewrite: bool = True, search_method: str = "hybrid"):
    try:
        # --- Rewrite and Classify ---
        if rewrite:
            queries = [query]
            rewrite_response = gen_queries(query)
            logging.info(f"rewrite_response: {rewrite_response}")   

            if rewrite_response.strip().startswith("queries"):
                queries += rewrite_response.strip()[8:].split('\n')
            elif rewrite_response.strip().startswith("response"):
                return rewrite_response.strip()[8:]
        else:
            queries = [query]
        logging.info(f"queries: {queries}")

        # --- Get Context ---
        search_method = search_method.lower().strip()
        if queries:
            contexts = []
            if search_method == "hybrid":
                hb_doc_ids = []
                for sub_query in queries:
                    hb_results = es.hybrid_search(index_name=INDEX_NAME, query=sub_query, k=k)
                    hb_doc_ids.extend(hb_results)

                for id_ in list(set(hb_doc_ids)):
                    doc = es.get_doc_by_id(index_name=INDEX_NAME, id=id_)
                    contexts.append(doc['hits']['hits'][0]['_source']['content'])
            elif search_method in ["bm25", "vector"]:
                if search_method == "bm25":
                    doc_ids = []
                    for sub_query in queries:
                        bm25_results = es.bm25_search(index_name=INDEX_NAME, query=sub_query, k=k)
                        for hit in bm25_results['hits']['hits']:
                            if hit['_id'] not in doc_ids:
                                doc_ids.append(hit['_id'])
                                contexts.append(hit['_source']['content'])
                else:
                    doc_ids = []
                    for sub_query in queries:
                        vector_results = es.vector_search(index_name=INDEX_NAME, query=sub_query, k=k)
                        for hit in vector_results['hits']['hits']:
                            if hit['_id'] not in doc_ids:
                                doc_ids.append(hit['_id'])
                                contexts.append(hit['_source']['content'])
            else:
                contexts = []

            context = '\n\n'.join(contexts)
        else:
            context = ""

        logging.info(f"context: {context}")

        # --- Get Response ---
        prompt = """\
        # Context
        {context}
        # Question
        {query}
        # Answer
        """
        response = openai.get_response(prompt=prompt.format(context=context, query=query), system_prompt=ANSWER_TEMPLATE, stream=True)
        for r in response:
            yield r
        return
    except Exception as e:
        logging.error(f"GET RESPONSE: {e}")
        return "Xin lỗi, hiện tại tôi chưa thể trả lời câu hỏi này. Bạn có thể hỏi câu hỏi khác được không?", ""

def main():
    query = "quan hệ với người cùng dòng máu là gì và sẽ bị xử phạt như thế nào"
    # query = "xin chào, bạn là ai"
    response = gen_answer(query=query, search_method="hybrid")
    for r in response:
        print(r, end="", flush=True)
    print()

if __name__=="__main__":
    main()
