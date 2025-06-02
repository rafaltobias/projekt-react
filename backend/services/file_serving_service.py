"""
File serving service - business logic for serving static files
"""
from typing import Optional, Tuple
import os
import logging

logger = logging.getLogger(__name__)


class FileServingService:
    """Service for file serving operations"""
    
    @staticmethod
    def get_frontend_static_path() -> str:
        """Get the path to frontend static files"""
        return os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 
            '..', 'frontend', 'src', 'static'
        )
    
    @staticmethod
    def get_frontend_public_path() -> str:
        """Get the path to frontend public files"""
        return os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 
            '..', 'frontend', 'public'
        )
    
    @staticmethod
    def validate_file_exists(file_path: str, filename: str) -> bool:
        """
        Validate if a file exists in the specified path
        
        Args:
            file_path: Path to the directory
            filename: Name of the file
            
        Returns:
            True if file exists, False otherwise
        """
        try:
            full_path = os.path.join(file_path, filename)
            return os.path.exists(full_path) and os.path.isfile(full_path)
        except Exception as e:
            logger.error(f"Error checking file existence: {e}")
            return False
    
    @staticmethod
    def get_tracker_script_info(script_type: str = 'regular') -> Tuple[str, str]:
        """
        Get tracker script path and filename
        
        Args:
            script_type: 'regular' or 'minified'
            
        Returns:
            Tuple of (path, filename)
        """
        filename = 'tracker.min.js' if script_type == 'minified' else 'tracker.js'
        path = FileServingService.get_frontend_static_path()
        return path, filename
