import os
from typing import Optional
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

# 加载环境变量
load_dotenv()

def main():
    # 创建 LLM，使用自定义 API 端点
    llm = ChatOpenAI(
        model="deepseek-ai/deepseek-llm-7b-chat",  # 替换为您的模型名称
        base_url=os.getenv("OPENAI_API_BASE"),  # 从环境变量读取 API 端点
        api_key=os.getenv("OPENAI_API_KEY")  # 从环境变量读取 API 密钥
    )
    
    # 创建提示模板
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个有帮助的AI助手。"),
        ("user", "{input}")
    ])
    
    # 定义 Joke 结构化输出
    class Joke(BaseModel):
        """Joke to tell user."""
        setup: str = Field(description="The setup of the joke")
        punchline: str = Field(description="The punchline to the joke")
        rating: Optional[int] = Field(
            default=None, description="How funny the joke is, from 1 to 10"
        )
    
    # 使用结构化输出调用 LLM
    structured_llm = llm.with_structured_output(Joke)
    
    # 使用自定义 prompt 模板
    joke_response = structured_llm.invoke(prompt.format(input="Tell me a joke about cats"))
    print("Joke Response:", joke_response)

if __name__ == "__main__":
    main() 