import sqlite3
import csv

# Database file path
db_path = "/workspaces/gs2video/data/db.sqlite3"  # Updated to create db.sqlite3
csv_path = "/workspaces/gs2video/data/pronunciations.csv"

# Connect to SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create table with unique constraint on 'word'
cursor.execute('''
CREATE TABLE IF NOT EXISTS pronunciations (
    word TEXT UNIQUE,
    ipa TEXT
)
''')

# Load data from CSV and insert into the database
with open(csv_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        try:
            cursor.execute('INSERT OR IGNORE INTO pronunciations (word, ipa) VALUES (?, ?)', (row['word'], row['ipa']))
        except sqlite3.IntegrityError:
            print(f"Duplicate entry skipped: {row['word']}")

# Commit changes and close connection
conn.commit()
conn.close()
