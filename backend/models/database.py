import psycopg2
from psycopg2.extras import RealDictCursor
from config import DB_HOST, DB_NAME, DB_USER, DB_PASS, DB_PORT

# Create database connection string
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# For logging
print(f"Connecting to PostgreSQL database: {DB_HOST}:{DB_PORT}/{DB_NAME}")

def get_db_connection():
    """Create a new database connection"""
    connection = psycopg2.connect(DATABASE_URL)
    connection.autocommit = True
    return connection, connection.cursor(cursor_factory=RealDictCursor)

def close_connection(connection):
    """Close a database connection"""
    if connection:
        connection.close()

def execute_query(query, params=None):
    """Execute a query and return results"""
    connection, cursor = None, None
    try:
        connection = psycopg2.connect(DATABASE_URL)
        connection.autocommit = True
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute(query, params)
        
        # Check if the query returns rows
        if cursor.description:
            result = cursor.fetchall()
            return result
        return None
    except Exception as e:
        print(f"Database error: {e}")
        raise
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            
def create_tables():
    """Create necessary tables if they don't exist"""
    # Visits table
    visits_table = """
    CREATE TABLE IF NOT EXISTS visits (
        id SERIAL PRIMARY KEY,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        page_url TEXT,
        referrer TEXT,
        user_agent TEXT,
        ip_address TEXT,
        browser TEXT,
        os TEXT,
        device TEXT,
        country TEXT,
        session_id TEXT,
        is_entry_page BOOLEAN DEFAULT FALSE,
        is_exit_page BOOLEAN DEFAULT FALSE,
        event_name TEXT,
        event_data JSONB
    );
    """
    
    # Tags table
    tags_table = """
    CREATE TABLE IF NOT EXISTS tags (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    execute_query(visits_table)
    execute_query(tags_table)
    
    print("Database tables created or already exist")

# Initialize tables
create_tables()
