import datetime

def log_action(action_type, message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {action_type.upper()}: {message}")
