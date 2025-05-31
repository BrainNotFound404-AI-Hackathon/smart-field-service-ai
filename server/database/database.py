
from datetime import datetime
from sqlmodel import SQLModel, create_engine, Session, select
from typing import Optional, List
import json

from server.database.model import Ticket    

class Database:
    def __init__(self, db_url: str = "sqlite:///./data/fix-wise.db"):
        self.engine = create_engine(db_url)
        SQLModel.metadata.create_all(self.engine)

    # 新增
    def add_ticket(self, ticket: Ticket):
        with Session(self.engine) as session:
            session.add(ticket)
            session.commit()

    # 查询单个
    def get_ticket_by_id(self, ticket_id: str) -> Optional[Ticket]:
        with Session(self.engine) as session:
            return session.get(Ticket, ticket_id)

    # 查询所有
    def list_tickets(self) -> List[Ticket]:
        with Session(self.engine) as session:
            statement = select(Ticket)
            return list(session.exec(statement))

    # 更新（支持部分字段更新）
    def update_ticket(self, ticket_id: str, update_fields: dict):
        with Session(self.engine) as session:
            ticket = session.get(Ticket, ticket_id)
            if not ticket:
                return None
            for k, v in update_fields.items():
                setattr(ticket, k, v)
            session.add(ticket)
            session.commit()
            session.refresh(ticket)
            return ticket

    # 删除
    def delete_ticket(self, ticket_id: str):
        with Session(self.engine) as session:
            ticket = session.get(Ticket, ticket_id)
            if ticket:
                session.delete(ticket)
                session.commit()

    def init_data(self):
        if len(self.list_tickets()) == 0:
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            tickets = [
                Ticket(
                    id="T001",
                    elevator_id="E001",
                    location="Building 1 Unit 1",
                    description="Elevator door cannot close properly",
                    status="Pending",
                    priority="High",
                    create_time=now_str
                ),
                Ticket(
                    id="T002",
                    elevator_id="E002",
                    location="Building 2 Unit 2",
                    description="Abnormal noise during elevator operation",
                    status="Pending",
                    priority="Medium",
                    create_time=now_str
                ),
                Ticket(
                    id="T003",
                    elevator_id="E003",
                    location="Building 3 Unit 1",
                    description="Elevator display screen not working",
                    status="Pending",
                    priority="Low",
                    create_time=now_str
                )
            ]
            for t in tickets:
                self.add_ticket(t)
            print("Initialized demo data.")