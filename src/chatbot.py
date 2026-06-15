from dotenv import load_dotenv
import os
from google import genai
from src.memory import save_memory,get_memories
# Load .env file
load_dotenv()

# Read API key
api_key = os.getenv("GEMINI_API_KEY")

# Create Gemini client
client = genai.Client(api_key=api_key)

# AI personality
system_prompt = """
You are AI Companion.

You are Mohammed's personal AI companion.

You help with:
- AI Engineering
- Coding
- Productivity
- Mindfulness
- Fitness
- Learning

Be friendly and concise.
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

        if user_input == "quit":
            break

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=system_prompt + "\n" + "\n".join(conversation)
        )

        conversation.append(f"AI: {response.text}")

        print("AI:", response.text)


    with open("data/conversation.txt", "w", encoding="utf-8") as file:
        file.write("\n".join(conversation))