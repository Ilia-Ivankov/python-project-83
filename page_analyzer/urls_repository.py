import psycopg2
from psycopg2.extras import DictCursor
from datetime import datetime
from page_analyzer.config import DATABASE_URL


class UrlRepository:
    """Repository class for handling URL-related database operations."""

    def save_url(self, url: str) -> int:
        """Saves url(url) by its name and returns id"""
        with psycopg2.connect(DATABASE_URL) as db_connection:
            with db_connection.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(
                    """
                    INSERT INTO urls (name, created_at)
                    VALUES (%s, %s)
                    RETURNING id
                    """,
                    (url, datetime.now()),
                )
                db_connection.commit()
                return cursor.fetchone()["id"]

    def get_url_by_id(self, url_id: int) -> dict:
        """Returns url data by it's id"""
        with psycopg2.connect(DATABASE_URL) as db_connection:
            with db_connection.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(
                    """
                    SELECT * FROM urls WHERE id = %s
                    """,
                    (url_id,),
                )
                result = cursor.fetchone()
                return result if result else None

    def get_all_urls(self) -> list:
        """Shows all urls"""
        with psycopg2.connect(DATABASE_URL) as db_connection:
            with db_connection.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute("SELECT * FROM urls ORDER BY created_at DESC")
                return cursor.fetchall()

    def get_url_by_name(self, url_name: str) -> dict:
        """
        Returns url data by its name
        """
        with psycopg2.connect(DATABASE_URL) as db_connection:
            with db_connection.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(
                    """
                    SELECT * FROM urls WHERE name = %s
                    """,
                    (url_name,),
                )
                result = cursor.fetchone()
                return result if result else None
