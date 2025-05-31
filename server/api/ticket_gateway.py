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

@router.get("/tickets/{ticket_id}", response_model=Ticket)
async def get_ticket_by_id(ticket_id: str):
    """
    根据ID获取工单详情
    
    Args:
        ticket_id (str): 工单ID
        
    Returns:
        Ticket: 工单详情
        
    Raises:
        HTTPException: 当工单不存在时抛出404错误
    """
    try:
        ticket_service = TicketService()
        ticket = ticket_service.get_ticket_by_id(ticket_id)
        if not ticket:
            raise HTTPException(status_code=404, detail=f"工单 {ticket_id} 不存在")
        return ticket
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
