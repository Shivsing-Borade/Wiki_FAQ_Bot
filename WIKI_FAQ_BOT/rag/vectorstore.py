import streamlit as st

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS


@st.cache_resource
def create_vector_store(docs, embeddings):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = text_splitter.split_documents(docs)

    vector_store = FAISS.from_documents(
        chunks,
        embeddings
    )

    return vector_store