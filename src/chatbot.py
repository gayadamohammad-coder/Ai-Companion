import ollama
import os
from src.memory import(
 create_database, 
    save_memory,
    get_memories,
    delete_memory,
    save_goal,
    get_goals,
    create_database,
    create_goals_table
    
    ) 



# AI personality
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
    
    if os.path.exists("data/conversation.txt"):
        with open("data/conversation.txt","r",encoding="utf-8") as files:
            conversation = files.read().splitlines()

    else:
        conversation=[]

    while True:
        user_input = input("You: ")

        conversation.append(f"User: {user_input}")

        if user_input.startswith("set goal "):
            goal_text = user_input[9:]

            save_goal(goal_text)

            print("AI: Goal saved.")

            continue

        if user_input == "show goals":
            goals = get_goals()

            print("AI goals:")
            for goal in goals:
                print("-",goal[0])
            continue

        if user_input.startswith("remember "):

            memory_text = user_input[9:]

            save_memory(memory_text)

            print("AI: I'll remember that.")

            continue

        if user_input == "show memories":

            memories = get_memories()

            print("AI Memory:")

            for memory in memories:
                print("-", memory[0])

            continue

        if user_input.startswith("forget "):

            memory_text = user_input[7:]

            delete_memory(memory_text)

            print("AI: Memory deleted.")

            continue

        if user_input == "quit":
            break

        response = ollama.chat(
            model="qwen3:4b",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": "\n".join(conversation)
                }
            ]
        )   

        ai_text = response["message"]["content"]

        conversation.append(f"AI: {ai_text}")

        print("AI:", ai_text)


    with open("data/conversation.txt", "w", encoding="utf-8") as file:
        file.write("\n".join(conversation))