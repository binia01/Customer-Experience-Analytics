import os
import pandas as pd
from google_play_scraper import reviews, Sort
from src.config import apps_config

class PlayStoreScraper:
    def __init__(self, count=500):
        self.apps = apps_config
        self.count = count
        self.all_reviews = []

    def scrape(self):
        """Iterates through configured banks and scrapes reviews."""
        for app in self.apps:
            print(f"Scraping {app['name']} ({app['app_id']})...")
            result, _ = reviews(
                app['app_id'],
                lang='en',
                country='us',
                sort=Sort.NEWEST,
                count=self.count
            )
            
            # Normalize structure immediately
            for r in result:
                r['bank'] = app['name']
                r['source'] = 'Google Play'
                
            self.all_reviews.extend(result)
            print(f"Fetched {len(result)} reviews.")
            
    def save(self, filepath):
        """Saves raw data to CSV."""
        df = pd.DataFrame(self.all_reviews)
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        df.to_csv(filepath, index=False)
        print(f"Raw data saved to {filepath}")

