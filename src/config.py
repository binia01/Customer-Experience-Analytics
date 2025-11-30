# Define the Apps to scrape
apps_config = [
    {
        "name": "Commercial Bank of Ethiopia",
        "app_id": "com.combanketh.mobilebanking"
    },
    {
        "name": "Bank of Abyssinia",
        "app_id": "com.boa.boaMobileBanking" 
    },
    {
        "name": "Dashen Bank",
        "app_id": "com.dashen.dashensuperapp"
    }
]

PATHS = {
    "raw_data": "data/raw/reviews_raw.csv",
    "cleaned_data": "data/processed/reviews_cleaned.csv",
    "final_data": "data/processed/reviews_analyzed.csv"
}

SENTIMENT_MODEL = "distilbert-base-uncased-finetuned-sst-2-english"