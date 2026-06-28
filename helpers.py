# helpers.py
import requests
import logging
from datetime import datetime

REQUIRED_DOMAINS = [
    'www.googleapis.com',
    'us-central1-cp-multiplayer.cloudfunctions.net',
    'api.telegram.org'
]

def log_attempt(email):
    """Silent logging for audit trail."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logging.info(f"[{timestamp}] Attempted login for: {email}")

def check_network_access():
    """Verify PA can reach required endpoints (free tier whitelist check)."""
    for domain in REQUIRED_DOMAINS:
        try:
            requests.get(f"https://{domain}", timeout=3)
        except requests.exceptions.RequestException:
            logging.warning(f"Network access blocked for: {domain}")
            return False
    return True

def retry_request(func, max_retries=2, delay=1):
    """Simple retry wrapper for flaky game APIs."""
    import time
    for attempt in range(max_retries):
        try:
            return func()
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(delay * (attempt + 1))