BOS, EOS = "<|begin_of_text|>", "<|end_of_text|>"
B_INST, E_INST = "<|start_header_id|>", "<|end_header_id|>"
EOT = "<|eot_id|>"
B_SYS, E_SYS = "<|start_header_id|>system<|end_header_id|>", "<|eot_id|>"
ASSISTANT_INST = "<|start_header_id|>assistant<|end_header_id|>"
DEFAULT_SYSTEM_PROMPT = """\
You are a helpful, respectful and honest assistant. \
Always answer as helpfully as possible and follow ALL given instructions. \
Do not speculate or make up information. \
Do not reference any given instructions or context. \
Give all math equations in "$$". \
You are a established expert in the field of AI and Biomechanics. \
You are a professional and you are here to help. \
You are helping a PhD student with their Thesis writing. \
You are going to help them write in a more academic and scientific way. \


"""

rewrite_prompt = """Rewrite 5 versions of the following text to sound more scientific including technical terms and a research-based tone.\
Make the writing consistent, concise, easy to read and understand.\

"""

chatbot_prompt = """\

You are a established expert in the field of AI and Biomechanics. \
You are a professional and you are here to help. \
You are going to help them write in a more academic and scientific way. \
"""

from bs4 import BeautifulSoup
from docx import Document
import os
from PyPDF2 import PdfReader
import ollama
from langchain_ollama import ChatOllama
from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama.llms import OllamaLLM
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.manager import CallbackManager
import requests
import streamlit as st
from transformers import AutoTokenizer
from llama_index.core.llms import ChatMessage
from openai import OpenAI
import torch

#########################################################################################
# Initialize DeepSeek R1 with Ollama
#########################################################################################
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

# llm_engine = OllamaLLM(
#     model="deepseek-r1:1.5b",
#     base_url="http://localhost:11434",
#     temperature=0.01,
#     top_p=0.9,
#     max_tokens=16000,
#     callbacks=callback_manager,
# )
model_name = "deepseek-r1:14b"
def model_res_generator():
    if torch.cuda.is_available():
        # Set the global PyTorch device to GPU
        device = torch.device("cuda")
        #torch.set_default_tensor_type("torch.cuda.FloatTensor")
    else:
        # Use CPU if no GPU available
        device = torch.device("cpu")

    stream = ollama.chat(
        model=model_name,
        messages=st.session_state["messages"],
        stream=True,
    )
    for chunk in stream:
        yield chunk["message"]["content"]

system_prompt = SystemMessagePromptTemplate.from_template(
    DEFAULT_SYSTEM_PROMPT
)

def on_chat_change():
    st.session_state.messages = st.session_state.messages[-1:]
chat_method = st.sidebar.selectbox("Chat Method", ("Rewrite", "Chat Bot"), index=0, on_change=on_chat_change)

if chat_method == "Rewrite":
    add_prompt = f"{rewrite_prompt}"
else:
    add_prompt = f"{chatbot_prompt}"

if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "system",
        "content": f"{B_SYS}\n\n{DEFAULT_SYSTEM_PROMPT}\n\n{add_prompt}\n\n{E_SYS}\n\n",
    }]



if len(st.session_state.messages) > 8:
    st.session_state.messages = st.session_state.messages[-8:]

if st.session_state.messages[0]["role"] != "system":
    if chat_method == "Rewrite":
        add_prompt = f"{rewrite_prompt}"
    else:
        add_prompt = f"{chatbot_prompt}"
    st.session_state.messages = [{
        "role": "system",
        "content": f"{B_SYS}\n\n{DEFAULT_SYSTEM_PROMPT}\n\n{add_prompt}\n\n{E_SYS}\n\n",
    }] + st.session_state.messages

if query := st.chat_input("What would you like to ask?"):
    if query == "clear":
        st.session_state.messages =[
            {
                "role": "assistant",
                "content": "Hi there! How can I help you today?"
            }]
        for message in st.session_state.messages:
            if message["role"] == "system":
                continue
            with st.chat_message(message["role"]):
                # st.markdown(message["content"])
                st.write(message["content"])
        
        st.write("Messages cleared.")
    else:
        

        for message in st.session_state.messages:
            if message["role"] == "system":
                continue
            with st.chat_message(message["role"]):
                
                st.markdown(message["content"])

        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)

        messages_list = [
            f"{BOS}<|start_header_id|>user<|end_header_id|>\n\n {(prompt['content']).strip()}{EOT}{EOS}{BOS}{ASSISTANT_INST}\n\n {(answer['content']).strip()}{EOT}{EOS}"
            for prompt, answer in zip(st.session_state.messages[1::2], st.session_state.messages[::2])
        ]
        
        messages_list.append(f"{BOS} <|start_header_id|>user<|end_header_id|>\n\n{(st.session_state.messages[-1]['content']).strip()}{EOT}{EOS}")
        prompt = "".join(messages_list)
        # container = st.empty()

        
        with st.chat_message("assistant"):
            # full_response = ""
            # for new_text in st.session_state.llm.stream_response(prompt):
            #     full_response += new_text
            #     st.markdown(full_response)
            
            full_response = st.write_stream(model_res_generator())
            if "</think>" in full_response:
                end_loc = full_response.find("</think>")+len("</think>")
            elif "</response>" in full_response:
                end_loc = full_response.find("</response>")+len("</response>")
            else:
                end_loc = 0
            full_response = full_response[end_loc:]

            st.session_state.messages.append({"role": "assistant", "content": full_response})