import pandas as pd
from google_play_scraper import reviews, Sort

# Define the Apps to scrape
apps_config = [
    {
        "bank_name": "Commercial Bank of Ethiopia",
        "app_id": "com.combanketh.mobilebanking"
    },
    {
        "bank_name": "Bank of Abyssinia",
        "app_id": "com.boa.boaMobileBanking" 
    },
    {
        "bank_name": "Dashen Bank",
        "app_id": "com.dashen.dashensuperapp"
    }
]

all_reviews = []

# Loop through apps and scrape

for app in apps_config:
    print(f"Scraping {app['bank_name']}...")

    result, continuation_token = reviews(
        app['app_id'],
        lang='en',
        country='et',
        sort=Sort.NEWEST,
        count=500 
    )

    # add bank name and app ID to each review dict

    for review in result:
        review['bank_name'] = app['bank_name']
        review['app_id'] = app["app_id"]
        review['source'] = 'Google Play'

    all_reviews.extend(result)
    print(f"Collected {len(result)} reviews for {app['bank_name']}")

# Convert to DataFrame to check initial data

df = pd.DataFrame(all_reviews)

# Save raw data
df.to_csv('./data/raw_reviews.csv', index=False)
print(f"Total reviews collected: {len(df)}")