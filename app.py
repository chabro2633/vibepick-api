from flask import Flask, jsonify
import gspread
import random
import os
import json
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# 구글시트 API 연결
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# 환경변수에서 JSON 키 문자열을 불러와 dict로 변환
json_key = os.environ.get("GOOGLE_CREDENTIAL_JSON")
key_dict = json.loads(json_key)

# 인증 객체 생성
credentials = ServiceAccountCredentials.from_json_keyfile_dict(key_dict, scope)
client = gspread.authorize(credentials)

# 시트 열기
sheet = client.open("TodaysCookie").sheet1
cookies = sheet.col_values(1)

@app.route("/get-cookie")
def get_cookie():
    return jsonify({"cookie": random.choice(cookies)})

if __name__ == "__main__":
    app.run()
