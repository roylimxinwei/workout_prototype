import streamlit as st
from utils.auth_utils import require_login
from langchain_openai.chat_models import ChatOpenAI

st.title("Fitness AI Assistant")
st.info("This page is still under development. ")

openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")


def generate_response(input_text):
    model = ChatOpenAI(temperature=0.7, api_key=openai_api_key)
    st.info(model.invoke(input_text))

@ require_login
def ask_ai():
    with st.form("my_form"):
        text = st.text_area(
            "Enter text:",
            "How much calories should I eat to maintain my weight?",
        )
        submitted = st.form_submit_button("Submit")
        if not openai_api_key.startswith("sk-"):
            st.warning("Please enter your OpenAI API key!", icon="⚠")
        if submitted and openai_api_key.startswith("sk-"):
            generate_response(text)

ask_ai()