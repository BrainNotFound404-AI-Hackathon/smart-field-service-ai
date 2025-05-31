import os

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import SQLiteVec
from langchain_community.document_loaders import PyPDFLoader

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = "AIzaSyBSFs4_X_-T3Ry49JeMMbBs6-LozKGNAIo"


def generate_embedding_data():
    gemini_embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    connection = SQLiteVec.create_connection(db_file="../data/fix-wise.db")
    vector_store = SQLiteVec(
        table="manual_kb",
        connection=connection,
        embedding=gemini_embeddings
    )

    loader = PyPDFLoader("../data/mannual.pdf")

    pages = []
    for page in loader.lazy_load():
        pages.append(page)
    vector_store.add_documents(pages)

# one-time script
if __name__ == '__main__':
    generate_embedding_data()
