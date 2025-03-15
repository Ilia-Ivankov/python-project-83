import psycopg2
from psycopg2.extras import DictCursor
from datetime import datetime
from page_analyzer.config import DATABASE_URL

conn = psycopg2.connect(DATABASE_URL)


class UrlRepository:
    def add_url(url):
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                """
    `       INSERT INTO urls (name, created_at) VALUES (%s, %s) RETURNING ID
            """, (url, datetime.now())
            )
            return cursor.fetchone()[id]
