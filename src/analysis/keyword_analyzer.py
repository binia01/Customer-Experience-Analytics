import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import logging

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class KeywordExtractor:
    def __init__(self, max_features=20):
        self.max_features = max_features
        # English stop words + common bank terms that might confuse analysis
        self.stop_words = 'english' 

    def _get_top_n_words(self, corpus, n=None):
        """
        Runs TF-IDF on a list of texts and returns top N words/phrases.
        """
        try:
            vec = TfidfVectorizer(
                stop_words=self.stop_words, 
                ngram_range=(1, 2), # Capture "login" and "login error"
                max_features=5000
            )
            bag_of_words = vec.fit_transform(corpus)
            sum_words = bag_of_words.sum(axis=0) 
            
            words_freq = [
                (word, sum_words[0, idx]) 
                for word, idx in vec.vocabulary_.items()
            ]
            
            # Sort by frequency score
            words_freq = sorted(words_freq, key=lambda x: x[1], reverse=True)
            return words_freq[:n]
        except ValueError:
            # Handle cases with empty vocabulary or too few documents
            logging.warning("Not enough text data to extract keywords.")
            return []
        except Exception as e:
            logging.error(f"Keyword extraction failed: {e}")
            return []

    def extract(self, df):
        """
        Extracts top keywords per bank.
        Returns a dictionary: { 'Bank Name': [('keyword', score), ...] }
        """
        logging.info("Starting TF-IDF Keyword Extraction...")
        
        if df.empty or 'review' not in df.columns or 'bank' not in df.columns:
            logging.error("DataFrame is empty or missing required columns.")
            return {}

        results = {}
        banks = df['bank'].unique()

        for bank in banks:
            # Filter reviews for this bank
            bank_reviews = df[df['bank'] == bank]['review'].astype(str).tolist()
            
            if len(bank_reviews) < 5:
                logging.warning(f"Skipping {bank}: Not enough reviews for TF-IDF.")
                continue

            # Get Keywords
            top_words = self._get_top_n_words(bank_reviews, self.max_features)
            results[bank] = top_words
            logging.info(f"Extracted {len(top_words)} keywords for {bank}")

        return results