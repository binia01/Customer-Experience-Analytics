import pandas as pd
from transformers import pipeline
from tqdm import tqdm
from src.config import SENTIMENT_MODEL

class SentimentAnalyzer:
    def __init__(self):
        print("Loading Sentiment Model (this may take a moment)...")
        self.pipe = pipeline("sentiment-analysis", model=SENTIMENT_MODEL)

    def _get_score(self, text):
        """Helper to process single text string."""
        try:
            # Truncate to 512 tokens to prevent BERT errors
            res = self.pipe(str(text)[:512])[0]
            return res['label'], res['score']
        except:
            return "NEUTRAL", 0.0

    def analyze(self, df):
        """Applies sentiment analysis to a DataFrame."""
        print("Running Sentiment Analysis...")
        tqdm.pandas()
        
        # Apply pipeline
        results = df['review'].progress_apply(lambda x: self._get_score(x))
        
        # Unpack results
        df['sentiment_label'] = results.apply(lambda x: x[0])
        df['sentiment_score'] = results.apply(lambda x: x[1])
        
        return df