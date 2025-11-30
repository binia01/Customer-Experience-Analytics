from src.config import PATHS
from src.scraper_reviews import PlayStoreScraper
from src.preprocess_reviews import DataCleaner
from src.sentiment_analyzer import SentimentAnalyzer
from src.theme_analyzer import ThemeClassifier

def main():
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

    # --- Step 4: Thematic Analysis ---
    theme_engine = ThemeClassifier()
    final_df = theme_engine.apply_themes(df_with_sentiment)

    # --- Step 5: Final Save ---
    final_df.to_csv(PATHS['final_data'], index=False)
    print(f"\nPipeline Complete! Final dataset ready at: {PATHS['final_data']}")

if __name__ == "__main__":
    main()