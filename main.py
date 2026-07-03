import os
import json
from datetime import datetime

# Manages all the operations like creating user and managing chats
class UserAccount:

  def __init__(self, username, email):
    self.username = username
    self.__email = email
    self.chats = []


  def to_dict(self):
      return{
          "username": self.username,
          "email": self.__email,
          "chats": [chat_obj.to_dict() for chat_obj in self.chats]
      }

  @classmethod
  def from_dict(cls, data):
      username = data["username"]
      email = data["email"]
      user = cls(username, email)

      for chat in data["chats"]:
          user.chats.append(Chat.from_dict(chat))
      return user

  # Renaming or setting new email
  @property
  def email(self):
    return self.__email

  @email.setter
  def email(self, new_email):
    if self.__email != new_email:
      self.__email = new_email

    else:
      print("You cannot use previous email id")

  # Display chats
  def display_chats(self):
    return self.chats.copy()

  # Creates new chat object
  def create_chat(self, title):
    chat_obj = Chat(title)
    self.chats.append(chat_obj)

  # Find chats
  def find_chat(self, title):
      for my_chat in self.chats:
          if my_chat.title == title:
              return my_chat
      return None

  # Delete chats
  def delete_chat(self, title):
      chat = self.find_chat(title)
      if chat:
          self.chats.remove(chat)

  # Displays user profile details (username and email)
  @property
  def profile(self):
    return f"Username: {self.username}\nEmail: {self.__email}"

  def save(self, filename):
      with open(filename, "w") as my_file:
          json.dump(
              self.to_dict(),
              my_file,
              indent=4
          )

  @classmethod
  def load(cls, filename):
      with open(filename, "r") as my_file:
          my_dict = json.load(my_file)
      return cls.from_dict(my_dict)

# Manages state of the chat like attributes and features
class Chat:
    def __init__(self, title):
        self.title = title
        self.messages = []

    def to_dict(self):
        return{
            "title": self.title,
            "messages": [msg.to_dict() for msg in self.messages]
        }

    @classmethod
    def from_dict(cls, data):
        chat = cls(data["title"])
        for msg in data["messages"]:
            chat.messages.append(Message.from_dict(msg))
        return chat

    # Display messages
    def display_messages(self):
        return self.messages.copy()

    # Adds new messages
    def add_message(self, text):
        timestamp = datetime.now()
        msg = Message(timestamp, text)
        self.messages.append(msg)

    # Edit existing messages
    def edit_message(self, text, new_text):
        for msg in self.messages:
            if msg.text == text:
                msg.text = new_text
                break

    # Rename chats
    def rename_chat(self, new_title):
        if self.title != new_title:
            self.title = new_title
        else:
            print("New title is same as current title.")

    # Deletes messages
    def delete_message(self, text):
        for msgs in self.messages:
            if msgs.text == text:
                self.messages.remove(msgs)
                break

    # Dunder methods to instruct python to display in proper format instead of memory address
    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title

class Message:
    def __init__(self, timestamp, text):
        self.timestamp = timestamp
        self.text = text

    def to_dict(self):
        return{
            "timestamp": self.timestamp.isoformat(),
            "text": self.text
        }
    @classmethod
    def from_dict(cls, data):
        timestamp = datetime.fromisoformat(data["timestamp"])
        text = data["text"]

        return cls(timestamp, text)

    def __str__(self):
        return f"{self.timestamp}: {self.text}"

    def __repr__(self):
        return f"{self.timestamp}: {self.text}"

user = UserAccount("rajatkr_07", "rajatkrishnan2002@gmail.com")
# user_file = json.dump(user.to_dict())

# Creating Chats
user.create_chat("AI Masterclass")
user.create_chat("Master Python")
user.create_chat("JAVA Bootcamp")
print(user.display_chats())

#Deleting Chat with title "Master Python"
user.delete_chat("Master Python")
print(user.display_chats())

# Adding messages to the chats using title
chat = user.find_chat("JAVA Bootcamp")
chat.add_message("Welcome, Let's learn Java!")
chat.add_message("Crack Java SDE roles in 6 months")
chat.add_message("Are you excited??!!!")
print(type(chat.messages[0].timestamp))
print(chat.messages[0].to_dict())
print(chat.display_messages())

# Renaming Chats
user.find_chat("AI Masterclass").rename_chat("Advanced AI Masterclass")
print(user.display_chats())

# Deleting Message
user.find_chat("JAVA Bootcamp").delete_message("Are you excited??!!!")
print(user.find_chat("JAVA Bootcamp").display_messages())
#
# # Edit Message
user.find_chat("JAVA Bootcamp").edit_message("Crack Java SDE roles in 6 months", "Crack Java SDE roles in 8 months")
print(user.find_chat("JAVA Bootcamp").display_messages())

# Dumping python dictionary to json
user.save("user_data.json")

# Loading class back from json
user = UserAccount.load("user_data.json")

# Returns Class 
print(user)

