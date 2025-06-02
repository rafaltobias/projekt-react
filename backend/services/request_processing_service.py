"""
Request processing service - business logic for HTTP request processing
"""
from typing import Optional, Dict, Any
from flask import request
import logging

logger = logging.getLogger(__name__)


class RequestProcessingService:
    """Service for processing HTTP request data"""
    
    @staticmethod
    def extract_request_metadata(flask_request) -> Dict[str, Any]:
        """
        Extract metadata from Flask request object
        
        Args:
            flask_request: Flask request object
            
        Returns:
            Dictionary with extracted metadata
        """
        return {
            'ip_address': flask_request.remote_addr,
            'user_agent': flask_request.headers.get('User-Agent'),
            'referer_header': flask_request.headers.get('Referer')
        }
    
    @staticmethod
    def resolve_referrer(request_referrer: Optional[str], header_referrer: Optional[str]) -> Optional[str]:
        """
        Resolve final referrer from request data and headers
        
        Args:
            request_referrer: Referrer from request body
            header_referrer: Referrer from HTTP headers
            
        Returns:
            Final referrer to use
        """
        return request_referrer or header_referrer
    
    @staticmethod
    def validate_ip_address(ip_address: str) -> bool:
        """
        Validate if IP address is valid for processing
        
        Args:
            ip_address: IP address to validate
            
        Returns:
            True if IP is valid for processing
        """
        if not ip_address:
            return False
            
        # Skip localhost and private networks for geolocation
        if ip_address in ['127.0.0.1', 'localhost', '::1']:
            return False
            
        # Add more validation as needed
        return True
