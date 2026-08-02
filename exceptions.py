from pydantic import EmailStr

# Domain Exceptions
class UserNotFoundError(Exception):
    def __init__(self, user_id: str):
        self.user_id = user_id
        super().__init__(f"User {user_id} was not found.")

class ChatNotFoundError(Exception):
    def __init__(self, chat_id: str):
        self.chat_id = chat_id
        super().__init__(f"Chat {chat_id} was not found.")

class MessageNotFoundError(Exception):
    def __init__(self, message_id: str):
        self.message_id = message_id
        super().__init__(f"Message {message_id} was not found.")

class AIResponseNotFoundError(Exception):
    def __init__(self, ai_response_id: str):
        self.message_id = ai_response_id
        super().__init__(f"AIResponse {ai_response_id} was not found.")

class DuplicateChatError(Exception):
    pass

class DuplicateEmailError(Exception):
    pass

class NoEmailChangeError(Exception):
    def __init__(self, email: EmailStr):
        self.email = email
        super().__init__(f"New email can't be same as the current email.")


class ChatRenameError(Exception):
    pass

