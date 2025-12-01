import pandas as pd
import sys
import logging
from src.config import PATHS
from src.scraper_reviews import PlayStoreScraper
from src.preprocess_reviews import DataCleaner
from src.sentiment_analyzer import SentimentAnalyzer
from src.theme_analyzer import ThemeClassifier
from src.keyword_analyzer import KeywordExtractor

# Setup Global Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)


def main():

    logger = logging.getLogger("MainPipeline")
    # --- Step 1: Data Collection ---
    scraper = PlayStoreScraper(count=500) 
    scraper.scrape()
    scraper.save(PATHS['raw_data'])

    # --- Step 2: Preprocessing ---
    cleaner = DataCleaner(PATHS['raw_data'])
    cleaner.load_data()
    clean_df = cleaner.preprocess()
    cleaner.save(PATHS['cleaned_data'])

    # --- Step 3: Sentiment Analysis ---
    sentiment_engine = SentimentAnalyzer()
    df_with_sentiment = sentiment_engine.analyze(clean_df)

    # --- Step 4: Keyword Extraction (New Task Requirement) ---
    keyword_engine = KeywordExtractor(max_features=15)
    top_keywords = keyword_engine.extract(df_with_sentiment)
    
    # Save keywords to file for analysis/reporting
    with open("data/processed/top_keywords.txt", "w") as f:
        for bank, words in top_keywords.items():
            f.write(f"--- {bank} ---\n")
            for w, score in words:
                f.write(f"{w} (score: {round(score, 2)})\n")
            f.write("\n")
    logger.info("Keywords saved to data/processed/top_keywords.txt")

    # --- Step 5: Thematic Analysis ---
    theme_engine = ThemeClassifier()
    final_df = theme_engine.apply_themes(df_with_sentiment)

    # --- Step 6: Final Save ---
    final_df.to_csv(PATHS['final_data'], index=False)
    print(f"\nPipeline Complete! Final dataset ready at: {PATHS['final_data']}")

if __name__ == "__main__":
    main()