import os
import dotenv
dotenv.load_dotenv()

from utils.generate import gen_response
from retrieval.hybrid_search import hybrid_search

INDEX_NAME = os.getenv('INDEX_NAME')


def get_response(query: str, history = None, k: int = 5):
    hb_results = hybrid_search(index_name=INDEX_NAME, query=query, k=k)
    if len(hb_results) > k:
        hb_results = hb_results[:k]

    context = '\n\n'.join([result['content'] for result in hb_results])
    response = gen_response(query=query, context=context, history=history)

    for chunk in response:
        chunk_message = chunk.choices[0].delta.content
        yield chunk_message if chunk_message != None else "\n"

def main():
    history = []
    while True:
        query = input("Enter your question: ")
        if query.strip() == "exit":
            break

        answer = ""
        for chunk in get_response(query, history=history, k=5):
            print(chunk, end="", flush=True)
            answer += chunk
        
        history.append({"question": query, "answer": answer})

if __name__=="__main__":
    main()
