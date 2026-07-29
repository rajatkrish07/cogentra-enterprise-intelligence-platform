from fastapi import APIRouter, HTTPException

debug_router = APIRouter(
    prefix="/debug",
    tags=["Debug"]
)

# Exception Handling Test
@debug_router.get("/error")
async def error():
    raise Exception("Something went wrong!")

@debug_router.get("/not-found")
async def not_found():
    raise HTTPException(status_code=404, detail="User not found")