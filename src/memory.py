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


def delete_memory(memory_text):
    conn = sqlite3.connect("data/companion.db")

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM memories WHERE memory_text = ?",
        (memory_text,)
    )

    conn.commit()
    conn.close()


def create_goals_table():
    conn = sqlite3.connect("data/companion.db")

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS goals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        goal_text TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()

def save_goal(goal_text):
    conn=sqlite3.connect("data/companion.db")

    cursor=conn.cursor()

    cursor.execute(
        "INSERT INTO goals (goal_text) VALUES(?)",
        (goal_text,)
    )

    conn.commit()
    conn.close()

def get_goals():
    conn=sqlite3.connect("data/companion.db")

    cursor = conn.cursor()

    cursor.execute(
        "SELECT goal_text FROM goals"
    )
    goals = cursor.fetchall()
    conn.close()
    return goals


def create_profile_table():
    conn=sqlite3.connect("data/companion.db")
    
    cursor=conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS profile(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        field_name TEXT NOT NULL,
        field_value TEXT NOT NULL
        )
        """)
    conn.commit()
    conn.close()


def save_profile(field_name, field_value):
    conn = sqlite3.connect("data/companion.db")

    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO profile (field_name, field_value) VALUES (?, ?)",
        (field_name, field_value)
    )

    conn.commit()
    conn.close()