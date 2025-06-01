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
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os

from server.service.ticket_service import TicketService

# 加载环境变量
load_dotenv()

router = APIRouter()

class MaintenanceReport(BaseModel):
    """维护报告结构"""
    solutions: str = Field(description="推荐的技术操作步骤列表")
    results: str = Field(description="应用这些解决方案后的预期或观察结果")

def format_messages_to_context(messages: List[Message]) -> str:
    role_map = {
        "user": "User",
        "assistant": "Assistant",
        "system": "System"
    }
    return "\n".join(
        f"{role_map[msg.role]}: {msg.content}" for msg in messages
    )

@router.post("/report/generation", tags=["report"], summary="生成电梯维护报告")
def report_generation(request: ChatRequest):
    """
    生成电梯维护报告
    """
    try:
        # 初始化Google模型
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash-8b",
            temperature=0,
            max_retries=2
        )
        structured_llm = llm.with_structured_output(MaintenanceReport)

        # 加载数据
        base_path = Path("data/")
        ticket_service = TicketService()
        ticket = ticket_service.get_ticket_by_id(request.session_id)
        # 获取会话中的聊天记录
        messages_context = ""
        if request.session_id in store:
            qa_memory = store[request.session_id].chat_memory.messages
            messages = convert_all_messages(qa_memory)
            messages_context = format_messages_to_context(messages)

        with open(base_path / "manual_fragments.json", "r", encoding="utf-8") as f:
            manual_fragments_data = json.load(f)

        # 构建提示词
        prompt = f"""
        You are an experienced elevator maintenance AI assistant.
        Below is the conversation between the technician and AI assistant:
        {messages_context}
        
        Based on the following information, please generate a report for the current issue.
        The ticket information represents the current problem. The output should be well-structured,
        highlighting solution steps and referencing manual excerpts and common pitfalls.

        Ticket Information:
        {ticket}

        Equipment Manual Excerpts:
        {json.dumps(manual_fragments_data, indent=2)}
        
        DO NOT ouptput the report over 1000 tokens
        Please generate a concise maintenance report containing:
        1. A list of recommended technical operation steps
        2. Expected or observed outcomes from applying these solutions
        """

        # 调用模型获取结构化输出
        response = structured_llm.invoke(prompt)
        return response

    except Exception as e:
        return {"error": f"生成报告时出错：{str(e)}"}