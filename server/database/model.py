from datetime import datetime
from sqlmodel import SQLModel, Field
from typing import Optional

class Ticket(SQLModel, table=True):
    id: str = Field(primary_key=True, description="工单ID")
    elevator_id: str
    location: str
    description: str
    status: str
    priority: str
    create_time: datetime
    close_time: Optional[str] = None
    solution: Optional[str] = None
    result: Optional[str] = None
    images: Optional[str] = None  # 建议存json字符串
    ai_suggestion: Optional[str] = None