import os
import joblib
from django.conf import settings

# Define the base path for BOW models
BOW_MODEL_PATH = os.path.join(settings.BASE_DIR, 'movies', 'joblibs', 'BOW')

# Load joblib files using relative paths
tfidf = joblib.load(os.path.join(BOW_MODEL_PATH, 'tfidf_vectorizer.joblib'))
model = joblib.load(os.path.join(BOW_MODEL_PATH, 'nn_model.joblib'))
title_to_index = joblib.load(os.path.join(BOW_MODEL_PATH, 'title_to_index.joblib'))
tfidf_matrix = joblib.load(os.path.join(BOW_MODEL_PATH, 'tfidf_matrix.joblib'))

def recommend_movies_sparse_list(movie_titles, n=5):
    recommendations = {}
    for movie_title in movie_titles:
        if movie_title not in title_to_index:
            recommendations[movie_title] = f"'{movie_title}' not found."
            continue

        idx = title_to_index[movie_title]
        distances, indices = model.kneighbors(tfidf_matrix[idx], n_neighbors=n + 1)
        recommended = [list(title_to_index.keys())[list(title_to_index.values()).index(i)]
                       for i in indices.flatten() if i != idx]
        recommendations[movie_title] = recommended[:n]
    return recommendations