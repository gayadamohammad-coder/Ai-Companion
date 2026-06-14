from dotenv import load_dotenv
import os
from google import genai

#load .env file
load_dotenv()


#Read API key

api_key=os.getenv("GEMINI_API_KEY")


#Create Gemini client
client = genai.Client(api_key=api_key)


conversation = []

while True:
    user_input=input("You: ")
    conversation.append(f"User:{user_input}")
    if user_input=="quit":
        break
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="\n".join(conversation)
    )

    conversation.append(f"AI:{response.text}")

    print("AI:",response.text)
    

