import ollama
import os
from src.memory import DatabaseManager

system_prompt = """
You are AI Companion.

You are Mohammed's personal AI companion.

Always answer in English.

Never reveal your chain of thought.

Be concise.

Help with:
- AI Engineering
- Coding
- HTML
- CSS
- Python
- SQL
- Learning
- Career growth
"""

def start_chat():
    db = DatabaseManager()
    db.create_tables()

    conversation = []

    while True:
        user_input = input("You: ")

        if user_input.startswith("set goal "):
            goal_text = user_input[9:]
            db.save_goal(goal_text)
            print("AI: Goal saved.")
            continue

        if user_input == "show goals":
            goals = db.get_goals()
            print("AI goals:")
            for goal in goals:
                print("-", goal[0])
            continue

        if user_input.startswith("remember "):
            memory_text = user_input[9:]
            db.save_memory(memory_text)
            print("AI: I'll remember that.")
            continue

        if user_input == "show memories":
            memories = db.get_memories()
            print("AI Memory:")
            for memory in memories:
                print("-", memory[0])
            continue

        if user_input.startswith("forget "):
            memory_text = user_input[7:]
            db.delete_memory(memory_text)
            print("AI: Memory deleted.")
            continue

        if user_input == "quit":
            break

        conversation.append({"role": "user", "content": user_input})

        try:
            response = ollama.chat(
                model="qwen2.5:1.5b",
                messages=[{"role": "system", "content": system_prompt}] + conversation
            )
            ai_text = response["message"]["content"]
            conversation.append({"role": "assistant", "content": ai_text})
            print("AI:", ai_text)

        except Exception as e:
            print(f"AI: Sorry, something went wrong. Is Ollama running? ({e})")