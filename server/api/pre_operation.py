import json
from pathlib import Path
import requests

# Paths to the .json files (assumed to be stored in same directory)
base_path = Path(r"C:\Users\yunxuliu\Downloads\Hackathon")  # 注意 r 前缀防止 \ 转义
alerts_file = base_path / "alerts.json"
maintenance_logs_file = base_path / "maintenance_logs.json"
manual_fragments_file = base_path / "manual_fragments.json"
bug_file = base_path / "bug.json"
# Load alert JSON content
with open(alerts_file, "r", encoding="utf-8") as f:
    alerts_data = json.load(f)
with open(maintenance_logs_file, "r", encoding="utf-8") as f:
    Maintenance_logs_data = json.load(f)
with open(manual_fragments_file, "r", encoding="utf-8") as f:
    manual_fragments_data = json.load(f)
with open(bug_file, "r", encoding="utf-8") as f:
    bug_data = json.load(f)
# Construct prompt
prompt = f"""You are now an experienced elevator maintenance AI assistant. Based on the following information, 
     please generate a "Key Troubleshooting Recommendations" for the current issue. 
    The alarm code represents the current issue, the bug code represent the error code for each action(situation), 
    if there is no error code it means it is correct. The output should be well-structured, 
    clearly highlight high-priority checks, and refer to the manual references and common pitfalls.

Alarm Code Information:
{json.dumps(alerts_data, indent=2)}

Bug code:
{json.dumps(alerts_data, indent=2)}

Maintenance History:
{json.dumps(Maintenance_logs_data, indent=2)}

Equipment Manual Excerpts:
{json.dumps(manual_fragments_data, indent=2)}

Please output your response in the following structure:
1. High-Priority Checks and error code
2. Recommended Troubleshooting Procedure
3. Common Pitfalls and Cautions
4. Relevant Manual References (summary)
"""

# Prepare request (API Key should be manually inserted by user)
api_request = {
    "url": "https://containers.datacrunch.io/brainnotfound404/v1/chat/completions",
    "headers": {
        "Content-Type": "application/json",
        "Authorization": "Bearer dc_161419f95a0e0a7c83d950d8bddf42cc57bbd49345ebf7c56d9b31e220a8d7b8b3a149244058d3c74b11bf137afe0130130e22e59ff7e9e93091772e23ef4f233969c21ffcd7e2498e25c06ccf847a522f544aeb94353b89c114b14825fdc7750608611d7bbd136c0390fab99cf2cfc7522262a281a2411331d9b30f2dccca5d"  # Replace with your actual key
    },
    "json": {
        "messages": [
            {"role": "system", "content": "You are an experienced elevator maintenance assistant."},
            {"role": "user", "content": prompt}
        ]
    }
}

response = requests.post(
    api_request["url"],
    headers=api_request["headers"],
    json=api_request["json"]
)
print("Content-Type:", response.headers.get("Content-Type"))
print(response.status_code)
print(response.text)


output_file = Path("C:/Users/yunxuliu/Downloads/Hackathon/elevator_diagnostics_summary.md")

if response.status_code == 200:
    try:
        result = response.json()  # 比 json.loads(response.text) 更健壮
        assistant_content = result["choices"][0]["message"]["content"]
        #with open(output_file, "w", encoding="utf-8") as f:        # json
        #    json.dump(result, f, ensure_ascii=False)
        #with open(output_file, "w", encoding="utf-8") as f:        # content
        #    json.dump({"summary": assistant_content}, f, indent=2, ensure_ascii=False)
        with open(output_file, "w", encoding="utf-8") as f:      # markdown
            f.write(assistant_content)
        print(f"✅ JSON saved to {output_file}")
    except Exception as e:
        print("⚠️ Not valid JSON response:", e)
        with open(base_path / "raw_response.bin", "wb") as f:
            f.write(response.content)
        print("⚠️ Saved raw response to raw_response.bin for manual inspection")
else:
    print(f"❌ HTTP {response.status_code} - request failed")