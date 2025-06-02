"""
Database connection module.
Now using SQLAlchemy ORM instead of direct SQL execution.
"""
import os
import logging
from models.db_instance import db

logger = logging.getLogger(__name__)

def init_db(app):
    """Initialize the database with the Flask app"""
    try:
        with app.app_context():
            # This will create tables based on ORM models if they don't exist
            db.create_all()
            logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise

def create_tables():
    """Create database tables using SQLAlchemy ORM"""
    try:
        # This is now handled by db.create_all() in init_db
        db.create_all()
        logger.info("Tables created successfully")
        return True
    except Exception as e:
        logger.error(f"Error creating tables: {str(e)}")
        return False
