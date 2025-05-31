import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough

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
    
    # 创建输出解析器
    output_parser = StrOutputParser()
    
    # 构建链
    chain = (
        {"input": RunnablePassthrough()}
        | prompt
        | llm
        | output_parser
    )
    
    # 运行链
    response = chain.invoke("你好，请介绍一下你自己。")
    print(response)

if __name__ == "__main__":
    main() 