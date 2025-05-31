from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from knowledge_base.store import get_retriever
from server.model.ticket import Ticket

system_instruction = """
You are now an experienced elevator maintenance AI assistant. Based on the following information, 
please generate a "Key Troubleshooting Recommendations" for the current issue. 

Equipment Manual Excerpts:
{manual}

Please output your response in the following structure:
1. High-Priority Checks and Error Codes
2. Recommended Troubleshooting Procedure
3. Common Pitfalls and Cautions
4. Relevant Manual References (summary)
"""

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash-8b",
    temperature=0,
    timeout=None,
    max_retries=2,
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_instruction),
    ("user", "{input}")
])


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def get_suggestion_assistant():
    """
    获取当前线程的suggestion assistant实例
    """
    retriever = get_retriever()
    return (
        {
            "manual": retriever | format_docs,
            "input": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )


def generate_ai_suggestion_from_ticket(ticket: Ticket):
    suggestion_assistant = get_suggestion_assistant()
    result = suggestion_assistant.invoke(f"The following are the problems encountered by users: \n {ticket.description}")
    return result


# for test
if __name__ == "__main__":
    description = "Elevator fails to stop at the 5th floor and skips to the 6th floor."
    suggestion_assistant = get_suggestion_assistant()
    result = suggestion_assistant.invoke(f"The following are the problems encountered by users: \n {description}")
    print(result)
