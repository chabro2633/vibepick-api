from flask import Flask, jsonify, request
import gspread
import random
import os
import json
from datetime import datetime
from flask_cors import CORS
from oauth2client.service_account import ServiceAccountCredentials
from supabase_client import save_cookie, get_recent_cookies
from math import radians, cos, sin, asin, sqrt

app = Flask(__name__)
CORS(app, origins=["https://vibepick.tech"])

# Google Sheets 연결
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
json_key = os.environ.get("GOOGLE_CREDENTIAL_JSON")
key_dict = json.loads(json_key)
credentials = ServiceAccountCredentials.from_json_keyfile_dict(key_dict, scope)
client = gspread.authorize(credentials)

sheet = client.open("TodaysCookie").sheet1
cookies = sheet.col_values(1)

@app.route("/get-cookie")
def get_cookie():
    return jsonify({"cookie": random.choice(cookies)})

@app.route("/submit-cookie", methods=["POST"])
def submit_cookie():
    data = request.json
    cookie = data.get("cookie")
    lat = data.get("lat")
    lng = data.get("lng")
    if not all([cookie, lat, lng]):
        return jsonify({"error": "Missing fields"}), 400

    result = save_cookie(cookie, lat, lng)
    return jsonify(result)

def haversine(lat1, lng1, lat2, lng2):
    R = 6371  # 지구 반지름 (km)
    dlat = radians(lat2 - lat1)
    dlng = radians(lng2 - lng1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlng/2)**2
    return R * 2 * asin(sqrt(a))

@app.route("/nearby-cookies")
def nearby_cookies():
    lat = float(request.args.get("lat"))
    lng = float(request.args.get("lng"))
    all_cookies = get_recent_cookies()

    nearby = []
    for row in all_cookies:
        if row.get("lat") is None or row.get("lng") is None:
            continue
        dist = haversine(lat, lng, row["lat"], row["lng"])
        if dist <= 1.0:
            row["distance_km"] = round(dist, 3)
            nearby.append(row)

    return jsonify({"cookies": nearby})

if __name__ == "__main__":
    app.run()
