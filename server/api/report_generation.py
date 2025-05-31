#from google import genai
from fastapi import APIRouter
from server.api.utils import ChatRequest, Message
from langchain_google_genai import ChatGoogleGenerativeAI
from pathlib import Path
import json
from server.api.chat import lang_chat, stream_chat_response
from fastapi.responses import JSONResponse
from typing import List
from server.api.chat import store
from server.api.utils import convert_all_messages
from server.api.ticket_gateway import get_ticket_by_id
import httpx
import asyncio

router = APIRouter()

def format_messages_to_context(messages: List[Message]) -> str:
    role_map = {
        "user": "User",
        "assistant": "Assistant",
        "system": "System"
    }
    return "\n".join(
        f"{role_map[msg.role]}: {msg.content}" for msg in messages
    )


@router.post("/report/generation",tags=["report"], summary="Generate Elevator Maintenance Report")
def report_generation(
        request: ChatRequest,
):
    """
    生成电梯维修报告的函数
    """

    # ✅ 加载数据
    base_path = Path("data/")

    ticket = get_ticket_by_id(request.session_id)

    qa_memory = store[request.session_id].chat_memory.messages
    messages = convert_all_messages(qa_memory)
    messages_context = format_messages_to_context(messages)

    with open(base_path / "manual_fragments.json", "r", encoding="utf-8") as f:
        manual_fragments_data = json.load(f)

    # ✅ 构造 Prompt
    structured_prompt = f"""
    You are now an experienced elevator maintenance AI assistant. 
    Below is the previous fixing conversation between technician and AI assistant:
    {messages_context}
    
    Based on the following information, 
    please generate a report for the current issue. 
    The ticket file represents the current issue that are facing. The output should be well-structured, 
    clearly highlight solution procedures, and refer to the manual references and common pitfalls.

    Ticket Code Information:
    {ticket}

    Equipment Manual Excerpts:
    {json.dumps(manual_fragments_data, indent=2)}

    DO NOT GENERATE the report over 1000 tokens! 
    The report must follow **strict JSON format**, and should contain only the following two top-level fields:
- "solutions": a concise list of recommended technical actions.
- "results": a summary of expected or observed outcomes from applying these solutions.
    """
    # ✅ 调用 LangChain Chat 接口
    try:
        response = lang_chat(ChatRequest(
            messages=[Message(role="user", content=structured_prompt)],
            session_id=request.session_id
        ))
        print(f"Response: {response}")
        print(f"Response Type: {type(response)}")
    except Exception as e:
        return {"error": f"LLM 调用失败：{str(e)}"}

    return response