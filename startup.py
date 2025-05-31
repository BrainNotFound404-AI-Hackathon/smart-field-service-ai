from fastapi import FastAPI

from server.ticket_robot import TicketRobot


def create_app() -> FastAPI:
    app = FastAPI(
        title="Chat API",
        description="API for chat functionalities",
        version="1.0.0",
        openapi_tags=[
            {
                "name": "Chat",
                "description": "Endpoints for chat functionalities"
            }
        ]
    )

    from fastapi.middleware.cors import CORSMiddleware

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    mount_app_routes(app)

    TicketRobot()

    return app

def mount_app_routes(app: FastAPI):
    from server.api.chat import router as chat_router
    from server.api.ticket_gateway import router as ticket_gateway_router
    from server.api.clean_up import router as clean_up_router
    from server.api.report_generation import router as report_generation_router
    app.include_router(chat_router)
    app.include_router(ticket_gateway_router)
    app.include_router(clean_up_router)
    app.include_router(report_generation_router)

if __name__ == "__main__":
    app = create_app()

    import uvicorn

    uvicorn.run(app, port=8000)


