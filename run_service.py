# from server.service.ticket_service import TicketService

# def main():
#     try:
#         service = TicketService()
#         similar_tickets = service.find_similar_tickets()
        
#         print("\n找到的相似工单:")
#         for ticket in similar_tickets:
#             print(f"\n工单ID: {ticket.ticket_id}")
#             print(f"相似度: {ticket.similarity_score:.2f}")
#             print(f"原因: {ticket.reason}")
#     except Exception as e:
#         print(f"运行出错: {e}")

# if __name__ == "__main__":
#     main() 
import getpass
import os
from dotenv import load_dotenv

load_dotenv()
if not os.environ.get("GOOGLE_API_KEY"):
  os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter API key for Google Gemini: ")

from langchain.chat_models import init_chat_model

llm = init_chat_model("gemini-2.0-flash", model_provider="google_genai")
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

tagging_prompt = ChatPromptTemplate.from_template(
    """
Extract the desired information from the following passage.

Only extract the properties mentioned in the 'Classification' function.

Passage:
{input}
"""
)


class Classification(BaseModel):
    sentiment: str = Field(description="The sentiment of the text")
    aggressiveness: int = Field(
        description="How aggressive the text is on a scale from 1 to 10"
    )
    language: str = Field(description="The language the text is written in")


# Structured LLM
structured_llm = llm.with_structured_output(Classification) 
inp = "你是什么人？"
prompt = tagging_prompt.invoke({"input": inp})
response = structured_llm.invoke(prompt)

print(response)