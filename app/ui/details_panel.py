import streamlit as st
import pandas as pd

from app.services.external_api_service import get_tmdb_movie_details


def safe_value(value, fallback="Unknown"):
    if value is None:
        return fallback
    if pd.isna(value):
        return fallback
    if isinstance(value, str) and value.strip() == "":
        return fallback
    return value


def format_genres(genres):
    genres = safe_value(genres, "")
    if not genres:
        return "Unknown"
    return genres.replace("|", " • ")


def format_rating_stars(avg_rating):
    if avg_rating is None:
        return ""
    star_count = max(1, min(5, round(avg_rating)))
    return "⭐" * star_count


def render_details_panel(details_df, ratings_df):
    if details_df.empty:
        st.warning("No details found for this movie.")
        return

    movie = details_df.iloc[0]

    tmdb_id = movie.get("tmdbId")
    tmdb_data = get_tmdb_movie_details(tmdb_id)

    title = safe_value(movie.get("title"))
    genres = format_genres(movie.get("genres"))
    language = safe_value(movie.get("language"))
    release_year = safe_value(movie.get("release_year"))
    country = safe_value(movie.get("country"))

    avg_rating = None
    rating_count = None

    if not ratings_df.empty:
        rating_row = ratings_df.iloc[0]
        if "avg_rating" in rating_row and not pd.isna(rating_row["avg_rating"]):
            avg_rating = round(float(rating_row["avg_rating"]), 2)
        if "rating_count" in rating_row and not pd.isna(rating_row["rating_count"]):
            rating_count = int(rating_row["rating_count"])

    poster_url = None
    overview = None

    if tmdb_data:
        poster_url = tmdb_data.get("poster")
        overview = tmdb_data.get("overview")

    st.markdown("---")
    st.subheader("🎬 Movie Details")

    with st.container(border=True):
        col1, col2 = st.columns([1, 2])

        with col1:
            if poster_url:
                st.image(poster_url, use_container_width=True)
            else:
                st.info("Poster not available")
                st.caption("No poster was returned by TMDB for this title.")

        with col2:
            st.markdown(f"## {title}")
            st.caption(f"{release_year} • {language} • {country}")

            st.write(f"**Genres:** {genres}")

            if avg_rating is not None:
                st.markdown(f"**Rating:** {avg_rating} {format_rating_stars(avg_rating)}")

            metric_col1, metric_col2 = st.columns(2)
            metric_col1.metric("Average rating", avg_rating if avg_rating is not None else "N/A")
            metric_col2.metric("Rating count", rating_count if rating_count is not None else "N/A")

            st.markdown("### Overview")
            if overview and str(overview).strip():
                st.write(overview)
            else:
                st.info("Overview not available from TMDB.")