from fastapi import APIRouter
from fastapi.responses import JSONResponse
from typing import Dict, List, Optional, Literal
from uuid import uuid4
import json
import os
from dotenv import load_dotenv

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, BaseMessage
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field

load_dotenv()

router = APIRouter()

class Message(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str

class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    messages: List[Message]

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个训练有素的中文 AI 助手，请专注回答用户问题，不要自作扩展或解释。"),
    MessagesPlaceholder(variable_name="messages"),
    ("user", "{input}")
])

chain = prompt | llm | StrOutputParser()

store: Dict[str, ConversationBufferMemory] = {}

def get_memory_by_session(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ConversationBufferMemory(return_messages=True)
    return store[session_id].chat_memory

chat_with_memory = RunnableWithMessageHistory(
    chain,
    get_memory_by_session,
    input_messages_key="input",
    history_messages_key="messages",
)

def convert_messages(messages: List[Message]) -> List[BaseMessage]:
    result = []
    for msg in messages:
        if msg.role == "user":
            result.append(HumanMessage(content=msg.content))
        elif msg.role == "system":
            result.append(SystemMessage(content=msg.content))
        elif msg.role == "assistant":
            result.append(AIMessage(content=msg.content))
    return result

@router.post("/lang_chat", tags=["Chat"], summary="LangChain Chat Interface")
def lang_chat(request: ChatRequest):
    session_id = request.session_id or str(uuid4())

    last_user_input = next((msg.content for msg in reversed(request.messages) if msg.role == "user"), None)
    if last_user_input is None:
        return JSONResponse(status_code=400, content={"error": "No user input found."})

    print(f"Session ID: {session_id}, Last User Input: {last_user_input}")
    print("Messages received:", request.messages)
    try:
        response = chat_with_memory.invoke(
            {"input": last_user_input},
            config={"configurable": {"session_id": session_id}}
        )
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

    print("Response received:", response)

    return JSONResponse(content={"response": response, "session_id": session_id})


