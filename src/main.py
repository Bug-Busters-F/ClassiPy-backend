from fastapi import FastAPI
from src.routers import template, uploadfile, agent

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Server Running..."}

app.include_router(template.router, prefix="/template")
app.include_router(uploadfile.router, prefix="/uploadfile")
app.include_router(agent.router, prefix="/agent")
