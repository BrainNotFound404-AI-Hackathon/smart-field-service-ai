from typing import List
from datetime import datetime
from server.service.mock_tickets import mock_tickets
from server.model.ticket import SimilarTicket, Ticket, SimilarTicketsResponse
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic.v1 import BaseModel, Field
import os


class TicketService:
    """工单服务类"""
    
    def __init__(self):
        """初始化工单服务"""
        load_dotenv()
        if "GOOGLE_API_KEY" not in os.environ:
            raise ValueError("GOOGLE_API_KEY environment variable is not set")
            
        # 初始化示例数据
        self.current = Ticket(
            id="N1",
            elevator_id="E100",
            location="Building 1 East",
            description="Door does not fully close on 2F",
            status="Pending",
            priority="High",
            create_time=datetime.now().isoformat(),
            ai_suggestion="建议检查门机系统、门锁装置和门机控制器"
        )
        
        self.historical = [
            Ticket(
                id="H1",
                elevator_id="E100",
                location="Building 1 East",
                description="Door fails to close; alarm beeps",
                status="Closed",
                priority="High",
                create_time=datetime.now().isoformat(),
                solution="Adjusted door sensors and replaced door operator",
                ai_suggestion="建议检查门机系统和门锁装置"
            ),
            Ticket(
                id="H2",
                elevator_id="E200",
                location="Building 2 West",
                description="Bumpy ride with screeching sound",
                status="Closed",
                priority="Medium",
                create_time=datetime.now().isoformat(),
                solution="Lubricated guide rails and adjusted counterweight",
                ai_suggestion="建议检查曳引机和导轨系统"
            ),
            Ticket(
                id="H3",
                elevator_id="E300",
                location="Building 3 North",
                description="Door is stuck open on 3F",
                status="Closed",
                priority="High",
                create_time=datetime.now().isoformat(),
                solution="Replaced door operator motor",
                ai_suggestion="建议检查门机电机和控制系统"
            )
        ]
        
        # 初始化AI模型
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0,
            max_retries=2
        )
        self.structured_llm = self.llm.with_structured_output(SimilarTicketsResponse)

    def _format_ticket_info(self, ticket: Ticket) -> str:
        """格式化工单信息为字符串"""
        return f"""ID: {ticket.id}
        Elevator: {ticket.elevator_id}
        Location: {ticket.location}
        Description: {ticket.description}
        Status: {ticket.status}
        Priority: {ticket.priority}
        Create Time: {ticket.create_time}
        Solution: {ticket.solution if ticket.solution else 'N/A'}
        AI Suggestion: {ticket.ai_suggestion if ticket.ai_suggestion else 'N/A'}"""

    def get_pending_tickets(self) -> List[Ticket]:
        """
        获取所有待处理的工单
        
        Returns:
            List[Ticket]: 待处理工单列表
        """
        from server.database.database import Database
        db = Database()
        tickets = db.list_tickets()
        return [t for t in tickets if t.status == "Pending"]
    
    def get_ticket_by_id(self, ticket_id: str) -> Ticket:
        """
        根据ID获取工单详情
        
        Args:
            ticket_id (str): 工单ID
            
        Returns:
            Ticket: 工单详情
        """
        # TODO: 实现数据库查询逻辑
        
        pass
    
    def create_ticket(self, ticket: Ticket) -> Ticket:
        """
        创建新工单
        
        Args:
            ticket (Ticket): 工单信息
            
        Returns:
            Ticket: 创建后的工单
        """
        # TODO: 实现数据库插入逻辑
        pass
    
    def update_ticket(self, ticket_id: str, ticket: Ticket) -> Ticket:
        """
        更新工单信息
        
        Args:
            ticket_id (str): 工单ID
            ticket (Ticket): 更新的工单信息
            
        Returns:
            Ticket: 更新后的工单
        """
        # TODO: 实现数据库更新逻辑
        pass
    
    
    def find_similar_tickets(self, current_ticket: Ticket = None, max_results: int = 3) -> List[SimilarTicket]:
        """
        查找与当前工单相似的历史工单
        
        Args:
            current_ticket: 当前工单，如果为None则使用self.current
            max_results: 返回的最大相似工单数量
            
        Returns:
            List[SimilarTicket]: 相似工单列表，按相似度降序排序
        """
        current_ticket = current_ticket or self.current
        
        # 格式化工单信息
        current_ticket_info = self._format_ticket_info(current_ticket)
        historical_tickets_info = "\n".join([
            f"{self._format_ticket_info(t)}\n---"
            for t in self.historical
        ])
        
        # 创建提示词
        prompt = f"""你是一个专门用于查找相似电梯维护工单的AI助手。
            请分析以下当前工单和历史工单，找出最相似的工单。
            考虑以下相似性因素：
            1. 相同电梯或位置
            2. 相似的问题类型
            3. 相似的故障描述
            4. 可能相关的历史解决方案
            5. 相似的优先级
            6. 可能相关的AI建议

            当前工单：
            {current_ticket_info}

            历史工单：
            {historical_tickets_info}

            请返回{max_results}个最相似的工单，按相似度降序排序。
            """
        
        try:
            # 获取结构化响应
            response = self.structured_llm.invoke(prompt)
            return response.similar_tickets[:max_results]
        except Exception as e:
            print(f"获取模型响应时出错: {e}")
            return []



# Example usage

