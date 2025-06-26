import os
from django.conf import settings
import joblib
import random

# Define the base directory for joblib files
KNN_GENRE_PATH = os.path.join(settings.BASE_DIR, 'books', 'joblibs', 'Genre_knn')

try:
    # Load pre-trained components
    books_df = joblib.load(os.path.join(KNN_GENRE_PATH, 'books_df.joblib'))
    category_encoder = joblib.load(os.path.join(KNN_GENRE_PATH, 'category_encoder.joblib'))
    category_knn_sparse = joblib.load(os.path.join(KNN_GENRE_PATH, 'category_knn_sparse.joblib'))
    
    # Create title to index mapping
    title_to_index = {title: idx for idx, title in enumerate(books_df['title'])}
    book_index_to_title = {idx: title for idx, title in enumerate(books_df['title'])}
    
    DATA_LOADED = True
except Exception as e:
    print(f"Warning: Could not load Genre KNN data: {e}")
    DATA_LOADED = False

def recommend_books_by_knn_genre(book_titles, n=5, regenerate=False):
    """
    Recommend N genre-similar books for each input title using KNN.
    Returns a dict: {book_title: [list of recommended book titles]}
    The recommendations are randomly sampled from a larger pool for variability.
    """
    if isinstance(book_titles, str):
        book_titles = [book_titles]
    
    results = {}
    default_pool_size = 25  # Can be adjusted if needed

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
            "Fahrenheit 451",
            "The Chronicles of Narnia",
            "Jane Eyre",
            "Wuthering Heights",
            "Brave New World",
            "The Picture of Dorian Gray"
        ]
        
        for title in book_titles:
            selected_books = random.sample(dummy_books, min(n, len(dummy_books)))
            results[title] = selected_books
        
        return results

    for title in book_titles:
        if title not in title_to_index:
            # Try partial matching
            partial_matches = [book_title for book_title in title_to_index.keys() 
                             if title.lower() in book_title.lower() or book_title.lower() in title.lower()]
            if partial_matches:
                title = partial_matches[0]
            else:
                results[title] = "Book not found"
                continue

        try:
            idx = title_to_index[title]
            input_vector = category_knn_sparse[idx]

            # Calculate similarity with all books using cosine similarity
            from sklearn.metrics.pairwise import cosine_similarity
            similarities = cosine_similarity([input_vector], category_knn_sparse)[0]
            
            # Exclude the book itself
            similarities[idx] = -1
            
            # Get indices sorted by similarity (highest first)
            sorted_indices = similarities.argsort()[::-1]
            
            # Get a larger pool of top similar books
            pool_size = min(default_pool_size, len(sorted_indices))
            top_similar_indices = sorted_indices[:pool_size]
            
            # Shuffle and pick n unique recommendations
            sampled_indices = random.sample(list(top_similar_indices), min(n, len(top_similar_indices)))

            recommended_titles = [book_index_to_title[i] for i in sampled_indices]
            results[title] = recommended_titles
            
        except Exception as e:
            # Fallback to dummy books if error occurs
            dummy_books = [
                "The Great Gatsby",
                "To Kill a Mockingbird", 
                "1984",
                "Pride and Prejudice",
                "The Catcher in the Rye",
            ]
            results[title] = random.sample(dummy_books, min(n, len(dummy_books)))

    return results
