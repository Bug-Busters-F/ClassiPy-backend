from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.services.agent_service import AgentService

router = APIRouter()
agent_service = AgentService()

class PromptRequest(BaseModel):
    prompt: str

@router.post("/run")
async def run_agent(request: PromptRequest):
    try:
        response = agent_service.run(request.prompt)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
