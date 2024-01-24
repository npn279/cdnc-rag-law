import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import json
import time
import openai 
import streamlit as st

from get_response import get_response

# --- Functions ---	
def new_chat():
	st.session_state.messages = [
         {"role": "assistant", "parts": ["Xin chào, tôi là Lawie. \nTôi là hệ thống hỗ trợ hỏi đáp pháp luật."]}
    ]

def on_button_click(conversation):
    st.write(f"You clicked: {conversation}")
	

# --- Web App ---
st.set_page_config(page_title="Lawie")
st.title("💬 Lawie")

# --- sidebar ---
# Button new chat
with st.sidebar:
	st.write("# 🤖 Lawie")
	st.divider()
	
	btn_new_chat = st.button("New Chat", on_click=new_chat, use_container_width=True)

	st.divider()
	st.write("# Members")
	st.write("👨‍💻 Nguyễn Phước Nguyên - 52000241")
	st.write("👨‍💻 Võ Hữu Trí - 52000288")

# --- Chat ---
if 'messages' not in st.session_state:
	st.session_state.messages = [
         {"role": "assistant", "parts": ["Xin chào, tôi là Lawie. \nTôi là hệ thống hỗ trợ hỏi đáp pháp luật."]}
    ]

for msg in st.session_state.messages:
	with st.chat_message(msg["role"]):
		st.write(msg['parts'][0])

if prompt := st.chat_input("Enter your question here"):
	st.session_state.messages.append({"role": "user", "parts": [prompt]})
	with st.chat_message("user"):
		st.write(prompt)

if st.session_state.messages[-1]['role'] == "user":
	with st.chat_message("assistant"):
		response = get_response(prompt)
		st.write(response)
	message = {"role": "model", "parts": [response]}
	st.session_state.messages.append(message)