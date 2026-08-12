from datetime import datetime
import time
import uuid
from starlette import status
from exceptions import UserNotFoundError, ChatNotFoundError, MessageNotFoundError, AIResponseNotFoundError
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from logger import logger
from routers.users import user_router
from routers.chats_router import chat_router
from routers.ai_response_router import ai_response_router
from routers.admin import admin_router
from routers.debug import debug_router
from routers.health import health_router
from contextlib import asynccontextmanager

# App Startup-Shutdown
@asynccontextmanager
async def startup_shutdown_manager(app: FastAPI):
    logger.info(f"Cogentra backend starting...")
    yield
    logger.info(f"Cogentra backend shutting down...")

# app -> FastAPI Application object
app = FastAPI(
    lifespan = startup_shutdown_manager
)

# Registering the routers with the app
app.include_router(user_router)
app.include_router(chat_router)
app.include_router(ai_response_router)
app.include_router(admin_router)
app.include_router(debug_router)
app.include_router(health_router)

# Middleware - HTTP
@app.middleware("http")
async def log_requests(
        request: Request,
        call_next
):

    # Start time
    start_time = time.perf_counter()
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    print(f"{request_id} --> {request.method} {request.url.path}")

    try:
        response = await call_next(request)
        process_time = time.perf_counter() - start_time

        # Response Customization
        response.headers["X-App-Name"] = "Cogentra"
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = f"{process_time:.4f}s"
        print(f"{request_id} <-- {response.status_code} {process_time:.4f}s")
        return response

    except Exception:
        process_time = time.perf_counter() - start_time
        print(f"{request_id} <-- Exception {process_time:.4f}s")
        raise

# Exception Handler Helper Function

def error_response(
        request: Request,
        status_code: int,
        error_code: str,
        message: str
) -> JSONResponse:

    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "error": {
                "code": error_code,
                "message": message
            },
            "request_id": request.state.request_id
        }
    )

# Global Exception Handler (Exception -> HTTP Response)

@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception
):

    logger.exception(f"Unhandled Exception: {str(exc)}")

    return error_response(
        request = request,
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
        error_code="INTERNAL_SERVER_ERROR",
        message="An unexpected error occurred."
    )

# Global Exception Handler (Domain Exception -> HTTP Response)

# For No User Found
@app.exception_handler(UserNotFoundError)
async def handle_user_not_found(
    request: Request,
    exc: UserNotFoundError
):

    logger.warning(str(exc))

    return error_response(
        request = request,
        status_code=status.HTTP_404_NOT_FOUND,
        error_code="USER_NOT_FOUND",
        message=str(exc)
    )

# For No Chats Found
@app.exception_handler(ChatNotFoundError)
async def handle_chat_not_found(
    request: Request,
    exc: ChatNotFoundError
):

    logger.warning(str(exc))

    return error_response(
        request = request,
        status_code=status.HTTP_404_NOT_FOUND,
        error_code="CHAT_NOT_FOUND",
        message=str(exc)
    )

# For No Message Found
@app.exception_handler(MessageNotFoundError)
async def handle_message_not_found(
    request: Request,
    exc: MessageNotFoundError
):

    logger.warning(str(exc))

    return error_response(
        request=request,
        status_code=status.HTTP_404_NOT_FOUND,
        error_code="MESSAGE_NOT_FOUND",
        message=str(exc)
    )

# For No AI Response Found
@app.exception_handler(AIResponseNotFoundError)
async def handle_ai_response_not_found(
    request: Request,
    exc: AIResponseNotFoundError
):
    logger.warning(str(exc))

    return error_response(
        request=request,
        status_code=status.HTTP_404_NOT_FOUND,
        error_code="AI_RESPONSE_NOT_FOUND",
        message=str(exc)
    )