from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from typing import Dict, List, Optional, Literal, AsyncGenerator
from uuid import uuid4
from dotenv import load_dotenv

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, BaseMessage
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI
from server.api.utils import ChatRequest, Message, convert_all_messages
from fastapi.responses import JSONResponse

load_dotenv()

router = APIRouter()



llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a professional elevator maintenance AI assistant. Your role is to provide accurate and concise answers about elevator maintenance, troubleshooting, and safety procedures. Focus on answering questions directly without unnecessary elaboration. Use technical terminology appropriately and maintain a professional tone."),
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



async def stream_chat_response(chain, input_text: str, session_id: str) -> AsyncGenerator[str, None]:
    """
    流式生成聊天响应

    Args:
        chain: LangChain 链
        input_text: 用户输入
        session_id: 会话ID

    Yields:
        str: 流式响应片段
    """
    try:
        async for chunk in chain.astream(
            {"input": input_text},
            config={"configurable": {"session_id": session_id}}
        ):
            if chunk:
                yield chunk
    except Exception as e:
        raise e


@router.post("/lang_chat_stream", tags=["Chat"], summary="LangChain Chat Interface")
async def lang_chat(request: ChatRequest):
    session_id = request.session_id or str(uuid4())
    last_user_input = request.message

    print(f"Session ID: {session_id}, Last User Input: {last_user_input}")

    return StreamingResponse(
        stream_chat_response(chat_with_memory, last_user_input, session_id),
        media_type="text/event-stream"
    )

@router.post("/lang_chat", tags=["Chat"], summary="Chat Interface")
def lang_chat(request: ChatRequest):
    session_id = request.session_id or str(uuid4())

    last_user_input = next((msg.content for msg in reversed(request.messages) if msg.role == "user"), None)
    if last_user_input is None:
        return JSONResponse(status_code=400, content={"error": "No user input found."})

    try:
        response = chat_with_memory.invoke(
            {"input": last_user_input},
            config={"configurable": {"session_id": session_id}}
        )
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

    return JSONResponse(content={"response": response, "session_id": session_id})

