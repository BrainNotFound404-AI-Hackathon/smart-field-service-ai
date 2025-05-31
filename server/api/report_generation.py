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
    troubleshooting_data = json.load(f)

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

# ✅ 调用 Gemini 模型
model = genai.GenerativeModel("gemini-2.0-flash")  # 或使用 gemini-1.5-pro
response = model.generate_content(structured_prompt)

# ✅ 输出结果
print("🔧 report:\n")
print(response.text)