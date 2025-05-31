"""
Model package - 数据模型层
包含工单、相似工单等数据模型定义
"""

from server.model.ticket import Ticket, SimilarTicket, SimilarTicketsResponse

__all__ = ["Ticket", "SimilarTicket", "SimilarTicketsResponse"] 