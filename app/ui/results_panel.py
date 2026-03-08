import streamlit as st


def render_results_panel(results_df):
    st.subheader("Search Results")
    st.write(f"Found {len(results_df)} movies.")

    if results_df.empty:
        st.info("No movies found.")
        return None

    st.dataframe(results_df, use_container_width=True)

    movie_options = {
        f"{row['title']} — {row['release_year']}": row["movieId"]
        for _, row in results_df.iterrows()
    }

    selected_label = st.selectbox(
        "Select a movie",
        list(movie_options.keys()),
        key="movie_selectbox",
    )

    return movie_options[selected_label]