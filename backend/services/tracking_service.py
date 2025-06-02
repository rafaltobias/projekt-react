"""
Tracking events service - business logic for event tracking
"""
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy import func, desc, and_, or_
from models.db_instance import db
from models.db_models import TrackingEvent
from services.base_service import BaseService
from services.geolocation_service import GeolocationService
from services.request_processing_service import RequestProcessingService
import logging

logger = logging.getLogger(__name__)


class TrackingService(BaseService):
    """Service for tracking events operations"""
    
    @staticmethod
    def create_tracking_event(
        session_id: str,
        page_url: str,
        ip_address: str,
        user_agent: str,
        referrer: Optional[str] = None,
        browser: Optional[str] = None,
        os: Optional[str] = None,
        device: Optional[str] = None,
        country: Optional[str] = None,
        city: Optional[str] = None,
        is_entry_page: bool = False,
        is_exit_page: bool = False,
        event_name: Optional[str] = None,
        event_data: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """Create a new tracking event"""
        try:
            event = TrackingEvent(
                session_id=session_id,
                page_url=page_url,
                ip_address=ip_address,
                user_agent=user_agent,
                referrer=referrer,
                browser=browser,
                os=os,
                device=device,
                country=country,
                city=city,
                is_entry_page=is_entry_page,
                is_exit_page=is_exit_page,
                event_name=event_name,
                event_data=event_data
            )
            
            db.session.add(event)
            TrackingService.commit_changes()
            
            logger.info(f"Created tracking event {event.id} for session {session_id}")
            return {
                'id': event.id,
                'timestamp': event.timestamp
            }
            
        except Exception as e:
            TrackingService.handle_db_error("create_tracking_event", e)
            return None
    
    @staticmethod
    def add_tracking_event(
        session_id: str,
        page_url: str,
        ip_address: str,
        user_agent: str,
        referrer: Optional[str] = None,
        browser: Optional[str] = None,
        os: Optional[str] = None,
        device: Optional[str] = None,
        country: Optional[str] = None,
        city: Optional[str] = None,
        is_entry_page: bool = False,
        is_exit_page: bool = False,
        event_name: Optional[str] = None,
        event_data: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """Add a new tracking event - alias for create_tracking_event"""
        return TrackingService.create_tracking_event(
            session_id=session_id,
            page_url=page_url,
            ip_address=ip_address,
            user_agent=user_agent,
            referrer=referrer,
            browser=browser,
            os=os,
            device=device,
            country=country,
            city=city,
            is_entry_page=is_entry_page,
            is_exit_page=is_exit_page,
            event_name=event_name,
            event_data=event_data
        )
    
    @staticmethod
    def get_tracking_events(limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """Get tracking events with pagination"""
        try:
            events = TrackingEvent.query.order_by(desc(TrackingEvent.timestamp)).limit(limit).offset(offset).all()
            return [event.to_dict() for event in events]
        except Exception as e:
            logger.error(f"Error getting tracking events: {str(e)}")
            return []
    
    @staticmethod
    def get_page_views(limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """Get page views (excluding custom events)"""
        try:
            events = TrackingEvent.query.filter(
                or_(TrackingEvent.event_name.is_(None), TrackingEvent.event_name == '')
            ).order_by(desc(TrackingEvent.timestamp)).limit(limit).offset(offset).all()
            return [event.to_dict() for event in events]
        except Exception as e:
            logger.error(f"Error getting page views: {str(e)}")
            return []
    
    @staticmethod
    def get_custom_events(limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """Get custom events only"""
        try:
            events = TrackingEvent.query.filter(
                and_(TrackingEvent.event_name.is_not(None), TrackingEvent.event_name != '')
            ).order_by(desc(TrackingEvent.timestamp)).limit(limit).offset(offset).all()
            return [event.to_dict() for event in events]
        except Exception as e:
            logger.error(f"Error getting custom events: {str(e)}")
            return []
    
    @staticmethod
    def get_session_data(session_id: str) -> Optional[Dict[str, Any]]:
        """Get all tracking events for a specific session"""
        try:
            events = TrackingEvent.query.filter_by(session_id=session_id).order_by(TrackingEvent.timestamp).all()
            
            if not events:
                return None
            
            # Calculate session metadata
            first_event = events[0]
            last_event = events[-1]
            duration = None
            if len(events) > 1:
                duration = (last_event.timestamp - first_event.timestamp).total_seconds()
            
            return {
                'session_id': session_id,
                'events': [event.to_dict() for event in events],
                'duration': duration,
                'entry_page': first_event.page_url,
                'exit_page': last_event.page_url,
                'total_events': len(events)
            }
            
        except Exception as e:
            logger.error(f"Error getting session data for {session_id}: {str(e)}")
            return None
    
    @staticmethod
    def get_session_analytics() -> Dict[str, Any]:
        """Get session analytics data"""
        try:
            # Total sessions
            total_sessions = db.session.query(func.count(func.distinct(TrackingEvent.session_id))).scalar()
            
            # Average session duration (rough estimate)
            # This is a simplified calculation - in production you might want more sophisticated logic
            avg_duration_query = db.session.query(
                func.avg(
                    func.extract('epoch', func.max(TrackingEvent.timestamp) - func.min(TrackingEvent.timestamp))
                )
            ).group_by(TrackingEvent.session_id).subquery()
            
            avg_duration = db.session.query(func.avg(avg_duration_query.c.avg)).scalar()
            
            # Bounce rate (sessions with only one page view)
            single_page_sessions = db.session.query(TrackingEvent.session_id).group_by(
                TrackingEvent.session_id
            ).having(func.count(TrackingEvent.id) == 1).count()
            
            bounce_rate = (single_page_sessions / total_sessions * 100) if total_sessions > 0 else 0
            
            # Top entry pages
            top_entry_pages = db.session.query(
                TrackingEvent.page_url,
                func.count(TrackingEvent.id).label('count')
            ).filter(TrackingEvent.is_entry_page == True).group_by(
                TrackingEvent.page_url
            ).order_by(desc('count')).limit(10).all()
            
            # Top exit pages
            top_exit_pages = db.session.query(
                TrackingEvent.page_url,
                func.count(TrackingEvent.id).label('count')
            ).filter(TrackingEvent.is_exit_page == True).group_by(
                TrackingEvent.page_url
            ).order_by(desc('count')).limit(10).all()
            
            return {
                'total_sessions': total_sessions or 0,
                'average_session_duration': avg_duration,
                'bounce_rate': bounce_rate,
                'top_entry_pages': [{'page': page, 'count': count} for page, count in top_entry_pages],
                'top_exit_pages': [{'page': page, 'count': count} for page, count in top_exit_pages]
            }
            
        except Exception as e:
            logger.error(f"Error getting session analytics: {str(e)}")
            return {
                'total_sessions': 0,
                'average_session_duration': None,
                'bounce_rate': 0,
                'top_entry_pages': [],
                'top_exit_pages': []
            }
    
    @staticmethod
    def get_tracking_stats(days: int = 30) -> Dict[str, Any]:
        """Get comprehensive tracking statistics"""
        try:
            # Calculate date cutoff
            cutoff_date = datetime.now() - timedelta(days=days)
            
            # Total page views
            total_page_views = TrackingEvent.query.filter(
                and_(
                    TrackingEvent.timestamp >= cutoff_date,
                    or_(TrackingEvent.event_name.is_(None), TrackingEvent.event_name == '')
                )
            ).count()
            
            # Total custom events
            total_custom_events = TrackingEvent.query.filter(
                and_(
                    TrackingEvent.timestamp >= cutoff_date,
                    TrackingEvent.event_name.is_not(None),
                    TrackingEvent.event_name != ''
                )
            ).count()
            
            # Unique sessions
            unique_sessions = db.session.query(
                func.count(func.distinct(TrackingEvent.session_id))
            ).filter(TrackingEvent.timestamp >= cutoff_date).scalar()
            
            # Top pages
            top_pages_query = db.session.query(
                TrackingEvent.page_url,
                func.count(TrackingEvent.id).label('views')
            ).filter(
                and_(
                    TrackingEvent.timestamp >= cutoff_date,
                    or_(TrackingEvent.event_name.is_(None), TrackingEvent.event_name == '')
                )
            ).group_by(TrackingEvent.page_url).order_by(desc('views')).limit(10)
            
            top_pages = [{'page_url': page, 'views': views} for page, views in top_pages_query.all()]
            
            # Top events
            top_events_query = db.session.query(
                TrackingEvent.event_name,
                func.count(TrackingEvent.id).label('count')
            ).filter(
                and_(
                    TrackingEvent.timestamp >= cutoff_date,
                    TrackingEvent.event_name.is_not(None),
                    TrackingEvent.event_name != ''
                )
            ).group_by(TrackingEvent.event_name).order_by(desc('count')).limit(10)
            
            top_events = [{'event_name': event, 'count': count} for event, count in top_events_query.all()]
            
            # Daily stats
            daily_stats_query = db.session.query(
                func.date(TrackingEvent.timestamp).label('date'),
                func.count(TrackingEvent.id).label('events')
            ).filter(TrackingEvent.timestamp >= cutoff_date).group_by(
                func.date(TrackingEvent.timestamp)
            ).order_by(desc('date'))
            
            daily_stats = [
                {'date': str(date), 'events': events} 
                for date, events in daily_stats_query.all()
            ]
            
            # Hourly stats (last 24 hours)
            hourly_cutoff = datetime.now() - timedelta(hours=24)
            hourly_stats_query = db.session.query(
                func.extract('hour', TrackingEvent.timestamp).label('hour'),
                func.count(TrackingEvent.id).label('events')
            ).filter(TrackingEvent.timestamp >= hourly_cutoff).group_by(
                func.extract('hour', TrackingEvent.timestamp)
            ).order_by('hour')
            
            hourly_stats = [
                {'hour': int(hour), 'events': events} 
                for hour, events in hourly_stats_query.all()
            ]
            
            return {
                'total_page_views': total_page_views,
                'total_custom_events': total_custom_events,
                'unique_sessions': unique_sessions or 0,
                'top_pages': top_pages,
                'top_events': top_events,
                'daily_stats': daily_stats,
                'hourly_stats': hourly_stats
            }
            
        except Exception as e:
            logger.error(f"Error getting tracking stats: {str(e)}")
            return {
                'total_page_views': 0,
                'total_custom_events': 0,
                'unique_sessions': 0,
                'top_pages': [],
                'top_events': [],
                'daily_stats': [],
                'hourly_stats': []
            }
    
    @staticmethod
    def get_realtime_stats() -> Dict[str, Any]:
        """Get real-time tracking statistics"""
        try:
            # Active sessions (last 30 minutes)
            thirty_minutes_ago = datetime.now() - timedelta(minutes=30)
            active_sessions = db.session.query(
                func.count(func.distinct(TrackingEvent.session_id))
            ).filter(TrackingEvent.timestamp >= thirty_minutes_ago).scalar()
            
            # Page views in last hour
            one_hour_ago = datetime.now() - timedelta(hours=1)
            page_views_last_hour = TrackingEvent.query.filter(
                and_(
                    TrackingEvent.timestamp >= one_hour_ago,
                    or_(TrackingEvent.event_name.is_(None), TrackingEvent.event_name == '')
                )
            ).count()
            
            # Top pages today
            today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            top_pages_today_query = db.session.query(
                TrackingEvent.page_url,
                func.count(TrackingEvent.id).label('views')
            ).filter(
                and_(
                    TrackingEvent.timestamp >= today_start,
                    or_(TrackingEvent.event_name.is_(None), TrackingEvent.event_name == '')
                )
            ).group_by(TrackingEvent.page_url).order_by(desc('views')).limit(5)
            
            top_pages_today = [
                {'page_url': page, 'views': views} 
                for page, views in top_pages_today_query.all()
            ]
            
            # Recent events (last 10 events)
            recent_events = TrackingEvent.query.order_by(
                desc(TrackingEvent.timestamp)
            ).limit(10).all()
            
            return {
                'active_sessions': active_sessions or 0,
                'page_views_last_hour': page_views_last_hour,
                'top_pages_today': top_pages_today,
                'recent_events': [event.to_dict() for event in recent_events]
            }
            
        except Exception as e:
            logger.error(f"Error getting realtime stats: {str(e)}")
            return {
                'active_sessions': 0,
                'page_views_last_hour': 0,
                'top_pages_today': [],
                'recent_events': []
            }
    
    @staticmethod
    def update_exit_pages(session_id: str, current_event_id: int) -> bool:
        """Update previous events in session to not be exit pages"""
        try:
            TrackingEvent.query.filter(
                and_(
                    TrackingEvent.session_id == session_id,
                    TrackingEvent.id != current_event_id
                )
            ).update({'is_exit_page': False})
            
            TrackingService.commit_changes()
            return True
            
        except Exception as e:
            TrackingService.handle_db_error("update_exit_pages", e)
            return False
    
    @staticmethod
    def process_tracking_event(
        tracking_data: Dict[str, Any], 
        request_metadata: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Process a complete tracking event request with business logic
        
        Args:
            tracking_data: Validated tracking data from request
            request_metadata: Request metadata (IP, user agent, etc.)
            
        Returns:
            Event result if successful, None otherwise
        """
        try:
            # Extract and process request data
            ip_address = request_metadata.get('ip_address')
            user_agent = request_metadata.get('user_agent')
            header_referrer = request_metadata.get('referer_header')
            
            # Resolve referrer
            final_referrer = RequestProcessingService.resolve_referrer(
                tracking_data.get('referrer'),
                header_referrer
            )
            
            # Handle geolocation if needed
            country = tracking_data.get('country')
            if GeolocationService.should_geolocate_ip(ip_address, country):
                location_data = GeolocationService.get_location_from_ip(ip_address)
                country = location_data.get('country')
            
            # Create the tracking event
            result = TrackingService.add_tracking_event(
                session_id=tracking_data.get('session_id'),
                page_url=tracking_data.get('page_url'),
                ip_address=ip_address,
                user_agent=user_agent,
                referrer=final_referrer,
                browser=tracking_data.get('browser'),
                os=tracking_data.get('os'),
                device=tracking_data.get('device'),
                country=country,
                city=tracking_data.get('city'),
                is_entry_page=tracking_data.get('is_entry_page', False),
                is_exit_page=tracking_data.get('is_exit_page', False),
                event_name=tracking_data.get('event_name'),
                event_data=tracking_data.get('event_data')
            )
            
            # Handle session exit page management
            if (result and 
                tracking_data.get('session_id') and 
                not tracking_data.get('is_exit_page')):
                TrackingService.update_exit_pages(
                    tracking_data.get('session_id'), 
                    result['id']
                )
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing tracking event: {str(e)}")
            return None
