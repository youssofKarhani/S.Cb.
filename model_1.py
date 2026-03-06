from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini with the modern SDK
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Use the fast, free Gemini 1.5 Flash model
MODEL_ID = "gemini-1.5-flash"

start_sequence = "\nBot:"
restart_sequence = "\n\nPerson:"
first_impression = "You are talking with S_Cb. A sentimental chatbot built using Google Gemini with fine-tuning towards gaming. This sentimental chatbot will allow you to have a smooth interaction in various topics, while trying to keep track of user emotions."

def ask(question, chat_log=""):
    # Combine history + current question into a single prompt for context
    full_prompt = f"{first_impression}\n{chat_log}\n{restart_sequence} {question}{start_sequence}"
    
    try:
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=full_prompt
        )
        return response.text.strip()
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return "Sorry, my brain hit a snag. Try again later!"

def return_ChatLog_Line(question, answer):
    return f"{restart_sequence} {question}{start_sequence} {answer}"
