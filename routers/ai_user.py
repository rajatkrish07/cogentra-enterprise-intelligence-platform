from fastapi import APIRouter
from models import UserAccount
from schemas import AIUserResponse

ai_router = APIRouter(
    prefix="/ai",
    tags=["ai"]
)

@ai_router.get("/users", response_model=AIUserResponse)
def ai_display(user: UserAccount):
    return user