import sqlite3
import os
import sys
src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
sys.path.append(src_path)
from src.config.config import Config

db_path = os.path.join(Config.CHROMA_PATH, 'chroma.sqlite3')

def main():
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM documents")
        count = cursor.fetchone()[0]
        print(f"Number of documents in the database: {count}")
        conn.close()
    else:
        print("Database file not found.")
if __name__ == "__main__":
    main()
