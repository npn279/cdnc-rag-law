import os
import dotenv
dotenv.load_dotenv()

from db.elastic_search import ElasticSearch
es = ElasticSearch()

from LLM.GEMINI import GEMINI
gemini = GEMINI()

from utils.prompt_template import *

INDEX_NAME = os.getenv('INDEX_NAME')


def get_response(query: str, history = [], k: int = 5):
    # try:
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
        rewrite_response = gemini.generate(prompt=REWRITE_TEMPLATE.format(query=query), temperature=0.3)
        queries = None
        default_answer = "Xin lỗi, hiện tại tôi chưa thể trả lời câu hỏi này. Bạn có thể hỏi câu hỏi khác được không?"
        if rewrite_response:
            if rewrite_response.candidates[0].content:
                print(rewrite_response.text)
                if rewrite_response.text.strip().lower() == "no":
                    queries = None
                else:
                    queries = rewrite_response.text.strip().split('\n')
                    queries = [query.strip() for query in queries]
                    queries = [query for query in queries if query]
                    queries.append(query)

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
        response = gemini.generate(prompt=prompt)

        answer = default_answer
        if response:
            if response.candidates[0].content:
                return response.text

    # except Exception as e:
    #     print(e)
    #     return "Xin lỗi, hiện tại tôi chưa thể trả lời câu hỏi này!"

def main():
    # query = "Tiền lương thử việc của người lao động được quy định như thế nào"
    # history = [
    #      {"role": "user", "parts": ["Chào bạn"]},
    #      {"role": "model", "parts": ["Xin chào, tôi là Lawie. \nTôi là hệ thống hỗ trợ hỏi đáp pháp luật."]}
    # ]
    # query = "chào bạn, tôi là Nguyên, tôi cần tìm thông tin luật hình sự"
    # query = "Ai là luật sư đầu tiên trên thế giới"
    query = "Tiền lương thử việc của người lao động được quy định như thế nào"

    response = get_response(query=query)
    print(response)

if __name__=="__main__":
    main()
