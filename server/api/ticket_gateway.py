from fastapi import APIRouter
from typing import List

from server.agent import generate_ai_suggestion_from_ticket
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


@router.post("/tickets", response_model=Ticket)
async def create_ticket(ticket: Ticket):
    """
    创建新的工单

    Args:
        ticket (Ticket): 工单信息

    Returns:
        Ticket: 创建后的工单
    """
    try:
        # 使用知识库获取AI建议
        ai_suggestions = generate_ai_suggestion_from_ticket(ticket)
        ticket.ai_suggestion = ai_suggestions

        ticket_service = TicketService()
        created_ticket = ticket_service.create_ticket(ticket)
        return created_ticket
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/tickets/similar/{ticket_id}", response_model=List[Ticket])
async def similar_find_ticket(ticket_id: str):
    try:
        ticket_service = TicketService()
        ticket = ticket_service.get_ticket_by_id(ticket_id)
        similar_tickets = ticket_service.find_similar_tickets(ticket)
        print(similar_tickets)
        tickets = [ticket_service.get_ticket_by_id(st.ticket_id) for st in similar_tickets]
        return tickets
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/tickets/{ticket_id}", response_model=Ticket)
async def close_ticket(ticket_id: str):
    """
    更新工单信息

    Args:
        ticket_id (str): 工单ID
        ticket (Ticket): 更新的工单信息

    Returns:
        Ticket: 更新后的工单

    Raises:
        HTTPException: 当工单不存在时抛出404错误
    """
    try:
        ticket_service = TicketService()
        ticket = ticket_service.get_ticket_by_id(ticket_id)
        ticket.status = "Closed"
        updated_ticket = ticket_service.update_ticket(ticket_id, ticket)
        if not updated_ticket:
            raise HTTPException(status_code=404, detail=f"工单 {ticket_id} 不存在")
        return updated_ticket
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
