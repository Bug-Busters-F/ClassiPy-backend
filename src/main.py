from fastapi import FastAPI
from src.routers import template, uploadfile, agent, product
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5173", 
    "http://127.0.0.1:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Classipy API is running"}

app.include_router(template.router, prefix="/template")
app.include_router(uploadfile.router, prefix="/uploadfile")
app.include_router(agent.router, prefix="/agent")
app.include_router(product.router)