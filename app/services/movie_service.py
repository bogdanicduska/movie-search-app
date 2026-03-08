from google.cloud import bigquery

from app.bq_client import run_query
from app.queries import (
    SEARCH_QUERY,
    MOVIE_DETAILS_QUERY,
    RATING_STATS_QUERY,
    LANGUAGES_QUERY,
    GENRES_QUERY,
)


def search_movies(title=None, language=None, genre=None, min_year=None, min_avg_rating=None):
    params = [
        bigquery.ScalarQueryParameter("title", "STRING", title),
        bigquery.ScalarQueryParameter("language", "STRING", language),
        bigquery.ScalarQueryParameter("genre", "STRING", genre),
        bigquery.ScalarQueryParameter("min_year", "INT64", min_year),
        bigquery.ScalarQueryParameter("min_avg_rating", "FLOAT64", min_avg_rating),
    ]
    return run_query(SEARCH_QUERY, params)


def get_movie_details(movie_id):
    params = [bigquery.ScalarQueryParameter("movie_id", "INT64", movie_id)]
    details_df = run_query(MOVIE_DETAILS_QUERY, params)
    ratings_df = run_query(RATING_STATS_QUERY, params)
    return details_df, ratings_df

def get_languages():
    return run_query(LANGUAGES_QUERY)


def get_genres():
    return run_query(GENRES_QUERY)