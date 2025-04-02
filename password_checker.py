import re
import math
import requests
from zxcvbn import zxcvbn

def calculate_entropy(password):
    if not password:
        return 0
    entropy = 0
    char_set = set(password)
    for char in char_set:
        p = password.count(char) / len(password)
        entropy -= p * math.log2(p)
    return round(entropy, 2)

def check_password_strength(password):
    criteria = {
        "length": len(password) >= 8,
        "uppercase": bool(re.search(r"[A-Z]", password)),
        "lowercase": bool(re.search(r"[a-z]", password)),
        "digit": bool(re.search(r"\d", password)),
        "special_char": bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)),
    }

    entropy = calculate_entropy(password)
    breached = is_password_breached(password)

    strength = "Strong" if all(criteria.values()) and entropy > 3.5 and not breached else "Weak"

    return {
        "Password": password,
        "Entropy": entropy,
        "Breached": breached,
        "Strength": strength
    }

def is_password_breached(password):
    hashed_pw = requests.get(f"https://api.pwnedpasswords.com/range/{password[:5]}").text
    return password in hashed_pw
