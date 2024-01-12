"""Database Client."""

import os
import sys
import psycopg2
import dotenv

dotenv.load_dotenv(".env")

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils import check_if_user_exists


class Database:
    def __init__(self) -> None:
        """Database Client Initialization."""
        # Connect to Database
        self.conn = psycopg2.connect(
            dbname=os.getenv("PG_DB_NAME"),
            user=os.getenv("PG_DB_USER"),
            password=os.getenv("PG_DB_PASSWORD"),
            host=os.getenv("PG_DB_HOST"),
            port=os.getenv("PG_DB_PORT"),
        )
        # Create Cursor
        self.cursor = self.conn.cursor()

        # Create Table `users` if not exists
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                username VARCHAR(6) NOT NULL PRIMARY KEY,
                password VARCHAR(64) NOT NULL
            )
        """
        )
        self.conn.commit()

        # Create Table `attendence` if not exists
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS attendence_table (
                username VARCHAR(6) REFERENCES users(username),
                subject VARCHAR(100) NOT NULL,
                max_hours INT NOT NULL,
                attended_hours INT NOT NULL,
                absent_hours INT NOT NULL,
                total_percentage FLOAT NOT NULL,
                date DATE NOT NULL,
                time TIME NOT NULL,
                PRIMARY KEY (username, subject, max_hours)
            )
        """
        )
        self.conn.commit()

    def __del__(self) -> None:
        """Database Client Deletion."""
        # Close Cursor
        self.cursor.close()
        # Close Connection
        self.conn.close()

    def add_user(self, username: str, password: str) -> dict:
        """Add User to Database."""
        # Check if User Exists in Database
        if not check_if_user_exists(username, self.cursor):
            try:
                self.cursor.execute(
                    "INSERT INTO users (username, password) VALUES (%s, %s)",
                    (username, password),
                )
                self.conn.commit()
                return {"status": "success", "message": "User Registered Successfully"}
            except Exception as e:
                return {
                    "status": "error",
                    "message": (
                        f"pg error code: {e.pgcode}" if hasattr(e, "pgcode") else str(e)
                    ),
                }
        return {"status": "error", "message": "User Already Exists"}

    def remove_user(self, username: str) -> dict:
        """Remove User from Database."""
        # Check if User Exists in Database
        if check_if_user_exists(username, self.cursor):
            self.cursor.execute("DELETE FROM users WHERE username = %s", (username,))
            self.conn.commit()
            return {"status": "success", "message": "User Removed Successfully"}
        return {"status": "error", "message": "User Does Not Exists"}

    def get_user_password(self, username: str) -> str | None:
        """Get User's Password from Database."""
        self.cursor.execute(
            "SELECT password FROM users WHERE username = %s", (username,)
        )
        res = self.cursor.fetchone()
        return res[0] if res else None

    def get_all_users(self) -> list:
        """Get All Users from Database."""
        self.cursor.execute("SELECT username, password FROM users")
        return self.cursor.fetchall()


if __name__ == "__main__":
    db = Database()
    # db.add_user('tempur', 'supersecrotpassword')
    # print(db.get_user_password('tempur'))
    # print(db.remove_user('tempur'))
    # print(db.get_user_password('dm0359'))
    # print(type(db.cursor))
