import streamlit as st

from app.services.movie_service import search_movies, get_movie_details
from app.ui.search_panel import render_search_panel
from app.ui.results_panel import render_results_panel
from app.ui.details_panel import render_details_panel


def init_session_state():
    if "results_df" not in st.session_state:
        st.session_state.results_df = None

    if "selected_movie_id" not in st.session_state:
        st.session_state.selected_movie_id = None


def main():
    st.set_page_config(
        page_title="Movie Search App",
        page_icon="🎬",
        layout="wide",
    )

    st.title("Movie Search App")

    st.markdown(
        """
        <div style="padding:1rem; border-radius:12px; background-color:#f5f7fb; margin-bottom:1rem;">
            <h2 style="margin:0;">Movie Explorer</h2>
            <p style="margin:0.5rem 0 0 0;">
                Search movies by title, language, genre, release year, and average rating.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    init_session_state()

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
        st.info("Use the filters in the sidebar and click Search to find movies.")

    st.markdown("---")
    st.caption("Movie Search App • BigQuery + Streamlit + TMDB API")


if __name__ == "__main__":
    main()