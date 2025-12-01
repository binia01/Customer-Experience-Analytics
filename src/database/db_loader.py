import pandas as pd
import psycopg2
import os
import sys
from dotenv import load_dotenv

# Add parent dir to path to import config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.config import apps_config, PATHS

# Load environment variable

load_dotenv()

class DatabaseLoader:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT")
            )
            self.cur = self.conn.cursor()
            print("Database connection established.")
        except Exception as e:
            print(f"Error connecting to database: {e}")
            sys.exit(1)
    
    def create_schema(self):
        """Reads the SQL schema file and executes it."""
        try:
            with open('schema.sql', 'r') as f:
                schema_sql = f.read()
            self.cur.execute(schema_sql)
            self.conn.commit()
            print("Schema created/verified successfully.")
        except Exception as e:
            print(f"Error creating schema: {e}")
            self.conn.rollback()

    def populate_banks(self):
        """Inserts bank details from config."""
        try:
            print("Populating Banks table...")
            for bank in apps_config:
                # Upsert logic: Insert if not exists
                query = """
                INSERT INTO banks (bank_name, app_id) 
                VALUES (%s, %s)
                ON CONFLICT (bank_name) DO NOTHING;
                """
                self.cur.execute(query, (bank['name'], bank['app_id']))
            self.conn.commit()
        except Exception as e:
            print(f"Error populating banks: {e}")
            self.conn.rollback()

    def load_reviews(self, csv_path):
        """Loads processed reviews into the database."""
        try:
            if not os.path.exists(csv_path):
                print(f"File not found: {csv_path}")
                return

            print(f"Loading data from {csv_path}...")
            df = pd.read_csv(csv_path)

            # Get Bank ID mapping (Name -> ID)
            self.cur.execute("SELECT bank_name, bank_id FROM banks;")
            bank_map = dict(self.cur.fetchall())

            count = 0
            for _, row in df.iterrows():
                bank_id = bank_map.get(row['bank'])
                
                if bank_id:
                    query = """
                    INSERT INTO reviews 
                    (bank_id, review_text, rating, review_date, sentiment_label, sentiment_score, source)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """
                    self.cur.execute(query, (
                        bank_id,
                        row['review'],
                        row['rating'],
                        row['date'],
                        row['sentiment_label'],
                        row['sentiment_score'],
                        row['source']
                    ))
                    count += 1
            
            self.conn.commit()
            print(f"Successfully inserted {count} reviews.")
            
        except Exception as e:
            print(f"Error loading reviews: {e}")
            self.conn.rollback()

    def close(self):
        self.cur.close()
        self.conn.close()
        print("Database connection closed.")

if __name__ == "__main__":
    loader = DatabaseLoader()
    loader.create_schema()
    loader.populate_banks()
    
    # Load the final analyzed data
    # Note: Adjust path if your main script saves it elsewhere
    loader.load_reviews(PATHS['final_data'])
    
    loader.close()