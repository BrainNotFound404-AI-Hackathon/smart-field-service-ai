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
    mount_app_routes(app)

    return app

def mount_app_routes(app: FastAPI):
    from server.api.chat import router as chat_router
    app.post("/chat",
            tags=["Chat"],
            summary="chat interface")(chat_router)


if __name__ == "__main__":
    app = create_app()

    import uvicorn

    uvicorn.run(app, host='172.25.208.1', port=8000)

