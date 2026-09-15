
from langchain_community.document_loaders import WebBaseLoader


def load_wikipedia(url):
    try:
       loader = WebBaseLoader(url)

       docs = loader.load()

       return docs
    except Exception as e:
        print("Wikipedia loading error:", e)
        return []