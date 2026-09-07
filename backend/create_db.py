import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

try:
    conn = psycopg2.connect("user='postgres' password='postgres' host='localhost' port='5432' dbname='postgres'")
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE ai_cyber_sentinel;")
    cursor.close()
    conn.close()
    print("Database 'ai_cyber_sentinel' created successfully.")
except psycopg2.errors.DuplicateDatabase:
    print("Database already exists.")
except Exception as e:
    print(f"Error creating database: {e}")
