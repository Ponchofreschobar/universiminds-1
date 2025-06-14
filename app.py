import os
# After all imports
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

# Then define your fetch_google_calendar_events() here

from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from dotenv import load_dotenv
from openai import OpenAI
from twilio.rest import Client
from apscheduler.schedulers.background import BackgroundScheduler

# Top
def send_weekly_summary():
# Load secrets
load_dotenv()

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Init OpenAI and Twilio
openai = OpenAI(api_key=os.getenv("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"))
twilio_client = Client(os.getenv("ACb7c1750d3cce41aa248d38c2786e500b"), os.getenv("15a19cdfb95b00b3e82571aeebf4ae85"))

TO_NUMBER = os.getenv("+9787905454")
FROM_NUMBER = os.getenv("+18884657356")

# 🔁 Scheduled task: Daily reminder via SMS
def send_daily_checkin():
    chat = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a supportive but strict accountability coach."},
            {"role": "user", "content": "Send my daily wakeup message and productivity challenge."}
        ]
    )
    msg = chat.choices[0].message.content.strip()
    twilio_client.messages.create(body=msg, from_=FROM_NUMBER, to=TO_NUMBER)

# Schedule every morning 8 AM
scheduler = BackgroundScheduler()
scheduler.add_job(send_daily_checkin, 'cron', hour=8)
scheduler.start()
# Bottom (with scheduler):
scheduler.add_job(send_weekly_summary, 'cron', day_of_week='sun', hour=20)
# 🌐 Routes
@app.route('/')
def home():
    return "✅ UniversiMinds AI Agent is Running"

@app.route('/check-in', methods=["GET"])
def manual_checkin():
    send_daily_checkin()
    return jsonify({"status": "✅ SMS Sent"})

@app.route('/mood', methods=['GET', 'POST'])
def mood():
    if request.method == 'POST':
        mood = request.form['mood']
        # Save to file or database
        with open('mood_log.txt', 'a') as f:
            f.write(f"{datetime.now()}: {mood}\n")
        return "Mood logged!"
    return '''
        <form method="post">
            How are you feeling? <input name="mood" type="text">
            <input type="submit">
        </form>

# 💬 Real-time chat
@socketio.on('user_message')
def handle_user_message(data):
    user_text = data.get("message", "")
    chat_response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a hyper-aware, always-on personal assistant and discipline coach."},
            {"role": "user", "content": user_text}
        ]
    )
    bot_reply = chat_response.choices[0].message.content.strip()
    emit('bot_reply', {"reply": bot_reply})

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
