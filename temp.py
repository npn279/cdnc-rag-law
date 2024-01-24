from LLM.GEMINI import GEMINI
gemini = GEMINI()

from utils.prompt_template import *

query = "chạy xe đụng chết người bị phạt bao nhiêu tiền"
rewrite_response = gemini.generate(prompt=REWRITE_TEMPLATE.format(query=query), temperature=0.4)
print(rewrite_response.candidates)