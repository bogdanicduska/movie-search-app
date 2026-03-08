AUTOCOMPLETE_QUERY = """
SELECT movieId, title
FROM `{project}.{dataset}.movies`
WHERE LOWER(title) LIKE CONCAT('%', LOWER(@q), '%')
ORDER BY title
LIMIT 20
"""

SEARCH_QUERY = """
SELECT
  m.movieId,
  m.title,
  m.genres,
  m.language,
  m.release_year,
  m.country,
  AVG(r.rating) AS avg_rating,
  COUNT(r.rating) AS rating_count
FROM `{project}.{dataset}.movies` m
LEFT JOIN `{project}.{dataset}.ratings` r
ON m.movieId = r.movieId
WHERE 1=1
  AND (@title IS NULL OR LOWER(m.title) LIKE CONCAT('%', LOWER(@title), '%'))
  AND (@language IS NULL OR m.language = @language)
  AND (@genre IS NULL OR m.genres LIKE CONCAT('%', @genre, '%'))
  AND (@min_year IS NULL OR m.release_year >= @min_year)
GROUP BY
  m.movieId, m.title, m.genres, m.language, m.release_year, m.country
HAVING (@min_avg_rating IS NULL OR AVG(r.rating) >= @min_avg_rating)
ORDER BY avg_rating DESC NULLS LAST, rating_count DESC, title
LIMIT 200
"""

MOVIE_DETAILS_QUERY = """
SELECT *
FROM `{project}.{dataset}.movies`
WHERE movieId = @movie_id
"""

RATING_STATS_QUERY = """
SELECT
  AVG(rating) AS avg_rating,
  COUNT(*) AS rating_count
FROM `{project}.{dataset}.ratings`
WHERE movieId = @movie_id
"""

LANGUAGES_QUERY = """
SELECT DISTINCT language
FROM `{project}.{dataset}.movies`
WHERE language IS NOT NULL
  AND TRIM(language) != ""
ORDER BY language
"""

GENRES_QUERY = """
SELECT DISTINCT genre
FROM `{project}.{dataset}.movies`,
UNNEST(SPLIT(genres, '|')) AS genre
WHERE genre IS NOT NULL
  AND TRIM(genre) != ""
ORDER BY genre
"""