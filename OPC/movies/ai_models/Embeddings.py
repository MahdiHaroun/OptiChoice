# recommendation_service.py
import joblib
import torch
from sentence_transformers import SentenceTransformer, util
import os
import random
from django.conf import settings

EMB_PATH = os.path.join(settings.BASE_DIR, 'movies', 'joblibs', 'Embeddings')

# Load model and data
model = SentenceTransformer('all-MiniLM-L6-v2')
movies = joblib.load(os.path.join(EMB_PATH, 'movies.pkl'))
movie_embeddings = torch.load(os.path.join(EMB_PATH, 'movie_embeddings.pt'), map_location=torch.device('cpu'))
movie_embeddings = torch.nn.functional.normalize(movie_embeddings, p=2, dim=1)

def recommend_movies_embeddings(movie_titles, top_k=10):
    """
    Recommend movies using embeddings for multiple input titles
    Args:
        movie_titles: List of movie titles
        top_k: Number of recommendations per movie
    Returns:
        Dictionary with input titles as keys and recommendation lists as values
    """
    # Reset random seed for different results each time
    import time
    random.seed(int(time.time()))
    
    if isinstance(movie_titles, str):
        movie_titles = [movie_titles]
    
    results = {}
    
    for title in movie_titles:
        title = title.strip()
        idx = movies[movies['title'].str.lower() == title.lower()].index
        
        if len(idx) == 0:
            results[title] = [f"Movie '{title}' not found in database."]
            continue
        
        try:
            # Get the movie description for embedding
            movie_description = movies.loc[idx[0], 'description']
            if not movie_description or str(movie_description).lower() == 'nan':
                # Fallback to title if no description
                movie_description = title
            
            query_embedding = model.encode(movie_description, convert_to_tensor=True)
            query_embedding = torch.nn.functional.normalize(query_embedding, p=2, dim=0)

            # Get more results than requested for randomization
            search_k = min(top_k * 3, len(movies))  # Get 3x more results or all available
            scores = util.pytorch_cos_sim(query_embedding, movie_embeddings)[0]
            
            # Add small random noise to scores for variety (without destroying ranking too much)
            noise = torch.randn_like(scores) * 0.01  # Small random noise
            scores = scores + noise
            
            top_results = torch.topk(scores, k=search_k + 1)

            recommendations = []
            for i, score in zip(top_results[1], top_results[0]):
                idx_int = i.item()
                recommended_title = movies.iloc[idx_int]['title']
                
                # Skip the input movie itself
                if recommended_title.lower() == title.lower():
                    continue
                    
                recommendations.append(recommended_title)
            
            # Randomly shuffle and select the requested number of recommendations
            if len(recommendations) > top_k:
                random.shuffle(recommendations)
                recommendations = recommendations[:top_k]
            
            results[title] = recommendations
            
        except Exception as e:
            results[title] = [f"Error processing '{title}': {str(e)}"]
    
    return results
