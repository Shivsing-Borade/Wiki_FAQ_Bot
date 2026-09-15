from langchain_huggingface import HuggingFaceEmbeddings
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
import streamlit as st


load_dotenv()


@st.cache_resource
def load_models():

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    llm = HuggingFaceEndpoint(
        repo_id="deepseek-ai/DeepSeek-V4-Flash-0731",
        task="text-generation",
        max_new_tokens=512,
        temperature=0.2
    )

    chat_model = ChatHuggingFace(llm=llm)

    return embeddings, chat_model