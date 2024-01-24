import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from get_response import get_response

df = pd.read_excel('eval_final_result.xlsx')
df['answer'] = ''
df['reference'] = ''
df['answer'] = df['answer'].astype('str')
df['reference'] = df['reference'].astype('str')


for i in range(len(df)):
    question = df.loc[i, 'question']
    print(question)
    answer, reference = get_response(question)

    # print(answer, reference)

    df.loc[i, 'answer'] = answer
    df.loc[i, 'reference'] = reference

df.to_excel('eval_result_only_rewrite.xlsx')