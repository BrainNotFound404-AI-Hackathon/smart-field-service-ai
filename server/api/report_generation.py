#from google import genai
from google.genai import types
import google.generativeai as genai

from pathlib import Path
import json

# ✅ 设置 Gemini API Key
genai.configure(api_key = "AIzaSyBSFs4_X_-T3Ry49JeMMbBs6-LozKGNAIo")

# ✅ 加载数据
base_path = Path("data/")
with open(base_path / "ticket.json", "r", encoding="utf-8") as f:
    ticket_data = json.load(f)
with open( "output/troubleshooting_output.txt", "r", encoding="utf-8") as f:
    troubleshooting_data = f.read()

##TODO: Q ^ A query

with open(base_path / "manual_fragments.json", "r", encoding="utf-8") as f:
    manual_fragments_data = json.load(f)

# ✅ 构造 Prompt
structured_prompt = f"""
You are now an experienced elevator maintenance AI assistant. Based on the following information, 
please generate a report for the current issue. 
The ticket file represents the current issue that are facing. The output should be well-structured, 
clearly highlight solution procedures, and refer to the manual references and common pitfalls.

Ticket Code Information:
{json.dumps(ticket_data, indent=2)}

Recommandation solutions based on the manual file and history repair ticket(closed):
{json.dumps(troubleshooting_data, indent=2)}

Equipment Manual Excerpts:
{json.dumps(manual_fragments_data, indent=2)}

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

# ✅ 调用 Gemini 模型
model = genai.GenerativeModel("gemini-2.0-flash")  # 或使用 gemini-1.5-pro
response = model.generate_content(structured_prompt)

output_path = Path("output/report.md")  # 你可以自定义文件名和路径
output_path.parent.mkdir(parents=True, exist_ok=True)  # 创建父目录（如果不存在）

# 保存为 Markdown 文件
with open(output_path, "w", encoding="utf-8") as f:
    f.write(response.text)

print(f"✅ Report saved to {output_path.resolve()}")