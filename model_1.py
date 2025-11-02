from dotenv import load_dotenv
from random import choice
from flask import Flask, request
import os
import openai
from database import db_controller

controller = db_controller.db_controller()

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
completion = openai.Completion()

start_sequence = "\nBot:"
restart_sequence = "\n\nPerson:"
first_impression = "\nYou are talking with S_Cb. A sentimental chatbot built using GPT-3 with fine tunning towards gaming. This sentimental chatbot will allow you to have a smooth interaction in various topics, while trying to keep track of your emotions through your sentences.\n\nPerson: Who are you?\nBot: I am S_Cb. A sentimental chatbot built using GPT-3 and ready to help you.\n\nPerson: How are you \nBot: I am doing great! Thanks for asking. \n\nPerson: Can you guess my feelings?\nBot: Yes I can, it is part of my functionalities.\n\nPerson: What is your favorite thing to do? \nBot: Looking for gaming news and share it with people as well as getting to know how you're feeling. \n\nPerson: What should I do to become famous? \nBot: You should just be you. Famous or not, you are enough."
ChatLog = None;

def ask(question, chat_log=None):
    prompt_text = f'{chat_log}{restart_sequence}: {question}{start_sequence}:'
    response = openai.Completion.create(
      engine="text-davinci-002",
      prompt=prompt_text,
      temperature=0.9,
      max_tokens=150,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0.6,
      stop=[" Person:", " Bot:"]
    )
    story = response['choices'][0]['text']
    return str(story)

    
def return_ChatLog_Line(question, answer):
    new_ChatLog_Line = f'{restart_sequence} {question}{start_sequence}{answer}'
    return new_ChatLog_Line;
    
'''
def return_ChatLog(self, username):
    self.ChatLog = controller.get_ChatLog(username);
    if ChatLog is None:
        ChatLog = first_impression
    return ChatLog;
        
    #new_ChatLog_Line = return_ChatLog_Line(question, answer);
    #new_ChatLog = f'{chat_log}', new_ChatLog_Line;
    #print(new_ChatLog);
    #self.ChatLog = new_ChatLog;
'''
'''
def append_first_impression(username):
    first_chatlog = first_impression;
    controller.add_Chatlog(username, first_chatlog);
'''
