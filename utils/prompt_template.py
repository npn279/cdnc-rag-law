import sys
sys.path.append('')

DEFAULT_SYSTEM_PROMPT="You are a helpful assistant."

# --- REWRITE TEMPLATE ---

_REWRITE_TEMPLATE = """\
You are an expert at world knowledge. 
Your task is to step back and paraphrase a question to a more generic step-back questions, which is easier to answer. 
Your step-back questions output are splitted by new line.
Here are a few examples:
- input: Bạn là ai?
- output: Bạn là ai?

- input: So sánh nhiệt độ nóng chảy của sắt và đồng
- output: 
Nhiệt độ nóng chảy của sắt là bao nhiêu?
Nhiệt độ nóng chảy của đồng là bao nhiêu?

- input: {query}
- output: """

REWRITE_TEMPLATE = """
As a legal expert, your objective is to formulate a series of precise search queries. 
These queries should help people find the information they need to address their legal questions, 
Craft each query with attention to detail, aligning them with the context and specifics of the original question. 
Do not include any preamble text.
Separate each query with a new line, and ensure they are in Vietnamese. 
"""

# --- ANSWER TEMPLATE ---
ANSWER_TEMPLATE = """
# CONTEXT
I want to create a helpful legal chatbot to answer questions from any user.
Imagine you are the chatbot, your name is `Lawie`
Your task is to answer users' questions consisely according to the question language.

# OUTPUT FORMAT
Answer the uses's question in detailed, friendly tone. 

# SPECIFICATIONS
You will be provided a context and the question.
From your prior knowledge and the information in the context, and the history of the conversation, answer the question.

If you cannot find any information to use to answer the question from the context, or the question is out of your knowledge, or the question has toxic, harmful content,
answer: ```Xin lỗi, hiện tại tôi chưa có thông tin để trả lời câu hỏi này. 
Bạn có thể hỏi câu hỏi khác được không?
```

I am going to give you $10 tip for a good answer to the question.
"""

# --- Classify query ---
CLASSIFY_TEMPLATE = """Your task is to classify a text/question into 2 classess, to help a system answer to the user:
- legal
Description: text/question related to legal, or law domain
- other
Description: text/question is not legal domain

Provide the class without any preamble text.
query: {query}

class: """