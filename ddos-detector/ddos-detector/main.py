from flask import Flask, jsonify, render_template
import time
from collections import deque

app = Flask(__name__)

request_log = deque(maxlen=500)
attack_threshold = 50  # requests per 5 seconds

@app.before_request
def log_request():
    request_log.append(time.time())

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/status")
def status():
    now = time.time()
    recent_requests = [r for r in request_log if now - r < 5]
    is_under_attack = len(recent_requests) > attack_threshold
    return jsonify({"attack": is_under_attack, "rate": len(recent_requests)})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
