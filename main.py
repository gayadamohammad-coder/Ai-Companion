from src.memory import create_database, create_goals_table
from src.chatbot import start_chat

create_database()
create_goals_table()

start_chat()