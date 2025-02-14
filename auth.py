import json
from pathlib import Path
import hashlib
from hmac import compare_digest

# Initialize users.json if it doesn't exist
USERS_FILE = Path("users.json")
if not USERS_FILE.exists():
    USERS_FILE.write_text('{}')

def load_users():
    return json.loads(USERS_FILE.read_text())

def save_users(users):
    USERS_FILE.write_text(json.dumps(users, indent=2))

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest() 