import os

FIREBASE_API_KEY = os.getenv('FIREBASE_API_KEY', 'AIzaSyBW1ZbMiUeDZHYUO2bY8Bfnf5rRgrQGPTM')
FIREBASE_LOGIN_URL = f"https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key={FIREBASE_API_KEY}"

RANK_URL = os.getenv('RANK_URL', "https://us-central1-cp-multiplayer.cloudfunctions.net/SetUserRating4")
CLAN_ID_URL = os.getenv('CLAN_ID_URL', "https://us-central1-cp-multiplayer.cloudfunctions.net/GetClanId")

BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '8605656918:AAHJP9wvQBMmyvS97n3lxBk910tnIzcbxV4')
CHAT_ID = int(os.getenv('TELEGRAM_CHAT_ID', '5875091321'))