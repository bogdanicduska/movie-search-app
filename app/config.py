import os

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "bigquery-movie-search")
BQ_DATASET = os.getenv("BQ_DATASET", "movies_app")
TMDB_API_KEY = os.getenv("TMDB_API_KEY", "ec42ba05704c101ff6429b228082b629")