from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from langchain_core.language_models.chat_models import BaseChatModel
from typing import Dict, List, Optional, Iterator, Any, Literal
import requests
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, BaseMessage
from langchain_core.outputs import ChatGenerationChunk, ChatResult, ChatGeneration
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import json
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv
load_dotenv()


router = APIRouter()


class Message(BaseModel):
    role: Literal["system", "user"]
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

@router.post("/lang_chat", tags=["Chat"], summary="LangChain Chat Interface")
def lang_chat(
    request: ChatRequest,
):
    """
    LangChain Chat endpoint for handling chat requests.
    This function will handle the chat logic and return a response.
    """
    # Here you would implement the chat logic
    # For now, we will just return a placeholder response
    llm = ChatOpenAI(
        model="deepseek-ai/deepseek-llm-7b-chat",
        base_url=os.getenv("OPENAI_API_BASE"),  # 从环境变量读取 API 端点
        api_key=os.getenv("OPENAI_API_KEY")
    )

    # 构造 LangChain 消息对象
    lc_messages = []
    for msg in request.messages:
        print(f"Processing message: {msg.role} - {msg.content}")
        if msg.role in ["system", "user"]:
            lc_messages.append((msg.role, msg.content))
        else:
            return JSONResponse(status_code=400, content={"error": f"Unsupported role: {msg.role}"})

    prompt = ChatPromptTemplate.from_messages(lc_messages)

    class Solution(BaseModel):
        """Solution to the chat request."""
        solution: str = Field(description="This is a structured solution response.")

        def to_dict(self):
            return {"solution": self.solution}

    structured_llm = llm.with_structured_output(Solution)

    response = structured_llm.invoke(prompt.format(input="This is a test input."))

    print("Response received:", response)

    return JSONResponse(content={"response": response.to_dict()})

@router.post("/chat", tags=["Chat"], summary="Chat Interface")
def chat(
        request: ChatRequest,
        stream: bool = Query(False),
        ):
    """
    Chat endpoint for handling chat requests.
    This function will handle the chat logic and return a response.
    """
    # Here you would implement the chat logic
    # For now, we will just return a placeholder response

    model = "deepseek-ai/deepseek-llm-7b-chat"
    api_url = "https://containers.datacrunch.io/brainnotfound404/v1/chat/completions"
    inference_key = "dc_161419f95a0e0a7c83d950d8bddf42cc57bbd49345ebf7c56d9b31e220a8d7b8b3a149244058d3c74b11bf137afe0130130e22e59ff7e9e93091772e23ef4f233969c21ffcd7e2498e25c06ccf847a522f544aeb94353b89c114b14825fdc7750608611d7bbd136c0390fab99cf2cfc7522262a281a2411331d9b30f2dccca5d"

    llm = DatacrunchChatModel(
        api_url=api_url,
        model=model,
        inference_key=inference_key,
        stream_mode=stream
    )

    # 构造 LangChain 消息对象
    lc_messages = []
    for msg in request.messages:
        print(f"Processing message: {msg.role} - {msg.content}")
        if msg.role == "system":
            lc_messages.append(SystemMessage(content=msg.content))
        elif msg.role == "user":
            lc_messages.append(HumanMessage(content=msg.content))
        else:
            return JSONResponse(status_code=400, content={"error": f"Unsupported role: {msg.role}"})
        print(lc_messages)

    if stream:
        output = llm.stream(lc_messages)
        return JSONResponse(content={"streaming": True, "response": [chunk.message.content for chunk in output]})
    else:
        output = llm.generate([lc_messages])
        return JSONResponse(content={"streaming": False, "response": output.generations[0][0].message.content})

class DatacrunchChatModel(BaseChatModel):
    api_url: str
    model: str
    inference_key: str
    stream_mode: bool = True

    def _map_role(self, message: BaseMessage) -> str:
        if isinstance(message, SystemMessage):
            return "system"
        elif isinstance(message, HumanMessage):
            return "user"
        elif isinstance(message, AIMessage):
            return "assistant"
        else:
            raise ValueError(f"Unsupported message type: {type(message)}")

    def _generate(
        self,
        messages: List[BaseMessage],
        config: Optional[RunnableConfig] = None,
        **kwargs: Any
    ) -> ChatResult:
        headers = {
            "Authorization": f"Bearer {self.inference_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": [{"role": self._map_role(m), "content": m.content} for m in messages],
            "stream": False
        }
        print(messages)

        resp = requests.post(self.api_url, json=payload, headers=headers)
        print(resp)
        content = resp.json()["choices"][0]["message"]["content"]
        print(f"Response content: {content}")
        return ChatResult(generations=[ChatGeneration(message=AIMessage(content=content))])

    def _stream(
        self,
        input: list,  # Typically List[BaseMessage]
        config: Optional[RunnableConfig] = None,
        **kwargs: Any
    ) -> Iterator[ChatGenerationChunk]:
        headers = {
            "Authorization": f"Bearer {self.inference_key}",
            "Content-Type": "application/json"
        }

        messages = [{"role": m.type, "content": m.content} for m in input]


        payload = {
            "model": self.model,
            "messages": messages,
            "stream": True
        }

        with requests.post(self.api_url, json=payload, headers=headers, stream=True) as resp:
            for line in resp.iter_lines(decode_unicode=True):
                if line and line.startswith("data: "):
                    line_content = line[len("data: "):].strip()
                    if line_content == "[DONE]":
                        break
                    try:
                        data = json.loads(line_content)
                        delta = data.get("choices", [{}])[0].get("delta", {}).get("content", "")
                        if delta:
                            yield ChatGenerationChunk(message=AIMessage(content=delta))
                    except Exception as e:
                        continue  # or log
    @property
    def _llm_type(self) -> str:
        return "custom_streaming_chat"

#
# llm = DatacrunchChatModel(
#     api_url="https://containers.datacrunch.io/brainnotfound404/v1/chat/completions",
#     model="deepseek-ai/deepseek-llm-7b-chat",
#     inference_key="dc_161419f95a0e0a7c83d950d8bddf42cc57bbd49345ebf7c56d9b31e220a8d7b8b3a149244058d3c74b11bf137afe0130130e22e59ff7e9e93091772e23ef4f233969c21ffcd7e2498e25c06ccf847a522f544aeb94353b89c114b14825fdc7750608611d7bbd136c0390fab99cf2cfc7522262a281a2411331d9b30f2dccca5d",
# )
#
# messages = [
#     [
#     SystemMessage(content="You are a helpful writer assistant."),
#     HumanMessage(content="What is deep learning?")
#     ]
# ]
#
# optput = llm.generate(messages)
#
# print(
#     "Output received:"
# )
# print(optput.generations[0][0].message.content)
#
# for chunk in llm.stream(messages[0]):
#     print("Chunk received:")
#     print(chunk)
#     print(chunk.message.content, end="", flush=True)