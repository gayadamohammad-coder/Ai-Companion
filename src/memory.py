import sqlite3
from config import DB_PATH
try:
    from sentence_transformers import SentenceTransformer
    from sentence_transformers.util import cos_sim
    EMBEDDINGS_AVAILABLE = True
except ImportError:
    EMBEDDINGS_AVAILABLE = False
import json

class DatabaseManager:
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2') if EMBEDDINGS_AVAILABLE else None

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

    def search_memories(self, query, top_n=3):
        if not EMBEDDINGS_AVAILABLE or self.embedding_model is None:
            return [(m[0], 0) for m in self.get_memories()]
        memories = self.get_memories()
        query_embedding = self.embedding_model.encode(query)
        results = []
        for memory_text, embedding_json in memories:
            stored_embedding = json.loads(embedding_json)
            similarity = cos_sim(query_embedding, stored_embedding)
            results.append((memory_text, similarity))
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_n]

    def save_memory(self, memory_text):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        if EMBEDDINGS_AVAILABLE and self.embedding_model:
            embedding = self.embedding_model.encode(memory_text)
            embedding_json = json.dumps(embedding.tolist())
        else:
            embedding_json = json.dumps([])
        cursor.execute(
            "INSERT INTO memories (memory_text, embedding) VALUES (?, ?)",
            (memory_text, embedding_json,)
        )
        conn.commit()
        conn.close()

    def get_memories(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT memory_text, embedding FROM memories")
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
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT role, content FROM chat_history
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
                date_added TEXT NOT NULL,
                current_concept TEXT,
                quiz_score INTEGER DEFAULT 0,
                total_questions INTEGER DEFAULT 0,
                last_updated TEXT
            )
        """)
        conn.commit()
        conn.close()


    NTFY_TOPIC = "jarvis-mohammed-7x9k"

    def send_notification(title, message):
        req.post(f"https://ntfy.sh/{NTFY_TOPIC}", data=message, headers={"Title": title, "Priority": "default"})

    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: send_notification("🌅 Morning", "Good morning Mohammed! Time to give thanks to God. Alhamdulillah for a new day."), "cron", hour=6, minute=0)
    scheduler.add_job(lambda: send_notification("🕌 Prayer", "Time to pray Mohammed. Don't delay it."), "cron", hour=9, minute=0)
    scheduler.add_job(lambda: send_notification("💧 Water & Food", "Mohammed, drink water and eat something. Your body needs fuel."), "cron", hour=16, minute=0)
    scheduler.add_job(lambda: send_notification("🌙 Mindfulness", "End your day with gratitude. Take a moment to thank God for everything today."), "cron", hour=22, minute=0)
    scheduler.start()
    def save_progress(self, topic, current_concept, quiz_score, total_questions):
        from datetime import datetime
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        now = datetime.now().isoformat()
        cursor.execute("""
            INSERT INTO learning_topics (topic, status, date_added, current_concept, quiz_score, total_questions, last_updated)
            VALUES (?, 'in_progress', ?, ?, ?, ?, ?)
            ON CONFLICT(topic) DO UPDATE SET
                current_concept = excluded.current_concept,
                quiz_score = excluded.quiz_score,
                total_questions = excluded.total_questions,
                status = 'in_progress',
                last_updated = excluded.last_updated
        """, (topic, now, current_concept, quiz_score, total_questions, now))
        conn.commit()
        conn.close()

    def get_progress(self, topic):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT current_concept, quiz_score, total_questions, last_updated
            FROM learning_topics WHERE topic = ?
        """, (topic,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return {
                'current_concept': row[0],
                'quiz_score': row[1],
                'total_questions': row[2],
                'last_updated': row[3]
            }
        return None