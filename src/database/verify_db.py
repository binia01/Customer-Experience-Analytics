import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST")
)
cur = conn.cursor()

print("--- Data Verification ---")

# 1. Count Reviews per Bank
print("\n1. Reviews per Bank:")
cur.execute("""
    SELECT b.bank_name, COUNT(r.review_id) 
    FROM reviews r 
    JOIN banks b ON r.bank_id = b.bank_id 
    GROUP BY b.bank_name;
""")
for row in cur.fetchall():
    print(f"{row[0]}: {row[1]}")

# 2. Average Rating
print("\n2. Average Rating per Bank:")
cur.execute("""
    SELECT b.bank_name, ROUND(AVG(r.rating), 2) 
    FROM reviews r 
    JOIN banks b ON r.bank_id = b.bank_id 
    GROUP BY b.bank_name;
""")
for row in cur.fetchall():
    print(f"{row[0]}: {row[1]}")

conn.close()