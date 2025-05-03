# supabase_client.py

import os
import requests

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

def save_cookie(cookie, lat, lng):
    return requests.post(
        f"{SUPABASE_URL}/rest/v1/cookies",
        headers={**HEADERS, "Prefer": "return=representation"},
        json={
            "cookie": cookie,
            "lat": lat,
            "lng": lng
        }
    ).json()

def get_recent_cookies(limit=50):
    res = requests.get(
        f"{SUPABASE_URL}/rest/v1/cookies?order=created_at.desc&limit={limit}",
        headers=HEADERS
    )
    return res.json()
