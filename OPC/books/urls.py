from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    # Template views
    path('books/', views.book_recommendation_page, name='book_recommendation_page'),
    path('history/', views.book_history_page, name='book_history_page'),
    path('genre-books/', views.genre_books_page, name='genre_books_page'),   
     
    # API endpoints
    path('api/book/search/', views.BookSearchView.as_view(), name='book_search'),
    path('api/book/recommend/', views.BookRecommendationView.as_view(), name='book_recommendation'),
    path('api/book/save-recommendations/', views.SaveSelectedRecommendations.as_view(), name='save_recommendations'),
    path('api/book/history/', views.BookHistoryView.as_view(), name='book_history'),
    path('api/book/history/delete-single/', views.BookHistoryDeleteView.as_view(), name='book_history_delete_single'),
    path('api/book/history/delete-bulk/', views.BookHistoryBulkClearView.as_view(), name='book_history_bulk_delete'),
]
