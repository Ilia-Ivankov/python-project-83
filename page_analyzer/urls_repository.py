import psycopg2
from psycopg2.extras import DictCursor
from datetime import datetime
from page_analyzer.config import DATABASE_URL

# Database connection
db_conn = psycopg2.connect(DATABASE_URL)


class UrlRepository:
    def save_url(self, url: str) -> int:
        """
        Save URL to database and return its ID

        Args:
            url (str): URL to be saved

        Returns:
            int: ID of the saved URL
        """
        with db_conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO urls (name, created_at) 
                VALUES (%s, %s) 
                RETURNING id
                """,
                (url, datetime.now()),
            )
            return cursor.fetchone()["id"]

    def get_url_by_id(self, url_id: int) -> dict:
        """
        Retrieve URL data from database by its ID

        Args:
            url_id (int): URL ID to search for

        Returns:
            dict: URL data as dictionary or None if not found
        """
        with db_conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                """
                SELECT * FROM urls WHERE id = %s
                """,
                (url_id,)
            )
            result = cursor.fetchone()
            return result if result else None

    def get_all_urls(self) -> list:
        """
        Retrieve all URLs from database

        Returns:
            list: List of all URLs as dictionaries
        """
        with db_conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("SELECT * FROM urls")
            return cursor.fetchall()
