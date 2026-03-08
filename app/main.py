import streamlit as st

from app.services.movie_service import search_movies, get_movie_details
from app.ui.search_panel import render_search_panel
from app.ui.results_panel import render_results_panel
from app.ui.details_panel import render_details_panel


st.set_page_config(page_title="Movie Search App", layout="wide")
st.title("Movie Search App")

if "results_df" not in st.session_state:
    st.session_state.results_df = None

if "selected_movie_id" not in st.session_state:
    st.session_state.selected_movie_id = None

filters = render_search_panel()

if filters["search_clicked"]:
    st.session_state.results_df = search_movies(
        title=filters["title"] or None,
        language=filters["language"],
        genre=filters["genre"],
        min_year=filters["min_year"],
        min_avg_rating=filters["min_avg_rating"],
    )
    st.session_state.selected_movie_id = None

if st.session_state.results_df is not None:
    results_df = st.session_state.results_df

    selected_movie_id = render_results_panel(results_df)
    st.session_state.selected_movie_id = selected_movie_id

    if st.session_state.selected_movie_id is not None:
        details_df, ratings_df = get_movie_details(st.session_state.selected_movie_id)
        render_details_panel(details_df, ratings_df)
else:
    st.info("Choose filters in the sidebar and click Search.")