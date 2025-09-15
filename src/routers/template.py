from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def templateMessage():
    return {"message": "Template Message"}
