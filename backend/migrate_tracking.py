#!/usr/bin/env python3
"""
Database migration script to create the tracking_events table
"""

import os
import sys
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

def get_db_connection():
    """Get database connection"""
    try:
        connection = psycopg2.connect(
            host=os.environ.get('POSTGRES_HOST', 'localhost'),
            database=os.environ.get('POSTGRES_DB', 'analytics'),
            user=os.environ.get('POSTGRES_USER', 'postgres'),
            password=os.environ.get('POSTGRES_PASSWORD', 'tobias'),
            port=os.environ.get('POSTGRES_PORT', '6666')
        )
        return connection
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def create_tracking_table():
    """Create the tracking_events table and views"""
    
    # SQL to create the tracking_events table
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS tracking_events (
        id SERIAL PRIMARY KEY,
        session_id VARCHAR(255) NOT NULL,
        page_url TEXT NOT NULL,
        referrer TEXT,
        ip_address INET,
        user_agent TEXT,
        browser VARCHAR(100),
        os VARCHAR(100),
        device VARCHAR(50),
        country VARCHAR(100),
        city VARCHAR(100),
        is_entry_page BOOLEAN DEFAULT FALSE,
        is_exit_page BOOLEAN DEFAULT FALSE,
        event_name VARCHAR(255),
        event_data JSONB,
        timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    # SQL to create indexes
    create_indexes_sql = [
        "CREATE INDEX IF NOT EXISTS idx_tracking_session_id ON tracking_events (session_id);",
        "CREATE INDEX IF NOT EXISTS idx_tracking_timestamp ON tracking_events (timestamp);",
        "CREATE INDEX IF NOT EXISTS idx_tracking_page_url ON tracking_events USING HASH (page_url);",
        "CREATE INDEX IF NOT EXISTS idx_tracking_event_name ON tracking_events (event_name);",
        "CREATE INDEX IF NOT EXISTS idx_tracking_country ON tracking_events (country);",
        "CREATE INDEX IF NOT EXISTS idx_tracking_browser ON tracking_events (browser);",
        "CREATE INDEX IF NOT EXISTS idx_tracking_os ON tracking_events (os);",
        "CREATE INDEX IF NOT EXISTS idx_tracking_device ON tracking_events (device);"
    ]
    
    # SQL to create views
    create_views_sql = [
        """
        CREATE OR REPLACE VIEW page_views AS
        SELECT 
            id,
            session_id,
            page_url,
            referrer,
            ip_address,
            user_agent,
            browser,
            os,
            device,
            country,
            city,
            is_entry_page,
            is_exit_page,
            timestamp
        FROM tracking_events
        WHERE event_name IS NULL OR event_name = 'page_view';
        """,
        """
        CREATE OR REPLACE VIEW custom_events AS
        SELECT 
            id,
            session_id,
            page_url,
            event_name,
            event_data,
            browser,
            os,
            device,
            country,
            timestamp
        FROM tracking_events
        WHERE event_name IS NOT NULL AND event_name != 'page_view';
        """,
        """
        CREATE OR REPLACE VIEW session_analytics AS
        SELECT 
            session_id,
            COUNT(*) as page_views,
            MIN(timestamp) as session_start,
            MAX(timestamp) as session_end,
            EXTRACT(EPOCH FROM (MAX(timestamp) - MIN(timestamp))) as duration_seconds,
            COUNT(DISTINCT page_url) as unique_pages,
            STRING_AGG(DISTINCT browser, ', ') as browsers,
            STRING_AGG(DISTINCT os, ', ') as operating_systems,
            STRING_AGG(DISTINCT device, ', ') as devices,
            STRING_AGG(DISTINCT country, ', ') as countries
        FROM tracking_events
        WHERE event_name IS NULL OR event_name = 'page_view'
        GROUP BY session_id;
        """
    ]
    
    connection = get_db_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        
        # Create the table
        print("Creating tracking_events table...")
        cursor.execute(create_table_sql)
        
        # Create indexes
        print("Creating indexes...")
        for index_sql in create_indexes_sql:
            cursor.execute(index_sql)
        
        # Create views
        print("Creating views...")
        for view_sql in create_views_sql:
            cursor.execute(view_sql)
        
        connection.commit()
        print("✅ Successfully created tracking_events table, indexes, and views!")
        return True
        
    except Exception as e:
        print(f"❌ Error creating tracking table: {e}")
        connection.rollback()
        return False
        
    finally:
        cursor.close()
        connection.close()

def check_table_exists():
    """Check if the tracking_events table already exists"""
    connection = get_db_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'tracking_events'
            );
        """)
        exists = cursor.fetchone()[0]
        return exists
        
    except Exception as e:
        print(f"Error checking table existence: {e}")
        return False
        
    finally:
        cursor.close()
        connection.close()

def main():
    """Main migration function"""
    print("🚀 Starting database migration for tracking system...")
    
    # Check if table already exists
    if check_table_exists():
        print("⚠️  tracking_events table already exists!")
        response = input("Do you want to continue anyway? This will recreate views. (y/N): ")
        if response.lower() != 'y':
            print("Migration cancelled.")
            return
    
    # Create the tracking table
    if create_tracking_table():
        print("🎉 Migration completed successfully!")
        print("\nNext steps:")
        print("1. Update your backend to use the new tracking routes")
        print("2. Deploy the tracking script to your websites")
        print("3. Start collecting visitor data!")
    else:
        print("💥 Migration failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
