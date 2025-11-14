"""
Simple offline embedding solution using TF-IDF
This avoids SSL certificate issues with external services
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pickle
import os
from typing import List

class OfflineTfIdfEmbeddings:
    """Simple TF-IDF based embeddings that work offline"""
    
    def __init__(self, max_features=5000):
        self.vectorizer = TfidfVectorizer(
            max_features=max_features,
            stop_words='english',
            lowercase=True,
            ngram_range=(1, 2)
        )
        self.is_fitted = False
        self.cache_file = "tfidf_embeddings.pkl"
        
    def fit(self, texts: List[str]):
        """Fit the vectorizer on the given texts"""
        self.vectorizer.fit(texts)
        self.is_fitted = True
        # Cache the fitted vectorizer
        with open(self.cache_file, 'wb') as f:
            pickle.dump(self.vectorizer, f)
    
    def load_cache(self):
        """Load cached vectorizer if available"""
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'rb') as f:
                self.vectorizer = pickle.load(f)
                self.is_fitted = True
                return True
        return False
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed multiple documents"""
        if not self.is_fitted:
            if not self.load_cache():
                # If no cache, fit on the texts themselves
                self.fit(texts)
        
        # Transform texts to vectors
        vectors = self.vectorizer.transform(texts)
        # Convert sparse matrix to dense and then to list
        return vectors.toarray().tolist()
    
    def embed_query(self, text: str) -> List[float]:
        """Embed a single query"""
        if not self.is_fitted:
            if not self.load_cache():
                raise RuntimeError("Vectorizer not fitted. Call embed_documents first.")
        
        # Transform single text
        vector = self.vectorizer.transform([text])
        return vector.toarray()[0].tolist()