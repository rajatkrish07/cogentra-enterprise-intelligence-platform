import time
import uuid
from starlette import status
from datetime import datetime
from dependencies import get_api_version, get_message
from models import UserAccount, Message, AIResponse
from schemas import UserResponse, AdminUserResponse, AIUserResponse ,GenerateAIResponse, RegenerateAIResponse, ResponseHistorySchema
from exceptions import UserNotFoundError, ChatNotFoundError, MessageNotFoundError, AIResponseNotFoundError
from fastapi import FastAPI, Query, Path, Header, Depends, Request, HTTPException
from fastapi.responses import JSONResponse
from logger import logger

# app -> FastAPI Application object
app = FastAPI()

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

# Global Exception Handler (Exception -> HTTP Response)

@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception
):

    logger.exception(f"{exc}")
    return JSONResponse(
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error":{
                "code": "INTERNAL SERVER ERROR",
                "message": str(exc)
            },
            "request_id": request.state.request_id
        }
    )

# Global Exception Handler (Domain Exception -> HTTP Response)

# For No User Found
@app.exception_handler(UserNotFoundError)
async def handle_user_not_found(
    request: Request,
    exc: UserNotFoundError
):

    logger.warning(str(exc))

    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "success": False,
            "error": {
                "code": "USER_NOT_FOUND",
                "message": str(exc)
            },
            "request_id": request.state.request_id
        }
    )

# For No Chats Found
@app.exception_handler(ChatNotFoundError)
async def handle_chat_not_found(
    request: Request,
    exc: ChatNotFoundError
):

    logger.warning(str(exc))

    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "success": False,
            "error": {
                "code": "CHAT_NOT_FOUND",
                "message": str(exc)
            },
            "request_id": request.state.request_id
        }
    )

# For No Message Found
@app.exception_handler(MessageNotFoundError)
async def handle_message_not_found(
    request: Request,
    exc: MessageNotFoundError
):

    logger.warning(str(exc))

    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "success": False,
            "error": {
                "code": "MESSAGE_NOT_FOUND",
                "message": str(exc)
            },
            "request_id": request.state.request_id
        }
    )
# For No AI Response Found
@app.exception_handler(AIResponseNotFoundError)
async def handle_ai_response_not_found(
    request: Request,
    exc: AIResponseNotFoundError
):
    logger.warning(str(exc))

    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "success": False,
            "error": {
                "code": "AI_RESPONSE_NOT_FOUND",
                "message": str(exc)
            },
            "request_id": request.state.request_id
        }
    )

# Different User Displays
@app.get("/admin/users", response_model=AdminUserResponse)
def admin_display(user: UserAccount):
    return user

@app.get("/users", response_model=UserResponse)
def user_display(user: UserAccount):
    return user

@app.get("/ai/users", response_model=AIUserResponse)
def ai_display(user: UserAccount):
    return user

# Welcome page
@app.get("/")
def welcome_user():
    return {"message": "Welcome User!"}

# App's health check
@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "cogentra"
    }

# Path Parameter

# Fetching user info by id

@app.get("/users/{user_id}")
def get_user(
        user_id: int = Path(
            ...,
            ge=1,
            title="User ID",
            description="Unique identifier of the user",
            examples=[1]
        )
):
    return {
        "requested_user": user_id
    }

# Fetching user info by name
@app.get("/users")
def search_users(
        name: str | None= Query(
            None,
            title="User Name",
            min_length=2,
            max_length=50,
            description="Search users by username",
        )):
    return {
        "searched_name": name
    }

# Header param
@app.get("/profile")
def profile(
        authorization: str = Header(
            ...,
            description="JWT Bearer Token"
        )
):
    return {
        "token": authorization
    }

# Generates the message
@app.post("/chats/{chat_id}/messages/{message_id}/generate", response_model=GenerateAIResponse, status_code=status.HTTP_201_CREATED)
def create_ai_response(
    version: str = Depends(get_api_version),
    message: Message = Depends(get_message)
):

    return {
        "chat_id": message.chat_id,
        "message_id": message.id,
        "user_prompt": message.text,
        "ai_response": "Dependency Injection allows...",
        "version": version
    }

# Regenerates the response and adds it to a list for persistence
@app.post("/chats/{chat_id}/messages/{message_id}/regenerate",response_model=RegenerateAIResponse, status_code=status.HTTP_201_CREATED)
def regenerate_ai_response(
        message: Message = Depends(get_message)
):
    new_response = AIResponse(
        id="resp_009",
        text="This is a regenerated AI response.",
        created_at=datetime.now()
    )

    message.responses.append(new_response)

    return{
        "message": "AI response regenerated successfully.",
        "response": new_response
    }

# Displays all the responses generated
@app.get("/chats/{chat_id}/messages/{message_id}/responses", response_model=ResponseHistorySchema, status_code=status.HTTP_200_OK)
def get_response_history(
        message: Message = Depends(get_message)
):

    return{
        "message": "Responses retrieved successfully.",
        "responses": message.responses
    }

# Exception Handling Test
@app.get("/error")
async def error():
    raise Exception("Something went wrong!")

@app.get("/not-found")
async def not_found():
    raise HTTPException(status_code=404, detail="User not found")
