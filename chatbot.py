import time
from google import genai
from google.genai import errors
from config import API_KEY

client = genai.Client(api_key=API_KEY)

def send_with_retry(chat, message, max_retries=3):
    for attempt in range(max_retries):
        try:
            return chat.send_message(message)
        except errors.ServerError:
            if attempt < max_retries - 1:
                print("(Server busy, retrying...)")
                time.sleep(3)
            else:
                raise

def main():
    print("AI Chatbot (type 'quit' to exit)")

    chat = client.chats.create(model="gemini-flash-latest")

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == "quit":
            print("Goodbye!")
            break

        try:
            response = send_with_retry(chat, user_input)
            print(f"Bot: {response.text}")
        except errors.ServerError:
            print("Bot: Sorry, the server is too busy right now. Try again in a bit.")

if __name__ == "__main__":
    main()