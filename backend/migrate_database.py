#!/usr/bin/env python3
"""
Database migration script to add event tracking fields to existing visits table
"""

from models.database import execute_query
import sys

def migrate_database():
    """Add new columns to the visits table for event tracking"""
    
    print("Starting database migration...")
    
    # Add event_name column
    try:
        add_event_name = """
        ALTER TABLE visits 
        ADD COLUMN IF NOT EXISTS event_name TEXT;
        """
        execute_query(add_event_name)
        print("✓ Added event_name column")
    except Exception as e:
        print(f"Warning: Could not add event_name column: {e}")
    
    # Add event_data column
    try:
        add_event_data = """
        ALTER TABLE visits 
        ADD COLUMN IF NOT EXISTS event_data JSONB;
        """
        execute_query(add_event_data)
        print("✓ Added event_data column")
    except Exception as e:
        print(f"Warning: Could not add event_data column: {e}")
    
    # Create indexes for better performance
    try:
        create_session_index = """
        CREATE INDEX IF NOT EXISTS idx_visits_session_id ON visits(session_id);
        """
        execute_query(create_session_index)
        print("✓ Created index on session_id")
    except Exception as e:
        print(f"Warning: Could not create session_id index: {e}")
    
    try:
        create_timestamp_index = """
        CREATE INDEX IF NOT EXISTS idx_visits_timestamp ON visits(timestamp);
        """
        execute_query(create_timestamp_index)
        print("✓ Created index on timestamp")
    except Exception as e:
        print(f"Warning: Could not create timestamp index: {e}")
    
    try:
        create_event_index = """
        CREATE INDEX IF NOT EXISTS idx_visits_event_name ON visits(event_name);
        """
        execute_query(create_event_index)
        print("✓ Created index on event_name")
    except Exception as e:
        print(f"Warning: Could not create event_name index: {e}")
    
    print("Database migration completed!")

if __name__ == "__main__":
    try:
        migrate_database()
    except Exception as e:
        print(f"Migration failed: {e}")
        sys.exit(1)
