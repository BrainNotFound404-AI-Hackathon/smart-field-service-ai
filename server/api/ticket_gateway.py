from fastapi import APIRouter
from typing import List
from server.service.ticket_service import TicketService
from server.model.ticket import Ticket
from fastapi import HTTPException
router = APIRouter()
@router.get("/tickets", response_model=List[Ticket])
async def get_tickets():
    """
    获取所有待处理的工单
    
    Returns:
        List[Ticket]: 待处理工单列表
    """
    try:
        ticket_service = TicketService()
        tickets = ticket_service.get_pending_tickets()
        return tickets
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
