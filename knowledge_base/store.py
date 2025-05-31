from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import SQLiteVec
import sqlite3
import sqlite_vec
from dotenv import load_dotenv

load_dotenv()


def get_vector_store():
    gemini_embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    connection = sqlite3.connect("../data/fix-wise.db", check_same_thread=False)
    connection.row_factory = sqlite3.Row
    connection.enable_load_extension(True)
    sqlite_vec.load(connection)
    connection.enable_load_extension(False)

    vector_store = SQLiteVec(
        table="manual_kb",
        connection=connection,
        embedding=gemini_embeddings
    )
    return vector_store


def get_retriever():
    return get_vector_store().as_retriever()

