"""
Geolocation service - business logic for IP-based geolocation
"""
from typing import Optional, Dict, Any
import requests
import logging

logger = logging.getLogger(__name__)


class GeolocationService:
    """Service for IP geolocation operations"""
    
    @staticmethod
    def get_location_from_ip(ip_address: str) -> Dict[str, Optional[str]]:
        """
        Get location information from IP address using a free IP geolocation service
        
        Args:
            ip_address: The IP address to geolocate
            
        Returns:
            Dictionary with country, city, and region information
        """
        if not ip_address or ip_address == '127.0.0.1':
            return {'country': None, 'city': None, 'region': None}
            
        try:
            response = requests.get(
                f'http://ip-api.com/json/{ip_address}', 
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    return {
                        'country': data.get('country'),
                        'city': data.get('city'),
                        'region': data.get('regionName')
                    }
                    
        except Exception as e:
            logger.error(f"Error getting location for IP {ip_address}: {e}")
        
        return {'country': None, 'city': None, 'region': None}
    
    @staticmethod
    def should_geolocate_ip(ip_address: str, provided_country: Optional[str] = None) -> bool:
        """
        Determine if IP geolocation should be performed
        
        Args:
            ip_address: The IP address
            provided_country: Country provided in request
            
        Returns:
            True if geolocation should be performed
        """
        return (
            not provided_country and 
            ip_address and 
            ip_address != '127.0.0.1' and
            ip_address != 'localhost'
        )
