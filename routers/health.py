from fastapi import APIRouter

health_router = APIRouter(
    prefix="/health",
    tags=["health"]
)

# App's health check
@health_router.get("")
def health_check():
    return {
        "status": "ok",
        "service": "cogentra"
    }