import json
import os

USER_DATA_FILE = "users.json"

def load_users():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USER_DATA_FILE, "w") as f:
        json.dump(users, f, indent=2)

def register_user(email_or_phone, password):
    users = load_users()
    if email_or_phone in users:
        return False  # User already exists
    users[email_or_phone] = password
    save_users(users)
    return True

def login_user(email_or_phone, password):
    users = load_users()
    return users.get(email_or_phone) == password