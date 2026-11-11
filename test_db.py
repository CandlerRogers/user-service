import mysql.connector

from db import get_db_connection


def test_database_connection():
    """Verify that the User Service can connect to MySQL."""

    connection = None

    try:
        connection = get_db_connection()

        if connection.is_connected():
            print("Successfully connected to MySQL!")

    except mysql.connector.Error as error:
        print(f"Database connection failed: {error}")

    finally:
        if connection is not None and connection.is_connected():
            connection.close()


if __name__ == "__main__":
    test_database_connection()