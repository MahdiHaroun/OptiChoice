import joblib
import os
import numpy as np
from django.conf import settings
from sklearn.metrics.pairwise import cosine_similarity
import random

# Define the base directory for joblib files
GENRE_BASED_PATH = os.path.join(settings.BASE_DIR, 'books', 'joblibs', 'Genre_knn')

try:
    # Load data
    books_df = joblib.load(os.path.join(GENRE_BASED_PATH, 'books_df.joblib'))
    category_encoder = joblib.load(os.path.join(GENRE_BASED_PATH, 'category_encoder.joblib'))
    category_knn_sparse = joblib.load(os.path.join(GENRE_BASED_PATH, 'category_knn_sparse.joblib'))
    
    # Create title to index mapping
    title_to_index = {title: idx for idx, title in enumerate(books_df['title'])}
    
    DATA_LOADED = True
except Exception as e:
    print(f"Warning: Could not load Genre-Based data: {e}")
    DATA_LOADED = False

def recommend_books_by_genre(favorite_books, number_of_results=5):
    """
    Generate random genre-based book recommendations for each favorite book.

    Args:
        favorite_books (list): List of favorite book titles.
        number_of_results (int): Number of random recommendations to return.

    Returns:
        dict: Mapping of favorite book to list of recommended titles.
    """
    if isinstance(favorite_books, str):
        favorite_books = [favorite_books]
    
    recommendations = {}

    # Check if data is loaded
    if not DATA_LOADED:
        # Return dummy data when models are not available
        dummy_books = [
            "The Great Gatsby",
            "To Kill a Mockingbird", 
            "1984",
            "Pride and Prejudice",
            "The Catcher in the Rye",
            "Lord of the Rings",
            "Harry Potter and the Philosopher's Stone",
            "The Hobbit",
            "Dune",
            "Fahrenheit 451"
        ]
        
        for book_name in favorite_books:
            selected_books = random.sample(dummy_books, min(number_of_results, len(dummy_books)))
            recommendations[book_name] = selected_books
        
        return recommendations

    for book_name in favorite_books:
        if book_name not in title_to_index:
            # Try partial matching
            partial_matches = [title for title in title_to_index.keys() 
                             if book_name.lower() in title.lower() or title.lower() in book_name.lower()]
            if partial_matches:
                book_name = partial_matches[0]
            else:
                recommendations[book_name] = "Book not found"
                continue

        try:
            idx = title_to_index[book_name]
            selected_vector = category_knn_sparse[idx]
            
            # Calculate similarity with all books using cosine similarity
            similarity_scores = cosine_similarity([selected_vector], category_knn_sparse)[0]
            similarity_scores[idx] = -1  # exclude itself

            all_indices = np.arange(len(similarity_scores))
            sorted_indices = all_indices[np.argsort(similarity_scores)[::-1]]
            shuffled_indices = np.random.permutation(sorted_indices)

            selected_indices = shuffled_indices[:number_of_results]
            recommended_titles = books_df.iloc[selected_indices]['title'].tolist()

            recommendations[book_name] = recommended_titles
            
        except Exception as e:
            # Fallback to dummy books if error occurs
            dummy_books = [
                "The Great Gatsby",
                "To Kill a Mockingbird", 
                "1984",
                "Pride and Prejudice",
                "The Catcher in the Rye",
            ]
            recommendations[book_name] = random.sample(dummy_books, min(number_of_results, len(dummy_books)))

    return recommendations
