import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import dotenv
dotenv.load_dotenv()

import google.generativeai as genai 
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')



class GEMINI:
    def __init__(self, api_key=GEMINI_API_KEY):
        genai.configure(api_key=api_key)

    def generate(self, prompt, model_name="gemini-pro", **kwargs):
        try:
            stream = kwargs.get("stream", False)
            temperature = kwargs.get("temperature", 0.9)
            top_k = kwargs.get("top_k", 1)
            top_p = kwargs.get("top_p", 1)
            max_output_tokens = kwargs.get("max_output_tokens", 2048)

            generation_config = {
                "temperature": temperature,
                "top_p": top_p,
                "top_k": top_k,
                "max_output_tokens": max_output_tokens,
            }

            safety_settings = [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
            ]

            model = genai.GenerativeModel(model_name=model_name,
                                        generation_config=generation_config,
                                        safety_settings=safety_settings)
            prompt_parts = [prompt]
            response = model.generate_content(prompt_parts, stream=stream)
            return response
        except:
            print("Exception in GEMINI.generate()")
            return None
        
    def chat(self, prompt, model_name="gemini-pro", **kwargs):
        # try:
            stream = kwargs.get("stream", False)
            temperature = kwargs.get("temperature", 0.9)
            top_k = kwargs.get("top_k", 1)
            top_p = kwargs.get("top_p", 1)
            max_output_tokens = kwargs.get("max_output_tokens", 2048)  
            history = kwargs.get("history", []) # format: [{"role": "user", "parts": ["hi"]}, {"role": "model", "parts": ["Hello"]}]

            generation_config = {
                "temperature": temperature,
                "top_p": top_p,
                "top_k": top_k,
                "max_output_tokens": max_output_tokens,
            }

            safety_settings = [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
            ]

            model = genai.GenerativeModel(model_name=model_name,
                                        generation_config=generation_config,
                                        safety_settings=safety_settings)

            convo = model.start_chat(history=history)
            response = convo.send_message(prompt, stream=stream)
            print(convo.last.text)
            return response
        # except:
        #     print("Exception in GEMINI.chat()")
        #     return None