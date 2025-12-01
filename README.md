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

### How to run database
1.  **Install PostgreSQL**: Ensure the PostgreSQL server is running locally.
2.  **Create Database**:
    ```sql
    CREATE DATABASE bank_reviews;
    ```
3.  **Environment Variables**: Create a `.env` file in the root directory (do not commit to Git):
    ```ini
    DB_NAME=bank_reviews
    DB_USER=postgres
    DB_PASSWORD=your_password
    DB_HOST=localhost
    DB_PORT=5432
    ```

### Execution
The database ingestion is integrated into the main pipeline, but can also be run independently.

**Option 1: Run via Main Pipeline**
The `main.py` script automatically creates the schema and inserts data after analysis.
```bash
python main.py
```
**Option2: Run via Script**
```bash
python src/database/db_loader.py
python src/database/verify_db.py
```