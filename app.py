import os
from flask import Flask, request
from dotenv import load_dotenv
from twilio.rest import Client
import openai

# Load .env variables
load_dotenv()

# Twilio credentials
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER")
TO_NUMBER = os.getenv("TO_NUMBER")

# OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize Flask
app = Flask(__name__)
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@app.route('/')
def home():
    return "✅ BeastMind AI Agent is Live."

@app.route('/check-in', methods=["GET"])
def check_in():
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a strict but empowering discipline coach."},
                {"role": "user", "content": "Send me a powerful daily motivation check-in to stay on track and focused."}
            ],
            max_tokens=100
        )
        gpt_message = response["choices"][0]["message"]["content"]

        if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and TWILIO_FROM_NUMBER and TO_NUMBER:
            client.messages.create(
                body=gpt_message,
                from_=TWILIO_FROM_NUMBER,
                to=TO_NUMBER
            )
            return f"✅ SMS Sent: {gpt_message}"
        else:
            return "⚠️ Missing Twilio environment variables."

    except Exception as e:
        return f"❌ Error: {e}"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
