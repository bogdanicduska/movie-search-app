import pandas as pd
import requests

from app.config import TMDB_API_KEY

BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE = "https://image.tmdb.org/t/p/w500"


def get_tmdb_movie_details(tmdb_id):
    if pd.isna(tmdb_id) or tmdb_id in ("", None):
        print("TMDB: missing tmdb_id")
        return None

    if not TMDB_API_KEY:
        print("TMDB: missing API key")
        return None

    try:
        tmdb_id = int(tmdb_id)
    except Exception:
        print(f"TMDB: invalid tmdb_id -> {tmdb_id}")
        return None

    url = f"{BASE_URL}/movie/{tmdb_id}"
    params = {"api_key": TMDB_API_KEY}

    try:
        response = requests.get(url, params=params, timeout=10)

        print("----- TMDB DEBUG -----")
        print("TMDB ID:", tmdb_id)
        print("API key loaded:", bool(TMDB_API_KEY))
        print("Status code:", response.status_code)
        print("Response text:", response.text[:500])
        print("----------------------")

        if response.status_code != 200:
            return None

        data = response.json()

        poster = None
        if data.get("poster_path"):
            poster = IMAGE_BASE + data["poster_path"]

        return {
            "poster": poster,
            "overview": data.get("overview"),
        }

    except Exception as e:
        print(f"TMDB error: {e}")
        return None