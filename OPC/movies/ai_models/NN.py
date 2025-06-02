import os
import joblib
import numpy as np
from tensorflow.keras.models import load_model
from django.conf import settings
from sklearn.metrics.pairwise import cosine_similarity

# Paths
NN_PATH = os.path.join(settings.BASE_DIR, 'movies', 'joblibs', 'NN')
MODEL_PATH = os.path.join(NN_PATH, 'movie_rating_model.keras')
SCALER_PATH = os.path.join(NN_PATH, 'rating_count_scaler.pkl')
MOVIES_DATA_PATH = os.path.join(NN_PATH, 'final_movie_data.pkl')

def recommend_movies_nn(movie_titles, top_k=10):
    """
    Recommend movies using a neural network model based on input movie titles.
    
    Args:
        movie_titles: List of movie titles or single movie title
        top_k: Number of recommendations to return for each input title
    
    Returns:
        Dictionary with input titles as keys and recommendation lists as values
    """
    if isinstance(movie_titles, str):
        movie_titles = [movie_titles]
    
    # Load the pre-trained model and movie data
    model = load_model(MODEL_PATH)
    movies_data = joblib.load(MOVIES_DATA_PATH)
    
    results = {}
    
    # Features to use for the neural network (21 features total)
    feature_columns = [col for col in movies_data.columns 
                      if col not in ['title', 'genres', 'movieId', 'rating_count', 'avg_rating']]
    
    for title in movie_titles:
        title = title.strip()
        
        # Find the input movie
        movie_match = movies_data[movies_data['title'].str.lower() == title.lower()]
        
        if movie_match.empty:
            results[title] = [f"Movie '{title}' not found in database."]
            continue
            
        # Get input movie features
        input_features = movie_match[feature_columns].values[0].astype('float32')
        
        # Get features for all movies in the dataset
        all_features = movies_data[feature_columns].values.astype('float32')
        
        # Calculate cosine similarity between input movie and all movies
        input_features = input_features.reshape(1, -1)
        similarities = cosine_similarity(input_features, all_features)[0]
        
        # Exclude the input movie itself
        input_index = movie_match.index[0]
        similarities[input_index] = -1
        
        # Get top-k most similar movies
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        # Extract movie titles
        recommendations = movies_data.iloc[top_indices]['title'].tolist()
        
        results[title] = recommendations
    
    return results

