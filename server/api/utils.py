from typing import Dict, List, Optional, Literal
from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage


class Message(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    messages: List[Message] = Field(..., description="message list")

class ChatRqst(BaseModel):
    session_id: Optional[str] = None
    message: str


def convert_langchain_message(msg: BaseMessage) -> Message:
    if isinstance(msg, HumanMessage):
        role = "user"
    elif isinstance(msg, AIMessage):
        role = "assistant"
    elif isinstance(msg, SystemMessage):
        role = "system"
    else:
        raise ValueError(f"Unsupported message type: {type(msg)}")

    return Message(role=role, content=msg.content)


def convert_all_messages(msgs: List[BaseMessage]) -> List[Message]:
    return [convert_langchain_message(msg) for msg in msgs]
