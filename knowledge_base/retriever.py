from typing import List
from knowledge_base.store import get_retriever

def retrieve_by_message(message: str) -> List[str]:
    """
    根据消息从知识库中检索相关内容
    
    Args:
        message (str): 查询消息
        
    Returns:
        List[str]: 检索到的相关内容列表
    """
    retriever = get_retriever()
    docs = retriever.invoke(message)
    return [doc.page_content for doc in docs]



