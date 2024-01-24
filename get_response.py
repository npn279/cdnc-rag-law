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
        hb_results = es.hybrid_search(index_name=INDEX_NAME, query=query, k=k)
        hb_results = list(set(hb_results))
        contexts = []
        for id_ in hb_results:
            doc = es.get_doc_by_id(index_name=INDEX_NAME, id=id_)
            contexts.append(doc['hits']['hits'][0]['_source']['content'])
        

        context = '\n\n'.join(contexts)
        prompt = ANSWER_TEMPLATE.format(context=context, query=query)
        print(prompt)
        response = gemini.generate(prompt=prompt)

        if response:
            if response.candidates[0].content:
                return response.text
            else:
                return "Xin lỗi, hiện tại tôi chưa thể trả lời câu hỏi này!"
        else:
            return "Xin lỗi, hiện tại tôi chưa thể trả lời câu hỏi này!"

    # except Exception as e:
    #     print(e)
    #     return "Xin lỗi, hiện tại tôi chưa thể trả lời câu hỏi này!"

def main():
    # query = "Tiền lương thử việc của người lao động được quy định như thế nào"
    history = [
         {"role": "user", "parts": ["Chào bạn"]},
         {"role": "model", "parts": ["Xin chào, tôi là Lawie. \nTôi là hệ thống hỗ trợ hỏi đáp pháp luật."]}
    ]
    query = "chào bạn, tôi là Nguyên, tôi cần tìm thông tin luật hình sự"

    response = get_response(query=query, history=history)
    print(response)

if __name__=="__main__":
    main()
