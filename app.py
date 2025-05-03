from flask import Flask, jsonify
import gspread
import random
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# 구글시트 API 연결
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name("mysheets_key.json", scope)
client = gspread.authorize(credentials)

sheet = client.open("TodaysCookie").sheet1  # 시트 이름
cookies = sheet.col_values(1)  # A열의 문구들

@app.route("/get-cookie")
def get_cookie():
    return jsonify({"cookie": random.choice(cookies)})

if __name__ == "__main__":
    app.run()
