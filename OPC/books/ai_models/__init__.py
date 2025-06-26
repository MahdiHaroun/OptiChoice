# AI models for book recommendations

# Import recommendation functions from each model
from .Embeddings import recommend_books_embeddings
from .KNN import recommend_books_knn
from .NN import recommend_books_nn
from .Genre_Based import recommend_books_by_genre
from .knn_genre import recommend_books_by_knn_genre

__all__ = [
    'recommend_books_embeddings',
    'recommend_books_knn',
    'recommend_books_nn',
    'recommend_books_by_genre',
    'recommend_books_by_knn_genre'
]
