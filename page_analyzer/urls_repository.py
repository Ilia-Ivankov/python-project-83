import psycopg2
from psycopg2.extras import DictCursor
from datetime import datetime
from page_analyzer.config import DATABASE_URL


class UrlRepository:
    """Repository class for handling URL-related database operations."""

    def save_url(self, url: str) -> int:
        """Saves a URL in the database and returns its ID."""
        with psycopg2.connect(DATABASE_URL) as db_connection:
            with db_connection.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(
                    """
                    INSERT INTO urls (name, created_at)
                    VALUES (%s, %s)
                    RETURNING id
                    """,
                    (url, datetime.today()),
                )
                db_connection.commit()
                return cursor.fetchone()["id"]

    def get_url_by_id(self, url_id: int) -> dict:
        """Retrieves URL data by its ID."""
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
        """
        Retrieves all URLs with their latest check date and response code.
        """
        with psycopg2.connect(DATABASE_URL) as db_connection:
            with db_connection.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(
                    """
                    SELECT
                        urls.id AS ID,
                        urls.name AS name,
                        (SELECT created_at
                            FROM url_checks
                            WHERE url_id = urls.id
                            ORDER BY id DESC
                            LIMIT 1) AS last_check_date,
                        (SELECT status_code
                            FROM url_checks
                            WHERE url_id = urls.id
                            ORDER BY id DESC
                            LIMIT 1) AS status_code
                    FROM urls
                    LEFT JOIN url_checks
                    ON urls.id = url_checks.url_id
                    GROUP BY urls.id, urls.name
                    ORDER BY urls.created_at DESC;
                    """
                )
                return cursor.fetchall()

    def get_url_by_name(self, url_name: str) -> dict:
        """Retrieves URL data by its name."""
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

    def save_url_check(
        self,
        url_id: int,
        status_code: int,
        h1: str | None,
        title: str | None,
        description: str | None,
    ) -> int:
        """Saves a URL check and returns the check ID."""
        with psycopg2.connect(DATABASE_URL) as db_connection:
            with db_connection.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(
                    """
                    INSERT INTO url_checks (
                        url_id, status_code, h1, title, description, created_at
                    ) VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                    (
                        url_id,
                        status_code,
                        h1,
                        title,
                        description,
                        datetime.today()
                    ),
                )
                db_connection.commit()
                return cursor.fetchone()["id"]

    def get_all_checks(self, url_id: int) -> list:
        """Retrieves all checks for a specific URL."""
        with psycopg2.connect(DATABASE_URL) as db_connection:
            with db_connection.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(
                    """
                    SELECT * FROM url_checks WHERE url_id = %s ORDER BY id DESC
                    """,
                    (url_id,),
                )
                return cursor.fetchall()
