from app.api import ticket_gateway
from app.model.ticket import Ticket


class TicketRobot: 
    def __init__(self):
        pass
    
    def create_ticket(self, ticket: Ticket):
        ticket_gateway.create_ticket(ticket)
        import asyncio
        from datetime import datetime

        async def check_pending_tickets():
            while True:
                try:
                    # 获取所有待处理工单
                    tickets = await ticket_gateway.get_tickets()
                    
                    # 处理每个待处理工单
                    for ticket in tickets:
                        print(f"[{datetime.now()}] 处理工单: {ticket.id}")
                        # TODO: 在这里添加具体的工单处理逻辑
                        
                    # 等待30秒
                    await asyncio.sleep(30)
                    
                except Exception as e:
                    print(f"处理工单时发生错误: {str(e)}")
                    await asyncio.sleep(30)

        # 启动定时任务
        asyncio.create_task(check_pending_tickets())
