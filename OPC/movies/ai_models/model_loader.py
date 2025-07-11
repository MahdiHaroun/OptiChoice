"""
Memory-efficient model loader for AI models
Implements lazy loading and memory management for low-RAM environments
"""
import os
import joblib
import logging
import gc
import psutil
from django.conf import settings
from functools import lru_cache

logger = logging.getLogger(__name__)

class MemoryEfficientModelLoader:
    """
    A memory-efficient model loader that implements lazy loading
    and automatic garbage collection for low-RAM environments.
    """
    
    def __init__(self):
        self.loaded_models = {}
        self.model_paths = {
            'knn': {
                'path': os.path.join(settings.BASE_DIR, 'movies', 'joblibs', 'KNN'),
                'files': ['knn_model.joblib', 'movie_mapping.joblib', 'reverse_mapping.joblib', 'sparse_matrix.joblib']
            },
            'tfidf': {
                'path': os.path.join(settings.BASE_DIR, 'movies', 'joblibs', 'BOW'),
                'files': ['tfidf_vectorizer.joblib', 'nn_model.joblib', 'title_to_index.joblib', 'tfidf_matrix.joblib']
            },
            'genre_based': {
                'path': os.path.join(settings.BASE_DIR, 'movies', 'joblibs', 'Genre-Based'),
                'files': ['movies_genre_based.joblib', 'genre_Based_matrix.joblib', 'title_index_genre-based.joblib']
            },
            'knn_genre': {
                'path': os.path.join(settings.BASE_DIR, 'movies', 'joblibs', 'GenreKnn'),
                'files': ['genre_knn_model.joblib', 'genre_index_to_title.joblib', 'genre_title_to_index.joblib', 'genre_movies_df.joblib']
            },
            'embeddings': {
                'path': os.path.join(settings.BASE_DIR, 'movies', 'joblibs', 'Embeddings'),
                'files': ['movies.pkl']
            },
            'nn': {
                'path': os.path.join(settings.BASE_DIR, 'movies', 'joblibs', 'NN'),
                'files': ['final_movie_data.pkl']
            },
            'grhr': {
                'path': os.path.join(settings.BASE_DIR, 'movies', 'joblibs', 'GRHR'),
                'files': ['GRHR.joblib']
            }
        }
    
    def get_memory_usage(self):
        """Get current memory usage percentage"""
        return psutil.virtual_memory().percent
    
    def cleanup_memory(self):
        """Force garbage collection and cleanup"""
        gc.collect()
        logger.info(f"Memory cleanup completed. Usage: {self.get_memory_usage():.1f}%")
    
    def load_model_safe(self, model_name, file_name):
        """
        Safely load a model with memory monitoring
        """
        try:
            # Check memory before loading
            memory_before = self.get_memory_usage()
            if memory_before > 80:
                logger.warning(f"High memory usage ({memory_before:.1f}%) before loading {model_name}")
                self.cleanup_memory()
            
            model_path = self.model_paths.get(model_name)
            if not model_path:
                logger.error(f"Unknown model: {model_name}")
                return None
            
            file_path = os.path.join(model_path['path'], file_name)
            
            if not os.path.exists(file_path):
                logger.warning(f"Model file not found: {file_path}")
                return None
            
            # Load the model
            model = joblib.load(file_path)
            
            # Check memory after loading
            memory_after = self.get_memory_usage()
            logger.info(f"Loaded {model_name}/{file_name}. Memory: {memory_before:.1f}% -> {memory_after:.1f}%")
            
            return model
            
        except Exception as e:
            logger.error(f"Failed to load {model_name}/{file_name}: {e}")
            self.cleanup_memory()
            return None
    
    def get_model(self, model_name, file_name):
        """
        Get a model with caching and memory management
        """
        cache_key = f"{model_name}_{file_name}"
        
        # Check if already loaded
        if cache_key in self.loaded_models:
            return self.loaded_models[cache_key]
        
        # Load the model
        model = self.load_model_safe(model_name, file_name)
        
        # Cache it if successful
        if model is not None:
            self.loaded_models[cache_key] = model
            
            # If memory is getting high, clear old models
            if self.get_memory_usage() > 90:
                self.clear_cache()
        
        return model
    
    def clear_cache(self):
        """Clear all cached models to free memory"""
        self.loaded_models.clear()
        self.cleanup_memory()
        logger.info("Model cache cleared due to high memory usage")
    
    def is_model_available(self, model_name):
        """Check if a model's files are available"""
        model_path = self.model_paths.get(model_name)
        if not model_path:
            return False
        
        # Check if at least one file exists
        for file_name in model_path['files']:
            file_path = os.path.join(model_path['path'], file_name)
            if os.path.exists(file_path):
                return True
        
        return False

# Global instance
model_loader = MemoryEfficientModelLoader()
