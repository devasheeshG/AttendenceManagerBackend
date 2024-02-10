"""Utils functions for the application."""

import psycopg2


def check_if_user_exists(username: str, cursor: psycopg2.extensions.connection) -> bool:
    """Check if User Exists."""
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    return cursor.fetchone()
