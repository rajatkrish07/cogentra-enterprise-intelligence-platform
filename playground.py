from models import UserAccount
from exceptions import ChatNotFoundError

# Object created for UserAccount class
user = UserAccount(
    username="rajatkr_07",
    email="rajatkrishnan2002@gmail.com",
    firstName="Rajat",
    lastName="Krishnan"
)

print(user.email)
user.email = "abc@gmail.com"
print(user.email)

# Creating Chats
user.create_chat("AI Masterclass")
user.create_chat("Master Python")
user.create_chat("JAVA Bootcamp")
print(user.display_chats())

#Deleting Chat with title "Master Python"

try:
    user.delete_chat("Python")
except ChatNotFoundError as e:
    print(e)

# Adding messages to the chats using title
chat = user.find_chat("JAVA Bootcamp")
chat.add_message("Welcome, Let's learn Java!")
chat.add_message("Crack Java SDE roles in 6 months")
chat.add_message("Are you excited??!!!")
print(type(chat.messages[0].timestamp))
print(type(chat.messages[0].model_dump()["timestamp"]))
print(chat.messages[0].model_dump())
print(chat.display_messages())

# Renaming Chats
user.find_chat("AI Masterclass").rename_chat("Advanced AI Masterclass")
print(user.display_chats())

# Edit Message
user.find_chat("JAVA Bootcamp").edit_message("Crack Java SDE roles in 6 months", "Crack Java SDE roles in 8 months")
print(user.find_chat("JAVA Bootcamp").display_messages())

# Dumping python dictionary to json
user.save("user_data.json")

# Loading class back from json
user = UserAccount.load("user_data.json")