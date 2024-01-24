import os
import dotenv
dotenv.load_dotenv()

import time
from pprint import pprint

from utils.prompt_template import *
from db.elastic_search import ElasticSearch
from LLM.GEMINI import GEMINI

es = ElasticSearch()
gemini = GEMINI()
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
        rewrite_response = gemini.generate(prompt=REWRITE_TEMPLATE.format(query=query), temperature=0.4)
        queries = None
        if rewrite_response:
            if "content" in rewrite_response.candidates[0]:
                print(rewrite_response.text)
                if rewrite_response.text.strip().lower() == "no":
                    queries = None
                else:
                    queries = rewrite_response.text.strip().split('\n')
                    queries.append(query)
        
        
        # cls_response = gemini.generate(prompt=CLASSIFY_TEMPLATE.format(query=query), temperature=0.4)
        # query_class = None
        # if cls_response:
        #     if "content" in cls_response.candidates[0]:
        #         if cls_response.text.strip().lower() == "legal":
        #             query_class = "legal"

        # if query_class == "legal":           
        #     queries = [query]
        # else:
        #     queries = None

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

        prompt = ANSWER_TEMPLATE.format(context=context, query=query)
        print(prompt)
        response = gemini.generate(prompt=prompt, temperature=0.4)

        answer = default_answer
        if response:
            if 'content' in response.candidates[0]:
                answer = response.text
        return answer, context

    except Exception as e:
        print(e)
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
    s_time = time.time()
    response = get_response(query=query)
    print(response[0])
    print("-----")
    print(response[1])
    e_time = time.time()
    print("Response time: ", e_time - s_time)

if __name__=="__main__":
    main()
