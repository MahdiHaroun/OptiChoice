import os
from django.conf import settings
import joblib
import logging
import random
from .model_loader import model_loader

logger = logging.getLogger(__name__)

# Define the base directory for joblib files
KNN_PATH = os.path.join(settings.BASE_DIR, 'movies', 'joblibs', 'KNN')

def get_knn_models():
    """
    Get KNN models using memory-efficient loading
    """
    try:
        model = model_loader.get_model('knn', 'knn_model.joblib')
        movie_mapping = model_loader.get_model('knn', 'movie_mapping.joblib')
        reverse_mapping = model_loader.get_model('knn', 'reverse_mapping.joblib')
        sparse_matrix = model_loader.get_model('knn', 'sparse_matrix.joblib')
        
        return model, movie_mapping, reverse_mapping, sparse_matrix
    except Exception as e:
        logger.error(f"Failed to load KNN models: {e}")
        return None, None, None, None

def recommend_movies_knn(movie_titles, n=5, top_k=20):
    """
    Recommend N random movies selected from the top K most similar movies.
    - n: number of final recommendations
    - top_k: number of top similar movies to consider for random sampling
    """
    # Get models using memory-efficient loading
    model, movie_mapping, reverse_mapping, sparse_matrix = get_knn_models()
    
    results = {}

    # Check if model files are loaded
    if model is None or not movie_mapping or not reverse_mapping or sparse_matrix is None:
        logger.warning("KNN model data not available")
        for title in movie_titles:
            results[title] = "AI model not available - please check model files"
        return results

    for title in movie_titles:
        try:
            if title not in reverse_mapping:
                results[title] = "Movie not found"
                continue

            idx = reverse_mapping[title]

            # Get top K similar (excluding self)
            distances, indices = model.kneighbors(sparse_matrix[idx], n_neighbors=top_k + 1)
            similar_indices = [i for i in indices.flatten() if i != idx]

            # Map to titles
            similar_titles = [movie_mapping[i] for i in similar_indices]

            # Randomly select N from the top K similar titles
            if len(similar_titles) >= n:
                recommended = random.sample(similar_titles, n)
            else:
                recommended = similar_titles  # fallback if not enough results

            results[title] = recommended
            
        except Exception as e:
            logger.error(f"Error in KNN recommendation for '{title}': {e}")
            results[title] = "Error processing recommendation"

    return results

        results[title] = recommended

    return results
