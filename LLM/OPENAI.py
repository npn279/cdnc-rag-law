import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import logging
from openai import OpenAI


class OPENAI:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def get_response(self, prompt, **kwargs):
        try:
            temperature = kwargs.get('temperature', 0)
            max_tokens = kwargs.get('max_tokens', 4000)
            stream = kwargs.get('stream', False)
            history = kwargs.get('history', [])
            system_prompt = kwargs.get('system_prompt', "You are a helpful assistant.")
            model = kwargs.get('model', "gpt-3.5-turbo-0125")

            completion = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    *history,
                    {"role": "user", "content": prompt},
                ],
                temperature=temperature,
                max_tokens=max_tokens,
                stream=stream,
            )

            if stream:
                for chunk in completion:
                    yield chunk.choices[0].delta.content or ""
                return 
            else:
                yield completion.choices[0].message.content 
                return
        except Exception as e:
            logging.error(e)
            yield None
            return