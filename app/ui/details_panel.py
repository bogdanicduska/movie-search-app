import streamlit as st
from app.services.external_api_service import get_tmdb_movie_details


def render_details_panel(details_df, ratings_df):
    if details_df.empty:
        st.warning("No details found for this movie.")
        return

    movie = details_df.iloc[0]
    tmdb_id = movie.get("tmdbId")
    tmdb_data = get_tmdb_movie_details(tmdb_id)

    st.markdown("---")
    st.subheader(movie["title"])

    col1, col2 = st.columns([1, 2])

    with col1:
        if tmdb_data and tmdb_data.get("poster"):
            st.image(tmdb_data["poster"], use_container_width=True)
        else:
            st.info("Poster not available.")

    with col2:
        st.write(f"**Genres:** {movie['genres']}")
        st.write(f"**Language:** {movie['language']}")
        st.write(f"**Release year:** {movie['release_year']}")
        st.write(f"**Country:** {movie['country'] if movie['country'] else 'Unknown'}")
        st.write(f"**TMDB ID:** {tmdb_id}")

        if not ratings_df.empty:
            rating_row = ratings_df.iloc[0]
            avg_rating = rating_row["avg_rating"]
            rating_count = rating_row["rating_count"]

            if avg_rating is not None:
                st.write(f"**Average rating:** {round(float(avg_rating), 2)}")
            if rating_count is not None:
                st.write(f"**Rating count:** {int(rating_count)}")

        if tmdb_data and tmdb_data.get("overview"):
            st.subheader("Overview")
            st.write(tmdb_data["overview"])
        else:
            st.info("Overview not available from TMDB.")