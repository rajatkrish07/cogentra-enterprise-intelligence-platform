from fastapi import APIRouter
from models import UserORM
from schemas import AdminUserResponse

admin_router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)

# Displays all info with admin rights
@admin_router.get("/users", response_model=AdminUserResponse)
def admin_display(user: UserORM):
    return user