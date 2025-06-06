import os
from langchain_community.document_loaders import PyPDFLoader
from knowledge_base.store import get_vector_store

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = "AIzaSyBSFs4_X_-T3Ry49JeMMbBs6-LozKGNAIo"


def generate_embedding_data():

    loader = PyPDFLoader("../data/mannual.pdf")

    pages = []
    for page in loader.lazy_load():
        pages.append(page)
    get_vector_store().add_documents(pages)

# one-time script
if __name__ == '__main__':
    generate_embedding_data()
