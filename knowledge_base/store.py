from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import SQLiteVec


gemini_embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
connection = SQLiteVec.create_connection(db_file="../data/fix-wise.db")
vector_store = SQLiteVec(
    table="manual_kb",
    connection=connection,
    embedding=gemini_embeddings
)

