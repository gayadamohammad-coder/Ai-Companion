import sqlite3

def create_database():
    conn = sqlite3.connect("data/companion.db")

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS memories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        memory_text TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()


def save_memory(memory_text):
    conn = sqlite3.connect("data/companion.db")

    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO memories (memory_text) VALUES (?)",
        (memory_text,)
    )

    conn.commit()
    conn.close()


def get_memories():
    conn = sqlite3.connect("data/companion.db")

    cursor = conn.cursor()

    cursor.execute("SELECT memory_text FROM memories")

    memories = cursor.fetchall()

    conn.close()

    return memories