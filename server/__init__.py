"""
Smart Field Service AI - 智能现场服务系统
"""

from server.model.ticket import Ticket, SimilarTicket, SimilarTicketsResponse
from server.service.ticket_service import TicketService

__version__ = "0.1.0"
__all__ = ["Ticket", "SimilarTicket", "SimilarTicketsResponse", "TicketService"]
