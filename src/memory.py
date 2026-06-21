import sqlite3
from config import DB_PATH
from sentence_transformers import SentenceTransformer
import json

class DatabaseManager:
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path

    def create_tables(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                memory_text TEXT NOT NULL,
                embedding TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                goal_text TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    def save_memory(self, memory_text):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        embedding=self.embedding_model.encode(memory_text)
        embedding_json=json.dumps(embedding.tolist())
        cursor.execute(
            "INSERT INTO memories (memory_text,embedding) VALUES (?,?)",
            (memory_text,embedding_json,)
        )
        conn.commit()
        conn.close()

    def get_memories(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT memory_text FROM memories")
        memories = cursor.fetchall()
        conn.close()
        return memories

    def delete_memory(self, memory_text):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM memories WHERE memory_text = ?",
            (memory_text,)
        )
        conn.commit()
        conn.close()

    def save_goal(self, goal_text):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO goals (goal_text) VALUES (?)",
            (goal_text,)
        )
        conn.commit()
        conn.close()

    def get_goals(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT goal_text FROM goals")
        goals = cursor.fetchall()
        conn.close()
        return goals
    

    def create_chat_history_table(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
             """)
        conn.commit()
        conn.close()

    

    def save_message(self, role, content):
        from datetime import datetime
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO chat_history (role, content, timestamp) VALUES (?, ?, ?)",
            (role, content, datetime.now().isoformat())
        )
        conn.commit()
        conn.close()

    def get_chat_history(self):
        conn=sqlite3.connect(self.db_path)
        cursor=conn.cursor()
        cursor.execute("""
                    SELECT role,content FROM chat_history
                    ORDER BY id ASC
                       """)
        chat_history = cursor.fetchall()
        conn.close()
        return chat_history
    

    def create_learning_table(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS learning_topics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT NOT NULL,
            status TEXT NOT NULL,
            date_added TEXT NOT NULL
             )
        """)
        conn.commit()
        conn.close()
    