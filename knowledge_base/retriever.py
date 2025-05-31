from typing import List

from dotenv import load_dotenv
from store import vector_store

load_dotenv()


"""similarity search from embedding table"""
def retrieve_by_message(message: str) -> List[str]:
    retriever = vector_store.as_retriever()
    docs = retriever.invoke(message)
    return [doc.page_content for doc in docs]



