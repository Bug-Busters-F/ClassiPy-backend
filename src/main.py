from fastapi import FastAPI
from src.routers import template, uploadfile, agent

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Classipy API is running"}

# Adicionar os roteadores da aplicação
app.include_router(agent.router, prefix="/agent", tags=["agent"])
app.include_router(template.router, prefix="/template", tags=["template"])
app.include_router(uploadfile.router, prefix="/uploadfile", tags=["uploadfile"])
