"""
Base service class with common functionality
"""
from flask import current_app
from models.db_models import db
import logging
from typing import Optional, List, Dict, Any

logger = logging.getLogger(__name__)


class BaseService:
    """Base service class with common database operations"""
    
    @staticmethod
    def commit_changes():
        """Commit database changes with error handling"""
        try:
            db.session.commit()
            return True
        except Exception as e:
            logger.error(f"Database commit error: {str(e)}")
            db.session.rollback()
            raise e
    
    @staticmethod
    def handle_db_error(operation: str, error: Exception):
        """Handle database errors consistently"""
        logger.error(f"Database error in {operation}: {str(error)}")
        db.session.rollback()
        raise error
