"""
Service package - 服务层模块
包含工单服务、相似工单查找等业务逻辑
"""

from server.service.ticket_service import TicketService
from server.service.mock_tickets import mock_tickets

__all__ = ["TicketService", "mock_tickets"]
