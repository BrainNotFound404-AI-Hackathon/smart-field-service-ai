from datetime import datetime
from sqlmodel import SQLModel, Field
from typing import Optional, List

class Ticket(SQLModel, table=True):
    id: str = Field(primary_key=True, description="ticket ID")
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

class Record(SQLModel, table=True):
    """电梯运行数据记录模型"""
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: str = Field(index=True)  # ISO格式时间戳
    elevator_id: str = Field(index=True)
    status: str  # idle, moving_up, moving_down
    
    # 环境数据
    temperature_c: float
    humidity_percent: float
    
    # 传感器数据
    vibration_rms: float
    motor_current_a: float
    car_load_kg: float
    acceleration_m_s2: float
    door_force_n: float
    door_speed_mps: float
    brake_gap_mm: float
    brake_force_n: float
    safety_chain_status: bool
    emergency_power_status: bool
    
    # 故障代码（JSON字符串）
    fault_codes: str  # 存储为JSON字符串的故障代码列表

class SimilarTicket(SQLModel):
    """用于返回相似工单的模型"""
    id: str
    elevator_id: str
    location: str
    description: str
    status: str
    priority: str
    create_time: str
    similarity_score: float

class SimilarTicketsResponse(SQLModel):
    """用于返回相似工单列表的模型"""
    similar_tickets: List[SimilarTicket]
    total_count: int
