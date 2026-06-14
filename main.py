from dotenv import load_dotenv
import os
from google import genai

#load .env file
load_dotenv()


#Read API key

api_key=os.getenv("GEMINI_API_KEY")


#Create Gemini client
client = genai.Client(api_key=api_key)

#Send a message
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents = "Say hello to Mohammed and tell him you are his AI Companion"
)


print(response.text)


while True:
    user_input=input("You: ")
    if user_input=="quit":
        break
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents = user_input
    )

    print("AI:",response.text)
    

