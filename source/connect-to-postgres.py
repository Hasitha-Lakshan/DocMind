import psycopg
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def list_databases():
    # Fetch database connection parameters from environment variables
    conn_params = {
        'dbname': os.getenv('POSTGRES_DB'),
        'user': os.getenv('POSTGRES_USER'),
        'password': os.getenv('POSTGRES_PASSWORD'),
        'host': 'docmind_db',  # Use the service name from docker-compose
        'port': os.getenv('POSTGRES_PORT', '5432')  # Default to 5432 if not set
    }

    try:
        # Establishing the connection using psycopg3
        with psycopg.connect(**conn_params) as conn:
            with conn.cursor() as cursor:
                # Query to list databases
                cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
                
                # Fetching all databases
                databases = cursor.fetchall()
                
                # Printing the database names
                print("Available databases:")
                for db in databases:
                    print(f"- {db[0]}")

    except Exception as error:
        print(f"Error: {error}")

# Call the function to list databases
if __name__ == "__main__":
    list_databases()
