#!/usr/bin/env python3
"""
Database migration script to add trigger and action fields to tags table
"""

from models.database import execute_query
import sys

def migrate_tags_table():
    """Add new columns to the tags table for triggers and actions"""
    
    print("Starting tags table migration...")
    
    # Add type column
    try:
        add_type = """
        ALTER TABLE tags 
        ADD COLUMN IF NOT EXISTS type TEXT;
        """
        execute_query(add_type)
        print("✓ Added type column to tags table")
    except Exception as e:
        print(f"Warning: Could not add type column: {e}")
    
    # Add trigger column
    try:
        add_trigger = """
        ALTER TABLE tags 
        ADD COLUMN IF NOT EXISTS trigger TEXT;
        """
        execute_query(add_trigger)
        print("✓ Added trigger column to tags table")
    except Exception as e:
        print(f"Warning: Could not add trigger column: {e}")
    
    # Add config column
    try:
        add_config = """
        ALTER TABLE tags 
        ADD COLUMN IF NOT EXISTS config TEXT;
        """
        execute_query(add_config)
        print("✓ Added config column to tags table")
    except Exception as e:
        print(f"Warning: Could not add config column: {e}")
    
    print("Tags table migration completed!")

if __name__ == "__main__":
    try:
        migrate_tags_table()
    except Exception as e:
        print(f"Migration failed: {e}")
        sys.exit(1)
