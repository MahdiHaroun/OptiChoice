import joblib
import os
from django.conf import settings
import random

GRHR_PATH = os.path.join(settings.BASE_DIR, 'movies', 'joblibs', 'GRHR')

movies_df = joblib.load(os.path.join(GRHR_PATH, 'GRHR.joblib'))


def recommend_movies_GRHR(selected_genres, n=5):
    df = movies_df.copy()

    for genre in selected_genres:
        if genre not in df.columns:
            return { "error": f"Genre '{genre}' not found." }

        df = df[df[genre] == 1]

    df = df.dropna(subset=['avg_rating'])
    if df.empty:
        return { "error": "No matching movies found for selected genres." }

    top_movies = df.sort_values(by='avg_rating', ascending=False).head(25)
    sampled = top_movies.sample(n=min(n, len(top_movies)), random_state=random.randint(1, 9999))

    return sampled['title'].tolist()