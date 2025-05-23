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
    
    # Get columns for visits table
    cur.execute("""
        SELECT column_name, data_type, character_maximum_length
        FROM information_schema.columns
        WHERE table_name = 'visits'
        ORDER BY ordinal_position;
    """)
    
    columns = cur.fetchall()
    
    print("\nColumns in 'visits' table:")
    for column in columns:
        print(f"- {column[0]}: {column[1]}", end="")
        if column[2]:
            print(f" (length: {column[2]})")
        else:
            print()
    
    # Get columns for tags table
    cur.execute("""
        SELECT column_name, data_type, character_maximum_length
        FROM information_schema.columns
        WHERE table_name = 'tags'
        ORDER BY ordinal_position;
    """)
    
    columns = cur.fetchall()
    
    print("\nColumns in 'tags' table:")
    for column in columns:
        print(f"- {column[0]}: {column[1]}", end="")
        if column[2]:
            print(f" (length: {column[2]})")
        else:
            print()
    
    # Close connection
    cur.close()
    conn.close()
    
except Exception as e:
    print(f"Error checking table schema: {str(e)}")
