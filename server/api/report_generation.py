#from google import genai
from fastapi import APIRouter
from server.api.utils import ChatRequest, Message
from langchain_google_genai import ChatGoogleGenerativeAI
from pathlib import Path
import json
from server.api.chat import lang_chat
from fastapi.responses import JSONResponse
from typing import List
from server.api.chat import store
from server.api.utils import convert_all_messages
from server.api.ticket_gateway import get_ticket_by_id

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

    # with open("output/troubleshooting_output.txt", "r", encoding="utf-8") as f:
    #     troubleshooting_data = json.load(f)

    ##TODO: Q ^ A message
    qa_memory = store[request.session_id].chat_memory.messages
    messages = convert_all_messages(qa_memory)
    messages_context = format_messages_to_context(messages)

    with open(base_path / "manual_fragments.json", "r", encoding="utf-8") as f:
        manual_fragments_data = json.load(f)

    # ✅ 构造 Prompt
    structured_prompt = f"""
    You are now an experienced elevator maintenance AI assistant. 
    Below is the previous conversation context:
    {messages_context}
    
    Based on the following information, 
    please generate a report for the current issue. 
    The ticket file represents the current issue that are facing. The output should be well-structured, 
    clearly highlight solution procedures, and refer to the manual references and common pitfalls.

    Ticket Code Information:
    {ticket}


    Equipment Manual Excerpts:
    {json.dumps(manual_fragments_data, indent=2)}

    generate the report using json format and the content should be as below:
      ticket_id
      elevator_id
      location
      priority
      issue_description
      report 
        high_priority_checks_and_error_codes
            component
            checks
            related_error_codes
            component
            checks
            related_error_codes
        recommended_troubleshooting_procedure
        common_pitfalls_and_cautions
        relevant_manual_references
            section
            title
            notes
            all of the component above
    """
generate the report using json format and the content should be as below:
# Report Structure
Include a JSON object with the following top-level fields:
- ticket_id: [string] → ID of the maintenance ticket.
- elevator_id: [string] → Unique elevator identifier.
- location: [string] → Location of the elevator.
- priority: [string] → Priority level of the ticket.
- issue_description: [string] → Short description of the issue.

- report: [object]
    - high_priority_checks_and_error_codes: [list of objects]
        # For each component suspected in the issue, include:
        - component: [string] → Component name (e.g., "Door Sensor", "Control Board")
        - checks: [list of strings] → Step-by-step checks to perform.
        - related_error_codes: [list of strings] → Any known error codes associated.

    - recommended_troubleshooting_procedure: [list of strings]
        # Describe the troubleshooting workflow in logical sequence.
        # E.g., Check sensor alignment → Test voltage → Reboot controller

    - common_pitfalls_and_cautions: [list of strings]
        # Warn technicians about possible mistakes or dangers.
        # E.g., "Don't skip cable re-seating", "Beware of ESD damage"

    - relevant_manual_references: [list of objects]
        # Link report to the manual for traceability and compliance.
        - section: [string] → Manual section number.
        - title: [string] → Title or heading from the manual.
        - notes: [string] → Summary of why this section is relevant.

# Output Format
Return the entire content as a valid JSON object with UTF-8 encoding.
Ensure all field values are plain text (no Markdown, no HTML).
Use double quotes for all keys and string values.

# Example usage
This output format will be consumed by a frontend UI and needs to be strict JSON.
"""

    # ✅ 调用 LangChain Chat 接口
    try:
        response = lang_chat(ChatRequest(
            messages=[Message(role="user", content=structured_prompt)],
            session_id=request.session_id
        ))
        print(f"Response: {response}")
    except Exception as e:
        return {"error": f"LLM 调用失败：{str(e)}"}

    return response

# TODO: 1. 改tikect 状态 2. 关闭上下文
output_path = Path("output/report.md")  # 你可以自定义文件名和路径
output_path.parent.mkdir(parents=True, exist_ok=True)  # 创建父目录（如果不存在）

# 保存为 Markdown 文件
with open(output_path, "w", encoding="utf-8") as f:
    f.write(response.text)

print(f"✅ Report saved to {output_path.resolve()}")