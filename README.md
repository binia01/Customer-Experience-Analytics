# Customer-Experience-Analytics

## Task 1: Data Collection & Preprocessing

### Objective
Scrape Google Play Store reviews for CBE, BOA, and Dashen Bank to analyze customer satisfaction.

### Methodology
1. **Scraping**: Used `google-play-scraper` library.
   - Target: >400 reviews per bank.
   - Sorted by: Newest.
2. **Preprocessing**: 
   - Selected columns: Review, Rating, Date, Bank, Source.
   - Removed duplicates and null values.
   - Normalized dates to `YYYY-MM-DD`.

### Clone the repository
```bash
git clone https://github.com/binia01/Customer-Experience-Analytics.git
cd Customer-Experience-Analysis
```

### Create and activate a virtual environment

For Windows:
```bash
python -m venv .venv
venv\Scripts\activate
```

For macOS / Linux:
```bash
python -m venv .venv
source venv/bin/activate
```

### How to Run
1. Install requirements: `pip install -r requirements.txt`
2. Run main.py: `python main.py`
4. Output file: `reviews_analyzed.csv`