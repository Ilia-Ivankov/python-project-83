import psycopg2
from psycopg2.extras import DictCursor, NamedTupleCursor
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


class UrlRepository:
    """Repository class for handling URL-related database operations."""

    def connect_db(self):
        """Establishes database connection."""
        return psycopg2.connect(DATABASE_URL)

    def commit(self, connection):
        """Commits transaction."""
        connection.commit()

    def close(self, connection):
        """Closes database connection."""
        connection.close()

    def insert_url(self, url: str) -> int:
        """Inserts URL into database and returns its ID."""
        with self.connect_db() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute(
                    """
                    INSERT INTO urls (name, created_at)
                    VALUES (%s, %s)
                    RETURNING id
                    """,
                    (url, datetime.today()),
                )
                self.commit(conn)
                return cur.fetchone()["id"]

    def get_url(self, url_id: int) -> dict:
        """Retrieves URL data by its ID."""
        with self.connect_db() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute(
                    """
                    SELECT * FROM urls WHERE id = %s
                    """,
                    (url_id,),
                )
                result = cur.fetchone()
                return result if result else None

    def get_url_by_name(self, url_name: str) -> dict:
        """Retrieves URL data by its name."""
        with self.connect_db() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute(
                    """
                    SELECT * FROM urls WHERE name = %s
                    """,
                    (url_name,),
                )
                result = cur.fetchone()
                return result if result else None

    def get_urls_with_last_check_date_and_status_code(self) -> list:
        """Retrieves all URLs with their latest check date and status code."""
        with self.connect_db() as conn:
            with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
                cur.execute(
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
                return cur.fetchall()

    def insert_url_check(
        self,
        url_id: int,
        status_code: int,
        h1: str | None,
        title: str | None,
        description: str | None,
    ) -> int:
        """Inserts URL check and returns the check ID."""
        with self.connect_db() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute(
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
                self.commit(conn)
                return cur.fetchone()["id"]

    def get_checks_by_url_id(self, url_id: int) -> list:
        """Retrieves all checks for a specific URL."""
        with self.connect_db() as conn:
            with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
                cur.execute(
                    """
                    SELECT * FROM url_checks WHERE url_id = %s ORDER BY id DESC
                    """,
                    (url_id,),
                )
                return cur.fetchall()
