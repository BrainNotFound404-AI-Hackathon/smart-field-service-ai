import os
import json
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# 加载环境变量
load_dotenv()

def main():
    # 1. 加载 JSON 数据
    base_path = Path("data/")
    with open(base_path / "alerts.json", "r", encoding="utf-8") as f:
        alerts_data = json.load(f)
    with open(base_path / "maintenance_logs.json", "r", encoding="utf-8") as f:
        maintenance_logs_data = json.load(f)
    with open(base_path / "manual_fragments.json", "r", encoding="utf-8") as f:
        manual_fragments_data = json.load(f)
    #with open(base_path / "bug.json", "r", encoding="utf-8") as f:
    #    bug_data = json.load(f)

#Bug Code:
#{json.dumps(bug_data, indent=2)}
# , the bug code represents the error code for each action/situation

    # 2. 格式化 Prompt 模板
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

    # 3. 创建 LLM 实例
    llm = ChatOpenAI(
        model="deepseek-ai/deepseek-llm-7b-chat",
        base_url=os.getenv("CHAT_API_BASE_URL"),
        api_key=os.getenv("CHAT_API_KEY"),
    )

    # 4. 构建消息模板
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an experienced elevator maintenance assistant."),
        ("user", "{input}")
    ])

    # 5. 调用模型
    try:
        result = llm.invoke(prompt.format(input=structured_prompt))
        print("🔧 Troubleshooting Recommendation:\n")
        print(result.content)
    except Exception as e:
        print("❌ LLM 调用失败：", e)


if __name__ == "__main__":
    main()