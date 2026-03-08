from dotenv import load_dotenv
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "bigquery-movie-search")
BQ_DATASET = os.getenv("BQ_DATASET", "movies_app")
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

print("PROJECT_ID:", PROJECT_ID)
print("TMDB key loaded in config:", bool(TMDB_API_KEY))