import asyncio # wait for certain conditions before performing
from fastapi import FastAPI, HTTPException # API handling
from revChatGPT.V1 import Chatbot # used to connect to gpt
import uvicorn # used for starting api server
from pydantic import BaseModel
import pdb # user for debugging
import json
import ssl
import ssl

context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE


# uvicorn main:app --reload
# http://127.0.0.1:8000/docs
# ngrok http (port # here)
'''
- with ngrok everytime you run it, a new url will be generated
- this means even when starting a new server ngrok will need to be re-ran 
'''

app = FastAPI()

class User(BaseModel):
    email: str
    password: str

# Define the chatbot variable in the global scope
chatbot = None

@app.post("/login/")
async def login(user: User):
    success = gptVerify(user.email, user.password)
    if success:
        return {"message": "Login successful"}
    else:
        return {"message": "Login failed"}

"""
def get_last_message(response: str) -> str:
    json_data = json.loads(response)
    last_msg = json_data['response'][-1]['message']
    return last_msg
"""
@app.post("/ask/")
async def ask(prompt: str):
    if chatbot is None:
        return {"error": "Chatbot not initialized. Please log in first."}
    else:
        print(prompt)
        # retrieve the text from chatgpt
        response = chatbot.ask(prompt)
        # store the text into a list
        response_list = list(response)
        # view only the last response from the json body
        last_message = response_list[-1]

        # write last message to file
        with open('last_response.txt', 'w') as outfile:
            json.dump({"response": last_message}, outfile)

        return {"response": last_message}

def gptVerify(email: str, password: str) -> bool:
    try:
        global chatbot
        chatbot = Chatbot(config={
            "email": email,
            "password": password
        })
        return True
        # rest of the function
    except Exception as e:
        print("Error establishing connection with server, please try again later:", e)
        return False
