import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from get_response import gen_answer

df = pd.read_excel('data/test/Data Test Final.xlsx', sheet_name='all_question')
df['answer'] = ''
df['reference'] = ''
df['answer'] = df['answer'].astype('str')
df['reference'] = df['reference'].astype('str')

for i in range(len(df)):
    question = df.loc[i, 'question']
    print(question)
    response = gen_answer(question, search_method='hybrid', rewrite=False, stream=False, return_context=True)
    answer, reference = '', ''
    for r in response:
        if r.strip().startswith("<REFERENCE>") and r.strip().endswith("</REFERENCE>"):
            reference = r.strip()[11:-12]
        else:
            answer += r
    df.loc[i, 'answer'] = answer
    df.loc[i, 'reference'] = reference

df.to_excel('data/test/results/norewrite_hybrid.xlsx')