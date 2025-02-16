"""
Authentication utilities for managing user data.

This module provides functions for loading and saving user data from a JSON file,
as well as securely hashing passwords for storage.

Attributes:
    USERS_FILE (Path): The file system path to the users.json data file.

Methods:
    load_users(): Loads user data from the users.json file.
    save_users(users): Saves user data to the users.json file.
    hash_password(password): Hashes a password for secure storage.
"""

import json
from pathlib import Path
import hashlib
from hmac import compare_digest

# Initialize users.json if it doesn't exist
USERS_FILE = Path("users.json")
if not USERS_FILE.exists():
    USERS_FILE.write_text('{}')

def load_users():
    """
    Loads user data from the users.json file.

    Returns:
        dict: A dictionary containing the user data.
    """
    return json.loads(USERS_FILE.read_text())

def save_users(users):
    """
    Saves user data to the users.json file.

    Args:
        users (dict): A dictionary containing the user data to save.
    """
    USERS_FILE.write_text(json.dumps(users, indent=2))

def hash_password(password):
    """
    Hashes a password for secure storage using SHA-256.

    Args:
        password (str): The password to hash.

    Returns:
        str: The hashed password as a hexadecimal string.
    """
    return hashlib.sha256(password.encode()).hexdigest()