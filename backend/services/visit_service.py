"""
Visit tracking service - business logic for visit management
"""
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy import func, desc, and_
from models.db_instance import db
from models.db_models import Visit
from services.base_service import BaseService
from services.geolocation_service import GeolocationService
from services.request_processing_service import RequestProcessingService
import logging

logger = logging.getLogger(__name__)


class VisitService(BaseService):
    """Service for visit tracking operations"""
    
    @staticmethod
    def create_visit(
        page_url: str,
        ip_address: str,
        user_agent: str,
        referrer: Optional[str] = None,
        browser: Optional[str] = None,
        os: Optional[str] = None,
        device: Optional[str] = None,
        country: Optional[str] = None,
        session_id: Optional[str] = None,
        is_entry_page: bool = False,
        is_exit_page: bool = False,
        event_name: Optional[str] = None,
        event_data: Optional[Dict[str, Any]] = None
    ) -> Optional[int]:
        """Create a new visit record"""
        try:
            visit = Visit(
                page_url=page_url,
                ip_address=ip_address,
                user_agent=user_agent,
                referrer=referrer,
                browser=browser,
                os=os,
                device=device,
                country=country,
                session_id=session_id,
                is_entry_page=is_entry_page,
                is_exit_page=is_exit_page,
                event_name=event_name,
                event_data=event_data
            )
            
            db.session.add(visit)
            VisitService.commit_changes()
            
            logger.info(f"Created visit {visit.id} for page {page_url}")
            return visit.id
            
        except Exception as e:
            VisitService.handle_db_error("create_visit", e)
            return None
    
    @staticmethod
    def get_visits(limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """Get visits with pagination"""
        try:
            visits = Visit.query.order_by(desc(Visit.timestamp)).limit(limit).offset(offset).all()
            return [visit.to_dict() for visit in visits]
        except Exception as e:
            logger.error(f"Error getting visits: {str(e)}")
            return []
    
    @staticmethod
    def get_visit_by_id(visit_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific visit by ID"""
        try:
            visit = Visit.query.get(visit_id)
            return visit.to_dict() if visit else None
        except Exception as e:
            logger.error(f"Error getting visit {visit_id}: {str(e)}")
            return None
    
    @staticmethod
    def get_visits_by_session(session_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all visits for a specific session"""
        try:
            visits = Visit.query.filter_by(session_id=session_id).order_by(Visit.timestamp).limit(limit).all()
            return [visit.to_dict() for visit in visits]
        except Exception as e:
            logger.error(f"Error getting visits for session {session_id}: {str(e)}")
            return []
    
    @staticmethod
    def update_exit_pages(session_id: str, new_visit_id: int) -> bool:
        """Update previous visits in the session to not be exit pages"""
        try:
            Visit.query.filter(
                and_(
                    Visit.session_id == session_id,
                    Visit.id != new_visit_id
                )
            ).update({'is_exit_page': False})
            
            VisitService.commit_changes()
            return True
            
        except Exception as e:
            VisitService.handle_db_error("update_exit_pages", e)
            return False
    
    @staticmethod
    def get_visit_count() -> int:
        """Get total count of visits"""
        try:
            return Visit.query.count()
        except Exception as e:
            logger.error(f"Error getting visit count: {str(e)}")
            return 0
    
    @staticmethod
    def get_unique_sessions_count(days: int = 30) -> int:
        """Get count of unique sessions within specified timeframe"""
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            return db.session.query(func.count(func.distinct(Visit.session_id))).filter(
                Visit.timestamp >= cutoff_date
            ).scalar()
        except Exception as e:
            logger.error(f"Error getting unique sessions count: {str(e)}")
            return 0
    
    @staticmethod
    def process_visit_tracking(
        visit_data: Dict[str, Any], 
        request_metadata: Dict[str, Any]
    ) -> Optional[int]:
        """
        Process a complete visit tracking request with business logic
        
        Args:
            visit_data: Validated visit data from request
            request_metadata: Request metadata (IP, user agent, etc.)
            
        Returns:
            Visit ID if successful, None otherwise
        """
        try:
            # Extract and process request data
            ip_address = request_metadata.get('ip_address')
            user_agent = request_metadata.get('user_agent')
            header_referrer = request_metadata.get('referer_header')
            
            # Resolve referrer
            final_referrer = RequestProcessingService.resolve_referrer(
                visit_data.get('referrer'),
                header_referrer
            )
            
            # Handle geolocation
            country = visit_data.get('country')
            if GeolocationService.should_geolocate_ip(ip_address, country):
                location_data = GeolocationService.get_location_from_ip(ip_address)
                country = location_data.get('country')
            
            # Create the visit
            visit_id = VisitService.create_visit(
                page_url=visit_data.get('page_url'),
                ip_address=ip_address,
                user_agent=user_agent,
                referrer=final_referrer,
                browser=visit_data.get('browser'),
                os=visit_data.get('os'),
                device=visit_data.get('device'),
                country=country,
                session_id=visit_data.get('session_id'),
                is_entry_page=visit_data.get('is_entry_page', False),
                is_exit_page=visit_data.get('is_exit_page', False),
                event_name=visit_data.get('event_name'),
                event_data=visit_data.get('event_data')
            )
            
            # Handle session management for page visits (not events)
            if visit_id and visit_data.get('session_id') and not visit_data.get('event_name'):
                VisitService.update_exit_pages(visit_data.get('session_id'), visit_id)
            
            return visit_id
            
        except Exception as e:
            logger.error(f"Error processing visit tracking: {str(e)}")
            return None
