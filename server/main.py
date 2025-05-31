from fastapi import FastAPI
from server.api.ticket_gateway import router as ticket_router

app = FastAPI(
    title="Smart Field Service AI",
    description="intelligent live service AI system",
    version="1.0.0"
)

# register route
app.include_router(ticket_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to Smart Field Service AI API"} 