import os
import streamlit as st
from dotenv import load_dotenv
from ollama import Client

load_dotenv()

API_KEY = os.getenv("OLLAMA_API_KEY")
MODEL_NAME = os.getenv("OLLAMA_MODEL")

client = Client(
    host = "https://ollama.com",
    headers={
        "Authorization": f"Bearer {API_KEY}"
    }
)

st.title("Raj's vediX")

if "messages" not in st.session_state:
    st.session_state.messages = []  

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Enter your prompt here...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant"):
        response_container = st.empty()
        full_response = ""

        for chunk in client.chat(
            model=MODEL_NAME, 
            messages=[{"role": "user", "content": prompt}],
            stream=True
        ):
            token = chunk["message"]["content"]
            full_response += token
            response_container.markdown(full_response + "▌")  # Show typing indicator  
        
        st.session_state.messages.append(
            {"role": "assistant", "content": full_response}
            )

