import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get connection parameters
postgres_user = os.environ.get('POSTGRES_USER', 'postgres')
postgres_host = os.environ.get('POSTGRES_HOST', 'localhost')
postgres_db = os.environ.get('POSTGRES_DB', 'analytics')
postgres_password = os.environ.get('POSTGRES_PASSWORD', 'tobias')
postgres_port = os.environ.get('POSTGRES_PORT', '6666')

print(f"Attempting to connect to PostgreSQL database:")
print(f"Host: {postgres_host}")
print(f"Port: {postgres_port}")
print(f"Database: {postgres_db}")
print(f"User: {postgres_user}")
print(f"Password: {'*' * len(postgres_password)}")

try:
    # Establish connection
    conn = psycopg2.connect(
        dbname=postgres_db,
        user=postgres_user,
        password=postgres_password,
        host=postgres_host,
        port=postgres_port
    )
    
    # Create a cursor
    cur = conn.cursor()
    
    # Get PostgreSQL version
    cur.execute('SELECT version();')
    version = cur.fetchone()
    print(f"PostgreSQL version: {version[0]}")
    
    # Check if tables exist
    cur.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
    """)
    tables = cur.fetchall()
    print("\nDatabase tables:")
    if tables:
        for table in tables:
            print(f"- {table[0]}")
    else:
        print("No tables found in the database")
    
    # Close connection
    cur.close()
    conn.close()
    
    print("\nConnection test successful!")
    
except Exception as e:
    print(f"Error connecting to PostgreSQL: {str(e)}")