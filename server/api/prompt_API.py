import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# 加载环境变量
load_dotenv()

# 初始化 LLM
llm = ChatOpenAI(
    model="Qwen/Qwen2.5-32B",
    base_url=os.getenv("CHAT_API_BASE_URL"),
    api_key=os.getenv("CHAT_API_KEY"),
)

prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are an experienced elevator maintenance assistant."),
    ("user", "{input}")
])

def run_prompt(input_text: str) -> str:
    """调用大模型生成内容"""
    try:
        result = llm.invoke(prompt_template.format(input=input_text))
        return result.content
    except Exception as e:
        return f"❌ LLM 调用失败：{e}"
