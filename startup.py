from fastapi import FastAPI


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

    return app

def mount_app_routes(app: FastAPI):
    from server.api.chat import router as chat_router
    from server.api.ticket_gateway import router as ticket_gateway_router
    app.include_router(chat_router)
    app.include_router(ticket_gateway_router)

if __name__ == "__main__":
    app = create_app()

    import uvicorn

    uvicorn.run(app, port=8000)


