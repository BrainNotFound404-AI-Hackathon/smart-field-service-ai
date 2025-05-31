from api.prompt_API import run_prompt
import sys
import json
from google import genai
from google.genai import types
from pathlib import Path

# Set Gemini API Key
genai.configure(api_key="YOUR_API_KEY_HERE")  # ← Replace this with your actual Gemini API key

# Load data
base_path = Path("data/")
with open(base_path / "alerts.json", "r", encoding="utf-8") as f:
    alerts_data = json.load(f)
with open(base_path / "maintenance_logs.json", "r", encoding="utf-8") as f:
    maintenance_logs_data = json.load(f)
with open(base_path / "manual_fragments.json", "r", encoding="utf-8") as f:
    manual_fragments_data = json.load(f)

# Construct Prompt
structured_prompt = f"""
You are now an experienced elevator maintenance AI assistant. Based on the following information, 
please generate a "Key Troubleshooting Recommendations" for the current issue. 
The alarm code represents the current issue. 
If there is no error code, it means the action is correct. The output should be well-structured, 
clearly highlight high-priority checks, and refer to the manual references and common pitfalls.

Alarm Code Information:
{json.dumps(alerts_data, indent=2)}

Maintenance History:
{json.dumps(maintenance_logs_data, indent=2)}

Equipment Manual Excerpts:
{json.dumps(manual_fragments_data, indent=2)}

Please output your response in the following structure:
1. High-Priority Checks and Error Codes
2. Recommended Troubleshooting Procedure
3. Common Pitfalls and Cautions
4. Relevant Manual References (summary)
"""

# Invoke the Gemini model
model = genai.GenerativeModel("gemini-2.0-flash")  # Or use "gemini-1.5-pro"
response = model.generate_content(structured_prompt)

# Output the result
print("🔧 Troubleshooting Recommendation:\n")
print(response.text)