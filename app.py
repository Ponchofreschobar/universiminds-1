from flask import Flask, request
from twilio.rest import Client
import openai
import os
from db import log_action
from datetime import datetime

app = Flask(__name__)

# Set environment vars
openai.api_key = os.getenv("OPENAI_API_KEY")
twilio_sid = os.getenv("TWILIO_ACCOUNT_SID")
twilio_auth = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_PHONE_NUMBER")
user_number = os.getenv("USER_PHONE_NUMBER")

client = Client(twilio_sid, twilio_auth)

@app.route("/", methods=["GET"])
def home():
    return "UniversiMinds Agent is running."

@app.route("/check-in", methods=["GET"])
def send_checkin():
    today = datetime.now().strftime("%A, %B %d")
    prompt = f"Create a 2-line motivational check-in for someone pushing through mental fatigue. Focus: Discipline, Momentum. Date: {today}"
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        ai_message = response.choices[0].message.content.strip()

        client.messages.create(
            body=f"UniversiMinds Check-In:\n{ai_message}",
            from_=twilio_number,
            to=user_number
        )

        log_action("check-in", ai_message)
        return "Check-in sent successfully."

    except Exception as e:
        return f"Error: {str(e)}"
