"""
Project API package - API层
包含FastAPI路由和API端点定义
"""

from fastapi import APIRouter

# 创建主路由
router = APIRouter(prefix="/api/v1", tags=["smart-field-service"])

# 导入并包含子路由
from server.project_API.ticket_gateway import router as ticket_router
router.include_router(ticket_router)

__all__ = ["router"]
