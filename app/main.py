import streamlit as st

from app.services.movie_service import search_movies, get_movie_details


st.set_page_config(page_title="Movie Search App", layout="wide")
st.title("Movie Search App")

st.sidebar.header("Search Filters")

title = st.sidebar.text_input("Movie title")
language = st.sidebar.text_input("Language code (e.g. en, fr, hi)")
genre = st.sidebar.text_input("Genre (e.g. Comedy, Drama)")
min_year = st.sidebar.number_input("Released after year", min_value=1900, max_value=2100, value=2000)
min_avg_rating = st.sidebar.slider("Minimum average rating", 0.0, 5.0, 3.5, 0.1)

search_clicked = st.sidebar.button("Search")

if search_clicked:
    results_df = search_movies(
        title=title or None,
        language=language or None,
        genre=genre or None,
        min_year=min_year,
        min_avg_rating=min_avg_rating,
    )

    st.subheader("Search Results")

    if results_df.empty:
        st.info("No movies found.")
    else:
        st.dataframe(results_df, use_container_width=True)

        movie_options = {
            f"{row['title']} ({row['release_year']})": row["movieId"]
            for _, row in results_df.iterrows()
        }

        selected_label = st.selectbox("Select a movie", list(movie_options.keys()))
        selected_movie_id = movie_options[selected_label]

        details_df, ratings_df = get_movie_details(selected_movie_id)

        if not details_df.empty:
            movie = details_df.iloc[0]
            st.subheader(movie["title"])
            st.write(f"**Genres:** {movie['genres']}")
            st.write(f"**Language:** {movie['language']}")
            st.write(f"**Release year:** {movie['release_year']}")
            st.write(f"**Country:** {movie['country']}")

        if not ratings_df.empty:
            rating_row = ratings_df.iloc[0]
            st.write(f"**Average rating:** {rating_row['avg_rating']}")
            st.write(f"**Rating count:** {rating_row['rating_count']}")
else:
    st.info("Choose filters in the sidebar and click Search.")