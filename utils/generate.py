import sys
sys.path.append('')

import os
import dotenv
dotenv.load_dotenv()
CHAT_MODEL = os.getenv('CHAT_MODEL')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

from openai import OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

from utils.prompt_template import RESPONSE_PROMPT

def gen_response(query: str, stream=True, **kwargs):
    """
    input: 
        - question: str (question from user)
        - history: list of dict (history of conversation)
        ex: history = [
            {"question": ..., "answer": ...},
            {"question": ..., "answer": ...},
            {"question": ..., "answer": ...},
        ]
    """

    context = kwargs.get("context", "")
    history = kwargs.get("history", [])

    history_msg = []
    if len(history) != 0:
        history_msg = []
        for _history in history:
            history_msg.extend(
                [
                    {"role": "user", "content": _history["question"]},
                    {"role": "assistant", "content": _history["answer"]}
                ]
            )    

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {"role": "system", "content": RESPONSE_PROMPT},
            *history_msg,
            {"role": "user", "content": 
             f"""\nContext: {context}
             \nCâu hỏi: {query}
             \nTrả lời:
             """}
        ],
        temperature=0.0,
        stream=stream
    )

    return response