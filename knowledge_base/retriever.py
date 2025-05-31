from typing import List
from knowledge_base.store import get_retriever

def retrieve_by_message(message: str) -> List[str]:
    """
    search related content from knowledge base according to the message
    
    Args:
        message (str): search message
        
    Returns:
        List[str]: related content lists that are searched
    """
    retriever = get_retriever()
    docs = retriever.invoke(message)
    return [doc.page_content for doc in docs]



