import streamlit as st

from app.services.movie_service import get_languages, get_genres, autocomplete_titles


@st.cache_data
def load_languages():
    return get_languages()


@st.cache_data
def load_genres():
    return get_genres()


def render_search_panel():
    st.sidebar.header("Search Filters")

    typed_title = st.sidebar.text_input("Movie title")

    selected_title = typed_title

    if typed_title and len(typed_title.strip()) >= 2:
        suggestions_df = autocomplete_titles(typed_title.strip())

        if not suggestions_df.empty:
            title_options = ["Keep typed text"] + suggestions_df["title"].tolist()

            chosen_option = st.sidebar.selectbox(
                "Title suggestions",
                title_options,
                key="title_suggestions"
            )

            if chosen_option != "Keep typed text":
                selected_title = chosen_option

    languages_df = load_languages()
    genres_df = load_genres()

    language_options = ["Any"] + languages_df["language"].tolist()
    genre_options = ["Any"] + genres_df["genre"].tolist()

    language = st.sidebar.selectbox("Language", language_options)
    genre = st.sidebar.selectbox("Genre", genre_options)

    min_year = st.sidebar.number_input(
        "Released after year",
        min_value=1900,
        max_value=2100,
        value=2000,
    )

    min_avg_rating = st.sidebar.slider(
        "Minimum average rating",
        0.0,
        5.0,
        3.5,
        0.1,
    )

    search_clicked = st.sidebar.button("Search")

    return {
        "title": selected_title,
        "language": None if language == "Any" else language,
        "genre": None if genre == "Any" else genre,
        "min_year": min_year,
        "min_avg_rating": min_avg_rating,
        "search_clicked": search_clicked,
    }