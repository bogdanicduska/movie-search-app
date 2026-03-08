import streamlit as st


def render_results_panel(results_df):
    st.subheader("🎬 Search Results")

    if results_df.empty:
        st.info("No movies found.")
        return None

    # ---- Metrics summary ----
    total_movies = len(results_df)

    best_rating = None
    if "avg_rating" in results_df.columns and results_df["avg_rating"].notna().any():
        best_rating = round(results_df["avg_rating"].max(), 2)

    newest_year = None
    if "release_year" in results_df.columns and results_df["release_year"].notna().any():
        newest_year = int(results_df["release_year"].max())

    col1, col2, col3 = st.columns(3)
    col1.metric("Movies found", total_movies)
    col2.metric("Best rating", best_rating if best_rating is not None else "N/A")
    col3.metric("Newest release", newest_year if newest_year is not None else "N/A")

    st.success(f"Found **{total_movies} movies** matching your filters.")
    st.markdown("")

    # ---- Clean dataframe for display ----
    display_df = results_df.copy()

    columns_to_show = [
        "title",
        "genres",
        "language",
        "release_year",
        "country",
        "avg_rating",
        "rating_count",
    ]

    available_columns = [c for c in columns_to_show if c in display_df.columns]
    display_df = display_df[available_columns]

    display_df = display_df.rename(
        columns={
            "title": "Title",
            "genres": "Genres",
            "language": "Language",
            "release_year": "Year",
            "country": "Country",
            "avg_rating": "Avg Rating",
            "rating_count": "Ratings",
        }
    )

    if "Avg Rating" in display_df.columns:
        display_df["Avg Rating"] = display_df["Avg Rating"].round(2)

    # ---- Results table in bordered container ----
    with st.container(border=True):
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
        )

    st.markdown("")

    # ---- Optional small chart for visual appeal ----
    if "Year" in display_df.columns:
        year_counts = display_df["Year"].value_counts().sort_index()

        if len(year_counts) > 1:
            st.caption("Distribution of release years in current results")
            st.bar_chart(year_counts)

    st.markdown("---")

    # ---- Movie selector ----
    movie_options = {
        f"{row['title']} — {row['release_year']}": row["movieId"]
        for _, row in results_df.iterrows()
    }

    selected_label = st.selectbox(
        "🎥 Select a movie to view full details",
        list(movie_options.keys()),
        key="movie_selectbox",
    )

    return movie_options[selected_label]