import os

import mysql.connector
from dotenv import load_dotenv


# Load variables from the .env file
load_dotenv()


def test_database_connection():
    """Test the connection to the SimVest MySQL database."""

    try:
        # Connect using credentials stored in environment variables
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT", "3306")),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )

        # Check whether the connection succeeded
        if connection.is_connected():
            print("Successfully connected to SimVest MySQL database!")

        # Close the database connection
        connection.close()

    except mysql.connector.Error as error:
        print(f"Database connection failed: {error}")


if __name__ == "__main__":
    test_database_connection()