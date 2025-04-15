
from flask import Flask, jsonify
import random

app = Flask(__name__)

cookies = [
    "오늘도 충분히 잘하고 있어요 🍀",
    "작은 선택이 큰 기회를 만듭니다 🌈",
    "생각보다 더 멋진 하루가 기다리고 있어요 ✨"
]

@app.route('/api/cookie')
def get_cookie():
    return jsonify({"cookie": random.choice(cookies)})

@app.route('/')
def hello():
    return "VibePick API is running"
