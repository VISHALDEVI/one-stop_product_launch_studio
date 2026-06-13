"""
Run once to create the MySQL database and tables.
Usage: python setup_db.py
"""
import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "product_launch_studio")


def setup():
    # Create database if not exists
    conn = pymysql.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD)
    with conn.cursor() as cur:
        cur.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    conn.commit()
    conn.close()
    print(f"✅ Database '{DB_NAME}' is ready.")

    # Create tables via SQLAlchemy
    from backend.database import create_tables
    create_tables()
    print("✅ Tables created successfully.")


if __name__ == "__main__":
    setup()
