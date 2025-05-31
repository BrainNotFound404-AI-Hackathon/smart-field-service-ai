from datetime import datetime
from typing import List, Optional, Literal
from pydantic import BaseModel, Field

class Ticket(BaseModel):
    """工单数据模型"""
    id: str = Field(description="工单ID")
    elevator_id: str = Field(description="电梯ID")
    location: str = Field(description="电梯位置")
    description: str = Field(description="故障描述")
    status: Literal["Pending", "Closed"] | str = Field(description="工单状态")
    priority: Literal["High", "Medium", "Low"] | str = Field(description="优先级")
    create_time: datetime = Field(description="创建时间")
    close_time: Optional[str] = Field(default=None, description="关闭时间（已关闭工单）")
    solution: Optional[str] = Field(default=None, description="解决方案（维修操作录入/AI建议/人工填写）")
    result: Optional[str] = Field(default=None, description="维修结果（人工填写）")
    images: Optional[List[str]] = Field(default=None, description="相关图片URL数组")
    ai_suggestion: Optional[str] = Field(default=None, description="AI生成的重点排查建议")

    class Config:
        arbitrary_types_allowed = True