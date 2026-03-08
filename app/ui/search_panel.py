import streamlit as st

from app.services.movie_service import get_languages, get_genres, autocomplete_titles


@st.cache_data
def load_languages():
    return get_languages()


@st.cache_data
def load_genres():
    return get_genres()


def init_search_state():
    defaults = {
        "title_input": "",
        "title_suggestion": "Keep typed text",
        "language_filter": "Any",
        "genre_filter": "Any",
        "min_year_filter": 2000,
        "min_rating_filter": 3.5,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_search_state():
    st.session_state["title_input"] = ""
    st.session_state["title_suggestion"] = "Keep typed text"
    st.session_state["language_filter"] = "Any"
    st.session_state["genre_filter"] = "Any"
    st.session_state["min_year_filter"] = 2000
    st.session_state["min_rating_filter"] = 3.5
    st.session_state["results_df"] = None
    st.session_state["selected_movie_id"] = None


def render_search_panel():
    init_search_state()

    st.sidebar.markdown("## 🔎 Search Filters")
    st.sidebar.caption("Refine the movie search using the filters below.")

    typed_title = st.sidebar.text_input("Movie title", key="title_input")
    selected_title = typed_title

    if typed_title and len(typed_title.strip()) >= 2:
        suggestions_df = autocomplete_titles(typed_title.strip())

        if not suggestions_df.empty:
            title_options = ["Keep typed text"] + suggestions_df["title"].tolist()

            chosen_option = st.sidebar.selectbox(
                "Title suggestions",
                title_options,
                key="title_suggestion",
            )

            if chosen_option != "Keep typed text":
                selected_title = chosen_option

    st.sidebar.markdown("---")

    languages_df = load_languages()
    genres_df = load_genres()

    language_options = ["Any"] + languages_df["language"].tolist()
    genre_options = ["Any"] + genres_df["genre"].tolist()

    language = st.sidebar.selectbox("Language", language_options, key="language_filter")
    genre = st.sidebar.selectbox("Genre", genre_options, key="genre_filter")

    st.sidebar.markdown("---")

    min_year = st.sidebar.number_input(
        "Released after year",
        min_value=1900,
        max_value=2100,
        key="min_year_filter",
    )

    min_avg_rating = st.sidebar.slider(
        "Minimum average rating",
        0.0,
        5.0,
        key="min_rating_filter",
    )

    st.sidebar.markdown("")

    col1, col2 = st.sidebar.columns(2)
    search_clicked = col1.button("Search", use_container_width=True)
    col2.button("Reset", on_click=reset_search_state, use_container_width=True)

    return {
        "title": selected_title,
        "language": None if language == "Any" else language,
        "genre": None if genre == "Any" else genre,
        "min_year": min_year,
        "min_avg_rating": min_avg_rating,
        "search_clicked": search_clicked,
    }