import sqlite3
from config import DB_PATH

class DatabaseManager:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path

    def create_tables(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                memory_text TEXT NOT NULL
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
        cursor.execute(
            "INSERT INTO memories (memory_text) VALUES (?)",
            (memory_text,)
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