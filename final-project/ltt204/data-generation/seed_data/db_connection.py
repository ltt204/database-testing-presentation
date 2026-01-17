import mysql.connector
from mysql.connector import Error
import os

def get_db_connection():
    """Create and return a MySQL database connection."""
    try:
        # Use 127.0.0.1 for Docker container on Linux
        connection = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST', '127.0.0.1'),
            port=3310,  # From docker-compose.yml
            database=os.getenv('MYSQL_DATABASE', 'orangehrm'),
            user=os.getenv('MYSQL_USER', 'orangehrm'),
            password=os.getenv('MYSQL_PASSWORD', 'orangehrm')
        )
        if connection.is_connected():
            print("✓ Successfully connected to MySQL database")
            return connection
    except Error as e:
        print(f"✗ Error connecting to MySQL: {e}")
        return None

def execute_query(connection, query, params=None):
    """Execute a single query."""
    cursor = connection.cursor()
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        connection.commit()
        return cursor.lastrowid
    except Error as e:
        print(f"✗ Error executing query: {e}")
        print(f"Query: {query}")
        connection.rollback()
        raise
    finally:
        cursor.close()

def execute_many(connection, query, data):
    """Execute batch insert."""
    cursor = connection.cursor()
    try:
        cursor.executemany(query, data)
        connection.commit()
        print(f"✓ Inserted {cursor.rowcount} rows")
        return cursor.rowcount
    except Error as e:
        print(f"✗ Error executing batch query: {e}")
        connection.rollback()
        raise
    finally:
        cursor.close()

def close_connection(connection):
    """Close database connection."""
    if connection and connection.is_connected():
        connection.close()
        print("✓ Database connection closed")
