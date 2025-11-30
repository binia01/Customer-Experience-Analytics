from src.config import PATHS
from src.scraper_reviews import PlayStoreScraper
from src.preprocess_reviews import DataCleaner

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

if __name__ == "__main__":
    main()