from fastapi import APIRouter

__all__ = ["router"]

router = APIRouter()


@router.get("/")
async def health_check():
    return "OK"
