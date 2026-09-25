import time
from google import genai
from google.genai import errors
from config import API_KEY

client = genai.Client(api_key=API_KEY)

PRIMARY_MODEL = "gemini-flash-latest"
BACKUP_MODEL = "gemini-3.5-flash-lite"

def try_model(model_name, history, message, max_retries=2):
    chat = client.chats.create(model=model_name, history=history)
    for attempt in range(max_retries):
        try:
            return chat.send_message(message), chat
        except errors.ServerError:
            if attempt < max_retries - 1:
                print(f"({model_name} busy, retrying...)")
                time.sleep(3)
            else:
                raise

def main():
    print("AI Chatbot (type 'quit' to exit)")

    current_model = PRIMARY_MODEL
    chat = client.chats.create(model=current_model)

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == "quit":
            print("Goodbye!")
            break

        history = chat.get_history()

        try:
            response, chat = try_model(current_model, [] if current_model == PRIMARY_MODEL else history, user_input)
            print(f"Bot: {response.text}")
        except errors.ServerError:
            if current_model == PRIMARY_MODEL:
                print(f"({PRIMARY_MODEL} unavailable, switching to backup model...)")
                current_model = BACKUP_MODEL
                try:
                    response, chat = try_model(current_model, history, user_input)
                    print(f"Bot: {response.text}")
                except errors.ServerError:
                    print("Bot: Sorry, both models are too busy right now. Try again in a bit.")
            else:
                print("Bot: Sorry, the server is too busy right now. Try again in a bit.")

if __name__ == "__main__":
    main()