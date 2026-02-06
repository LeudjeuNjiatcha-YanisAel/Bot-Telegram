# core/users.py
import json
import os
from Config.config import USERS_FILE

users = {}

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            try:
                users = json.load(f)
            except:
                users = {}

def save_users():
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)
