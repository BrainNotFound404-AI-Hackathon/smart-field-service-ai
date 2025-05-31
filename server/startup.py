from fastapi import FastAPI
import sys
import json
from pathlib import Path

from api.prompt_API import run_prompt


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
    app.include_router(chat_router)


if __name__ == "__main__":
    app = create_app()
    import uvicorn

    uvicorn.run(app, host='172.25.208.1', port=8000)

    '''
    ------------------------------------------pre_operation-------------------------------------
    '''
    base_path = Path("data/")
    with open(base_path / "alerts.json", "r", encoding="utf-8") as f:
        alerts_data = json.load(f)
    with open(base_path / "maintenance_logs.json", "r", encoding="utf-8") as f:
        maintenance_logs_data = json.load(f)
    with open(base_path / "manual_fragments.json", "r", encoding="utf-8") as f:
        manual_fragments_data = json.load(f)

    structured_prompt = f"""
    You are now an experienced elevator maintenance AI assistant. Based on the following information, 
    please generate a "Key Troubleshooting Recommendations" for the current issue. 
    The alarm code represents the current issue. 
    If there is no error code, it means the action is correct. The output should be well-structured, 
    clearly highlight high-priority checks, and refer to the manual references and common pitfalls.

    Alarm Code Information:
    {json.dumps(alerts_data, indent=2)}

    Maintenance History:
    {json.dumps(maintenance_logs_data, indent=2)}

    Equipment Manual Excerpts:
    {json.dumps(manual_fragments_data, indent=2)}

    Please output your response in the following structure:
    1. High-Priority Checks and Error Codes
    2. Recommended Troubleshooting Procedure
    3. Common Pitfalls and Cautions
    4. Relevant Manual References (summary)
    """

    result = run_prompt(structured_prompt)
    print("🔧 Troubleshooting Recommendation:\n")
    print(result)
    #-----------------------------------------------------------------------------------------

    '''
    ---------------------------------------On-site operation----------------------------------
    '''




    #-----------------------------------------------------------------------------------------

    '''
    ----------------------------------------Post operation------------------------------------
    '''
  

