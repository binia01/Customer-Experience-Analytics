import pandas as pd
import os

def clean_data(input_file, output_file):
    print("loading raw data...")
    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print("error: raw_reviews.csv not found. Run scraper first.")
        return
    
    # Select required columns
    # Mappings: content -> review, score -> rating, at -> date

    df = df[['content', 'score', 'at', 'bank_name', 'source']]

    # Rename columns to match requirements
    df.rename(columns={
        'content': 'review',
        'score': 'rating',
        'at': 'date',
        'bank_name': 'bank'
    }, inplace=True)

    initial_count = len(df)

    # handle missing data
    # drop rows where review text or rating is missing
    df.dropna(subset=['review', 'rating'], inplace=True)

    # Remove duplicates
    # Duplicate reviews from the same user are common in scraping
    df.drop_duplicates(subset=['review', 'bank', 'date'], inplace=True)

    # Normalize data
    # Convert 'date' to datetime object and then to YYYY-MM-DD string
    df['date'] = pd.to_datetime(df['date'])
    df['date'] = df['date'].dt.strftime('%Y-%m-%d')

    cleaned_count = len(df)
    print(f"Data cleaning complete.")
    print(f"Original rows: {initial_count}")
    print(f"Cleaned rows: {cleaned_count}")
    print(f"Rows dropped: {initial_count - cleaned_count}")

    # Save to CSV
    df.to_csv(output_file, index=False)
    print(f"Saved cleaned data to {output_file}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_path = os.path.join(base_dir, "data", "raw_reviews.csv")
    cleaned_path = os.path.join(base_dir, "data", "banking_reviews_cleaned.csv")
    clean_data(raw_path, cleaned_path)