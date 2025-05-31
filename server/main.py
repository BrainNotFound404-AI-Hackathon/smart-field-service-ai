from fastapi import FastAPI
from server.api.ticket_gateway import router as ticket_router

app = FastAPI(
    title="Smart Field Service AI",
    description="智能现场服务 AI 系统",
    version="1.0.0"
)

# 注册路由
app.include_router(ticket_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to Smart Field Service AI API"} 