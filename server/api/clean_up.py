from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from server.api.chat import store

# 假设这是你的上下文存储结构
# store: Dict[str, ConversationBufferMemory] = {...}
# 它应该在别的模块中被 import 并共享

router = APIRouter()

class CleanupRequest(BaseModel):
    session_id: str

@router.post("/session/cleanup", tags=["Session"], summary="清除指定会话的上下文")
def clean_up_session(request: CleanupRequest):
    session_id = request.session_id

    if session_id in store:
        store.pop(session_id)
        return JSONResponse(status_code=200, content={
            "message": f"Session '{session_id}' context has been cleaned up."
        })
    else:
        return JSONResponse(status_code=404, content={
            "error": f"Session '{session_id}' not found."
        })
