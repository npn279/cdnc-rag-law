import logging
logging.basicConfig(level=logging.INFO)

from LLM.OPENAI import get_response
from utils.prompt_template import *

prompt = """
Original question: Đi ngược chiều bị phạt bao nhiêu tiền?
Queries:

"""

response = get_response(prompt=prompt, stream=True, system_prompt=REWRITE_TEMPLATE)
# print(response)
for r in response:
    print(r, end="", flush=True)