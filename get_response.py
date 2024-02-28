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


def get_response(query: str, history = [], k: int = 5):
    try:
        """
        input:
            query: str
            history: list
                example: [{"role": "user", "parts": ["hi"]}, {"role": "model", "parts": ["Hello"]}]
            k: number of queries to be rewritten
        output:
            response: str
        """
        # --- Rewrite and Classify ---
        default_answer = "Xin lỗi, hiện tại tôi chưa thể trả lời câu hỏi này. Bạn có thể hỏi câu hỏi khác được không?"

        rewrite_prompt = """Original question: {query}\nQueries:\n"""
        queries = [query]
        rewrite_response = openai.get_response(prompt=rewrite_prompt, system_prompt=REWRITE_TEMPLATE, stream=False)
        rewrite_response = next(rewrite_response)
        if rewrite_response:
            queries = queries + rewrite_response.split('\n')
        logging.info(f"queries: {queries}")

        if queries:
            contexts = []
            hb_doc_ids = []
            for sub_query in queries:
                hb_results = es.hybrid_search(index_name=INDEX_NAME, query=query, k=k)
                hb_doc_ids.extend(hb_results)

            for id_ in list(set(hb_doc_ids)):
                doc = es.get_doc_by_id(index_name=INDEX_NAME, id=id_)
                contexts.append(doc['hits']['hits'][0]['_source']['content'])
            
            context = '\n\n'.join(contexts)
        else:
            context = ""

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

    except Exception as e:
        logging.error(f"GET RESPONSE: {e}")
        return "Xin lỗi, hiện tại tôi chưa thể trả lời câu hỏi này. Bạn có thể hỏi câu hỏi khác được không?", ""

def main():
    # query = "Tiền lương thử việc của người lao động được quy định như thế nào"
    # history = [
    #      {"role": "user", "parts": ["Chào bạn"]},
    #      {"role": "model", "parts": ["Xin chào, tôi là Lawie. \nTôi là hệ thống hỗ trợ hỏi đáp pháp luật."]}
    # ]
    # query = "Trong trường hợp nào thì có thể khởi tố, điều tra, truy tố, xét xử đối với người mà hành vi của họ đã có bản án của Tòa án đã có hiệu lực pháp luật?"
    # query = "Ai là luật sư đầu tiên trên thế giới"
    query = "Tiền lương thử việc của người lao động được quy định như thế nào"
    response = get_response(query=query)
    for r in response:
        print(r, end="", flush=True)

if __name__=="__main__":
    main()
