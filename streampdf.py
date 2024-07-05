# -*- coding: utf-8 -*-
"""
Created on Mar 15

@author: Oyasi

@app: v0.8
"""

#prerequisite pip install htbuilder
# pip3 install streamlit-extras
# change Loader 
# change input 

import logging
import sys
import time
from typing import Optional
import requests
import streamlit as st


## adding the library to upload and use document
from dotenv import load_dotenv
import os


## adding the library to use html format
from htbuilder import HtmlElement, div, ul, li, br, hr, a, p, img, styles, classes, fonts
from htbuilder.units import percent, px
from htbuilder.funcs import rgba, rgb


## adding the library to use sidebar
from streamlit_extras.add_vertical_space import add_vertical_space



log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(format=log_format, stream=sys.stdout, level=logging.INFO)

BASE_API_URL = "http://127.0.0.1:7860/api/v1/process"
FLOW_ID = "4087790a-77d8-440e-b5d1-15e6632ba664"


TWEAKS = {
  "Data-hSdBW": {},
  "OpenAIEmbeddings-1URfp": {},
  "ChatOpenAI-6K4YY": {},
  "CombineDocsChain-uiaIC": {},
  "RetrievalQA-zwK4k": {},
  "Chroma-lZLUr": {},
  "Data-wpM9G": {}
}


load_dotenv()

def run_flow(inputs: dict, flow_id: str, tweaks: Optional[dict] = None) -> dict:
    api_url = f"{BASE_API_URL}/{flow_id}"
    payload = {"inputs": inputs}
    if tweaks:
        payload["tweaks"] = tweaks
    response = requests.post(api_url, json=payload)
    return response.json()

def generate_response(query, filepath):
    logging.info(f"input: {query}, file_path={filepath}")
    inputs = {"query": query, "file_path": filepath}

    response = run_flow(inputs, flow_id=FLOW_ID, tweaks=TWEAKS)
    
    try:
        result = response.get('outputs', {})
        if 'text' in result:
            logging.info(f"answer: {result['text']}")
            return result['text']
        elif 'response' in result:
            logging.info(f"answer: {result['response']}")
            return result['response']
        elif 'result' in result: 
            logging.info(f"answer: {result['result']}")
        else:
            logging.error(f"Unexpected response format: {response}")
            return "Sorry, there was a problem finding an answer for you."
    except Exception as exc:
        logging.error(f"error: {response}")
        return "Sorry, there was a problem finding an answer for you."
    



# Sidebar contents
with st.sidebar:
    st.title('🤗💬 MSF ChatBot')
    st.markdown('''
    ## Upload your files here
                
    ''')


    # Upload a PDF file
    file = st.file_uploader("Upload your file", type=None, accept_multiple_files=True)

    filepaths = []
    
    if file:
        for file in filepaths:
            with open(file.name, "wb") as f:
                f.write(file.getbuffer())
            filepaths.append(file.name)

        st.info("Files uploaded successfully!")
        TWEAKS["Data-wpM9G"]["file_path"] = [os.path.abspath(filepath) for filepath in filepaths]
    else:
        st.warning("Please upload valid files.")



# main chatbox
def main(): 


    st.markdown("##### Multimodal Chat App powered by 🚀 Langflow")


    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=message["avatar"]):
            st.write(message["content"])

    if query := st.chat_input("Ask me anything..."):
        st.session_state.messages.append(
            {
                "role": "user",
                "content": query,
                "avatar": "💬",  # Emoji representation for user
            }
        )
        with st.chat_message(
            "user",
            avatar="💬",  # Emoji representation for user
        ):
            st.write(query)

        with st.chat_message(
            "assistant",
            avatar="🤖",  # Emoji representation for assistant
        ):
            message_placeholder = st.empty()
            with st.spinner(text="Thinking..."):
                assistant_response = generate_response(query, filepaths)
                message_placeholder.write(assistant_response)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": assistant_response,
                "avatar": "🤖",  # Emoji representation for assistant
            }
        )




### ---------------------------------------- Footer ---------------------------------------- ###

def image(src_as_string, **style):
    return img(src=src_as_string, style=styles(**style))


def link(link, text, **style):
    return a(_href=link, _target="_blank", style=styles(**style))(text)


def layout(*args):

    style = """
    <style>
      # MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
     .stApp { bottom: 105px; }
    </style>
    """

    style_div = styles(
        position="fixed",
        left=0,
        bottom=0,
        margin=px(0, 0, 0, 0),
        width=percent(100),
        color="black",
        text_align="center",
        height="auto",
        opacity=1
    )

    style_hr = styles(
        display="block",
        margin=px(4, 4, "auto", "auto"),
        border_style="inset",
        border_width=px(2)
    )

    body = p()
    foot = div(
        style=style_div
    )(
        hr(
            style=style_hr
        ),
        body
    )

    st.markdown(style, unsafe_allow_html=True)

    for arg in args:
        if isinstance(arg, str):
            body(arg)

        elif isinstance(arg, HtmlElement):
            body(arg)

    st.markdown(str(foot), unsafe_allow_html=True)


def footer():
    myargs = [
        "Made in ",
        image('https://avatars3.githubusercontent.com/u/45109972?s=400&v=4',
              width=px(25), height=px(25)),
        " with ❤️ by ",
        link("https://www.linkedin.com/in/oyasizakiananta/", "@Oyasi"),
    ]
    layout(*myargs)
### ---------------------------------------- Footer ---------------------------------------- ###


if __name__ == "__main__":
    main() ## main function execution 
    footer() ## footer call execution
