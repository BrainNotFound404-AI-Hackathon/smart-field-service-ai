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
    acquire all un-solved ticket

    Returns:
        List[Ticket]: to-be-solved ticket list
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
    acquire ticket detail according to ID

    Args:
        ticket_id (str): ticket ID

    Returns:
        Ticket: ticket information

    Raises:
        HTTPException: throw 404 error when ticket in-exist
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
    create new ticket

    Args:
        ticket (Ticket): ticket information

    Returns:
        Ticket: created ticket
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
    update ticket information

    Args:
        ticket_id (str): ticket ID
        ticket (Ticket): update ticket information

    Returns:
        Ticket: updated ticket

    Raises:
        HTTPException: throw 404 error when ticket in-exist
    """
    try:
        ticket_service = TicketService()
        ticket = ticket_service.get_ticket_by_id(ticket_id)
        ticket.status = "Closed"
        updated_ticket = ticket_service.update_ticket(ticket_id, ticket)
        if not updated_ticket:
            raise HTTPException(status_code=404, detail=f"ticket {ticket_id} do not exist")
        return updated_ticket
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
